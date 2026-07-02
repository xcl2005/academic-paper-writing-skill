# 06 Literature Engine

## Purpose

Search, verify, classify, and synthesize literature accurately.

## Literature Depth

Use task-appropriate depth:

- quick scan: 5-10 high-relevance papers;
- normal planning: 15-30 papers;
- serious novelty search: 30-80 papers;
- survey-level: 80+ papers when the field requires it.

The number is not the goal. Coverage and correctness are the goal.

## Required Categories

When relevant, include:

- foundational/classic work;
- recent SOTA/high-impact work;
- closest method/task/dataset papers;
- benchmark/dataset papers;
- negative/limitation/reproducibility papers;
- surveys for map-building only;
- official leaderboards and code repositories.

## Literature Matrix Columns

Use `templates/literature_matrix.csv` and `schemas/literature_matrix.schema.yaml`.

Minimum columns:

- paper_id;
- title;
- year;
- venue;
- source_url_or_doi;
- task_problem;
- method_family;
- dataset_benchmark;
- metrics;
- main_result;
- contribution;
- limitations;
- relation_to_user_idea;
- possible_gap;
- reliability_notes;
- verification_status.

## Accuracy Rules

- Do not rely only on titles/abstracts for technical claims.
- Inspect method, experiment, and limitation sections when possible.
- Separate paper claims from agent inference.
- If papers disagree, report disagreement.
- Do not say “no one has done this” unless novelty verification is broad enough.
