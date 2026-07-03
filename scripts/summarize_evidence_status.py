#!/usr/bin/env python3
"""Summarize evidence/status columns across an academic workspace."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import validate_evidence_status as evidence_status


def count_file(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        checks = evidence_status.status_columns(fieldnames)
        if not checks:
            return rows
        data = list(reader)
    for column, status_group in checks:
        counts: Counter[str] = Counter()
        empty_count = 0
        for row in data:
            value = (row.get(column) or "").strip()
            if value:
                counts[value] += 1
            else:
                empty_count += 1
        rows.append({
            "file": path.as_posix(),
            "column": column,
            "status_group": status_group,
            "row_count": len(data),
            "empty_count": empty_count,
            "counts": dict(sorted(counts.items())),
        })
    return rows


def build_summary(paths: list[Path]) -> dict[str, object]:
    csv_files = evidence_status.iter_csv(paths)
    files: list[dict[str, object]] = []
    totals: dict[str, Counter[str]] = defaultdict(Counter)
    for path in csv_files:
        for item in count_file(path):
            files.append(item)
            group = str(item["status_group"])
            counts = item["counts"]
            assert isinstance(counts, dict)
            totals[group].update({str(key): int(value) for key, value in counts.items()})
    return {
        "targets": [path.as_posix() for path in paths],
        "checked_csv_files": [path.as_posix() for path in csv_files],
        "status_column_count": len(files),
        "files": files,
        "totals_by_group": {group: dict(sorted(counter.items())) for group, counter in sorted(totals.items())},
    }


def render_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "-"
    return ", ".join(f"{key}: {value}" for key, value in counts.items())


def render_markdown(summary: dict[str, object]) -> str:
    files = summary["files"]
    assert isinstance(files, list)
    lines = [
        "# Evidence Status Summary",
        "",
        "Targets: " + ", ".join(f"`{target}`" for target in summary["targets"]),
        f"CSV files checked: {len(summary['checked_csv_files'])}",
        f"Status columns found: {summary['status_column_count']}",
        "",
    ]
    if not files:
        lines.extend(["No status columns found.", ""])
        return "\n".join(lines)
    lines.extend([
        "| File | Column | Group | Rows | Empty | Counts |",
        "|---|---|---|---:|---:|---|",
    ])
    for item in files:
        assert isinstance(item, dict)
        counts = item["counts"]
        assert isinstance(counts, dict)
        lines.append(
            "| {file} | {column} | {group} | {rows} | {empty} | {counts} |".format(
                file=item["file"],
                column=item["column"],
                group=item["status_group"],
                rows=item["row_count"],
                empty=item["empty_count"],
                counts=render_counts({str(k): int(v) for k, v in counts.items()}),
            )
        )
    lines.append("")
    lines.append("## Totals By Group")
    lines.append("")
    totals = summary["totals_by_group"]
    assert isinstance(totals, dict)
    for group, counts in totals.items():
        assert isinstance(counts, dict)
        lines.append(f"- `{group}`: {render_counts({str(k): int(v) for k, v in counts.items()})}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize evidence status values in CSV files.")
    parser.add_argument("paths", nargs="+", help="CSV files or directories to summarize")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--report", help="Write Markdown report to this path")
    args = parser.parse_args()

    summary = build_summary([Path(path) for path in args.paths])
    markdown = render_markdown(summary)
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
