# Rebuttal Response Matrix Demo

This demo shows how reviewer comments become a structured response matrix before final rebuttal prose.

## Input

```text
Use $academic-paper-writing-skill to build a rebuttal matrix from these reviewer comments. Do not overclaim new experiments.
```

## First outputs

| File | Purpose |
|---|---|
| `rebuttal_matrix.md` | Maps each reviewer concern to response strategy, evidence, revision, and tone |
| `claim_ledger.csv` | Checks whether each response claim is supported |
| `integrity_checklist.md` | Separates completed revisions, planned fixes, and limitations |

## Good stopping point

```text
Response ready for drafting: 5 comments have evidence-backed responses.
Needs human confirmation: one requested experiment is planned but not completed.
```

