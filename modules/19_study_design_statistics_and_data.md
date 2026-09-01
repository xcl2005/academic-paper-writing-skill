# 19 Study Design, Statistics, and Data Analysis

## Purpose

Turn research questions into defensible study designs and reproducible analyses. Use for experimental or observational design, sample-size reasoning, exploratory data analysis, statistical testing or modeling, uncertainty reporting, and analysis audits.

## Boundary

Do not invent data, results, significance, assumptions, sample sizes, effect sizes, or model diagnostics. Do not choose a test from the desired conclusion. Planned, exploratory, confirmatory, preliminary, and completed analyses must remain distinguishable.

## Design Contract

Define before analysis:

- scientific question and decision the analysis should inform;
- unit of observation, unit of assignment, and unit of analysis;
- population, sampling frame, inclusion and exclusion rules;
- exposure, intervention, predictors, outcomes, and time horizon;
- estimand or target quantity, not only a test name;
- controls, randomization, blocking, stratification, blinding, repeated measures, clusters, or hierarchy when relevant;
- plausible confounders, leakage paths, missingness, censoring, and measurement error;
- primary and secondary outcomes;
- confirmatory versus exploratory status.

For software and machine-learning studies, also define dataset version and split, preprocessing fit boundary, seeds, baseline parity, evaluation unit, repeated-run policy, compute budget, and leakage checks.

## Planning Standard

1. Create `templates/statistical_analysis_plan.md` before confirmatory analysis.
2. Justify sample size with domain evidence, precision targets, power or minimum detectable effect, simulation, or feasibility constraints. State assumptions and sensitivity. Do not use observed post-hoc power as evidence that a completed study was adequate.
3. Define the primary model or test, effect measure, uncertainty interval, assumption checks, missing-data strategy, multiplicity control, and sensitivity analyses before looking for favorable results.
4. Prefer estimates, effect sizes, and uncertainty intervals over p-values alone.
5. For Bayesian analysis, state priors, posterior summaries, convergence diagnostics, and predictive checks. Do not treat a credible interval as a frequentist confidence interval.
6. For qualitative or mixed-methods research, define sampling logic, coding or analysis procedure, reflexivity, triangulation, and how interpretations will be audited. Do not force a statistical test where it does not fit the design.

## Data Intake and Provenance

Before analysis:

- inventory every data asset in `templates/data_provenance.csv`;
- inspect schema, units, ranges, duplicates, impossible values, missingness patterns, labels, and joins;
- record ownership, consent or permission, licence, version, access constraints, and storage location;
- distinguish raw, cleaned, derived, simulated, and manually annotated data;
- preserve raw data and make transformations reproducible;
- freeze or version the analysis dataset before confirmatory reporting.

Never upload confidential or unpublished data to an external service without the user's authorization and an acceptable data-handling basis.

## Execution Standard

- Keep the analysis in runnable code or an equivalent auditable workflow.
- Record environment, package versions, seeds, parameters, exclusions, and generated artifacts.
- Run assumption and model diagnostics appropriate to the design.
- Correct or model multiplicity when a family of inferences is made.
- Label unplanned subgroup, outlier, transformation, and alternative-model analyses as exploratory.
- Report null, negative, and sensitivity results that materially affect interpretation.
- Keep plots and tables traceable to the exact analysis output.

## Reporting Contract

Report the design, actual sample size and exclusions, missing-data handling, model or test, effect estimate, uncertainty interval, exact or bounded p-value when relevant, multiplicity handling, diagnostics, software/version, and sensitivity results. A non-significant result is not proof of no effect; a significant result is not proof of practical importance or causality.

## Handoff Gate

Analysis is ready to support manuscript claims only when the data provenance, analysis plan, execution record, diagnostics, uncertainty, and result status are reviewable. Route unresolved claims to the claim ledger as `partially_supported`, `needs_recheck`, or `blocked`.
