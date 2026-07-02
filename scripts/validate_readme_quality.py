from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_FILES = [ROOT / "README.md", ROOT / "README_ZH.md"]

FORBIDDEN_PATTERNS = {
    "Mermaid diagrams": re.compile(r"```mermaid", re.IGNORECASE),
    "large README images": re.compile(r"<img[^>]+width=[\"']?100%[\"']?", re.IGNORECASE),
    "stale hero assets": re.compile(r"assets/(hero|workflow)\.svg|hero\.svg|workflow\.svg", re.IGNORECASE),
    "diagram residue": re.compile(r"\bchain\b|流程图", re.IGNORECASE),
}

REQUIRED_EN = [
    "English",
    "简体中文",
    "Install",
    "Control flow",
    "Module routing",
    "Evidence lifecycle",
    "Invariants",
    "Search keywords",
]

REQUIRED_ZH = [
    "English",
    "简体中文",
    "安装",
    "控制流程",
    "模块路由",
    "证据生命周期",
    "不可破坏的规则",
    "搜索关键词",
]


def fail(message: str) -> None:
    print(f"README quality check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_file(path: Path, required_terms: list[str]) -> None:
    if not path.exists():
        fail(f"{path.name} is missing")

    text = path.read_text(encoding="utf-8")

    if len(text) < 4_500:
        fail(f"{path.name} is too thin for this skill ({len(text)} chars)")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(text):
            fail(f"{path.name} contains forbidden {label}")

    missing = [term for term in required_terms if term not in text]
    if missing:
        fail(f"{path.name} missing required terms: {', '.join(missing)}")

    badge_count = text.count("img.shields.io")
    if badge_count < 4:
        fail(f"{path.name} should keep a compact badge row")

    table_count = text.count("|---")
    if table_count < 4:
        fail(f"{path.name} should document the workflow with tables")


def main() -> None:
    check_file(README_FILES[0], REQUIRED_EN)
    check_file(README_FILES[1], REQUIRED_ZH)

    assets_dir = ROOT / "assets"
    if assets_dir.exists():
        fail("assets directory still exists; remove ugly generated README images")

    print("README quality check passed.")


if __name__ == "__main__":
    main()
