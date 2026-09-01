#!/usr/bin/env python3
"""Behavioral tests for ready and blocked research stage gates."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import check_stage_gate


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="academic-stage-gate-") as temp:
        root = Path(temp)
        write(root / "project_state.yaml", "project_type: research_paper\nstage: analysis\ntopic: test topic\n")
        write(root / "matrices/research_idea_portfolio.csv", "idea_id,decision_status\nI1,selected\n")
        write(root / "evidence/search_protocol.md", "# Search Protocol\n\nGate status: ready\n")
        write(root / "matrices/screening_log.csv", "record_id,screening_status\nR1,include\n")
        write(root / "matrices/literature_matrix.csv", "paper_id,verification_status\nP1,verified\n")
        write(root / "matrices/statistical_analysis_plan.md", "# Statistical Analysis Plan\n\nGate status: ready\n")
        write(root / "matrices/data_provenance.csv", "asset_id,data_status\nD1,available\n")
        write(root / "matrices/experiment_matrix.csv", "experiment_id,result_status\nE1,achieved\n")
        write(root / "claim_ledger.csv", "claim_id,status\nC1,supported\n")
        write(root / "integrity_checklist.md", "# Integrity Checklist\n")
        write(root / "reports/submission_package_checklist.md", "# Submission Package\n\nGate status: ready\n")
        write(root / "evidence/paper_reading_note.md", "# Paper Reading Note\n\nGate status: ready\n")
        write(root / "reports/presentation_brief.md", "# Presentation Brief\n\nGate status: ready\n")

        for gate in check_stage_gate.GATES:
            report = check_stage_gate.check(root, gate, allow_empty=False)
            if report["decision"] != "ready_for_handoff":
                print(f"Expected ready gate {gate}, got: {report}")
                return 1

        write(root / "evidence/search_protocol.md", "# Search Protocol\n\nGate status: draft\n")
        blocked = check_stage_gate.check(root, "literature", allow_empty=False)
        if blocked["decision"] != "blocked":
            print(f"Expected blocked literature gate, got: {blocked}")
            return 1

    print("Stage gate tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
