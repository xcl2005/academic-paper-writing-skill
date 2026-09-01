# 11 Integrity and Reproducibility Guard

## Purpose

Audit claims, citations, statistics, equations, figures, and reproducibility before final output.

## Claim Audit

For each strong claim, record in `claim_ledger.csv`:

- claim;
- section;
- evidence type;
- evidence source;
- status: supported / weak / unsupported / assumption;
- fix needed.

High-risk words:

- novel;
- first;
- state-of-the-art;
- significant;
- robust;
- generalizable;
- efficient;
- superior;
- comprehensive;
- proves.

## Citation Audit

- No fabricated references.
- Prefer primary sources.
- Check titles, authors, venue, year, DOI/URL when possible.
- Ensure in-text citations and reference list match.
- Mark missing sources as `[citation needed]`.

## Statistical Audit

When relevant:

- repeated runs / seeds;
- variance / confidence intervals;
- significance test appropriate to metric and sample;
- effect size where useful;
- no p-hacking or cherry-picking.

Also check the unit of analysis, estimand, confirmatory/exploratory boundary, missing-data handling, multiplicity, model diagnostics, effect sizes, uncertainty intervals, sample-size rationale, and analysis deviations.

## Formula Audit

- Symbols defined before use.
- Dimensions and indices consistent.
- Loss/objective matches method description.
- Equations are necessary, not decorative.

## Figure/Table Audit

- Referenced in text.
- Captions meaningful.
- Axes/units readable.
- No misleading crop/scale.
- Data source clear.

## Reproducibility Audit

Record:

- code version / commit;
- environment;
- dependencies;
- dataset version/split;
- preprocessing;
- hyperparameters;
- seeds;
- training/evaluation commands;
- logs/checkpoints;
- plotting scripts;
- hardware/compute.

## Data, Code, and Open-Science Audit

Record in `templates/data_provenance.csv` when relevant:

- data/code ownership, licence, version, and access route;
- raw-to-derived transformations and storage locations;
- repository, DOI/accession, embargo, or controlled-access status;
- preregistration, protocol, model, prompt, environment, and source-data availability;
- privacy, consent, ethics, security, and third-party restrictions;
- manuscript statements that must match these records.

Do not invent repository deposits, accession numbers, licences, approvals, or access committees. Treat `available upon request` as unresolved unless a justified restriction is recorded.

## Cross-Artifact Consistency

Check that manuscript, abstract, figures, tables, supplement, response letter, data/code statements, presentation, and metadata use the same numbers, terminology, result status, and claim strength.
