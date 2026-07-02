# Changelog

## 8.0.0-final-candidate

- Rechecked the overall workflow as a final modular skill candidate.
- Added explicit compatibility with the user's existing skill-installer/self-updating skill workflow.
- Added `External Skill Gateway` with delegate-first, validate-always, fallback-if-needed policy.
- Added `External Skill Acceptance Tests` to prevent blindly using found skills.
- Preserved internal fallback search when the installer is unavailable or candidates fail validation.
- Strengthened low-coupling rules: external skills cannot silently mutate core modules; outputs go to project workspace.
- Kept undergraduate thesis mode uncertainty-aware: no fake numeric workload scoring.
- Kept canonical formats as Markdown/YAML/CSV; Excel remains optional export.
