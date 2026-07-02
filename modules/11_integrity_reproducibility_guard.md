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
