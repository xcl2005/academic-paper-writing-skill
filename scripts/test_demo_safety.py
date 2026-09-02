"""Demo replacement must not delete unowned folders or user additions."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import demo_academic_workflow as demo


class DemoSafetyTests(unittest.TestCase):
    def test_reject_unowned_directory_and_protected_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            important = root / "research.txt"
            important.write_text("Keep this", encoding="utf-8")
            for target in [root, demo.ROOT, demo.ROOT.parent, Path(root.anchor)]:
                with self.subTest(target=target), self.assertRaises(ValueError):
                    demo.build_demo(target, "research_paper", True)
            self.assertEqual(important.read_text(encoding="utf-8"), "Keep this")

    def test_owned_replacement_and_user_addition(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "demo"
            demo.build_demo(out, "research_paper")
            before = (out / "claim_ledger.csv").read_bytes()
            demo.build_demo(out, "research_paper", True)
            self.assertEqual(before, (out / "claim_ledger.csv").read_bytes())
            addition = out / "my-notes.txt"
            addition.write_text("User notes", encoding="utf-8")
            with self.assertRaises(ValueError):
                demo.build_demo(out, "research_paper", True)
            self.assertTrue(addition.is_file())

    def test_failed_generation_preserves_previous_demo(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "demo"
            demo.build_demo(out, "research_paper")
            before = (out / "DEMO_MANIFEST.json").read_bytes()
            with patch.object(demo, "populate_research_demo", side_effect=ValueError("Synthetic generation failure")):
                with self.assertRaises(ValueError):
                    demo.build_demo(out, "research_paper", True)
            self.assertEqual(before, (out / "DEMO_MANIFEST.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
