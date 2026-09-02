#!/usr/bin/env python3
"""One maintainer check entrypoint, with opt-in generated-file refresh."""
from pathlib import Path
import argparse
import subprocess
import sys
import tempfile

import check_claims_before_prose
import demo_academic_workflow as demo
import pre_prose_check
import summarize_evidence_status
from workspace_contract import ROOT


def run(*args):
    subprocess.run([sys.executable, "-B", *args], cwd=ROOT, check=True)


def generated_reports():
    target = Path("examples/generated-demo-workspace")
    return {
        "claim-blocker-report.generated.md": check_claims_before_prose.render_markdown(check_claims_before_prose.build_report(target)),
        "pre-prose-check.generated.md": pre_prose_check.render_markdown(pre_prose_check.build_report(target)),
        "evidence-status-summary.generated.md": summarize_evidence_status.render_markdown(summarize_evidence_status.build_summary([target])),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update-generated", action="store_true")
    args = parser.parse_args()
    import os
    os.chdir(ROOT)
    committed = ROOT / "examples/generated-demo-workspace"
    if args.update_generated:
        demo.build_demo(committed, "undergraduate_thesis", True)
        for name, content in generated_reports().items():
            (ROOT / "examples/outputs" / name).write_text(content, encoding="utf-8")
    for script in ["sync_contract_assets.py", "validate_skill.py", "validate_capability_registry.py", "validate_readme_quality.py", "test_evidence_gates.py", "test_provider_resolution.py", "test_demo_safety.py", "test_external_skill_screening.py"]:
        run("scripts/" + script)
    run("scripts/validate_evidence_status.py", "templates", "examples/outputs", "examples/fixtures", "examples/generated-demo-workspace")
    run("scripts/check_claims_before_prose.py", "examples/fixtures/claims/supported-claim.csv")
    for name in ["unsupported-strong-claim.csv", "chinese-unsupported-claim.csv"]:
        run("scripts/check_claims_before_prose.py", "examples/fixtures/claims/" + name, "--expect-block")
    with tempfile.TemporaryDirectory(prefix="academic-check-") as temp:
        for mode in ["research_paper", "undergraduate_thesis"]:
            out = Path(temp) / mode
            demo.build_demo(out, mode)
            run("scripts/validate_demo_workspace.py", str(out), "--mode", mode)
            run("scripts/pre_prose_check.py", str(out), "--expect-block")
            if mode == "undergraduate_thesis":
                expected = {p.relative_to(out).as_posix(): p.read_text(encoding="utf-8") for p in out.rglob("*") if p.is_file()}
                actual = {p.relative_to(committed).as_posix(): p.read_text(encoding="utf-8") for p in committed.rglob("*") if p.is_file()}
                if expected != actual:
                    raise ValueError("Generated demo drift; review and run check.py --update-generated")
    for name, content in generated_reports().items():
        if (ROOT / "examples/outputs" / name).read_text(encoding="utf-8") != content:
            raise ValueError(f"Generated report drift: {name}")
    print("All maintainer checks passed. Offline checks do not certify scientific truth.")


if __name__ == "__main__":
    main()
