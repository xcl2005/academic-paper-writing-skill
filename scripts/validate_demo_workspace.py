#!/usr/bin/env python3
"""Validate generated demo workspace contents."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_BY_MODE = {
    "research_paper": [
        "README_NEXT_STEPS.md",
        "DEMO_MANIFEST.json",
        "claim_ledger.csv",
        "integrity_checklist.md",
        "matrices/literature_matrix.csv",
        "matrices/novelty_check.md",
        "drafts/related_work_blocked.md",
    ],
    "undergraduate_thesis": [
        "README_NEXT_STEPS.md",
        "DEMO_MANIFEST.json",
        "claim_ledger.csv",
        "integrity_checklist.md",
        "evidence/requirement_discovery_log.md",
        "evidence/scope_ladder.md",
        "evidence/graduation_evidence_map.csv",
        "drafts/related_work_blocked.md",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated academic demo workspace.")
    parser.add_argument("workspace", help="Demo workspace path")
    parser.add_argument("--mode", choices=sorted(REQUIRED_BY_MODE), required=True)
    args = parser.parse_args()

    root = Path(args.workspace)
    errors: list[str] = []
    for rel in REQUIRED_BY_MODE[args.mode]:
        if not (root / rel).exists():
            errors.append(f"Missing required demo file: {rel}")

    manifest_path = root / "DEMO_MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("mode") != args.mode:
            errors.append(f"DEMO_MANIFEST.json mode should be {args.mode!r}")
        files = set(manifest.get("files") or [])
        for rel in REQUIRED_BY_MODE[args.mode]:
            if rel != "DEMO_MANIFEST.json" and rel not in files:
                errors.append(f"DEMO_MANIFEST.json missing file entry: {rel}")

    next_steps = root / "README_NEXT_STEPS.md"
    if next_steps.exists():
        text = next_steps.read_text(encoding="utf-8")
        for phrase in ["needs_recheck", "missing_source", "unknown"]:
            if phrase not in text:
                errors.append(f"README_NEXT_STEPS.md should mention {phrase}")

    if errors:
        print("Demo workspace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Demo workspace validation passed for {root}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
