#!/usr/bin/env python3
"""Canonical positive controls and regression cases for the evidence contract."""
from __future__ import annotations

import csv
from datetime import date, datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml
import check_stage_gate as stage
import migrate_workspace
import pre_prose_check as prose
import workspace_contract as wc


class WorkspaceCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="academic-evidence-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.today = date.today().isoformat()
        self.state = {"workspace_schema_version": 2, "project_type": "research_paper", "stage": "drafting", "topic": "Synthetic fixture only", "study_design": "experimental", "gate_reviews": {name: {"reviewed_by": "test-only reviewer", "reviewed_at": self.today, "scope": "Synthetic local fixture only", "decision": "ready"} for name in stage.GATES}}
        self.save_state()
        self.text("evidence/fixture.txt", "Synthetic fixture only. Two items: A and B.\n")
        self.put("claim_ledger", {"claim_id": "C1", "claim_text": "The fixture contains two items.", "section": "Results", "strength": "low", "evidence_type": "local fixture", "evidence_source": "P1", "status": "supported", "claim_kind": "factual", "output_scope": "active", "evidence_ids": "EV1"})
        self.put("literature_matrix", {"paper_id": "P1", "title": "Synthetic fixture", "source_url_or_doi": "evidence/fixture.txt", "verification_status": "verified", "read_scope": "Entire two-item fixture", "reviewed_by": "test-only reviewer", "reviewed_at": self.today})
        self.put("evidence_records", {"evidence_id": "EV1", "source_id": "P1", "locator": "line 1", "supports_claim_ids": "C1", "review_status": "verified", "reviewed_by": "test-only reviewer", "reviewed_at": self.today, "limitations": "Only describes synthetic fixture contents"})

    def path(self, kind):
        folder = "" if kind == "claim_ledger" else "evidence" if kind in {"evidence_records", "requirement_register", "graduation_evidence_map"} else "matrices"
        return self.root / folder / (kind + ".csv")

    def text(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def put(self, kind, row):
        path = self.path(kind)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=wc.contract()["tables"][kind]["columns"])
            writer.writeheader()
            writer.writerows(row if isinstance(row, list) else [row])

    def change(self, kind, **changes):
        row = wc.read_table(self.path(kind))["rows"][0]
        row.update(changes)
        self.put(kind, row)

    def save_state(self):
        self.text("project_state.yaml", yaml.safe_dump(self.state))

    def decision(self):
        return prose.build_report(self.root)["decision"]

    def add_result(self):
        self.put("experiment_matrix", {"experiment_id": "X1", "research_question": "Count fixture items", "procedure": "Read both labels", "result_status": "achieved", "result_summary": "Two labels", "artifact_path": "evidence/fixture.txt", "data_ids": "D1", "code_version": "fixture-v1"})
        self.put("data_provenance", {"asset_id": "D1", "asset_type": "synthetic", "source_or_owner": "test suite", "license_or_permission": "repository MIT", "version_or_date": "v1", "storage_location": "evidence/fixture.txt", "data_status": "available", "verification_status": "verified"})
        self.change("evidence_records", source_id="", result_id="X1")


class ClaimTests(WorkspaceCase):
    def test_date_only_review_across_timezones(self):
        with patch.object(wc, "datetime") as clock:
            clock.now.return_value = datetime(2026, 9, 2, 21, 0, tzinfo=timezone.utc)
            self.assertFalse(wc.review_errors({"reviewed_by": "test reviewer", "reviewed_at": "2026-09-03"}, "review"))
            self.assertTrue(wc.review_errors({"reviewed_by": "test reviewer", "reviewed_at": "2026-09-04"}, "review"))

    def test_positive_control(self):
        self.assertEqual(self.decision(), "ready_for_human_review")

    def test_supported_empty_evidence(self):
        self.change("claim_ledger", evidence_ids="", evidence_type="")
        self.assertEqual(self.decision(), "blocked")

    def test_unknown_numeric_and_non_english(self):
        for text in ["Accuracy reached 99 percent.", "准确率达到百分之九十九。", "La precision atteint 99 pour cent."]:
            with self.subTest(text=text):
                self.change("claim_ledger", claim_text=text, status="unknown", strength="high")
                self.assertEqual(self.decision(), "blocked")

    def test_explicit_unknown_limitation_is_allowed(self):
        self.change("claim_ledger", claim_text="School requirements remain unknown pending the handbook.", claim_kind="limitation", status="unknown", strength="low", evidence_ids="", evidence_type="")
        self.assertEqual(self.decision(), "ready_for_human_review")

    def test_high_strength_nonfactual_is_not_a_bypass(self):
        self.change("claim_ledger", claim_kind="assumption", status="unknown", strength="high")
        self.assertEqual(self.decision(), "blocked")

    def test_unsupported_backlog_does_not_block_current_output(self):
        row = wc.read_table(self.path("claim_ledger"))["rows"][0]
        self.put("claim_ledger", [row, {**row, "claim_id": "C2", "status": "unsupported", "output_scope": "backlog", "evidence_ids": ""}])
        self.assertEqual(self.decision(), "ready_for_human_review")

    def test_section_scope(self):
        row = wc.read_table(self.path("claim_ledger"))["rows"][0]
        self.put("claim_ledger", [row, {**row, "claim_id": "C2", "status": "unknown", "section": "Discussion"}])
        self.assertEqual(self.decision(), "blocked")
        self.assertEqual(prose.build_report(self.root, "Results")["decision"], "ready_for_human_review")
        self.assertEqual(prose.build_report(self.root, "Absent")["decision"], "blocked")

    def test_source_downgrade_propagates(self):
        for status in ["missing_source", "needs_recheck", "user_provided", "unknown"]:
            self.change("literature_matrix", verification_status=status)
            self.assertEqual(self.decision(), "blocked")

    def test_dangling_evidence_source_and_result(self):
        self.change("claim_ledger", evidence_ids="MISSING")
        self.assertEqual(self.decision(), "blocked")
        self.change("claim_ledger", evidence_ids="EV1")
        self.change("evidence_records", source_id="MISSING")
        self.assertEqual(self.decision(), "blocked")
        self.change("evidence_records", source_id="", result_id="MISSING")
        self.assertEqual(self.decision(), "blocked")

    def test_support_relation_and_review_required(self):
        for changes in [{"supports_claim_ids": "C2"}, {"reviewed_by": ""}, {"reviewed_at": "not-a-date"}, {"locator": ""}, {"review_status": "unknown"}]:
            original = wc.read_table(self.path("evidence_records"))["rows"][0]
            self.change("evidence_records", **changes)
            self.assertEqual(self.decision(), "blocked")
            self.put("evidence_records", original)

    def test_missing_and_outside_artifact(self):
        for value in ["missing.txt", "../outside.txt", str(self.root.parent / "outside.txt")]:
            self.change("evidence_records", source_id="", artifact_path=value)
            self.assertEqual(self.decision(), "blocked")

    def test_result_lifecycle_and_data(self):
        self.add_result()
        self.assertEqual(self.decision(), "ready_for_human_review")
        for status in ["planned", "preliminary", "not_run", "unknown"]:
            self.change("experiment_matrix", result_status=status)
            self.assertEqual(self.decision(), "blocked")
        self.change("experiment_matrix", result_status="achieved", data_ids="MISSING")
        self.assertEqual(self.decision(), "blocked")

    def test_duplicate_and_malformed_records(self):
        row = wc.read_table(self.path("evidence_records"))["rows"][0]
        self.put("evidence_records", [row, row])
        self.assertEqual(self.decision(), "blocked")
        self.text("claim_ledger.csv", 'claim_id,claim_text,status\nC1,"unfinished,supported\n')
        self.assertEqual(self.decision(), "blocked")

    def test_missing_columns(self):
        self.text("matrices/screening_log.csv", "record_id,screening_status\nR1,include\n")
        self.assertTrue(wc.read_table(self.path("screening_log"))["errors"])

    def test_no_input_never_approves(self):
        for target in [self.root / "absent", self.root / "empty", self.root / "evidence/fixture.txt"]:
            if target.name == "empty":
                target.mkdir()
            self.assertEqual(prose.build_report(target)["decision"], "blocked")


class StageGateTests(WorkspaceCase):
    def setUp(self):
        super().setUp()
        self.text("integrity_checklist.md", "# Integrity\nGate status: ready\n- [x] Synthetic evidence reviewed.\n")
        self.text("reports/submission_package_checklist.md", "# Package\nGate status: ready\n- [x] Fixture only, no actual submission.\n")

    def gate(self, name="drafting", allow_empty=False):
        return stage.check(self.root, name, allow_empty)["decision"]

    def test_ready_drafting_with_recorded_review(self):
        self.assertEqual(self.gate(), "ready_for_handoff")

    def test_missing_signoff_requires_review(self):
        self.state["gate_reviews"] = {}
        self.save_state()
        self.assertEqual(self.gate(), "evidence_review_required")

    def test_empty_missing_status_and_unchecked_markdown(self):
        for text in ["", "# Integrity\n", "Gate status: ready\n- [ ] Pending\n", "Gate status: ready\n- Source:\n"]:
            self.text("integrity_checklist.md", text)
            self.assertEqual(self.gate(), "blocked")

    def test_unsupported_claim_blocks_stage(self):
        self.change("claim_ledger", status="unsupported")
        self.assertEqual(self.gate(), "blocked")

    def test_structure_check_is_not_readiness(self):
        self.text("integrity_checklist.md", "")
        self.assertEqual(self.gate(allow_empty=True), "structure_valid")

    def test_literature_missing_source_blocks(self):
        self.text("evidence/search_protocol.md", "Gate status: ready\nFixture query Q1 only.\n")
        self.put("screening_log", {"record_id": "R1", "title": "Fixture", "identifier": "P1", "query_id": "Q1", "found_date": self.today, "inclusion_reason": "test scope", "screening_status": "include", "verification_status": "verified"})
        self.assertEqual(self.gate("literature"), "ready_for_handoff")
        self.change("literature_matrix", verification_status="missing_source")
        self.assertEqual(self.gate("literature"), "blocked")

    def test_analysis_requires_completed_result(self):
        self.add_result()
        self.text("matrices/statistical_analysis_plan.md", "Gate status: ready\nCount two fixture labels. No inference.\n")
        self.assertEqual(self.gate("analysis"), "ready_for_handoff")
        self.change("experiment_matrix", result_status="planned")
        self.assertEqual(self.gate("analysis"), "blocked")

    def test_explicit_nonexperimental_exemption(self):
        self.state["study_design"] = "theoretical"
        self.state["gate_exemptions"] = {"analysis": {"reason": "Proof-only project; no quantitative result asserted", "reviewed_by": "test-only reviewer", "reviewed_at": self.today}}
        self.save_state()
        self.assertEqual(self.gate("analysis"), "not_applicable")
        self.state["study_design"] = "experimental"
        self.save_state()
        self.assertEqual(self.gate("analysis"), "blocked")

    def test_thesis_must_have_verified_requirements_and_evidence(self):
        self.state["project_type"] = "undergraduate_thesis"
        self.save_state()
        self.assertEqual(self.gate("submission"), "blocked")
        self.put("requirement_register", {"requirement_id": "REQ1", "requirement_text": "Document the fixture items", "source_id": "P1", "locator": "line 1", "verification_status": "verified", "applicability": "required", "acceptance_criteria": "Evidence lists both items"})
        self.put("graduation_evidence_map", {"section": "Results", "current_status": "complete", "requirement_id": "REQ1", "evidence_ids": "EV1"})
        self.text("evidence/requirement_discovery_log.md", "Gate status: ready\nREQ1 is synthetic, not a real school requirement.\n")
        self.assertEqual(self.gate("submission"), "ready_for_handoff")
        self.change("graduation_evidence_map", requirement_id="MISSING")
        self.assertEqual(self.gate("submission"), "blocked")

    def test_invalid_yaml_and_unknown_schema(self):
        self.text("project_state.yaml", "type: [invalid")
        self.assertEqual(self.gate(), "blocked")

    def test_invalid_yaml_value_types_block_without_traceback(self):
        self.state["project_type"] = ["research_paper"]
        self.state["workspace_schema_version"] = [2]
        self.save_state()
        self.assertEqual(self.gate(), "blocked")
        self.state["workspace_schema_version"] = 999
        self.save_state()
        self.assertEqual(self.gate(), "blocked")


class InitializationMigrationTests(unittest.TestCase):
    def test_initializer_preserves_existing_work_and_rejects_type_conflict(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "project_state.yaml"
            original = "project_type: research_paper\ntopic: Keep my topic\n"
            path.write_text(original, encoding="utf-8")
            command = [sys.executable, str(wc.ROOT / "scripts/init_project.py"), "--out", str(root), "--type"]
            self.assertEqual(subprocess.run(command + ["research_paper"], capture_output=True).returncode, 0)
            self.assertNotEqual(subprocess.run(command + ["undergraduate_thesis"], capture_output=True).returncode, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_all_modes_initialize_consistently(self):
        with tempfile.TemporaryDirectory() as temp:
            for mode in stage.PROJECT_TYPES:
                out = Path(temp) / mode
                result = subprocess.run([sys.executable, str(wc.ROOT / "scripts/init_project.py"), "--out", str(out), "--type", mode], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                state = yaml.safe_load((out / "project_state.yaml").read_text(encoding="utf-8"))
                self.assertEqual(state["project_type"], mode)
                for gate in ["literature", "analysis"]:
                    self.assertEqual(stage.check(out, gate, True)["decision"], "structure_valid")
                    self.assertEqual(stage.check(out, gate, False)["decision"], "blocked")

    def test_legacy_migration_preview_backup_and_idempotence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "claim_ledger.csv"
            original = "claim_id,claim,status,evidence_pointer\nC1,Unknown finding,unknown,none\n"
            path.write_text(original, encoding="utf-8")
            report = migrate_workspace.migrate(root)
            self.assertTrue(report["changes"])
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            report = migrate_workspace.migrate(root, True)
            self.assertEqual((Path(report["backup"]) / path.name).read_text(encoding="utf-8"), original)
            self.assertEqual(wc.read_table(path)["rows"][0]["status"], "unknown")
            self.assertFalse(wc.read_table(path)["errors"])
            self.assertFalse(migrate_workspace.migrate(root)["changes"])
            self.assertEqual(prose.build_report(root)["decision"], "blocked")


if __name__ == "__main__":
    unittest.main()
