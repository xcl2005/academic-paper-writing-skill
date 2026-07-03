#!/usr/bin/env python3
"""One-command pre-prose gate for evidence-first academic workspaces."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import check_claims_before_prose as claim_check
import validate_evidence_status as evidence_status


def evidence_report(target: Path) -> dict[str, object]:
    statuses = evidence_status.load_statuses()
    csv_files = evidence_status.iter_csv([target])
    errors: list[str] = []
    for path in csv_files:
        errors.extend(evidence_status.validate_csv(path.resolve(), statuses))
    return {
        "checked_csv_files": [path.as_posix() for path in csv_files],
        "csv_count": len(csv_files),
        "error_count": len(errors),
        "errors": errors,
    }


def build_report(target: Path) -> dict[str, object]:
    evidence = evidence_report(target)
    claims = claim_check.build_report(target)
    evidence_errors = int(evidence["error_count"])
    claim_blockers = int(claims["blocker_count"])
    blocked = evidence_errors > 0 or claim_blockers > 0
    return {
        "target": target.as_posix(),
        "decision": "blocked" if blocked else "ready_for_human_review",
        "evidence_status": evidence,
        "claim_to_evidence": claims,
        "next_action": (
            "Produce a blocked-output explanation until evidence status errors and claim blockers are resolved."
            if blocked
            else "Final prose may proceed after human review."
        ),
    }


def render_markdown(report: dict[str, object]) -> str:
    evidence = report["evidence_status"]
    claims = report["claim_to_evidence"]
    assert isinstance(evidence, dict)
    assert isinstance(claims, dict)
    blockers = claims["blocked_claims"]
    errors = evidence["errors"]
    assert isinstance(blockers, list)
    assert isinstance(errors, list)

    lines = [
        "# Pre-Prose Workspace Gate",
        "",
        f"Target: `{report['target']}`",
        f"Decision: **{str(report['decision']).upper()}**",
        "",
        "## Evidence Status",
        "",
        f"Checked CSV files: {evidence['csv_count']}",
        f"Errors: {evidence['error_count']}",
        "",
    ]
    if errors:
        lines.extend(f"- {error}" for error in errors)
        lines.append("")
    else:
        lines.extend(["No evidence status errors found.", ""])

    lines.extend([
        "## Claim-to-Evidence",
        "",
        f"Checked claim files: {len(claims['checked_files'])}",
        f"Blockers: {claims['blocker_count']}",
        "",
    ])
    if blockers:
        lines.extend([
            "| File | Row | Claim ID | Status | Reason | Fix suggestion |",
            "|---|---:|---|---|---|---|",
        ])
        for item in blockers:
            assert isinstance(item, dict)
            lines.append(
                "| {file} | {row} | {claim_id} | {status} | {reason} | {fix} |".format(
                    file=item["file"],
                    row=item["row"],
                    claim_id=item["claim_id"],
                    status=item["status"],
                    reason=item["reason"],
                    fix=item["fix_suggestion"],
                )
            )
        lines.append("")
    else:
        lines.extend(["No claim blockers found.", ""])

    lines.extend([f"Next action: {report['next_action']}", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run evidence-status and claim-to-evidence checks before final prose.")
    parser.add_argument("target", help="Academic workspace or claim/evidence directory")
    parser.add_argument("--expect-block", action="store_true", help="Pass only if the gate blocks prose")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--report", help="Write a Markdown report to this path")
    args = parser.parse_args()

    report = build_report(Path(args.target))
    markdown = render_markdown(report)
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(markdown)

    blocked = report["decision"] == "blocked"
    if blocked:
        return 0 if args.expect_block else 1
    if args.expect_block:
        print("Expected a blocked pre-prose gate, but the workspace was ready.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
