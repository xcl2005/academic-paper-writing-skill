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
