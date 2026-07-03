#!/usr/bin/env python3
"""Validate evidence/status columns in templates and example CSV outputs."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STATUS_SCHEMA = ROOT / "schemas" / "evidence_status.schema.yaml"


def load_statuses() -> dict[str, set[str]]:
    data = yaml.safe_load(STATUS_SCHEMA.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("schemas/evidence_status.schema.yaml must contain a mapping")
    return {str(key): {str(item) for item in value or []} for key, value in data.items()}


def status_columns(fieldnames: list[str]) -> list[tuple[str, str]]:
    mapping: list[tuple[str, str]] = []
    for name in fieldnames:
        if name == "verification_status":
            mapping.append((name, "source_status"))
        elif name == "status":
            mapping.append((name, "claim_status"))
        elif name == "result_status":
            mapping.append((name, "result_status"))
        elif name == "current_status":
            mapping.append((name, "artifact_status"))
    return mapping


def validate_csv(path: Path, statuses: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        checks = status_columns(fieldnames)
        for row_number, row in enumerate(reader, start=2):
            for column, status_group in checks:
                value = (row.get(column) or "").strip()
                if not value:
                    continue
                allowed = statuses.get(status_group, set())
                if value not in allowed:
                    try:
                        rel = path.relative_to(ROOT)
                    except ValueError:
                        rel = path
                    errors.append(f"{rel}:{row_number}: {column}={value!r} is not in {sorted(allowed)}")
    return errors


def iter_csv(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.csv")))
        elif path.suffix.lower() == ".csv":
            files.append(path)
    return [p for p in files if ".git" not in p.parts]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate evidence status values in CSV files.")
    parser.add_argument("paths", nargs="+", help="CSV files or directories to validate")
    args = parser.parse_args()

    statuses = load_statuses()
    csv_files = iter_csv([Path(p) for p in args.paths])
    errors: list[str] = []
    for path in csv_files:
        errors.extend(validate_csv(path.resolve(), statuses))

    if errors:
        print("Evidence status validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Evidence status validation passed for {len(csv_files)} CSV file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
