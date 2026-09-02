#!/usr/bin/env python3
"""Preview legacy CSV/state migration; --apply saves originals before changes."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import shutil

import yaml
import workspace_contract as wc


def migrated_csv(path: Path) -> str | None:
    table = wc.read_table(path)
    spec = wc.contract()["tables"].get(table["kind"])
    if not spec:
        return None
    if any("wrong column count" in error or "cannot read" in error or "duplicate CSV columns" in error for error in table["errors"]):
        raise ValueError(f"Malformed CSV must be corrected manually: {path}")
    aliases = spec.get("aliases", {})
    fields = list(spec["columns"]) + [key for key in table["fields"] if key not in spec["columns"] and key not in aliases]
    rows = []
    for original in table["rows"]:
        row = dict(original)
        for old, new in aliases.items():
            if old in row:
                if row.get(new) and row[old] and row[new] != row[old]:
                    raise ValueError(f"Conflicting legacy columns {old}/{new} in {path}")
                row[new] = row.pop(old) or row.get(new, "")
        for key, value in spec.get("defaults", {}).items():
            if not row.get(key):
                row[key] = value
        rows.append(row)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def migrate(root: Path, apply: bool = False, project_type: str | None = None) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("Workspace directory does not exist")
    changes: dict[Path, str] = {}
    for path in wc.csv_files(root):
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"Refusing linked path outside workspace: {path}")
        content = migrated_csv(path)
        if content is not None and content != path.read_text(encoding="utf-8-sig"):
            changes[path] = content
    state_path = root / "project_state.yaml"
    if state_path.exists():
        state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        if not isinstance(state, dict) or type(state.get("workspace_schema_version", 1)) is not int or state.get("workspace_schema_version", 1) not in (1, 2):
            raise ValueError("Invalid or unsupported workspace schema version")
        if project_type and state.get("project_type") not in (None, "", project_type):
            raise ValueError("Requested type conflicts with the existing workspace")
        if project_type:
            state["project_type"] = project_type
        state["workspace_schema_version"] = 2
        state.setdefault("study_design", "unknown")
        state.setdefault("gate_reviews", {})
        state.setdefault("gate_exemptions", {})
        content = yaml.safe_dump(state, sort_keys=False, allow_unicode=True)
        if content != state_path.read_text(encoding="utf-8"):
            changes[state_path] = content
        additions = ["evidence_records.csv"]
        if state.get("project_type") in ("undergraduate_thesis", "hybrid_capstone_research"):
            additions.append("requirement_register.csv")
        for name in additions:
            path = root / "evidence" / name
            if not path.exists():
                changes[path] = (wc.ROOT / "templates" / name).read_text(encoding="utf-8")
    backup = None
    if apply and changes:
        backup = root / ".academic-backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup.mkdir(parents=True, exist_ok=False)
        created = []
        for path in changes:
            if not path.resolve().is_relative_to(root) or path.is_symlink():
                raise ValueError(f"Refusing linked output: {path}")
            if path.exists():
                destination = backup / path.relative_to(root)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
            else:
                created.append(path.relative_to(root).as_posix())
        (backup / "migration.json").write_text(json.dumps({"created": created, "changed": [p.relative_to(root).as_posix() for p in changes]}, indent=2), encoding="utf-8")
        for path, content in changes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return {"mode": "apply" if apply else "preview", "changes": [p.relative_to(root).as_posix() for p in changes],
            "backup": str(backup) if backup else None,
            "warning": "No evidence status or review was upgraded. Missing provenance, identity, and applicability still need human input."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--project-type", choices=["research_paper", "undergraduate_thesis", "hybrid_capstone_research"])
    args = parser.parse_args()
    try:
        print(json.dumps(migrate(args.workspace, args.apply, args.project_type), indent=2))
    except (ValueError, OSError, yaml.YAMLError) as exc:
        parser.exit(1, f"Migration stopped: {exc}\n")
