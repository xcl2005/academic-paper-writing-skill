from __future__ import annotations

import re
import struct
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
README_ZH = ROOT / "README.md"
README_EN = ROOT / "README_EN.md"
LEGACY_ZH = ROOT / "README_ZH.md"

FORBIDDEN_PATTERNS = {
    "Mermaid diagrams": re.compile(r"```mermaid", re.IGNORECASE),
    "full-width README images": re.compile(r"<img[^>]+width=[\"']?100%[\"']?", re.IGNORECASE),
    "diagram residue": re.compile(r"workflow\s+diagram|流程图", re.IGNORECASE),
    "release-note framing": re.compile(r"^##\s+(?:✨\s*)?v\d", re.IGNORECASE | re.MULTILINE),
    "internal module routing": re.compile(r"模块路由|Module Routing", re.IGNORECASE),
    "compatibility pitch": re.compile(r"原功能兼容|Original Feature Compatibility|Backward Compatibility", re.IGNORECASE),
    "SEO keyword dump": re.compile(r"搜索关键词|Search Keywords", re.IGNORECASE),
}

REQUIRED_ZH = [
    "assets/hero.png",
    "简体中文",
    "README_EN.md",
    "快速开始",
    "一次典型任务",
    "核心能力",
    "证据优先",
    "已接入的专业 Skill 生态",
    "K-Dense-AI/scientific-agent-skills",
    "Yuan1z0825/nature-skills",
    "Imbad0202/academic-research-skills-codex",
    "可插拔的专业能力",
    "capability_registry.yaml",
    "完整性边界",
]

REQUIRED_EN = [
    "assets/hero.png",
    "English",
    "README.md",
    "Quick Start",
    "A typical task",
    "Core capabilities",
    "Evidence first",
    "Integrated specialist-skill ecosystem",
    "K-Dense-AI/scientific-agent-skills",
    "Yuan1z0825/nature-skills",
    "Imbad0202/academic-research-skills-codex",
    "Pluggable specialist skills",
    "capability_registry.yaml",
    "Integrity boundary",
]


def fail(message: str) -> None:
    print(f"README quality check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_local_links(path: Path, text: str) -> None:
    targets = re.findall(r'\]\(([^)]+)\)|(?:src|href)=[\"\']([^\"\']+)[\"\']', text)
    for markdown_target, html_target in targets:
        target = markdown_target or html_target
        parsed = urlsplit(target.strip("<>"))
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        local_path = path.parent / unquote(parsed.path)
        if not local_path.exists():
            fail(f"{path.name} has a broken local link: {target}")


def check_file(path: Path, required_terms: list[str]) -> None:
    if not path.exists():
        fail(f"{path.name} is missing")

    text = path.read_text(encoding="utf-8")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(text):
            fail(f"{path.name} contains forbidden {label}")

    missing = [term for term in required_terms if term not in text]
    if missing:
        fail(f"{path.name} missing required terms: {', '.join(missing)}")

    first_section = text.find("\n## ")
    hero_position = text.find("assets/hero.png")
    if first_section == -1 or hero_position == -1 or hero_position > first_section:
        fail(f"{path.name} should show the project artwork before the first section")

    intro_end = text.find("</div>")
    intro = text[:intro_end] if intro_end != -1 else text[:first_section]
    badge_count = intro.count("img.shields.io")
    if not 3 <= badge_count <= 6:
        fail(f"{path.name} should keep a compact header badge row, found {badge_count}")

    if not re.search(r"assets/hero\.png[^>]+width=[\"']860[\"']", text, re.IGNORECASE):
        fail(f"{path.name} should render assets/hero.png at the reviewed 860px width")

    if len(re.findall(r"^# ", text, re.MULTILINE)) != 1:
        fail(f"{path.name} should have one project title")
    if len(re.findall(r"^```", text, re.MULTILINE)) % 2:
        fail(f"{path.name} has an unclosed code fence")
    for tag in ("details", "div"):
        if text.count(f"<{tag}>") + text.count(f"<{tag} ") != text.count(f"</{tag}>"):
            fail(f"{path.name} has unbalanced {tag} sections")

    check_local_links(path, text)


def check_hero() -> None:
    hero = ROOT / "assets" / "hero.png"
    if not hero.exists():
        fail("assets/hero.png is missing")

    with hero.open("rb") as image:
        header = image.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        fail("assets/hero.png is not a valid PNG")

    width, height = struct.unpack(">II", header[16:24])
    if width < 1_200 or height < 600:
        fail(f"assets/hero.png is too small for a crisp README header ({width}x{height})")


def main() -> None:
    check_file(README_ZH, REQUIRED_ZH)
    check_file(README_EN, REQUIRED_EN)
    check_hero()

    if LEGACY_ZH.exists():
        legacy_text = LEGACY_ZH.read_text(encoding="utf-8")
        if "README.md" not in legacy_text or "README_EN.md" not in legacy_text:
            fail("README_ZH.md should point readers to README.md and README_EN.md")

    print("README structure, bilingual navigation, local links, and artwork checks passed. Visual QA is separate.")


if __name__ == "__main__":
    main()
