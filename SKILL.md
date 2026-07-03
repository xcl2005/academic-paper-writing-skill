---
name: academic-paper-writing-skill
description: Assist with academic research papers, literature reviews, rebuttals, revisions, research writing, claim-evidence checks, citation workflows, and research integrity checks. Also supports thesis and graduation project evidence workflows as compatible scenarios. Use when an agent is asked to plan, write, revise, evaluate, or package academic papers, research writing, rebuttals, or evidence-grounded thesis/capstone work.
---
# Academic Paper Writing Skill

Research papers, literature reviews, rebuttals, and undergraduate thesis workflows.

## Purpose

Use this skill to assist future academic work, including:

- top-tier or ordinary research papers;
- workshop / B-class / C-class conference papers;
- journal submissions;
- undergraduate thesis and graduation project writing;
- proposal, midterm, final report, defense, rebuttal, and revision workflows.

This skill is for Codex, Claude Code, ChatGPT, and future stronger models. It is a **modular workflow system**, not a single long prompt.

---

## Non-Negotiable Invariants

These rules must never be removed or weakened, even during self-maintenance.

1. **No fabricated papers**: never cite or summarize a paper that has not been found and verified.
2. **No fabricated SOTA**: SOTA, benchmark status, model versions, leaderboards, venue policies, and tool capabilities must be rechecked when relevant.
3. **No fabricated results**: planned, expected, preliminary, and achieved results must be clearly separated.
4. **No invented local requirements**: do not invent school, college, advisor, template, rubric, defense, or workload requirements. Unknown means unknown.
5. **Primary-source first**: prefer official papers, official datasets, official code, official venue pages, official school templates, and advisor-provided documents.
6. **Claim-to-evidence mapping**: every strong claim must map to literature, experiment, implementation evidence, test result, proof, or official requirement.
7. **Integrity before persuasion**: reduce or qualify claims instead of overclaiming.
8. **Modular loading**: load only modules needed for the current task.
9. **External-skill low coupling**: external skills/tools may assist, but must not silently override this skill's invariants or mutate core files.
10. **Human review for high-stakes decisions**: final submission, authorship, ethics, school compliance, and thesis requirements require human confirmation.
11. **Self-maintenance is allowed**: wording, module layout, templates, and tools may be improved, but these invariants cannot be broken.

---

## First Decision: Select Project Type

Set `project_type` before doing substantial work.

### `research_paper`
Use when the user wants a publishable academic paper, especially involving venue fit, SOTA, novelty, experiments, reviewer simulation, or rebuttal.

### `undergraduate_thesis`
Use when the user wants an undergraduate thesis, graduation project, proposal, midterm report, final thesis, defense slides, or ordinary school-assessed project.

Important: undergraduate thesis “workload” is usually an implicit assessment by school/advisor/reviewers, not a universal numeric standard. Do not fake exact workload scores.

### `hybrid_capstone_research`
Use when the graduation project may also become a paper, portfolio project, or application material.

Default priority for hybrid projects:

1. satisfy graduation requirements and evidence expectations;
2. then upgrade novelty, experiments, and writing toward research-paper standards.

---

## Standard Call Protocol

1. Read `skill_manifest.yaml`.
2. Determine `project_type`, `stage`, `task`, known constraints, and missing information.
3. Load `modules/00_core_invariants.md`, `modules/01_agent_orchestrator.md`, and only required task modules.
4. For a new paper/thesis workspace, prefer running `python scripts/init_project.py --out <project_workspace> --type <research_paper|undergraduate_thesis|hybrid_capstone_research>` instead of hand-copying templates.
5. If external tools/skills are needed, load `modules/03_external_skill_gateway.md` before searching or installing anything.
6. Create/update a project state file from `templates/project_state.yaml`.
7. Produce intermediate matrices before final prose when relevant:
   - literature matrix;
   - novelty verification matrix;
   - experiment matrix;
   - claim ledger;
   - integrity checklist;
   - graduation evidence map when applicable.
8. Before final output, run integrity/reproducibility checks relevant to the task.

---

## Default Module Routing

Use the smallest route that fits the task. The full routes below are for substantial project work; lightweight requests should load only the named task modules plus `00_core_invariants.md` and `01_agent_orchestrator.md`.

### Lightweight Routes

- Literature review or related work matrix: add `06_literature_engine.md` and `11_integrity_reproducibility_guard.md`.
- Novelty or SOTA check: add `07_novelty_verification_and_scoring.md` and `11_integrity_reproducibility_guard.md`.
- Experiment planning: add `09_experiment_matrix_engine.md` and `11_integrity_reproducibility_guard.md`.
- Figure/table planning: add `10_figure_table_engine.md`.
- Rebuttal or simulated review: add `13_simulated_review_rebuttal.md` and `11_integrity_reproducibility_guard.md`.
- Undergraduate requirement discovery: add `04_requirement_discovery.md`, `14_undergraduate_thesis_engine.md`, and `11_integrity_reproducibility_guard.md`.

### Research Paper Route

Load:

- `00_core_invariants.md`
- `01_agent_orchestrator.md`
- `02_mode_router.md`
- `03_external_skill_gateway.md`
- `05_venue_intelligence.md`
- `06_literature_engine.md`
- `07_novelty_verification_and_scoring.md`
- `08_research_roi_scope.md`
- `09_experiment_matrix_engine.md`
- `10_figure_table_engine.md`
- `11_integrity_reproducibility_guard.md`
- `12_writing_style_adapter.md`
- `13_simulated_review_rebuttal.md`

### Undergraduate Thesis Route

Load:

- `00_core_invariants.md`
- `01_agent_orchestrator.md`
- `02_mode_router.md`
- `04_requirement_discovery.md`
- `14_undergraduate_thesis_engine.md`
- `11_integrity_reproducibility_guard.md`
- `12_writing_style_adapter.md`

### Hybrid Route

First load undergraduate route. Then selectively add:

- `06_literature_engine.md`
- `07_novelty_verification_and_scoring.md`
- `08_research_roi_scope.md`
- `09_experiment_matrix_engine.md`
- `10_figure_table_engine.md`

---

## Excel Policy

Excel is useful for humans, but it should not be the canonical source for this skill.

Use CSV/YAML/Markdown as the working source. Export Excel only when needed for advisor review, collaborator review, or submission packaging.

---

## Maintenance Rule

This skill is allowed to evolve. Future agents may delete, merge, rewrite, or replace modules if doing so improves reliability, reduces duplication, or adapts to new tools and models. However, they must preserve the non-negotiable invariants.
