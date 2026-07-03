#!/usr/bin/env python3
"""Pre-prose claim blocker for evidence-first academic workspaces."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


STRONG_CLAIM_PATTERNS = [
    r"\bfirst\b",
    r"\bnovel\b",
    r"\bstate-of-the-art\b",
    r"\bSOTA\b",
    r"\boutperform\w*\b",
    r"\bsignificant(?:ly)? improves?\b",
    r"\bproves?\b",
    r"\bguarantees?\b",
    r"\bbest\b",
    r"首次",
    r"最优",
    r"显著优于",
    r"达到\s*SOTA",
]

SUPPORTED_STATUSES = {"supported", "verified", "achieved", "user_provided"}
BLOCKING_STATUSES = {"blocked", "unsupported", "needs_recheck", "missing_source"}
UNCERTAIN_STATUSES = {"unknown", "planned", "preliminary", "not_run", "partially_supported"}
REQUIREMENT_TERMS = ["requirement", "required", "must", "school", "advisor", "rubric", "template", "要求", "必须", "学校", "导师"]


def is_strong_claim(text: str) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in STRONG_CLAIM_PATTERNS)


def is_requirement_claim(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in REQUIREMENT_TERMS)


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def claim_text(row: dict[str, str]) -> str:
    return (row.get("claim_text") or row.get("claim") or row.get("text") or "").strip()


def claim_status(row: dict[str, str]) -> str:
    return (row.get("status") or row.get("result_status") or "").strip()


def claim_id(row: dict[str, str], row_number: int) -> str:
    return (row.get("claim_id") or row.get("id") or f"row-{row_number}").strip()


def discover_claim_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    candidates: list[Path] = []
    for path in sorted(target.rglob("*.csv")):
        if ".git" in path.parts:
            continue
        fieldnames, _ = read_rows(path)
        lowered = {name.lower() for name in fieldnames}
        has_claim = bool({"claim", "claim_text", "text"} & lowered)
        has_status = bool({"status", "result_status"} & lowered)
        if has_claim and has_status:
            candidates.append(path)
    return candidates


def blocker(file: Path, row_number: int, row: dict[str, str], reason: str, fix_suggestion: str) -> dict[str, str | int]:
    return {
        "severity": "blocker",
        "file": file.as_posix(),
        "row": row_number,
        "claim_id": claim_id(row, row_number),
        "claim": claim_text(row),
        "status": claim_status(row) or "missing",
        "reason": reason,
        "fix_suggestion": fix_suggestion,
    }


def blockers_for_file(path: Path) -> list[dict[str, str | int]]:
    _, rows = read_rows(path)
    blockers: list[dict[str, str | int]] = []
    for row_number, row in enumerate(rows, start=2):
        text = claim_text(row)
        status = claim_status(row)
        if not text:
            continue
        if status in BLOCKING_STATUSES:
            blockers.append(blocker(
                path,
                row_number,
                row,
                f"claim status is {status}",
                "Add evidence, downgrade the claim, or keep prose blocked.",
            ))
        elif is_strong_claim(text) and status not in SUPPORTED_STATUSES:
            blockers.append(blocker(
                path,
                row_number,
                row,
                "strong claim without supported evidence status",
                "Add verified source or experiment evidence, or rewrite the claim as planned/limited.",
            ))
        elif is_requirement_claim(text) and status in UNCERTAIN_STATUSES:
            blockers.append(blocker(
                path,
                row_number,
                row,
                "local requirement claim is still uncertain",
                "Provide school template, advisor note, rubric, or mark the requirement as unknown.",
            ))
    return blockers


def build_report(target: Path) -> dict[str, object]:
    files = discover_claim_files(target)
    blockers: list[dict[str, str | int]] = []
    for path in files:
        blockers.extend(blockers_for_file(path))
    return {
        "target": target.as_posix(),
        "checked_files": [path.as_posix() for path in files],
        "blocker_count": len(blockers),
        "warning_count": 0,
        "blocked_claims": blockers,
        "next_action": "Produce a blocked-output explanation until blockers are resolved." if blockers else "Final prose may proceed after human review.",
    }


def render_markdown(report: dict[str, object]) -> str:
    blockers = report["blocked_claims"]
    assert isinstance(blockers, list)
    lines = [
        "# Claim-to-Prose Preflight Report",
        "",
        f"Target: `{report['target']}`",
        f"Checked files: {len(report['checked_files'])}",
        f"Blockers: {report['blocker_count']}",
        "",
    ]
    if not blockers:
        lines.extend(["No claim blockers found.", "", f"Next action: {report['next_action']}", ""])
        return "\n".join(lines)
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
    lines.extend(["", f"Next action: {report['next_action']}", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether workspace claims can safely enter final prose.")
    parser.add_argument("target", help="Claim ledger CSV or workspace directory")
    parser.add_argument("--expect-block", action="store_true", help="Pass only if blockers are found")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON report")
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

    blocked = int(report["blocker_count"]) > 0
    if blocked:
        return 0 if args.expect_block else 1
    if args.expect_block:
        print("Expected blockers, but none were found.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
