#!/usr/bin/env python3
"""Validate evidence/status columns in templates and example CSV outputs."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml
import workspace_contract as wc


ROOT = Path(__file__).resolve().parents[1]
STATUS_SCHEMA = ROOT / "schemas" / "evidence_status.schema.yaml"

REQUIRED_STATUS_COLUMNS = [
    ("literature_matrix", "verification_status"),
    ("literature-matrix", "verification_status"),
    ("claim_ledger", "status"),
    ("claim-ledger", "status"),
    ("experiment_matrix", "result_status"),
    ("experiment-matrix", "result_status"),
    ("graduation_evidence_map", "current_status"),
    ("evidence-map", "current_status"),
    ("research_idea_portfolio", "decision_status"),
    ("screening_log", "screening_status"),
    ("data_provenance", "data_status"),
]


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
        elif name == "decision_status":
            mapping.append((name, "decision_status"))
        elif name == "screening_status":
            mapping.append((name, "screening_status"))
        elif name == "data_status":
            mapping.append((name, "data_status"))
        elif name == "analysis_status":
            mapping.append((name, "analysis_status"))
    return mapping


def validate_csv(path: Path, statuses: dict[str, set[str]]) -> list[str]:
    table = wc.read_table(path)
    if table["kind"] or table["errors"]:
        return table["errors"]
    errors: list[str] = list(table["errors"])
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        lowered_name = path.name.lower()
        for name_fragment, required_column in REQUIRED_STATUS_COLUMNS:
            if name_fragment in lowered_name and required_column not in fieldnames:
                try:
                    rel = path.relative_to(ROOT)
                except ValueError:
                    rel = path
                errors.append(f"{rel}: missing required status column {required_column!r}")
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
    return sorted(set(path for target in paths for path in wc.csv_files(target)))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate evidence status values in CSV files.")
    parser.add_argument("paths", nargs="+", help="CSV files or directories to validate")
    args = parser.parse_args()

    statuses = load_statuses()
    csv_files = iter_csv([Path(p) for p in args.paths])
    errors = [f"Input does not exist: {path}" for path in args.paths if not Path(path).exists()]
    if not csv_files:
        errors.append("No CSV files were checked.")
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
