# 07 Novelty Verification and Scoring

## Purpose

Find innovation points and check whether they are already covered by existing work.

## Novelty Verification First

Before scoring novelty, search for overlap:

- same task + same method;
- same task + similar method;
- same dataset + same evaluation;
- same claim but different terminology;
- recent arXiv/preprints;
- related work in adjacent fields;
- official benchmark submissions;
- GitHub implementations not yet published.

## Gap Types

A valid gap can be:

- dataset/domain/language/modality gap;
- evaluation/metric/robustness gap;
- method/generalization/efficiency/interpretablity gap;
- application/deployment gap;
- reproducibility gap;
- theory/explanation gap;
- undergraduate engineering gap: system completeness, testability, maintainability, usable demo.

## Novelty Scoring

Score ideas only as decision support, not truth.

Suggested dimensions, 1-5:

- originality;
- literature support;
- non-obviousness;
- experimental verifiability;
- feasibility;
- venue/school fit;
- risk of being trivial engineering combination;
- risk of being already done.

Output labels:

- `high-confidence gap`;
- `possible gap`;
- `weak gap`;
- `needs verification`;
- `likely duplicate`.

## Required Output

Use `templates/novelty_verification.csv` with:

- idea;
- closest_existing_work;
- overlap;
- difference;
- evidence_needed;
- novelty_score;
- feasibility_score;
- risk_level;
- decision.
