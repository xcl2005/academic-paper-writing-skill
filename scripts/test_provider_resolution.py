#!/usr/bin/env python3
"""Isolated provider discovery tests; fixtures are never installed as skills."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch

import resolve_capability as resolver


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="academic-provider-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def install(self, name="scientific-brainstorming", text=None, root=None):
        path = (root or self.root) / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        if text is None:
            text = f"---\nname: {name}\ndescription: Isolated provider test.\n---\n\n# Test workflow\nThis fixture does not perform research.\n"
        path.write_text(text, encoding="utf-8")
        return path

    def resolve(self, capability="research_ideation", provider=None):
        return resolver.resolve(capability, provider, set(), [self.root])

    def test_valid_provider_requires_review(self):
        fixture = resolver.ROOT / "examples/fixtures/provider-skills/scientific-brainstorming/SKILL.fixture"
        self.install(text=fixture.read_text(encoding="utf-8"))
        result = self.resolve()
        self.assertEqual(result["decision"], "use_installed_provider")
        self.assertTrue(result["review_required"])
        self.assertFalse(result["accepted"])

    def test_invalid_provider_falls_back(self):
        for text in ["", "# No metadata", "---\nname: other\ndescription: test\n---\nBody", "---\nname: [broken\n---\nBody", "---\nname: scientific-brainstorming\ndescription: test\n---\n"]:
            with self.subTest(text=text):
                self.install(text=text)
                result = self.resolve()
                self.assertEqual(result["decision"], "use_internal_fallback")
                self.assertFalse(result["providers"][0]["usable"])

    def test_missing_resource_falls_back(self):
        path = self.install()
        path.write_text(path.read_text(encoding="utf-8") + "\n[guide](references/missing.md)\n", encoding="utf-8")
        self.assertEqual(self.resolve()["decision"], "use_internal_fallback")

    def test_invalid_companion_falls_back(self):
        self.install("nature-writing")
        self.install("nature-shared", "")
        self.assertEqual(self.resolve("manuscript_drafting", "nature-writing")["decision"], "requested_provider_unavailable")
        self.install("nature-shared")
        self.assertEqual(self.resolve("manuscript_drafting", "nature-writing")["decision"], "use_installed_provider")

    def test_missing_requested_provider(self):
        self.assertEqual(self.resolve(provider="scientific-brainstorming")["decision"], "requested_provider_unavailable")

    def test_explicit_roots_are_isolated(self):
        self.install()
        self.assertEqual(resolver.resolve("research_ideation", None, set(), [self.root / "empty"])["decision"], "use_internal_fallback")

    def test_claude_and_codex_paths(self):
        home = self.root / "home"
        cwd = self.root / "project"
        with patch.object(Path, "home", return_value=home), patch.object(Path, "cwd", return_value=cwd), patch.dict(os.environ, {}, clear=True):
            roots = resolver.candidate_roots()
            for expected in [cwd / ".claude/skills", home / ".claude/skills", cwd / ".agents/skills", home / ".agents/skills", home / ".codex/skills"]:
                self.assertIn(expected, roots)
            self.assertEqual(resolver.candidate_roots("claude")[0], cwd / ".claude/skills")

    def test_duplicate_precedence_is_visible(self):
        self.install()
        second = self.root / "second"
        self.install(root=second)
        result = resolver.resolve("research_ideation", None, set(), [self.root, second])
        self.assertEqual(result["provider_path"], str(self.root / "scientific-brainstorming/SKILL.md"))
        self.assertEqual(len(result["providers"][0]["duplicate_paths"]), 2)

    def test_installation_has_one_entrypoint(self):
        self.assertEqual([p for p in resolver.ROOT.rglob("SKILL.md") if ".git" not in p.parts], [resolver.ROOT / "SKILL.md"])


if __name__ == "__main__":
    unittest.main()
