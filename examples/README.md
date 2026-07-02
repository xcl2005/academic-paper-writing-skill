# Examples

Use these examples to see the intended evidence-first workflow.

## Start a research-paper workspace

```bash
python scripts/init_project.py --out paper_workspace --type research_paper
```

Then fill:

- `literature_matrix.csv`
- `novelty_verification.csv`
- `experiment_matrix.csv`
- `claim_ledger.csv`
- `integrity_checklist.md`

## Start an undergraduate thesis workspace

```bash
python scripts/init_project.py --out thesis_workspace --type undergraduate_thesis
```

Then fill:

- `requirement_discovery_log.md`
- `assumption_register.md`
- `scope_ladder.md`
- `graduation_evidence_map.csv`

## Example Codex prompts

```text
$academic-paper-writing-skill build a literature matrix for my topic, but do not invent papers.
```

```text
$academic-paper-writing-skill check whether my claimed novelty is supported by verified sources.
```

```text
$academic-paper-writing-skill create a rebuttal matrix from these reviewer comments.
```

## Suggested GitHub topics

Use these repository topics to make the project easier to discover:

`codex`, `codex-skills`, `agent-skills`, `academic-writing`, `research-paper`, `literature-review`, `thesis`, `research-integrity`, `claim-evidence`, `ai-agents`
