#!/usr/bin/env python3
"""Validator for the Academic Paper Writing skill."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "academic-paper-writing-skill"

REQUIRED_FILES = [
    "SKILL.md",
    "skill_manifest.yaml",
    "agents/openai.yaml",
    "modules/00_core_invariants.md",
    "modules/01_agent_orchestrator.md",
    "modules/02_mode_router.md",
    "modules/03_external_skill_gateway.md",
    "modules/17_external_skill_acceptance_tests.md",
    "templates/project_state.yaml",
    "templates/literature_matrix.csv",
    "templates/experiment_matrix.csv",
    "templates/claim_ledger.csv",
    "scripts/demo_academic_workflow.py",
    "scripts/pre_prose_check.py",
    "scripts/summarize_evidence_status.py",
    "scripts/validate_evidence_status.py",
    "scripts/check_claims_before_prose.py",
    "scripts/validate_demo_workspace.py",
    "examples/outputs/sample-source-note.md",
    "examples/fixtures/claims/chinese-unsupported-claim.csv",
    "examples/fixtures/claims/unsupported-strong-claim.csv",
    "examples/fixtures/claims/supported-claim.csv",
    "examples/generated-demo-workspace/DEMO_MANIFEST.json",
    "examples/generated-demo-workspace/README_NEXT_STEPS.md",
    "examples/outputs/evidence-status-summary.generated.md",
    "examples/outputs/pre-prose-check.generated.md",
    "examples/outputs/claim-blocker-report.generated.md",
    "schemas/evidence_status.schema.yaml",
]

PROTECTED_PHRASES = [
    "No fabricated papers",
    "No fabricated SOTA",
    "No fabricated results",
    "No invented local requirements",
    "Claim-to-evidence mapping",
    "External-skill low coupling",
    "Do not treat demo samples as verified sources",
    "Do not turn `needs_recheck`, `missing_source`, or `unknown` rows into final prose",
    "Pre-Prose Checks",
    "pre_prose_check.py",
    "summarize_evidence_status.py",
    "validate_evidence_status.py",
    "check_claims_before_prose.py",
    "blocked-output explanation",
]

SAMPLE_NOTE_REQUIRED_PHRASES = [
    "not a complete literature review",
    "not a submission-ready evidence package",
    "must be checked",
    "needs_recheck",
    "missing_source",
    "unknown",
]


def fail(message: str) -> int:
    print(message)
    return 1


def read_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"{path.relative_to(ROOT)} is not valid YAML: {e}") from e
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a YAML mapping")
    return data


def validate_frontmatter() -> list[str]:
    errors: list[str] = []
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ["SKILL.md has no YAML frontmatter"]
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return ["SKILL.md has invalid YAML frontmatter delimiters"]
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except Exception as e:
        return [f"SKILL.md frontmatter is invalid YAML: {e}"]
    if not isinstance(frontmatter, dict):
        return ["SKILL.md frontmatter must be a mapping"]
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if name != SKILL_NAME:
        errors.append(f"SKILL.md name should be {SKILL_NAME!r}, got {name!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append("SKILL.md description is missing")
    elif len(description.strip()) > 1024:
        errors.append("SKILL.md description exceeds 1024 characters")
    return errors


def collect_manifest_paths(value) -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for v in value.values():
            paths.extend(collect_manifest_paths(v))
    elif isinstance(value, list):
        for item in value:
            paths.extend(collect_manifest_paths(item))
    elif isinstance(value, str):
        if value.startswith(("modules/", "templates/", "schemas/", "scripts/", "agents/")):
            paths.append(value)
    return paths


def validate_sample_source_note() -> list[str]:
    errors: list[str] = []
    note = (ROOT / "examples" / "outputs" / "sample-source-note.md").read_text(encoding="utf-8").lower()
    for phrase in SAMPLE_NOTE_REQUIRED_PHRASES:
        if phrase.lower() not in note:
            errors.append(f"sample-source-note.md should warn about: {phrase}")
    return errors


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        for e in errors:
            print(e)
        return 1

    errors.extend(validate_frontmatter())

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for phrase in PROTECTED_PHRASES:
        if phrase not in skill_text:
            errors.append(f"Protected phrase missing from SKILL.md: {phrase}")

    errors.extend(validate_sample_source_note())

    try:
        manifest = read_yaml(ROOT / "skill_manifest.yaml")
        openai_yaml = read_yaml(ROOT / "agents" / "openai.yaml")
    except ValueError as e:
        errors.append(str(e))
        manifest = {}
        openai_yaml = {}

    if manifest.get("skill_name") != SKILL_NAME:
        errors.append(f"skill_manifest.yaml skill_name should be {SKILL_NAME!r}")

    for rel in sorted(set(collect_manifest_paths(manifest))):
        if not (ROOT / rel).exists():
            errors.append(f"Manifest references missing path: {rel}")

    interface = openai_yaml.get("interface", {}) if isinstance(openai_yaml, dict) else {}
    if not isinstance(interface, dict):
        errors.append("agents/openai.yaml interface must be a mapping")
    else:
        prompt = interface.get("default_prompt", "")
        if f"${SKILL_NAME}" not in str(prompt):
            errors.append(f"agents/openai.yaml default_prompt should mention ${SKILL_NAME}")

    if errors:
        print("Skill validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
