#!/usr/bin/env python3
"""Resolve a research capability to an installed provider or internal fallback."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capability_registry.yaml"


def load_registry() -> dict:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("capability_registry.yaml must contain a mapping")
    return data


def candidate_roots() -> list[Path]:
    roots: list[Path] = []
    configured = os.getenv("CODEX_SKILLS_DIR")
    if configured:
        roots.append(Path(configured).expanduser())

    cwd = Path.cwd().resolve()
    roots.append(cwd / ".agents" / "skills")
    for parent in cwd.parents:
        roots.append(parent / ".agents" / "skills")

    roots.append(Path.home() / ".agents" / "skills")
    roots.append(Path.home() / ".codex" / "skills")

    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root.resolve()) if root.exists() else str(root)
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def find_skill(name: str, roots: list[Path]) -> Path | None:
    for root in roots:
        candidate = root / name / "SKILL.md"
        if candidate.is_file():
            return candidate
    return None


def resolve(
    capability: str,
    requested_provider: str | None,
    tags: set[str],
    roots: list[Path] | None = None,
) -> dict:
    registry = load_registry()
    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, dict) or capability not in capabilities:
        known = ", ".join(sorted(capabilities or {}))
        raise ValueError(f"Unknown capability {capability!r}. Known capabilities: {known}")

    spec = capabilities[capability]
    if not isinstance(spec, dict):
        raise ValueError(f"Capability {capability!r} must be a mapping")

    roots = candidate_roots() if roots is None else roots
    providers = spec.get("providers") or []
    evaluated: list[dict[str, object]] = []
    available: list[tuple[int, int, dict, Path]] = []

    for index, provider in enumerate(providers):
        if not isinstance(provider, dict):
            continue
        name = str(provider.get("skill") or "")
        path = find_skill(name, roots) if name else None
        required = [str(item) for item in provider.get("requires_skills") or []]
        missing_companions = [item for item in required if find_skill(item, roots) is None]
        provider_tags = {str(item) for item in provider.get("tags") or []}
        tag_score = len(tags & provider_tags)
        installed = path is not None
        usable = installed and not missing_companions
        evaluated.append({
            "skill": name,
            "installed": installed,
            "usable": usable,
            "path": str(path) if path else None,
            "missing_companions": missing_companions,
            "matching_tags": sorted(tags & provider_tags),
        })
        if usable:
            if requested_provider and name != requested_provider:
                continue
            priority = int(provider.get("priority", 100))
            available.append((-tag_score, priority, provider, path))

    if requested_provider and not available:
        return {
            "capability": capability,
            "decision": "requested_provider_unavailable",
            "requested_provider": requested_provider,
            "fallback": spec.get("internal_fallback"),
            "providers": evaluated,
        }

    if available:
        available.sort(key=lambda item: (item[0], item[1]))
        _, _, provider, path = available[0]
        return {
            "capability": capability,
            "decision": "use_installed_provider",
            "provider": provider.get("skill"),
            "provider_path": str(path),
            "selection_when": provider.get("selection_when"),
            "input_contract": spec.get("input_contract") or [],
            "output_contract": spec.get("output_contract") or [],
            "acceptance": spec.get("acceptance") or [],
            "providers": evaluated,
        }

    fallback = ROOT / str(spec.get("internal_fallback") or "")
    return {
        "capability": capability,
        "decision": "use_internal_fallback",
        "fallback": str(fallback),
        "fallback_exists": fallback.is_file(),
        "input_contract": spec.get("input_contract") or [],
        "output_contract": spec.get("output_contract") or [],
        "acceptance": spec.get("acceptance") or [],
        "providers": evaluated,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capability", nargs="?", help="Capability name from capability_registry.yaml")
    parser.add_argument("--provider", help="Request a specific provider skill")
    parser.add_argument("--tag", action="append", default=[], help="Target tag used to rank available providers")
    parser.add_argument("--list", action="store_true", help="List known capability names")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    registry = load_registry()
    capabilities = registry.get("capabilities") or {}
    if args.list:
        for name in sorted(capabilities):
            print(name)
        return 0
    if not args.capability:
        parser.error("capability is required unless --list is used")

    try:
        result = resolve(args.capability, args.provider, set(args.tag))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Capability: {result['capability']}")
        print(f"Decision: {result['decision']}")
        if result.get("provider"):
            print(f"Provider: {result['provider']}")
            print(f"SKILL.md: {result['provider_path']}")
        else:
            print(f"Fallback: {result.get('fallback')}")
    return 0 if result["decision"] != "requested_provider_unavailable" else 1


if __name__ == "__main__":
    raise SystemExit(main())
