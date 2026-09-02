#!/usr/bin/env python3
"""Resolve a research capability to an installed provider or internal fallback."""
from __future__ import annotations

import argparse
import json
import os
import hashlib
import re
import shutil
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


def candidate_roots(agent: str = "auto") -> list[Path]:
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
    if agent in {"auto", "claude"}:
        claude = [base / ".claude" / "skills" for base in [cwd, *cwd.parents, Path.home()]]
        roots = claude + roots if agent == "claude" else roots + claude

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


def inspect_skill(path: Path | None, name: str) -> dict:
    result = {"discovered": path is not None, "metadata_valid": False, "errors": [], "unchecked": ["task suitability", "instruction safety", "undeclared runtime requirements", "output quality"]}
    if path is None:
        result["errors"].append("SKILL.md not found")
        return result
    try:
        text = path.read_text(encoding="utf-8-sig")
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", text, re.S)
        if not match:
            raise ValueError("Missing valid frontmatter and body")
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict) or metadata.get("name") != name:
            raise ValueError("Skill identity does not match requested name")
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip() or not match.group(2).strip():
            raise ValueError("Description and workflow body must be nonempty")
        result["metadata_valid"] = True
        result["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        version = (metadata.get("metadata") or {}).get("version") if isinstance(metadata.get("metadata", {}), dict) else None
        result["version"] = str(version) if version is not None else None
        resources = re.findall(r"\]\(([^)]+)\)", match.group(2))
        for resource in resources:
            resource = resource.split("#", 1)[0].strip("<>")
            if resource and not re.match(r"^[a-zA-Z]+:", resource) and not (path.parent / resource).exists():
                result["errors"].append(f"Missing linked resource: {resource}")
        requires = metadata.get("requires", {})
        if not isinstance(requires, dict):
            raise ValueError("requires must be a mapping")
        for field in ["bins", "env"]:
            if not isinstance(requires.get(field, []), list) or not all(isinstance(item, str) for item in requires.get(field, [])):
                raise ValueError(f"requires.{field} must be a list of names")
        for binary in requires.get("bins", []):
            if not shutil.which(str(binary)):
                result["errors"].append(f"Missing declared executable: {binary}")
        for variable in requires.get("env", []):
            if not os.getenv(str(variable)):
                result["errors"].append(f"Missing declared environment variable: {variable}")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        result["errors"].append(str(exc))
    return result


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
        missing_companions = [item for item in required if inspect_skill(find_skill(item, roots), item)["errors"]]
        inspection = inspect_skill(path, name)
        provider_tags = {str(item) for item in provider.get("tags") or []}
        tag_score = len(tags & provider_tags)
        installed = path is not None
        usable = installed and not inspection["errors"] and not missing_companions
        evaluated.append({
            "skill": name,
            "installed": installed,
            "usable": usable,
            "path": str(path) if path else None,
            "missing_companions": missing_companions,
            "matching_tags": sorted(tags & provider_tags),
            **inspection,
            "dependencies_ready": not missing_companions and not inspection["errors"],
            "review_required": True,
            "accepted": False,
            "duplicate_paths": [str(root / name / "SKILL.md") for root in roots if (root / name / "SKILL.md").is_file()],
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
            "review_required": True,
            "accepted": False,
            "selection_boundary": "Eligible for full content review only. No skill execution or scientific output has been validated.",
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
    parser.add_argument("--agent", choices=["auto", "codex", "claude"], default="auto")
    parser.add_argument("--skill-root", action="append", type=Path, help="Explicit skill roots, in priority order; replaces automatic discovery")
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
        result = resolve(args.capability, args.provider, set(args.tag), roots=args.skill_root if args.skill_root is not None else candidate_roots(args.agent))
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
