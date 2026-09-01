<div align="center">

# Academic Paper Writing Skill

**An evidence-first, capability-routed research workflow from ideation and search to statistics, writing, review, submission, and presentation.**

<a href="https://github.com/xcl2005/academic-paper-writing-skill/stargazers"><img src="https://img.shields.io/github/stars/xcl2005/academic-paper-writing-skill?style=flat-square" alt="GitHub stars"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/network/members"><img src="https://img.shields.io/github/forks/xcl2005/academic-paper-writing-skill?style=flat-square" alt="GitHub forks"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/xcl2005/academic-paper-writing-skill/ci.yml?branch=main&style=flat-square" alt="CI status"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/releases"><img src="https://img.shields.io/github/v/release/xcl2005/academic-paper-writing-skill?style=flat-square" alt="Latest release"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT license"></a>
<img src="https://img.shields.io/badge/Agent%20Skills-Codex%20%7C%20Claude-111827?style=flat-square" alt="Codex and Claude Code">
<img src="https://img.shields.io/badge/workflow-evidence--first-0F766E?style=flat-square" alt="Evidence first">
<img src="https://img.shields.io/badge/providers-pluggable-7C3AED?style=flat-square" alt="Pluggable providers">

[简体中文](README.md) · English

[Quick Start](#-quick-start) · [Capability Interfaces](#-capability-interfaces) · [Working Standards](#-working-standards) · [Module Routing](#-module-routing) · [Quality Checks](#-quality-checks)

</div>

## 🔥 What It Is

This is neither one long “write my paper” prompt nor a fixed sequence of external skills.

It has three layers:

| Layer | Role |
|---|---|
| Internal baseline | Preserves and strengthens the established literature matrix, novelty/SOTA, ROI, experiment matrix, claim ledger, integrity, thesis, review, and rebuttal workflows |
| Capability interfaces | Give ideation, search, statistics, figures, writing, polishing, review, data availability, and paper-to-PPT stable input/output contracts |
| Pluggable providers | Load a specialist skill's complete detail when it is installed and suitable; fall back internally when it is unavailable, incomplete, or fails acceptance |

The project can use specialist depth without permanently binding every research task to one repository, skill name, toolchain, or journal style.

## ✨ v2.0

- Adds 13 research capability interfaces and 18 optional provider mappings.
- Adds internal modules for research ideation, reproducible scholarly search, study design/statistics/data, and submission/presentation delivery.
- Adds `capability_registry.yaml` to resolve providers by task, target, language, format, and installed state.
- Adds `resolve_capability.py` to show whether a task uses a specialist provider or internal fallback.
- Adds stage gates that check whether artifacts are populated and ready for handoff.
- Preserves all three original project types, seven original modes, core modules, demos, and pre-prose checks.

## 🧩 Capability Interfaces

Providers are optional and are never installed silently. When one is selected, the agent must read its complete `SKILL.md` and required workflow resources, then apply its detailed domain, layout, export, and QA standards.

| Capability | Preferred provider | Internal fallback | Key acceptance |
|---|---|---|---|
| 🧭 Research orchestration | `academic-research-suite` | agent orchestrator + mode router | Stages, evidence boundaries, artifacts, and human gates remain traceable |
| 💡 Ideation and question design | `scientific-brainstorming` | research ideation module | Independent generation, assumptions, adversarial review, and decision log |
| 🔎 Scholarly search and references | `nature-academic-search`, `paper-lookup` | scholarly search module | Queries, sources, dates, failures, deduplication, and coverage are reproducible |
| 📚 Literature review and synthesis | `literature-review` | literature engine | Screening, appraisal, study matrix, disagreements, and limitations are traceable |
| 🧪 Study design and statistics | `experimental-design`, `statistical-analysis`, `statistical-power` | study design/statistics module | Estimand, effects, intervals, assumptions, multiplicity, and diagnostics are explicit |
| 📊 Scientific figures and tables | `nature-figure`, `scientific-visualization` | figure/table engine | Final-size QA, accessibility, source trace, editable source, and export checks |
| ✍️ Manuscript drafting | `nature-writing`, `scientific-writing` | writing adapter | Numbers, citations, terminology, claim strength, and reporting guidance agree |
| 📝 Polishing and translation | `nature-polishing` | writing adapter | Facts, equations, citations, result direction, and technical terms are preserved |
| 🧐 Simulated peer review | `nature-reviewer`, `peer-review` | review/rebuttal engine | Concern IDs, evidence pointers, severity, blocking status, and revision paths |
| 💬 Reviewer response | `nature-response` | review/rebuttal engine | Every comment maps to evidence, an exact revision, or an explicit unresolved action |
| 🗃️ Data and code availability | `nature-data` | delivery + integrity modules | Repository, licence, version, access route, and FAIR fields are not invented |
| 🎤 Paper to presentation | `nature-paper2ppt` | delivery/presentation module | Real PPTX, argument spine, figure handling, speaker notes, and rendered QA |

See [`capability_registry.yaml`](capability_registry.yaml) for the executable interface definitions and [`docs/CAPABILITY_COVERAGE.md`](docs/CAPABILITY_COVERAGE.md) for the design audit.

## 🧱 Working Standards

Feature names are not enough. v2.0 also adopts the execution standards that make mature research skills useful:

| Stage | Minimum standard |
|---|---|
| Ideation | Generate independently before convergence; each idea has a falsifiable prediction, minimum study, nearest work, risks, and decision rationale |
| Search | Preserve databases, exact queries, field/date limits, run dates, result counts, failures, deduplication, and exclusion reasons |
| Review | Label rapid, narrative, scoping, or systematic work accurately; incomplete retrieval cannot borrow systematic-review authority |
| Study design | Define observation, assignment, and analysis units, the estimand, sampling, controls, confounding, missingness, and bias |
| Statistics | Separate confirmatory and exploratory work; report effect size, uncertainty, diagnostics, multiplicity, and deviations |
| Figures | Define claim, data, statistical annotation, physical size, and exports before styling; render and inspect the final output |
| Writing | Keep drafting separate from polishing; numbers, citations, equations, terminology, and claim strength are protected facts |
| Review/response | Keep reviewer assessment separate from author response; every concern has a stable ID and source/evidence pointer |
| Submission | Reconcile manuscript, figures, supplement, references, declarations, data/code, and portal or rendered previews |
| Presentation | Use the scientific argument as the spine; figures are evidence, and speaker notes plus package QA are part of delivery |

## 📦 Quick Start

Codex / Claude Code share the same `SKILL.md`, capability registry, and internal modules; their install paths and explicit invocation syntax differ.

### Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.agents/skills/academic-paper-writing-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
git clone https://github.com/xcl2005/academic-paper-writing-skill.git "$HOME\.agents\skills\academic-paper-writing-skill"
```

Example:

```text
Use $academic-paper-writing-skill to take this project from topic selection to a submission-ready paper.
Start with candidate directions and a search protocol. Do not invent sources, and use the best installed specialist for statistics, figures, and final formatting.
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.claude/skills/academic-paper-writing-skill
```

Direct invocation:

```text
/academic-paper-writing-skill audit this manuscript and create an evidence-backed revision record for every major concern
```

### Inspect Providers

```bash
python scripts/resolve_capability.py --list
python scripts/resolve_capability.py research_ideation --json
python scripts/resolve_capability.py scientific_visualization --tag nature --json
```

`use_installed_provider` returns the selected `SKILL.md`; `use_internal_fallback` keeps the task inside this repository's corresponding module.

## 🧭 Workflows

There is no mandatory long sequence. Each request composes the smallest useful capability set:

| Step | Decision and behavior |
|---:|---|
| 1 | Set project type, stage, target, source boundary, and missing inputs |
| 2 | Detect one or more capabilities from the registry |
| 3 | Preserve a user-selected provider; otherwise resolve by target tags, installed state, and priority |
| 4 | Read the internal baseline; if a provider is selected, also read its complete skill and required resources |
| 5 | Pass inputs, protected facts, permissions, and outputs through `capability_handoff.yaml` |
| 6 | Produce matrices, ledgers, plans, code, or the requested real artifact |
| 7 | Run capability acceptance, stage gate, pre-prose gate, or artifact QA |
| 8 | Continue only after acceptance; otherwise preserve blockers, fall back, or request necessary evidence |

### Module Routing

| Task | Primary internal modules |
|---|---|
| Project coordination | `01_agent_orchestrator`, `02_mode_router`, `22_capability_provider_router` |
| Ideation | `18_research_ideation_and_question_design`, `07_novelty_verification_and_scoring`, `08_research_roi_scope` |
| Search and synthesis | `20_scholarly_search_screening_and_references`, `06_literature_engine` |
| Study design and analysis | `19_study_design_statistics_and_data`, `09_experiment_matrix_engine` |
| Figures and tables | `10_figure_table_engine` |
| Writing and polishing | `12_writing_style_adapter`, `11_integrity_reproducibility_guard` |
| Review and response | `13_simulated_review_rebuttal`, `11_integrity_reproducibility_guard` |
| Submission and presentation | `21_research_delivery_and_presentation` |
| Undergraduate thesis | `04_requirement_discovery`, `14_undergraduate_thesis_engine` |
| External skill governance | `03_external_skill_gateway`, `17_external_skill_acceptance_tests` |

## 🗂️ Artifacts

| File | Purpose |
|---|---|
| `research_idea_portfolio.csv` | Candidate topics, evidence, predictions, minimum studies, risks, and decisions |
| `search_protocol.md` / `screening_log.csv` | Reproducible retrieval, screening, deduplication, and exclusions |
| `paper_reading_note.md` / `literature_matrix.csv` | Close reading, source boundaries, and cross-study synthesis |
| `novelty_verification.csv` / `roi_matrix.csv` | Prior-work comparison, novelty risk, and scope/ROI decisions |
| `statistical_analysis_plan.md` | Estimand, sample size, model, assumptions, intervals, multiplicity, and sensitivity analyses |
| `data_provenance.csv` / `experiment_matrix.csv` | Data lineage, permissions, transformations, experiment status, and reproducibility |
| `figure_brief.md` / `terminology_ledger.csv` | Scientific figure contract and terminology consistency |
| `claim_ledger.csv` / `integrity_checklist.md` | Claim evidence and the pre-prose integrity boundary |
| `simulated_review.md` / `rebuttal_matrix.md` | Traceable assessment and point-by-point response |
| `submission_package_checklist.md` / `presentation_brief.md` | Submission package, journal club, group meeting, or defense delivery |

## ✅ Stage Gates

```bash
python scripts/init_project.py --out paper_workspace --type research_paper
python scripts/check_stage_gate.py paper_workspace --gate ideation
python scripts/check_stage_gate.py paper_workspace --gate literature
python scripts/check_stage_gate.py paper_workspace --gate analysis
python scripts/check_stage_gate.py paper_workspace --gate drafting
python scripts/check_stage_gate.py paper_workspace --gate submission
python scripts/check_stage_gate.py paper_workspace --gate presentation
```

A failed gate lists missing files, empty records, or artifacts still marked `draft`. Failure is a work queue, not permission to fabricate data or sources.

## 🔁 Backward Compatibility

| Preserved capability | Status |
|---|---|
| `research_paper`, `undergraduate_thesis`, `hybrid_capstone_research` | Preserved |
| Literature Matrix, Novelty Verification, Experiment Matrix, Figure Design | Preserved and strengthened |
| Claim Ledger, Integrity Audit, Pre-Prose Gate | Preserved |
| Simulated Review / Rebuttal | Preserved with stronger role separation and evidence pointers |
| Requirement Discovery, Scope Ladder, Graduation Evidence Map | Preserved |
| External Skill Gateway / Acceptance Tests | Preserved and extended into provider interfaces |
| Existing demos, fixtures, generated reports, and CI drift checks | Preserved |

`scripts/validate_skill.py` treats the original project types, modes, modules, and scripts as a backward-compatibility contract.

## 🛡️ Integrity Rules

### Integrity-first by default

- Do not fabricate papers, authors, identifiers, venues, SOTA, leaderboards, data, results, or local requirements.
- Separate verified fact, paper claim, agent inference, assumption, and user-provided information.
- Map every strong claim to a source, data, analysis, experiment, implementation, test, proof, or official requirement.
- Keep planned, exploratory, preliminary, achieved, and externally reported results distinct.
- Do not call a rapid scan systematic, or turn significance into practical importance or causality.
- Do not send unpublished manuscripts, peer-review materials, personal data, or restricted data to an external provider without authorization.
- Final submission, authorship, ethics, consent, restricted-data, and school-compliance decisions remain human decisions.

When evidence is `needs_recheck`, `missing_source`, `unknown`, `unsupported`, or `blocked`, final prose must be qualified, left as an explicit placeholder, or blocked.

## 🛠️ Quality Checks

```bash
python scripts/validate_skill.py
python scripts/validate_capability_registry.py
python scripts/validate_readme_quality.py
python scripts/validate_evidence_status.py templates examples/outputs examples/fixtures examples/generated-demo-workspace
python scripts/pre_prose_check.py examples/generated-demo-workspace --expect-block
```

CI also checks initialized workspaces, provider fallback, legacy demos, unsupported Chinese claims, generated-report drift, and stage gates.

## 📁 Repository Layout

```text
.
|-- SKILL.md
|-- skill_manifest.yaml
|-- capability_registry.yaml
|-- agents/
|-- modules/
|-- templates/
|-- schemas/
|-- scripts/
|-- examples/
|-- docs/
|-- README.md
`-- README_EN.md
```

## 🔎 Search Keywords

Academic writing AI, research workflow, scientific brainstorming, academic search, literature review, systematic review, statistical analysis, scientific visualization, Nature writing, paper polishing, peer review, reviewer response, data availability, paper to PPT, thesis writing assistant, claim evidence mapping, research integrity, Codex skills, Claude Code skills, Agent Skills.

## 📄 License

MIT. External providers are not installed or redistributed by this repository; their code, content, and licences remain with their respective projects. This repository maintains interfaces, routing, internal fallbacks, and acceptance checks.
