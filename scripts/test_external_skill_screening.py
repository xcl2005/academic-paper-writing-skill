import tempfile
from pathlib import Path
import unittest
import external_skill_gate as gate


class ScreeningTests(unittest.TestCase):
    def test_negated_and_positive_directives_differ(self):
        self.assertFalse(gate.risk_signals("Do not fabricate citations.")["requires_review"])
        self.assertTrue(gate.risk_signals("Fabricate citations.")["requires_review"])

    def test_mixed_clauses_are_not_treated_as_prohibitions(self):
        self.assertTrue(gate.risk_signals("Do not fabricate citations but invent results.")["requires_review"])

    def test_documentation_score_is_never_acceptance(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "sample"
            root.mkdir()
            (root / "SKILL.md").write_text("---\nname: sample\ndescription: Academic example\n---\nReview citations. Never fabricate citations.\n", encoding="utf-8")
            report = gate.screen_candidate(root)
            self.assertFalse(report["accepted"])
            self.assertEqual(report["decision"], "needs_review")
            self.assertTrue(report["not_checked"])


if __name__ == "__main__":
    unittest.main()
