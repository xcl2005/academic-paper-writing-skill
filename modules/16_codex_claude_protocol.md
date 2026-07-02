# 16 Codex / Claude Code Protocol

## Purpose

Make the skill easy for code agents to call.

## Loading Rules

- Start from `SKILL.md` and `skill_manifest.yaml`.
- Load only required modules.
- Prefer machine-readable templates and schemas.
- Write project outputs to a separate project workspace.
- Do not edit this skill's files unless the user asks for skill maintenance.

## File Handling

For each project, create:

```text
project_workspace/
  project_state.yaml
  matrices/
  evidence/
  experiments/
  figures/
  drafts/
  reports/
```

## Agent Output Discipline

- Produce small artifacts early.
- Keep assumptions explicit.
- Use CSV/YAML for structures that need future editing.
- Use Markdown for reports and narrative plans.
- Generate Excel/Word/PDF/slides only as export formats.

## Safety

Before running code or installing tools:

- inspect scripts;
- avoid unsafe commands;
- record dependencies;
- prefer virtual environments;
- document limitations.
