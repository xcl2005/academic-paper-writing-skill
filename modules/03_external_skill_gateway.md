# 03 External Skill Gateway

## Purpose

Make this skill compatible with the user's existing skill-installer / self-updating skill workflow while preserving low coupling.

This skill is **not** a package manager. It should delegate search/install/update to the user's external installer skill when available, then validate candidates before use.

## Core Policy

Use this order:

1. **Delegate first**: if the user's install/update skill is available, call it to search/update/install candidate skills/tools.
2. **Validate always**: every candidate returned by the installer must pass this skill's acceptance tests before use.
3. **Fallback if needed**: if no installer exists, or the installer fails, use this skill's internal search/fallback workflow.
4. **Record decisions**: selected, rejected, and deferred candidates must be recorded.
5. **Keep low coupling**: external skills produce artifacts in the project workspace; they do not silently mutate this skill's core files.

## When to Invoke External Installer

Invoke before tasks involving:

- large literature search;
- paper crawling / arXiv / Semantic Scholar / ACL Anthology / OpenReview processing;
- PDF parsing;
- citation checking;
- LaTeX, Word, PDF, or official template formatting;
- publication-quality figure generation;
- statistical testing;
- experiment tracking;
- benchmark reproduction;
- slides/poster generation;
- school thesis template extraction;
- repository/codebase analysis for graduation project evidence.

## Adapter Contract

The installer or external skill should return or create a report with:

- tool/skill name;
- source URL or local path;
- version, commit, or download date;
- purpose;
- install path;
- required dependencies;
- license;
- security notes;
- reason selected;
- known limitations.

If the installer cannot provide this, the agent must create `templates/skill_selection_report.md` manually.

## Search Behavior

### Preferred Behavior

Ask the installer to search with multiple task-specific queries, for example:

- `academic paper writing skill`
- `literature review automation`
- `citation audit tool`
- `latex paper skill`
- `venue template skill`
- `paper review rebuttal skill`
- `publication quality figure tool`
- `experiment tracking reproducibility`
- `undergraduate thesis template tool`

### Fallback Behavior

If no installer is available, this skill may search directly using web/GitHub/gh CLI, but it must:

- not rely on a single keyword;
- not clone everything blindly;
- inspect README/SKILL/examples/license before use;
- score and reject candidates;
- generate a dynamic download script containing only selected candidates.

## Compatibility Gate

A candidate external skill/tool can be used only if it passes:

1. **Task fit**: it solves the current task, not just a loosely related problem.
2. **Integrity fit**: it does not encourage fabricated citations, invented results, or overclaiming.
3. **Source transparency**: source, license, docs, and examples are inspectable.
4. **Maintenance fit**: recent enough or stable enough for the task.
5. **Environment fit**: installable in the current OS/runtime without excessive risk.
6. **Output fit**: produces Markdown/YAML/CSV/artifacts that can be inspected.
7. **Coupling fit**: does not require modifying this skill's core modules.
8. **Override fit**: accepts that this skill's invariants override its own weaker rules.

If a candidate fails, record it as rejected and explain why.

## Low-Coupling Workspace Layout

External resources should use:

```text
paper_skills_workspace/
  raw_repos/
  selected_skills/
  tools/
  templates/
  reports/
  DOWNLOAD_LOG.md
  SKILLS_INDEX.md
  SKILL_SELECTION_REPORT.md
```

Project-specific outputs should use:

```text
project_workspace/
  project_state.yaml
  matrices/
  figures/
  experiments/
  drafts/
  evidence/
  reports/
  external_skill_outputs/
```

## Conflict Resolution

When this skill and an external skill disagree:

1. official source overrides both;
2. this skill's invariants override external skill instructions;
3. user-provided template/requirement overrides generic style advice;
4. newer verified venue/school rules override stale internal text;
5. unverified external claims are treated as suggestions, not facts.

## Minimal Final Report

After using external skills, output or save:

- what installer/search was used;
- what was selected;
- what was rejected;
- what was installed or reused;
- what limitations remain;
- which internal modules are still responsible for final judgment.
