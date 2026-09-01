#!/usr/bin/env python3
"""Offline behavioral checks for capability provider resolution."""
from __future__ import annotations

import sys
from pathlib import Path

import resolve_capability


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "examples" / "fixtures" / "provider-skills"


def main() -> int:
    provider = resolve_capability.resolve(
        "research_ideation",
        requested_provider=None,
        tags={"evidence-aware"},
        roots=[FIXTURE_ROOT],
    )
    if provider.get("decision") != "use_installed_provider":
        print(f"Expected installed provider, got: {provider}")
        return 1
    if provider.get("provider") != "scientific-brainstorming":
        print(f"Wrong provider selected: {provider}")
        return 1

    fallback = resolve_capability.resolve(
        "paper_to_presentation",
        requested_provider=None,
        tags=set(),
        roots=[FIXTURE_ROOT],
    )
    if fallback.get("decision") != "use_internal_fallback" or not fallback.get("fallback_exists"):
        print(f"Expected internal fallback, got: {fallback}")
        return 1

    unavailable = resolve_capability.resolve(
        "manuscript_drafting",
        requested_provider="nature-writing",
        tags={"nature"},
        roots=[FIXTURE_ROOT],
    )
    if unavailable.get("decision") != "requested_provider_unavailable":
        print(f"Expected unavailable requested provider, got: {unavailable}")
        return 1

    print("Provider resolution tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
