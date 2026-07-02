<div align="center">

# Academic Paper Writing Skill

**Evidence-first workflows for papers, theses, reviews, rebuttals, and defenses.**

<a href="https://github.com/xcl2005/academic-paper-writing-skill/stargazers"><img src="https://img.shields.io/github/stars/xcl2005/academic-paper-writing-skill?style=flat-square" alt="stars"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/network/members"><img src="https://img.shields.io/github/forks/xcl2005/academic-paper-writing-skill?style=flat-square" alt="forks"></a>
<a href="https://github.com/xcl2005/academic-paper-writing-skill/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="license"></a>
<img src="https://img.shields.io/badge/Codex-Agent%20Skill-111827?style=flat-square" alt="Codex Agent Skill">
<img src="https://img.shields.io/badge/Policy-No%20Fake%20Papers-0F766E?style=flat-square" alt="No fake papers">

English · [简体中文](README_ZH.md)

[Install](#install) · [Why](#why) · [Control Flow](#control-flow) · [Workflows](#workflows) · [Artifacts](#artifacts) · [Examples](examples/)

</div>

## Why

Academic writing is not just prose. A useful agent must track sources, claims, experiments, assumptions, requirements, and integrity risks before drafting.

**Academic Paper Writing Skill** gives Codex a modular route for academic work without fabricated papers, invented SOTA, fake results, or unsupported claims.

## Highlights

| | Capability |
|---|---|
| 📚 | Literature matrices with verified sources |
| 🧠 | Novelty and SOTA checks before strong claims |
| 🧪 | Experiment matrices for metrics, baselines, and results |
| 🔗 | Claim ledgers that map every strong claim to evidence |
| 🎓 | Undergraduate thesis and graduation project requirement discovery |
| 🛡️ | Integrity checks before final prose, rebuttal, or defense packaging |

## Control flow

This skill is modular because academic tasks vary widely. A literature review, a rebuttal, a thesis proposal, and a full paper package should not load the same instructions.

| Step | Decision | What happens |
|---:|---|---|
| 1 | Select project type | Choose `research_paper`, `undergraduate_thesis`, or `hybrid_capstone_research`. |
| 2 | Identify stage | Determine whether the user is doing idea discovery, literature review, novelty check, experiment planning, writing, revision, rebuttal, or defense. |
| 3 | Load minimal modules | Read only the modules needed for the current stage plus core invariants. |
| 4 | Create structured artifacts | Build matrices and ledgers before final prose when evidence matters. |
| 5 | Verify claims | Map strong claims to papers, experiments, implementation evidence, tests, proofs, or official requirements. |
| 6 | Run integrity checks | Separate planned, preliminary, and achieved results; avoid invented local requirements. |
| 7 | Draft or revise | Write only after the evidence trail is visible enough to inspect. |
| 8 | Package with human review | Final submission, authorship, ethics, school compliance, and defense decisions require human confirmation. |

### Module routing

| Task | Modules normally loaded |
|---|---|
| Literature review | `00_core_invariants`, `01_agent_orchestrator`, `06_literature_engine`, `11_integrity_reproducibility_guard` |
| Novelty or SOTA check | `07_novelty_verification_and_scoring`, `11_integrity_reproducibility_guard` |
| Experiment planning | `09_experiment_matrix_engine`, `11_integrity_reproducibility_guard` |
| Figure/table planning | `10_figure_table_engine` |
| Rebuttal or simulated review | `13_simulated_review_rebuttal`, `11_integrity_reproducibility_guard` |
| Undergraduate thesis requirements | `04_requirement_discovery`, `14_undergraduate_thesis_engine`, `11_integrity_reproducibility_guard` |

### Evidence lifecycle

| Artifact | Purpose |
|---|---|
| Literature matrix | Track verified sources, claims, methods, datasets, and relevance |
| Novelty matrix | Compare the user's idea against verified prior work |
| Experiment matrix | Record metrics, baselines, datasets, ablations, and result status |
| Claim ledger | Make every strong claim auditable |
| Integrity checklist | Catch fabricated, exaggerated, or unsupported statements before final prose |

## Install

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/xcl2005/academic-paper-writing-skill.git ~/.agents/skills/academic-paper-writing-skill
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills"
git clone https://github.com/xcl2005/academic-paper-writing-skill.git "$HOME\.agents\skills\academic-paper-writing-skill"
```

Restart Codex if the skill list does not refresh automatically.

## Workflows

| Mode | Use it for | Outputs |
|---|---|---|
| `research_paper` | papers, related work, experiments, rebuttal, revision | literature matrix, novelty check, experiment matrix, claim ledger |
| `undergraduate_thesis` | proposal, midterm, thesis, defense, graduation project | requirement log, scope ladder, graduation evidence map |
| `hybrid_capstone_research` | graduation-first projects that may become papers | thesis MVP, evidence package, research upgrade plan |

## Quick start

```bash
# Create a research-paper workspace
python scripts/init_project.py --out paper_workspace --type research_paper

# Create an undergraduate-thesis workspace
python scripts/init_project.py --out thesis_workspace --type undergraduate_thesis

# Validate this skill
python scripts/validate_skill.py
```

## Artifacts

- `templates/literature_matrix.csv`
- `templates/novelty_verification.csv`
- `templates/experiment_matrix.csv`
- `templates/claim_ledger.csv`
- `templates/integrity_checklist.md`
- `templates/rebuttal_matrix.md`
- `templates/graduation_evidence_map.csv`
- `templates/project_state.yaml`

Markdown, YAML, and CSV are the canonical working formats. Word, PDF, Excel, and slides are exports.

## Invariants

This skill is strict by design:

- no fabricated papers;
- no fabricated SOTA;
- no fabricated results;
- no invented local school, advisor, rubric, or defense requirements;
- primary-source first;
- claim-to-evidence mapping;
- human review for final submission, authorship, ethics, and compliance.

## Files worth reading

| File | Purpose |
|---|---|
| `SKILL.md` | Entry point and non-negotiable invariants |
| `skill_manifest.yaml` | Project types, stages, modes, and module routing |
| `modules/00_core_invariants.md` | Integrity baseline |
| `modules/06_literature_engine.md` | Literature review workflow |
| `modules/07_novelty_verification_and_scoring.md` | Novelty and SOTA checks |
| `modules/14_undergraduate_thesis_engine.md` | Thesis and graduation project route |

## Project quality checks

This repository includes a README quality gate:

```bash
python scripts/validate_readme_quality.py
```

The check blocks oversized README images, Mermaid flowcharts, stale hero assets, and missing install/integrity sections.

## Repository layout

```text
.
|-- SKILL.md
|-- skill_manifest.yaml
|-- modules/
|-- templates/
|-- schemas/
|-- scripts/
|-- examples/
`-- README.md
```

## Search keywords

Academic writing AI, research paper workflow, literature review matrix, thesis writing assistant, graduation project, rebuttal assistant, claim evidence mapping, research integrity, Codex skills, Agent Skills.

## Version

`8.0.0-final-candidate`

## License

MIT
