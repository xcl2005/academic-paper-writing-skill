#!/usr/bin/env python3
"""Create a small demo workspace for evidence-first academic workflows."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
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

## Capability templates

- `matrices/research_idea_portfolio.csv`
- `evidence/search_protocol.md`
- `matrices/screening_log.csv`
- `matrices/statistical_analysis_plan.md`
- `matrices/data_provenance.csv`
- `reports/presentation_brief.md`
- `reports/submission_package_checklist.md`

These are intentionally unfilled in the demo. Stage gates should keep their
capabilities blocked until real project evidence is added and the relevant
Markdown artifact is marked `Gate status: ready`.

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


def build_demo(out: Path, mode: str, force: bool = False) -> None:
    out = out.absolute()
    resolved = out.resolve()
    if resolved == Path(resolved.anchor) or ROOT.resolve().is_relative_to(resolved) or Path.cwd().resolve().is_relative_to(resolved):
        raise ValueError("Refusing repository, current directory, root, or ancestor as demo output")
    if out.is_symlink() or (hasattr(out, "is_junction") and out.is_junction()):
        raise ValueError("Refusing linked demo output")
    if out.exists():
        if not force:
            raise ValueError(f"Output exists: {out}; --force only replaces a recognized demo")
        manifest_path = out / "DEMO_MANIFEST.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError("Existing output is not an owned demo; no files changed") from exc
        if not isinstance(manifest, dict) or manifest.get("generated_by") != "scripts/demo_academic_workflow.py":
            raise ValueError("Demo manifest has no recognized generator")
        owned = set(manifest.get("files", [])) | {"DEMO_MANIFEST.json"}
        for path in out.rglob("*"):
            if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()) or not path.resolve().is_relative_to(resolved):
                raise ValueError("Linked content in existing demo; refusing replacement")
            if path.is_file() and path.relative_to(out).as_posix() not in owned:
                raise ValueError(f"Unowned file in demo output: {path.name}; no files changed")
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".academic-demo-", dir=out.parent))
    backup = None
    try:
        run_init(staging, mode)
        if mode == "research_paper":
            populate_research_demo(staging)
        else:
            populate_thesis_demo(staging)
        write_next_steps(staging, mode)
        write_manifest(staging, mode)
        if out.exists():
            backup = out.with_name(out.name + ".previous-" + uuid.uuid4().hex)
            out.rename(backup)
        try:
            staging.rename(out)
        except OSError:
            if backup:
                backup.rename(out)
            raise
        if backup:
            shutil.rmtree(backup)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an academic workflow demo workspace.")
    parser.add_argument("--mode", choices=["research_paper", "undergraduate_thesis"], default="research_paper")
    parser.add_argument("--out", default="demo_workspace")
    parser.add_argument("--force", action="store_true", help="Replace only a recognized demo with no unowned files")
    args = parser.parse_args()

    out = Path(args.out)
    try:
        build_demo(out, args.mode, args.force)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Demo generation stopped: {exc}\n")
    print(f"Wrote demo workspace at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
