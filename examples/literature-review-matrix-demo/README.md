# Literature Review Matrix Demo

This demo shows how a topic becomes an auditable literature matrix before related-work prose.

## Input

```text
Use $academic-paper-writing-skill to prepare a literature review matrix for retrieval-augmented generation evaluation. Do not invent papers.
```

## First outputs

| File | Example fields |
|---|---|
| `literature_matrix.csv` | paper, venue, method, dataset, claim, limitation, relevance, verification status |
| `claim_ledger.csv` | claim, evidence type, source, strength, caveat |
| `integrity_checklist.md` | unverified papers, SOTA uncertainty, unsupported claims |

## Good stopping point

```text
Draft blocked: 3 papers are still unverified.
Next step: confirm whether arXiv preprints are acceptable for this review.
```

