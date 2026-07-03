#!/usr/bin/env python3
"""Create a small demo workspace for evidence-first academic workflows."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_OUTPUTS = ROOT / "examples" / "outputs"


def run_init(out: Path, mode: str) -> None:
    project_type = "research_paper" if mode == "research_paper" else "undergraduate_thesis"
    subprocess.check_call([
        sys.executable,
        str(ROOT / "scripts" / "init_project.py"),
        "--out",
        str(out),
        "--type",
        project_type,
    ])


def copy_required(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Required demo source missing: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def populate_research_demo(out: Path) -> None:
    copy_required(EXAMPLE_OUTPUTS / "rag-evaluation-literature-matrix.sample.csv", out / "matrices" / "literature_matrix.csv")
    copy_required(EXAMPLE_OUTPUTS / "rag-evaluation-novelty-check.sample.md", out / "matrices" / "novelty_check.md")
    copy_required(EXAMPLE_OUTPUTS / "rag-evaluation-claim-ledger.sample.csv", out / "claim_ledger.csv")
    copy_required(EXAMPLE_OUTPUTS / "output-related-work-blocked.sample.md", out / "drafts" / "related_work_blocked.md")


def populate_thesis_demo(out: Path) -> None:
    copy_required(EXAMPLE_OUTPUTS / "undergraduate-thesis-scope-ladder.sample.md", out / "evidence" / "scope_ladder.md")
    copy_required(EXAMPLE_OUTPUTS / "undergraduate-thesis-evidence-map.sample.csv", out / "evidence" / "graduation_evidence_map.csv")
    copy_required(EXAMPLE_OUTPUTS / "rag-evaluation-claim-ledger.sample.csv", out / "claim_ledger.csv")
    copy_required(EXAMPLE_OUTPUTS / "output-related-work-blocked.sample.md", out / "drafts" / "related_work_blocked.md")


def write_next_steps(out: Path, mode: str) -> None:
    next_steps = f"""# Demo Workspace Next Steps

Mode: `{mode}`

This workspace is a deterministic demo. It shows the evidence-first shape of the
skill; it is not a complete paper, thesis, or literature review.

## Inspect first

- `claim_ledger.csv`
- `integrity_checklist.md`
- `drafts/related_work_blocked.md`

## Do not copy blindly

Sample rows marked `needs_recheck`, `missing_source`, or `unknown` must be
verified before prose generation.

## Next user action

Provide real sources, advisor notes, school templates, or experiment evidence.
Unknown requirements stay unknown until confirmed.
"""
    (out / "README_NEXT_STEPS.md").write_text(next_steps, encoding="utf-8")


def write_manifest(out: Path, mode: str) -> None:
    files = sorted(
        str(path.relative_to(out)).replace("\\", "/")
        for path in out.rglob("*")
        if path.is_file()
    )
    manifest = {
        "mode": mode,
        "generated_by": "scripts/demo_academic_workflow.py",
        "files": files,
        "prose_policy": "blocked until sources, claim ledger, and integrity checks are reviewable",
    }
    (out / "DEMO_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an academic workflow demo workspace.")
    parser.add_argument("--mode", choices=["research_paper", "undergraduate_thesis"], default="research_paper")
    parser.add_argument("--out", default="demo_workspace")
    parser.add_argument("--force", action="store_true", help="Replace an existing output folder")
    args = parser.parse_args()

    out = Path(args.out)
    if out.exists():
        if not args.force:
            raise SystemExit(f"Output exists: {out}. Use --force to replace it.")
        shutil.rmtree(out)
    run_init(out, args.mode)
    if args.mode == "research_paper":
        populate_research_demo(out)
    else:
        populate_thesis_demo(out)
    write_next_steps(out, args.mode)
    write_manifest(out, args.mode)
    print(f"Wrote demo workspace at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
