#!/usr/bin/env python3
"""Validate capability interfaces and provider declarations."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capability_registry.yaml"
EXPECTED_PROVIDERS = {
    "scientific-brainstorming",
    "nature-academic-search",
    "literature-review",
    "academic-research-suite",
    "statistical-analysis",
    "scientific-visualization",
    "nature-figure",
    "nature-writing",
    "nature-polishing",
    "nature-reviewer",
    "nature-response",
    "nature-data",
    "nature-paper2ppt",
}


def main() -> int:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    errors: list[str] = []
    if not isinstance(data, dict):
        print("capability_registry.yaml must contain a mapping", file=sys.stderr)
        return 1
    if data.get("registry_version") != 1:
        errors.append("registry_version must be 1")

    capabilities = data.get("capabilities")
    if not isinstance(capabilities, dict) or not capabilities:
        errors.append("capabilities must be a non-empty mapping")
        capabilities = {}

    seen_providers: set[str] = set()
    for name, spec in capabilities.items():
        if not isinstance(spec, dict):
            errors.append(f"{name}: specification must be a mapping")
            continue
        for field in ["purpose", "triggers", "internal_fallback", "input_contract", "output_contract", "acceptance"]:
            if not spec.get(field):
                errors.append(f"{name}: missing {field}")
        fallback = ROOT / str(spec.get("internal_fallback") or "")
        if not fallback.is_file():
            errors.append(f"{name}: missing fallback {fallback.relative_to(ROOT)}")
        providers = spec.get("providers") or []
        if not isinstance(providers, list) or not providers:
            errors.append(f"{name}: providers must be a non-empty list")
            continue
        for provider in providers:
            if not isinstance(provider, dict):
                errors.append(f"{name}: provider entry must be a mapping")
                continue
            provider_name = str(provider.get("skill") or "")
            if not provider_name:
                errors.append(f"{name}: provider has no skill name")
            else:
                seen_providers.add(provider_name)
            if not provider.get("selection_when"):
                errors.append(f"{name}/{provider_name}: missing selection_when")

    missing = sorted(EXPECTED_PROVIDERS - seen_providers)
    if missing:
        errors.append("expected provider coverage missing: " + ", ".join(missing))

    if errors:
        print("Capability registry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Capability registry validation passed ({len(capabilities)} capabilities, {len(seen_providers)} providers).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
