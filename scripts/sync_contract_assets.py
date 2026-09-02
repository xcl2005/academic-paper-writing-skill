"""Check or regenerate header-only templates and legacy schema reference files."""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

import yaml
from workspace_contract import ROOT, contract

SCHEMA_NAMES = {"research_idea_portfolio": "idea_portfolio"}


def sync(write: bool = False) -> list[str]:
    errors = []
    for name, spec in contract()["tables"].items():
        template = ROOT / "templates" / (name + ".csv")
        buffer = io.StringIO(newline="")
        csv.writer(buffer, lineterminator="\n").writerow(spec["columns"])
        expected = buffer.getvalue()
        if not template.exists() or template.read_text(encoding="utf-8") != expected:
            if write:
                if template.exists() and len(list(csv.reader(template.read_text(encoding="utf-8").splitlines()))) > 1:
                    raise ValueError(f"Refusing to overwrite data rows in {template}")
                template.write_text(expected, encoding="utf-8")
            else:
                errors.append(f"template out of sync: {template.name}")
        schema = ROOT / "schemas" / (SCHEMA_NAMES.get(name, name) + ".schema.yaml")
        expected_schema = yaml.safe_dump({"contract": "workspace_contract.yaml", "table": name}, sort_keys=False)
        if not schema.exists() or schema.read_text(encoding="utf-8") != expected_schema:
            if write:
                schema.write_text(expected_schema, encoding="utf-8")
            else:
                errors.append(f"schema reference out of sync: {schema.name}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    failures = sync(args.write)
    print("\n".join(failures) if failures else "Contract assets are synchronized.")
    raise SystemExit(bool(failures))
