# Changelog

## 0.1.0 - 2026-07-03

- Added CI workflow and validation badge.
- Added `scripts/demo_academic_workflow.py` for one-command evidence-first demo workspaces.
- Added sample source notes to make demo data boundaries explicit.
- Added validation coverage for the demo script and sample-source warning text.
- Added evidence-status schema and `scripts/validate_evidence_status.py` for machine-checkable source, claim, result, and artifact statuses.
- Added `scripts/check_claims_before_prose.py` plus claim fixtures to block unsupported strong claims before final prose.
- Added demo workspace manifests and `scripts/validate_demo_workspace.py` so CI verifies generated demo contents.
- Added SKILL.md negative triggers for ghostwriting-style requests and demo-sample misuse.
- Upgraded `scripts/check_claims_before_prose.py` to scan a workspace directory and generate Markdown/JSON pre-prose reports.
- Added committed generated thesis demo workspace and claim-blocker report with CI drift checks.
- Added required status-column checks for evidence CSVs.
- Added `SKILL.md` pre-prose checks so validation scripts are part of the skill call protocol.
- Added `scripts/pre_prose_check.py` as a one-command gate that combines evidence-status and claim-to-evidence checks.
- Added `scripts/summarize_evidence_status.py` and a generated summary report for workspace status counts.
- Added a Chinese unsupported-claim fixture so strong Chinese claims and local requirement claims stay covered by validation.
- Added issue and pull request templates for integrity risks, thesis workflows, template requests, guardrail improvements, and docs examples.
- Added filled sample outputs for literature matrices, claim ledgers, novelty checks, thesis scope, thesis evidence maps, and blocked related-work drafting.
- Added README `Star this if` / `Not for` blocks to position the skill as evidence review before prose, not ghostwriting.
- Added social preview copy guidance for GitHub repository sharing.
- Sharpened public positioning around evidence-first academic AI writing without hallucinated citations, fake evidence, or integrity drift.
- Added scenario examples for literature-review, undergraduate-thesis proposal, and rebuttal-response workflows.
- Added README demo, What you get, direct-AI comparison, text workflow, release badge, and example output links.
- Renamed the visible skill title to `Academic Paper Writing Skill`.
- Normalized `skill_manifest.yaml` version to `0.1.0` for the public release.
- Clarified that final prose should come after verifiable matrices, claim ledgers, and integrity checks.
- Kept the undergraduate thesis path uncertainty-aware: missing school, advisor, rubric, and workload requirements remain unknown until confirmed.

## Internal pre-release history

- Rechecked the overall workflow during internal modular-skill iteration.
- Added explicit compatibility with the user's existing skill-installer/self-updating skill workflow.
- Added `External Skill Gateway` with delegate-first, validate-always, fallback-if-needed policy.
- Added `External Skill Acceptance Tests` to prevent blindly using found skills.
- Preserved internal fallback search when the installer is unavailable or candidates fail validation.
- Strengthened low-coupling rules: external skills cannot silently mutate core modules; outputs go to project workspace.
- Kept undergraduate thesis mode uncertainty-aware: no fake numeric workload scoring.
- Kept canonical formats as Markdown/YAML/CSV; Excel remains optional export.
