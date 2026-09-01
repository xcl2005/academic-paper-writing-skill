# 06 Literature Engine

## Purpose

Search, verify, classify, and synthesize literature accurately.

Use `modules/20_scholarly_search_screening_and_references.md` for reproducible retrieval, screening, deduplication, and reference management. This module owns close reading and synthesis after the source set is defined.

## Review Type

Label the job before synthesis:

- paper reading or annotated note;
- rapid evidence scan;
- narrative review;
- scoping review;
- systematic review;
- meta-analysis or quantitative synthesis.

Do not borrow the authority of a systematic review when the search and screening protocol does not support that label.

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

For each deeply used paper, also keep `templates/paper_reading_note.md` with exact figure, table, section, or supplementary pointers for evidence-bearing claims.

## Synthesis Standard

- Organize by question, mechanism, method family, evidence pattern, or disagreement, not as a paper-by-paper parade.
- Distinguish study findings, author interpretations, reviewer-independent limitations, and agent inference.
- Compare populations, datasets, outcomes, baselines, estimands, evaluation protocols, and uncertainty before comparing headline results.
- Surface contradictory findings, negative evidence, publication bias, inaccessible full text, and evidence gaps.
- For systematic or scoping work, preserve screening counts, exclusion reasons, protocol deviations, quality or risk-of-bias assessment, and update date.
- For quantitative synthesis, route statistical modeling to `modules/19_study_design_statistics_and_data.md`; report heterogeneity, model choice, sensitivity, and study dependence.

## Accuracy Rules

- Do not rely only on titles/abstracts for technical claims.
- Inspect method, experiment, and limitation sections when possible.
- Separate paper claims from agent inference.
- If papers disagree, report disagreement.
- Do not say “no one has done this” unless novelty verification is broad enough.
- Do not treat citation count, journal prestige, or one survey as proof of methodological quality.
