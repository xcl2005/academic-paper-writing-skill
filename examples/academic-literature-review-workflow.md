# Literature Review Workflow

This example shows the intended workflow for a paper or thesis literature review. The skill should create evidence structures before writing final prose.

## User request

```text
Use $academic-paper-writing-skill to build a literature matrix for my topic on retrieval-augmented generation evaluation. Do not invent papers or citations.
```

## Expected workflow

1. Set `project_type` to `research_paper` unless the user says this is a thesis or capstone.
2. Load the literature and integrity modules.
3. Ask for the user's seed papers, BibTeX, PDF folder, or search scope if sources are missing.
4. Verify each paper before summarizing it.
5. Fill a literature matrix before drafting related work.
6. Mark unknowns explicitly instead of filling gaps with guesses.

## Working artifacts

| Artifact | Purpose |
|---|---|
| `templates/literature_matrix.csv` | Verified paper, method, dataset, claim, limitation, and relevance |
| `templates/claim_ledger.csv` | Strong claims mapped to source, experiment, or implementation evidence |
| `templates/integrity_checklist.md` | Checks for fabricated citations, exaggerated SOTA, and unsupported claims |

## Good output shape

```text
I found 12 verified sources and left 3 unverified entries out of the prose.
Next artifact: literature_matrix.csv with method, dataset, claim, limitation, and relevance columns filled.
Draft status: related-work prose is blocked until the user confirms whether preprints may be used.
```

