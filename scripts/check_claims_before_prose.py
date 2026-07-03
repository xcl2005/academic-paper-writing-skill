#!/usr/bin/env python3
"""Block final prose when strong claims lack evidence status support."""
from __future__ import annotations

import argparse
import csv
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
    return any(term.lower() in lowered for term in REQUIREMENT_TERMS)


def read_claims(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def claim_text(row: dict[str, str]) -> str:
    return (row.get("claim_text") or row.get("claim") or row.get("text") or "").strip()


def claim_status(row: dict[str, str]) -> str:
    return (row.get("status") or row.get("result_status") or "").strip()


def blockers_for_claims(path: Path) -> list[str]:
    blockers: list[str] = []
    for index, row in enumerate(read_claims(path), start=2):
        text = claim_text(row)
        status = claim_status(row)
        if not text:
            continue
        if status in BLOCKING_STATUSES:
            blockers.append(f"{path}:{index}: status {status!r} blocks prose for claim: {text}")
        elif is_strong_claim(text) and status not in SUPPORTED_STATUSES:
            blockers.append(f"{path}:{index}: strong claim requires supported/verified/achieved status: {text} [{status or 'missing'}]")
        elif is_requirement_claim(text) and status in UNCERTAIN_STATUSES:
            blockers.append(f"{path}:{index}: local requirement claim is still uncertain: {text} [{status}]")
    return blockers


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether claim ledger rows can safely enter final prose.")
    parser.add_argument("claim_ledger", help="Claim ledger CSV path")
    parser.add_argument("--expect-block", action="store_true", help="Pass only if blockers are found")
    args = parser.parse_args()

    blockers = blockers_for_claims(Path(args.claim_ledger))
    if blockers:
        print("Claim-to-prose blockers:")
        for blocker in blockers:
            print(f"- {blocker}")
        return 0 if args.expect_block else 1

    if args.expect_block:
        print("Expected blockers, but none were found.")
        return 1

    print("Claim-to-prose check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
