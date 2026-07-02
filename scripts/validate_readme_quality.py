from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_ZH = ROOT / "README.md"
README_EN = ROOT / "README_EN.md"
LEGACY_ZH = ROOT / "README_ZH.md"

FORBIDDEN_PATTERNS = {
    "Mermaid diagrams": re.compile(r"```mermaid", re.IGNORECASE),
    "large README images": re.compile(r"<img[^>]+width=[\"']?100%[\"']?", re.IGNORECASE),
    "stale hero assets": re.compile(r"assets/(hero|workflow)\.svg|hero\.svg|workflow\.svg", re.IGNORECASE),
    "diagram residue": re.compile(r"workflow\s+diagram|流程图", re.IGNORECASE),
}

REQUIRED_ZH = [
    "简体中文",
    "README_EN.md",
    "快速开始",
    "Codex / Claude Code",
    "完整性规则",
    "模块路由",
    "搜索关键词",
]

REQUIRED_EN = [
    "English",
    "README.md",
    "Quick Start",
    "Codex / Claude Code",
    "Integrity Rules",
    "Module Routing",
    "Search Keywords",
]


def fail(message: str) -> None:
    print(f"README quality check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_file(path: Path, required_terms: list[str], min_chars: int) -> None:
    if not path.exists():
        fail(f"{path.name} is missing")

    text = path.read_text(encoding="utf-8")

    if len(text) < min_chars:
        fail(f"{path.name} is too thin for this skill ({len(text)} chars)")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(text):
            fail(f"{path.name} contains forbidden {label}")

    missing = [term for term in required_terms if term not in text]
    if missing:
        fail(f"{path.name} missing required terms: {', '.join(missing)}")

    badge_count = text.count("img.shields.io")
    if badge_count < 5:
        fail(f"{path.name} should keep a compact badge row")

    table_count = text.count("|---")
    if table_count < 5:
        fail(f"{path.name} should document the workflow with tables")


def main() -> None:
    check_file(README_ZH, REQUIRED_ZH, 5_500)
    check_file(README_EN, REQUIRED_EN, 5_500)

    if LEGACY_ZH.exists():
        legacy_text = LEGACY_ZH.read_text(encoding="utf-8")
        if "README.md" not in legacy_text or "README_EN.md" not in legacy_text:
            fail("README_ZH.md should point readers to README.md and README_EN.md")

    assets_dir = ROOT / "assets"
    if assets_dir.exists():
        fail("assets directory still exists; remove generated README hero images")

    print("README quality check passed.")


if __name__ == "__main__":
    main()
