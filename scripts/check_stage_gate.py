#!/usr/bin/env python3
"""Validate stage artifacts, evidence dependencies, and recorded human review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import yaml
import pre_prose_check
import workspace_contract as wc

PROJECT_TYPES = {"research_paper", "undergraduate_thesis", "hybrid_capstone_research"}
GATES = {
    "ideation": ["matrices/research_idea_portfolio.csv"],
    "literature": ["evidence/search_protocol.md", "matrices/screening_log.csv", "matrices/literature_matrix.csv"],
    "analysis": ["matrices/statistical_analysis_plan.md", "matrices/data_provenance.csv", "matrices/experiment_matrix.csv"],
    "drafting": ["claim_ledger.csv", "integrity_checklist.md"],
    "submission": ["claim_ledger.csv", "integrity_checklist.md", "reports/submission_package_checklist.md"],
    "presentation": ["claim_ledger.csv", "evidence/paper_reading_note.md", "reports/presentation_brief.md"],
    "proposal": ["evidence/requirement_discovery_log.md", "evidence/scope_ladder.md"],
    "midterm": ["evidence/requirement_discovery_log.md", "evidence/graduation_evidence_map.csv"],
}
GATES["final"] = list(GATES["submission"])
GATES["defense"] = list(GATES["presentation"])


def markdown_errors(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path.name}: cannot read Markdown: {exc}"]
    states = re.findall(r"^Gate status:\s*(\S+)\s*$", text, re.M | re.I)
    errors = []
    if len(states) != 1 or states[0].lower() not in {"ready", "complete"}:
        errors.append(f"{path.name}: one explicit Gate status: ready/complete is required")
    if re.search(r"^\s*- \[ \]", text, re.M):
        errors.append(f"{path.name}: unchecked items remain")
    if re.search(r"^\s*- [^\n:]+:\s*$", text, re.M):
        errors.append(f"{path.name}: empty fields remain; explain any non-applicable fields")
    body = [line for line in text.splitlines() if line.strip() and not line.startswith(("#", "Gate status:"))]
    if not body:
        errors.append(f"{path.name}: no substantive record")
    return errors


def requirement_errors(workspace: dict, completed: bool) -> list[str]:
    requirements = workspace["records"].get("requirement_register", {})
    if not requirements:
        return ["No requirement register records; school/advisor requirements remain unknown."]
    maps = [row for table in workspace["tables"] if table["kind"] == "graduation_evidence_map" for row in table["rows"]]
    errors = []
    for identity, row in requirements.items():
        label = f"requirement {identity}"
        if row.get("verification_status") != "verified" or row.get("applicability") == "unknown":
            errors.append(f"{label}: verification/applicability is unresolved")
        errors.extend(wc.missing_values(row, ["source_id", "locator", "acceptance_criteria"], label))
        if row.get("source_id"):
            errors.extend(wc.source_errors(workspace, row["source_id"]))
        if completed and row.get("applicability") == "required":
            matches = [item for item in maps if item.get("requirement_id") == identity]
            if not matches:
                errors.append(f"{label}: missing graduation evidence mapping")
            for item in matches:
                if item.get("current_status") != "complete" or not item.get("evidence_ids"):
                    errors.append(f"{label}: evidence mapping is incomplete")
                for evidence_id in wc.split_ids(item.get("evidence_ids", "")):
                    errors.extend(wc.evidence_errors(workspace, evidence_id))
    for row in maps:
        if completed and row.get("requirement_id") not in requirements:
            errors.append("Graduation evidence map has an unresolved requirement_id")
    return errors


def check(workspace: Path, gate: str, allow_empty: bool = False) -> dict:
    errors = []
    state = {}
    state_path = workspace / "project_state.yaml"
    try:
        state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise ValueError("state must be a mapping")
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        errors.append(f"project_state.yaml: {exc}")
        state = {}
    if not isinstance(state.get("project_type"), str) or state["project_type"] not in PROJECT_TYPES:
        errors.append("project_state.yaml: missing/invalid project_type")
    if type(state.get("workspace_schema_version")) is not int or state["workspace_schema_version"] != wc.contract()["workspace_schema_version"]:
        errors.append("project_state.yaml: unsupported/missing schema version; preview migrate_workspace.py")
    if not allow_empty:
        errors.extend(wc.missing_values(state, ["stage", "topic"], "project_state.yaml"))
    thesis = state.get("project_type") in ("undergraduate_thesis", "hybrid_capstone_research")
    required = ["project_state.yaml", *GATES[gate]]
    if thesis and gate in {"submission", "final", "defense", "proposal", "midterm"}:
        required += ["evidence/requirement_register.csv", "evidence/requirement_discovery_log.md"]
        if gate in {"submission", "final", "defense"}:
            required.append("evidence/graduation_evidence_map.csv")
    exemption = (state.get("gate_exemptions") or {}).get(gate) if isinstance(state.get("gate_exemptions", {}), dict) else None
    if exemption and not allow_empty:
        if gate != "analysis" or state.get("study_design") not in ("theoretical", "review", "qualitative") or not isinstance(exemption, dict):
            errors.append("Invalid gate exemption; only non-quantitative analysis may be explicitly exempted")
        else:
            errors.extend(wc.missing_values(exemption, ["reason"], "analysis exemption"))
            errors.extend(wc.review_errors(exemption, "analysis exemption"))
            return {"workspace": workspace.as_posix(), "gate": gate, "decision": "blocked" if errors else "not_applicable", "checked": ["project_state.yaml"], "errors": errors, "review_required": [], "reason": exemption.get("reason")}
    required = list(dict.fromkeys(required))
    tables = {}
    for rel in required:
        path = workspace / rel
        if not path.is_file():
            errors.append(f"missing required artifact: {rel}")
            continue
        if path.suffix == ".csv":
            table = wc.read_table(path)
            tables[table["kind"]] = table
            errors.extend(table["errors"])
            if not allow_empty and not table["rows"]:
                errors.append(f"artifact has no data rows: {rel}")
        elif path.suffix == ".md" and not allow_empty:
            errors.extend(markdown_errors(path))
    if not allow_empty:
        loaded = wc.load_workspace(workspace)
        errors.extend(loaded["errors"])
        if gate in {"drafting", "submission", "final", "presentation", "defense"}:
            prose = pre_prose_check.build_report(workspace)
            errors.extend(item["reason"] for item in prose["claim_to_evidence"]["blocked_claims"])
        if gate == "literature":
            source_keys = set(loaded["records"].get("literature_matrix", {}))
            source_keys.update(row.get("source_url_or_doi") for row in loaded["records"].get("literature_matrix", {}).values())
            for source_id in loaded["records"].get("literature_matrix", {}):
                errors.extend(wc.source_errors(loaded, source_id))
            for row in tables.get("screening_log", {}).get("rows", []):
                if row.get("screening_status") not in {"include", "exclude", "duplicate"}:
                    errors.append(f"screening {row.get('record_id')}: unresolved screening")
                if row.get("screening_status") == "include":
                    errors.extend(wc.missing_values(row, ["identifier", "query_id", "found_date", "inclusion_reason"], "included screening record"))
                    if row.get("verification_status") != "verified":
                        errors.append("Included screening record is not verified")
                    if row.get("identifier") not in source_keys:
                        errors.append("Included screening identifier does not resolve to the literature matrix")
        if gate == "ideation":
            ideas = loaded["records"].get("research_idea_portfolio", {}).values()
            if not any(row.get("decision_status") in {"selected", "shortlisted"} and row.get("decision_reason") for row in ideas):
                errors.append("Ideation needs a shortlisted/selected question and explicit decision rationale")
        if gate == "analysis":
            for identity in loaded["records"].get("experiment_matrix", {}):
                errors.extend(wc.result_errors(loaded, identity))
        if thesis and gate in {"submission", "final", "defense", "proposal", "midterm"}:
            errors.extend(requirement_errors(loaded, gate in {"submission", "final", "defense"}))
    reviews = state.get("gate_reviews", {})
    review = reviews.get(gate) if isinstance(reviews, dict) else None
    pending = []
    if not allow_empty:
        if not isinstance(review, dict):
            pending.append(f"Record human review in project_state.yaml gate_reviews.{gate}")
        else:
            pending.extend(wc.review_errors(review, f"{gate} review"))
            pending.extend(wc.missing_values(review, ["scope"], f"{gate} review"))
            if review.get("decision") != "ready":
                pending.append(f"{gate} human review is not ready")
    decision = "blocked" if errors else "structure_valid" if allow_empty else "evidence_review_required" if pending else "ready_for_handoff"
    return {"workspace": workspace.as_posix(), "gate": gate, "decision": decision,
            "checked": required, "errors": list(dict.fromkeys(errors)), "review_required": pending,
            "verification_boundary": "Offline record checks plus recorded human sign-off; not scientific truth certification or authorization to submit."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--gate", choices=sorted(GATES), required=True)
    parser.add_argument("--allow-empty", action="store_true", help="Validate initialized structure only; never report readiness")
    parser.add_argument("--expect-block", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = check(Path(args.workspace), args.gate, args.allow_empty)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else "\n".join([f"Gate: {args.gate}", f"Decision: {report['decision']}", *report["errors"], *report["review_required"]]))
    blocked = report["decision"] in {"blocked", "evidence_review_required"}
    return int(not blocked if args.expect_block else blocked)


if __name__ == "__main__":
    raise SystemExit(main())
