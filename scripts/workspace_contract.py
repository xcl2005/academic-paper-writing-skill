"""Shared CSV contracts and offline evidence checks. No online truth certification."""
from __future__ import annotations

import csv
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".venv", "__pycache__", ".academic-backups"}


@lru_cache(maxsize=1)
def contract() -> dict:
    return yaml.safe_load((ROOT / "schemas/workspace_contract.yaml").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def statuses() -> dict:
    return yaml.safe_load((ROOT / "schemas/evidence_status.schema.yaml").read_text(encoding="utf-8"))


def csv_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".csv" else []
    if not target.is_dir():
        return []
    return sorted(p for p in target.rglob("*.csv") if not (set(p.relative_to(target).parts) & IGNORED_PARTS))


def table_name(path: Path, fields: list[str]) -> str | None:
    name = path.stem.replace("-", "_")
    tables = contract()["tables"]
    for key in tables:
        if key in name:
            return key
    if "expected_evidence" in fields and "current_status" in fields:
        return "graduation_evidence_map"
    for key, spec in tables.items():
        if spec.get("id") in fields:
            return key
    return None


def read_table(path: Path) -> dict:
    errors: list[str] = []
    rows: list[dict] = []
    fields: list[str] = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            fields = reader.fieldnames or []
            if not fields or any(not field.strip() for field in fields):
                errors.append("missing or empty CSV header")
            if len(fields) != len(set(fields)):
                errors.append("duplicate CSV columns")
            for line, row in enumerate(reader, 2):
                if None in row or any(value is None for value in row.values()):
                    errors.append(f"row {line}: wrong column count")
                rows.append({key: (value or "").strip() for key, value in row.items() if key is not None})
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f"cannot read CSV: {exc}")
    kind = table_name(path, fields)
    spec = contract()["tables"].get(kind, {})
    if spec:
        missing = sorted(set(spec["columns"]) - set(fields))
        if missing:
            errors.append("missing columns: " + ", ".join(missing) + "; preview migrate_workspace.py for legacy data")
        seen: set[str] = set()
        for line, row in enumerate(rows, 2):
            for field in spec.get("required_values", []):
                if not row.get(field):
                    errors.append(f"row {line}: empty {field}")
            for field, choices in spec.get("enums", {}).items():
                allowed = statuses()[choices] if isinstance(choices, str) else choices
                value = row.get(field, "")
                if value and value not in allowed:
                    errors.append(f"row {line}: invalid {field}={value!r}; expected {allowed}")
            identity = row.get(spec.get("id", ""))
            if identity:
                if identity in seen:
                    errors.append(f"row {line}: duplicate {spec['id']}={identity}")
                seen.add(identity)
    return {"path": path, "kind": kind, "fields": fields, "rows": rows, "errors": [f"{path.as_posix()}: {error}" for error in errors]}


def workspace_root(target: Path) -> Path:
    if target.is_dir():
        return target
    parent = target.parent
    for candidate in [parent, *parent.parents]:
        if (candidate / "project_state.yaml").is_file():
            return candidate
    return parent


def load_workspace(target: Path) -> dict:
    if not target.exists() or (target.is_file() and target.suffix.lower() != ".csv"):
        return {"root": target, "tables": [], "records": {}, "errors": ["Expected an existing workspace directory or CSV ledger."]}
    root = workspace_root(target)
    tables = [read_table(path) for path in csv_files(root)]
    if target.is_file():
        tables = [table for table in tables if table["kind"] != "claim_ledger" or table["path"].resolve() == target.resolve()]
    errors = [error for table in tables for error in table["errors"]]
    records: dict[str, dict[str, dict]] = {}
    for table in tables:
        kind = table["kind"]
        spec = contract()["tables"].get(kind, {})
        field = spec.get("id")
        if not field:
            continue
        index = records.setdefault(kind, {})
        for row in table["rows"]:
            identity = row.get(field)
            if identity:
                if identity in index:
                    errors.append(f"duplicate {field} across workspace: {identity}")
                index[identity] = row
    return {"root": root, "tables": tables, "records": records, "errors": errors}


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def missing_values(row: dict, fields: list[str], label: str) -> list[str]:
    return [f"{label}: missing/invalid {field}" for field in fields if not isinstance(row.get(field), str) or not row[field].strip() or row[field].lower() in {"none", "unknown", "tbd", "n/a"}]


def review_errors(row: dict, label: str) -> list[str]:
    errors = missing_values(row, ["reviewed_by", "reviewed_at"], label)
    try:
        checked = date.fromisoformat(row.get("reviewed_at", ""))
        # A date-only review may come from any timezone, including UTC+14.
        latest_calendar_date = (datetime.now(timezone.utc) + timedelta(hours=14)).date()
        if checked > latest_calendar_date:
            errors.append(f"{label}: review date is in the future")
    except (ValueError, TypeError):
        errors.append(f"{label}: reviewed_at must be an ISO date (YYYY-MM-DD)")
    return errors


def artifact_errors(root: Path, value: str, label: str) -> list[str]:
    if not value:
        return [f"{label}: missing artifact_path"]
    path = Path(value)
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root.resolve()):
        return [f"{label}: artifact_path must stay inside the workspace"]
    if not resolved.is_file() or resolved.stat().st_size == 0:
        return [f"{label}: missing or empty artifact {value}"]
    return []


def source_errors(workspace: dict, identity: str) -> list[str]:
    source = workspace["records"].get("literature_matrix", {}).get(identity)
    label = f"source {identity}"
    if not source:
        return [f"{label}: unresolved source_id (paper_id)"]
    errors = missing_values(source, ["source_url_or_doi", "read_scope"], label)
    if source.get("verification_status") != "verified":
        errors.append(f"{label}: verification_status must be verified, got {source.get('verification_status')}")
    reference = source.get("source_url_or_doi", "")
    if reference and not re.match(r"^(https?://\S+|(?:doi:)?10\.\d{4,9}/\S+)$", reference, re.I):
        errors.extend(artifact_errors(workspace["root"], reference, label))
    errors.extend(review_errors(source, label))
    return errors


def result_errors(workspace: dict, identity: str) -> list[str]:
    result = workspace["records"].get("experiment_matrix", {}).get(identity)
    label = f"result {identity}"
    if not result:
        return [f"{label}: unresolved result_id (experiment_id)"]
    errors = missing_values(result, ["result_summary", "code_version", "data_ids", "procedure"], label)
    if result.get("result_status") != "achieved":
        errors.append(f"{label}: result is not achieved")
    errors.extend(artifact_errors(workspace["root"], result.get("artifact_path", ""), label))
    for data_id in split_ids(result.get("data_ids", "")):
        data = workspace["records"].get("data_provenance", {}).get(data_id)
        if not data:
            errors.append(f"{label}: unresolved data_id {data_id}")
        else:
            if data.get("verification_status") != "verified" or data.get("data_status") not in {"available", "derived", "restricted", "archived"}:
                errors.append(f"{label}: data {data_id} is not verified and available")
            errors.extend(missing_values(data, ["source_or_owner", "license_or_permission", "version_or_date"], f"data {data_id}"))
            if data.get("storage_location"):
                errors.extend(artifact_errors(workspace["root"], data["storage_location"], f"data {data_id}"))
            elif not data.get("access_route"):
                errors.append(f"data {data_id}: missing storage_location or access_route")
    return errors


def evidence_errors(workspace: dict, identity: str, claim_id: str | None = None) -> list[str]:
    evidence = workspace["records"].get("evidence_records", {}).get(identity)
    label = f"evidence {identity}"
    if not evidence:
        return [f"{label}: unresolved evidence_id"]
    errors = missing_values(evidence, ["locator"], label)
    if evidence.get("review_status") != "verified":
        errors.append(f"{label}: support relationship requires verified review")
    errors.extend(review_errors(evidence, label))
    if claim_id and claim_id not in split_ids(evidence.get("supports_claim_ids", "")):
        errors.append(f"{label}: support relationship does not name claim {claim_id}")
    if not any(evidence.get(field) for field in ["source_id", "result_id", "artifact_path"]):
        errors.append(f"{label}: no source, result, or artifact")
    if evidence.get("source_id"):
        errors.extend(source_errors(workspace, evidence["source_id"]))
    if evidence.get("result_id"):
        errors.extend(result_errors(workspace, evidence["result_id"]))
    if evidence.get("artifact_path"):
        errors.extend(artifact_errors(workspace["root"], evidence["artifact_path"], label))
    return errors


def claim_errors(workspace: dict, row: dict) -> list[str]:
    kind = row.get("claim_kind", "factual")
    status = row.get("status", "")
    if kind in {"limitation", "proposal", "assumption"}:
        if status != "unknown" or row.get("strength") not in {"low", "none"}:
            return ["Non-factual notes require status=unknown and strength=low/none; do not use them to assert results."]
        return []
    errors: list[str] = []
    if status != "supported":
        errors.append(f"Factual claim is {status or 'missing status'}, not supported; add evidence or retain it in the backlog.")
    errors.extend(missing_values(row, ["evidence_type", "evidence_ids", "strength"], "claim"))
    for identity in split_ids(row.get("evidence_ids", "")):
        errors.extend(evidence_errors(workspace, identity, row.get("claim_id")))
    return errors
