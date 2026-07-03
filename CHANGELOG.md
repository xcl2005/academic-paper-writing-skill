# Changelog

## 0.1.0 - 2026-07-03

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
