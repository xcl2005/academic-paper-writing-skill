# Examples

Use these examples to see the intended evidence-first workflow. The goal is not to generate polished prose first; it is to make claims, sources, experiments, and integrity risks inspectable before writing.

## Scenario walkthroughs

- [Output: literature matrix sample](outputs/rag-evaluation-literature-matrix.sample.csv): verified, recheck, and missing-source rows.
- [Output: claim ledger sample](outputs/rag-evaluation-claim-ledger.sample.csv): supported, blocked, and unknown claims.
- [Output: novelty check sample](outputs/rag-evaluation-novelty-check.sample.md): safer novelty wording and blocked claims.
- [Output: thesis evidence map sample](outputs/undergraduate-thesis-evidence-map.sample.csv): thesis sections mapped to evidence status.
- [Output: related work blocked sample](outputs/output-related-work-blocked.sample.md): shows how the skill stops before unsupported prose.
- [Sample source note](outputs/sample-source-note.md): explains what the demo data does and does not prove.
- [Fixture: unsupported strong claim](fixtures/claims/unsupported-strong-claim.csv): should be blocked before prose.
- [Fixture: supported claim](fixtures/claims/supported-claim.csv): should pass the claim-to-prose check.
- [Literature review matrix demo](literature-review-matrix-demo/README.md): a topic-to-matrix path before related-work prose.
- [Undergraduate thesis proposal demo](undergraduate-thesis-proposal-demo/README.md): a scope and evidence package without invented school requirements.
- [Rebuttal response matrix demo](rebuttal-response-matrix-demo/README.md): reviewer comments turned into auditable responses.
- [Literature review workflow](academic-literature-review-workflow.md): build a source-grounded literature matrix before related-work prose.
- [Thesis outline workflow](thesis-outline-workflow.md): turn a graduation project idea into a scope, evidence plan, and thesis outline without inventing school requirements.

## Start a research-paper workspace

```bash
python scripts/init_project.py --out paper_workspace --type research_paper
```

Or run a populated demo workspace:

```bash
python scripts/demo_academic_workflow.py --mode research_paper --out demo_workspace
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

Or run a populated thesis demo workspace:

```bash
python scripts/demo_academic_workflow.py --mode undergraduate_thesis --out demo_workspace
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
