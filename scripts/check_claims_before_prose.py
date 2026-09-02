#!/usr/bin/env python3
"""Check selected claims and their evidence dependencies before bounded prose."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import workspace_contract as wc


def build_report(target: Path, section: str | None = None) -> dict:
    workspace = wc.load_workspace(target)
    errors = list(workspace["errors"])
    if not target.exists():
        errors.append("Target does not exist.")
    elif target.is_file() and target.suffix.lower() != ".csv":
        errors.append("Expected a claim ledger CSV or workspace directory.")
    tables = [table for table in workspace["tables"] if table["kind"] == "claim_ledger"]
    blockers = []
    selected = 0
    notices = []
    for table in tables:
        for line, row in enumerate(table["rows"], 2):
            if row.get("output_scope") == "backlog" or (section and row.get("section") != section):
                continue
            selected += 1
            reasons = wc.claim_errors(workspace, row)
            for reason in reasons:
                blockers.append({
                    "severity": "blocker", "file": table["path"].as_posix(), "row": line,
                    "claim_id": row.get("claim_id", ""), "claim": row.get("claim_text", ""),
                    "status": row.get("status", "missing"), "reason": reason,
                    "fix_suggestion": "Supply the named evidence and review record, or explicitly exclude this claim from the current output.",
                })
            if not reasons and row.get("claim_kind") in {"limitation", "proposal", "assumption"}:
                notices.append(f"{row['claim_id']}: retain the explicit {row['claim_kind']} label; not a verified finding.")
    if not selected:
        errors.append("No active claims were checked for the requested output; this is not a prose approval.")
    for error in errors:
        blockers.append({"severity": "blocker", "file": target.as_posix(), "row": 0,
                         "claim_id": "input", "claim": "", "status": "invalid", "reason": error,
                         "fix_suggestion": "Correct the input or preview an explicit workspace migration; never fill evidence from guesses."})
    return {
        "target": target.as_posix(), "section": section,
        "checked_files": [table["path"].as_posix() for table in tables],
        "selected_claim_count": selected, "blocker_count": len(blockers),
        "warning_count": len(notices), "notices": notices, "blocked_claims": blockers,
        "next_action": "Produce a blocked-output explanation until blockers are resolved." if blockers else "Records are consistent for the selected claims. Human review of source support and bounded wording is still required.",
        "verification_boundary": "Offline structure, recorded review, and dependency checks only; not independent scientific verification or submission approval.",
    }


def blockers_for_file(path: Path) -> list[dict]:
    return build_report(path)["blocked_claims"]


def render_markdown(report: dict) -> str:
    lines = ["# Claim-to-Prose Preflight Report", "", f"Target: `{report['target']}`",
             f"Selected claims: {report['selected_claim_count']}", f"Blockers: {report['blocker_count']}", ""]
    for item in report["blocked_claims"]:
        lines.append(f"- `{item['claim_id']}`: {item['reason']}")
    lines.extend(["", *report["notices"], "", report["next_action"], "", report["verification_boundary"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target")
    parser.add_argument("--section", help="Check only active claims in this exact section")
    parser.add_argument("--expect-block", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report")
    args = parser.parse_args()
    report = build_report(Path(args.target), args.section)
    markdown = render_markdown(report)
    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else markdown)
    blocked = bool(report["blocker_count"])
    return int(not blocked if args.expect_block else blocked)


if __name__ == "__main__":
    raise SystemExit(main())
