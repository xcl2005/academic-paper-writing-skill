#!/usr/bin/env python3
"""Offline helper to inspect an external skill/tool directory.
This does not install anything; it only checks basic compatibility signals.
"""
from __future__ import annotations

import argparse
from pathlib import Path

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
    if any(r in text for r in RISK_WORDS):
        score -= 30
        notes.append("risk phrase found")

    score = max(0, min(100, score))
    return score, notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    path = Path(args.path)
    if not path.exists() or not path.is_dir():
        print("Candidate path not found or not a directory")
        return 1
    score, notes = score_candidate(path)
    print(f"score={score}")
    for note in notes:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
