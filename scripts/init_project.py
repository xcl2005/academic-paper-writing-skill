#!/usr/bin/env python3
"""Initialize a paper/thesis project workspace from templates."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

COMMON = [
    "project_state.yaml",
    "claim_ledger.csv",
    "integrity_checklist.md",
    "assumption_register.md",
]
RESEARCH = [
    "literature_matrix.csv",
    "novelty_verification.csv",
    "experiment_matrix.csv",
    "roi_matrix.csv",
    "figure_brief.md",
    "simulated_review.md",
    "rebuttal_matrix.md",
]
THESIS = [
    "requirement_discovery_log.md",
    "scope_ladder.md",
    "graduation_evidence_map.csv",
]


def copy_files(files: list[str], out: Path) -> None:
    for name in files:
        src = TEMPLATES / name
        dst = out / name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="Output project workspace directory")
    parser.add_argument(
        "--type",
        choices=["research_paper", "undergraduate_thesis", "hybrid_capstone_research"],
        required=True,
    )
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for sub in ["matrices", "evidence", "experiments", "figures", "drafts", "reports", "external_skill_outputs"]:
        (out / sub).mkdir(exist_ok=True)

    copy_files(COMMON, out)
    if args.type == "research_paper":
        copy_files(RESEARCH, out / "matrices")
    elif args.type == "undergraduate_thesis":
        copy_files(THESIS, out / "evidence")
    else:
        copy_files(RESEARCH, out / "matrices")
        copy_files(THESIS, out / "evidence")

    print(f"Initialized {args.type} workspace at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
