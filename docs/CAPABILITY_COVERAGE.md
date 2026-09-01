# Capability Coverage and Provider Design

Audit date: 2026-09-02

This document records how `academic-paper-writing-skill` covers the recommended research-skill categories without permanently binding the workflow to one implementation.

## Design Rule

Each capability has five parts:

1. a stable capability name;
2. a normalized input contract;
3. one or more optional specialist providers;
4. an internal fallback module;
5. output acceptance criteria.

When a provider is installed and fits the task, its complete `SKILL.md` and required workflow resources control detailed execution, layout, formatting, and QA. The registry summary is not a substitute for those instructions. When no provider is usable, the internal baseline preserves the capability and integrity boundary.

External providers are not vendored, installed, or relicensed by this repository.

## Benchmark Mapping

| Recommended category | Provider interface | Internal coverage | Standards retained at the interface |
|---|---|---|---|
| Topic selection | `scientific-brainstorming` | `modules/18_research_ideation_and_question_design.md` | Independent generation, explicit assumptions, adversarial review, falsifiable predictions, transparent evaluation, decision log |
| Academic search | `nature-academic-search`, `paper-lookup` | `modules/20_scholarly_search_screening_and_references.md` | Source routing, exact query/date/limit log, identifier verification, deduplication, partial-result disclosure, reference export |
| Literature review | `literature-review` | `modules/06_literature_engine.md` | Review-type labeling, screening and exclusions, study matrix, quality assessment, synthesis, disagreements and coverage limits |
| Research orchestration | `academic-research-suite` | `modules/01_agent_orchestrator.md`, `modules/02_mode_router.md` | Project state, stage gates, artifact ownership, source boundary, human decisions, no false completion |
| Statistics | `statistical-analysis`, `statistical-power` | `modules/19_study_design_statistics_and_data.md` | Estimand, sample-size rationale, confirmatory/exploratory split, assumptions, effect sizes, intervals, multiplicity, diagnostics, deviations |
| Scientific figures | `nature-figure`, `scientific-visualization` | `modules/10_figure_table_engine.md` | Claim-first figure brief, source-data trace, final-size rendering, accessibility, editable source, export metadata and visual QA |
| Manuscript drafting | `nature-writing`, `scientific-writing` | `modules/12_writing_style_adapter.md` | Evidence packet, reporting guidance, terminology ledger, fact invariants, author checks and submission components |
| Polishing | `nature-polishing` | `modules/12_writing_style_adapter.md` | Drafting/polishing separation, numbers/citations/equations/claim-strength preservation, terminology and material-change checks |
| Pre-submission review | `nature-reviewer`, `peer-review` | `modules/13_simulated_review_rebuttal.md` | Reviewer/author role separation, stable concern IDs, evidence pointers, blocking logic, methods/statistics/reproducibility/ethics audit |
| Reviewer response | `nature-response` | `modules/13_simulated_review_rebuttal.md` | Comment taxonomy, action mapping, exact revisions, feasible promises, unresolved actions, package consistency |
| Data and code | `nature-data` | `modules/21_research_delivery_and_presentation.md`, `modules/11_integrity_reproducibility_guard.md` | Asset inventory, repository/access route, verified identifiers, licences/restrictions, FAIR metadata and manuscript consistency |
| Paper to presentation | `nature-paper2ppt` | `modules/21_research_delivery_and_presentation.md` | Paper-type routing, evidence-led narrative, figure handling, terminology, real PPTX when requested, speaker notes and rendered QA |

## Additional Coverage

The registry also exposes study design through `experimental-design`, general paper lookup through `paper-lookup`, statistical power through `statistical-power`, scientific writing through `scientific-writing`, and general peer review through `peer-review`. These providers improve target-specific selection without changing the stable capability names.

## Selection Examples

| Request | Selection behavior |
|---|---|
| “Brainstorm three publishable directions” | Resolve `research_ideation`; use `scientific-brainstorming` if installed, otherwise module 18 |
| “Run a reproducible multi-database search and export BibTeX” | Resolve `scholarly_search`; prefer `nature-academic-search` or `paper-lookup` according to available tools |
| “Make a Nature-ready multi-panel figure in R” | Resolve `scientific_visualization` with tags `nature` and `r`; use the selected provider's full backend/export rules |
| “Polish this section without changing numbers or claims” | Resolve `language_polishing`; use `nature-polishing` if its companion resources are installed |
| “Turn this paper into a Chinese journal-club deck” | Resolve `paper_to_presentation`; use `nature-paper2ppt` when complete, then run rendered artifact QA |

## Provider Acceptance

A provider is not accepted merely because it exists. The handoff must preserve:

- source boundary and protected facts;
- user choice, permissions, language, target, and output format;
- required companion skills, references, scripts, and runtime dependencies;
- inspectable outputs and unresolved fields;
- the capability-specific acceptance contract;
- this project's no-fabrication, provenance, privacy, and human-accountability rules.

Provider installation quality and provider task output are assessed separately. A provider can be acceptable to keep installed but still fail a particular output; that task then falls back or routes elsewhere.

## Backward Compatibility

The interface layer does not remove the original project types, modes, modules, templates, scripts, demos, or generated reports. `scripts/validate_skill.py` enforces the established project types, seven original modes, and protected files as a compatibility contract.

## Public Design References

- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills), especially its public scientific brainstorming, literature review, statistics, visualization, writing, experimental design, and peer-review skill structures.
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills), especially its public academic search, writing, polishing, reviewer, response, figure, data, reader, and paper-to-PPT routers.
- [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex), used as a public benchmark for optional full-project orchestration concepts. No CC BY-NC implementation content is vendored here.

These sources are benchmarks and optional runtime providers, not bundled dependencies. Their own licences and attribution requirements continue to apply when users install or use them.
