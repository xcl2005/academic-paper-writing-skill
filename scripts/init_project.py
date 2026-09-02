#!/usr/bin/env python3
"""Initialize a paper/thesis project workspace from templates."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

COMMON = [
    "project_state.yaml",
    "claim_ledger.csv",
    "integrity_checklist.md",
    "assumption_register.md",
    "terminology_ledger.csv",
]
COMMON_MATRICES = [
    "literature_matrix.csv",
    "experiment_matrix.csv",
    "research_idea_portfolio.csv",
    "screening_log.csv",
    "statistical_analysis_plan.md",
    "data_provenance.csv",
]
COMMON_EVIDENCE = [
    "evidence_records.csv",
    "search_protocol.md",
    "paper_reading_note.md",
]
COMMON_REPORTS = [
    "presentation_brief.md",
    "submission_package_checklist.md",
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
    "requirement_register.csv",
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
    state_path = out / "project_state.yaml"
    new_state = not state_path.exists()
    if not new_state:
        existing = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        if not isinstance(existing, dict):
            parser.error("Existing project_state.yaml is not a mapping; no files changed.")
        if existing.get("project_type") != args.type:
            parser.error("Existing project type is different or unknown; use migrate_workspace.py explicitly. No files changed.")
    out.mkdir(parents=True, exist_ok=True)
    for sub in ["matrices", "evidence", "experiments", "figures", "drafts", "reports", "external_skill_outputs"]:
        (out / sub).mkdir(exist_ok=True)

    copy_files(COMMON, out)
    copy_files(COMMON_MATRICES, out / "matrices")
    copy_files(COMMON_EVIDENCE, out / "evidence")
    copy_files(COMMON_REPORTS, out / "reports")
    if args.type == "research_paper":
        copy_files(RESEARCH, out / "matrices")
    elif args.type == "undergraduate_thesis":
        copy_files(THESIS, out / "evidence")
    else:
        copy_files(RESEARCH, out / "matrices")
        copy_files(THESIS, out / "evidence")

    if new_state:
        state = yaml.safe_load((TEMPLATES / "project_state.yaml").read_text(encoding="utf-8"))
        state["project_type"] = args.type
        state["stage"] = "requirement_discovery" if args.type != "research_paper" else "idea_discovery"
        state["skill_version"] = yaml.safe_load((ROOT / "skill_manifest.yaml").read_text(encoding="utf-8"))["version"]
        state_path.write_text(yaml.safe_dump(state, sort_keys=False), encoding="utf-8")

    print(f"Initialized {args.type} workspace at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
