# 09 Experiment Matrix Engine

## Purpose

Design experiments that answer specific research questions and support paper/thesis claims.

## Experiment Matrix Principle

Every experiment must map to:

- research question;
- hypothesis;
- dataset;
- baseline;
- metric;
- controlled variable;
- expected evidence;
- failure interpretation.

Before filling the matrix, define the unit of analysis, estimand or evaluation target, data split or sampling plan, and confirmatory versus exploratory status in `templates/statistical_analysis_plan.md` when applicable.

## Required Experiment Types

For research papers, consider:

- main comparison;
- ablation;
- sensitivity/parameter analysis;
- robustness/OOD/generalization;
- efficiency/cost/latency;
- error analysis;
- case study;
- statistical/repeated-run checks;
- negative results when informative.

For undergraduate thesis, consider:

- functional testing;
- module testing;
- integration testing;
- performance test if relevant;
- user/demo scenario;
- comparison with a simple baseline if feasible;
- screenshots/logs/video evidence.

## Fairness Rules

- Match train/test data and metrics across baselines.
- Include simple baselines when meaningful.
- Include strong recent baselines for research-paper mode.
- Report variance or confidence intervals when appropriate.
- Avoid cherry-picking and excessive decimal precision.

## Design and Analysis Standard

- Match randomization, blocking, controls, blinding, repeated measures, clustering, and hierarchy to the scientific design.
- Justify sample size, repetitions, or seeds with power, precision, minimum detectable effect, stability, or transparent feasibility limits.
- Fit preprocessing and model selection only on permitted training or development data; audit leakage across samples, subjects, time, sites, and labels.
- Define primary outcomes and baselines before running confirmatory comparisons.
- Record all exclusions, failed runs, stopping rules, deviations, and post-hoc analyses.
- Report effect sizes and uncertainty, not only significance or a single best score.
- Preserve negative and null results when they change the interpretation or scope.

Route detailed statistical planning and raw-data analysis to `modules/19_study_design_statistics_and_data.md` or a resolved provider.
