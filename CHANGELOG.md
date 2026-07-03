# Changelog

## 0.1.0-public-positioning - 2026-07-03

- Sharpened public positioning around evidence-first academic AI writing without hallucinated citations, fake evidence, or integrity drift.
- Added scenario examples for literature-review and undergraduate-thesis workflows.
- Clarified that final prose should come after verifiable matrices, claim ledgers, and integrity checks.
- Kept the undergraduate thesis path uncertainty-aware: missing school, advisor, rubric, and workload requirements remain unknown until confirmed.

## 8.0.0-final-candidate

- Rechecked the overall workflow as a final modular skill candidate.
- Added explicit compatibility with the user's existing skill-installer/self-updating skill workflow.
- Added `External Skill Gateway` with delegate-first, validate-always, fallback-if-needed policy.
- Added `External Skill Acceptance Tests` to prevent blindly using found skills.
- Preserved internal fallback search when the installer is unavailable or candidates fail validation.
- Strengthened low-coupling rules: external skills cannot silently mutate core modules; outputs go to project workspace.
- Kept undergraduate thesis mode uncertainty-aware: no fake numeric workload scoring.
- Kept canonical formats as Markdown/YAML/CSV; Excel remains optional export.
