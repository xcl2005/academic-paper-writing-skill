#!/usr/bin/env python3
"""Offline helper to inspect an external skill/tool directory.
This does not install anything; it only checks basic compatibility signals.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from resolve_capability import inspect_skill

GOOD_FILES = ["SKILL.md", "README.md", "LICENSE", "LICENSE.md", "pyproject.toml", "package.json"]
RISK_WORDS = ["fabricate citation", "fake citation", "invent results", "disable safety"]


def score_candidate(path: Path) -> tuple[int, list[str]]:
    notes: list[str] = []
    score = 0
    existing = {p.name.lower() for p in path.iterdir()} if path.is_dir() else set()

    if "skill.md" in existing:
        score += 25
        notes.append("has SKILL.md")
    if "readme.md" in existing:
        score += 20
        notes.append("has README.md")
    if "license" in existing or "license.md" in existing:
        score += 10
        notes.append("has license")

    text = ""
    for name in ["SKILL.md", "README.md"]:
        f = path / name
        if f.exists():
            text += f.read_text(encoding="utf-8", errors="ignore").lower()[:20000]

    if any(k in text for k in ["paper", "academic", "latex", "citation", "review", "literature"]):
        score += 20
        notes.append("academic-paper related keywords found")
    if any(k in text for k in ["example", "usage", "install", "template"]):
        score += 10
        notes.append("has usage/install/template signals")
    if risk_signals(text)["requires_review"]:
        score -= 30
        notes.append("risk phrase found")

    score = max(0, min(100, score))
    return score, notes


def risk_signals(text: str) -> dict:
    risky, prohibited = [], []
    for clause in re.split(r"[\n.;]|\bbut\b", text.lower()):
        for phrase in RISK_WORDS:
            for match in re.finditer(re.escape(phrase), clause):
                prefix = clause[:match.start()]
                if re.search(r"(?:do not|must not|never|avoid|no)\s+(?:\w+\s+){0,2}$", prefix):
                    prohibited.append(phrase)
                else:
                    risky.append(phrase)
    return {"requires_review": sorted(set(risky)), "explicit_prohibitions": sorted(set(prohibited))}


def screen_candidate(path: Path) -> dict:
    score, notes = score_candidate(path)
    texts = []
    for name in ["SKILL.md", "README.md"]:
        file = path / name
        if file.is_file():
            texts.append(file.read_text(encoding="utf-8", errors="replace")[:20000])
    signals = risk_signals("\n".join(texts))
    inspection = inspect_skill(path / "SKILL.md" if (path / "SKILL.md").is_file() else None, path.name)
    return {"decision": "needs_review", "accepted": False, "documentation_signal_score": score,
            "notes": notes, "risk_signals": signals, "structure_errors": inspection["errors"],
            "checked": ["top-level documentation", "skill metadata and linked resources", "limited phrase context"],
            "not_checked": ["nested scripts", "runtime behavior", "task output", "all prompt-injection variants", "license validity"],
            "boundary": "Heuristic triage only. A high score is not a safety or suitability endorsement."}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.path)
    if not path.exists() or not path.is_dir():
        print("Candidate path not found or not a directory")
        return 1
    report = screen_candidate(path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report["risk_signals"]["requires_review"] or report["structure_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
