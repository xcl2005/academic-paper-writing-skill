#!/usr/bin/env python3
"""Check whether research workspace artifacts are ready for a stage handoff."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml


GATES = {
    "ideation": [
        "project_state.yaml",
        "matrices/research_idea_portfolio.csv",
    ],
    "literature": [
        "evidence/search_protocol.md",
        "matrices/screening_log.csv",
        "matrices/literature_matrix.csv",
    ],
    "analysis": [
        "matrices/statistical_analysis_plan.md",
        "matrices/data_provenance.csv",
        "matrices/experiment_matrix.csv",
    ],
    "drafting": [
        "claim_ledger.csv",
        "integrity_checklist.md",
    ],
    "submission": [
        "claim_ledger.csv",
        "integrity_checklist.md",
        "reports/submission_package_checklist.md",
    ],
    "presentation": [
        "evidence/paper_reading_note.md",
        "reports/presentation_brief.md",
    ],
}


def csv_has_rows(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return next(reader, None) is not None


def markdown_ready(path: Path) -> bool | None:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.lower().startswith("gate status:"):
            return line.split(":", 1)[1].strip().lower() in {"ready", "complete"}
    return None


def state_ready(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["project_state.yaml must contain a mapping"]
    errors: list[str] = []
    for key in ["project_type", "stage", "topic"]:
        if not str(data.get(key) or "").strip():
            errors.append(f"project_state.yaml has no {key}")
    return errors


def check(workspace: Path, gate: str, allow_empty: bool) -> dict[str, object]:
    required = GATES[gate]
    errors: list[str] = []
    checked: list[str] = []
    for rel in required:
        path = workspace / rel
        checked.append(rel)
        if not path.is_file():
            errors.append(f"missing required artifact: {rel}")
            continue
        if allow_empty:
            continue
        if path.name == "project_state.yaml":
            errors.extend(state_ready(path))
        elif path.suffix.lower() == ".csv" and not csv_has_rows(path):
            errors.append(f"artifact has no data rows: {rel}")
        elif path.suffix.lower() == ".md":
            ready = markdown_ready(path)
            if ready is False:
                errors.append(f"artifact gate status is not ready: {rel}")

    return {
        "workspace": workspace.as_posix(),
        "gate": gate,
        "decision": "ready_for_handoff" if not errors else "blocked",
        "checked": checked,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", help="Research workspace directory")
    parser.add_argument("--gate", choices=sorted(GATES), required=True)
    parser.add_argument("--allow-empty", action="store_true", help="Check structure only, without readiness content")
    parser.add_argument("--expect-block", action="store_true", help="Pass only when the gate is blocked")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    report = check(Path(args.workspace), args.gate, args.allow_empty)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Gate: {report['gate']}")
        print(f"Decision: {report['decision']}")
        for error in report["errors"]:
            print(f"- {error}")

    blocked = report["decision"] == "blocked"
    if args.expect_block:
        return 0 if blocked else 1
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
