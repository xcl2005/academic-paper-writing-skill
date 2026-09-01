# 13 Simulated Review and Rebuttal Engine

## Purpose

Simulate reviewer concerns and prepare rebuttal/revision plans.

Keep two roles separate:

- reviewer assessment evaluates the manuscript and evidence packet;
- author response maps received or simulated comments to evidence and exact revisions.

Do not let a response draft masquerade as an independent review, and do not rewrite a review merely to make the response easier.

## Simulated Review Setup

Simulate:

- Reviewer 1: method/technical rigor;
- Reviewer 2: experiments/baselines/statistics;
- Reviewer 3: writing/related work/clarity/impact;
- Area Chair: overall decision, consistency, venue fit.

When multiple reviewers are requested, define distinct emphasis briefs, keep their source packets identical, and generate their assessments independently before synthesis. Do not invent reviewer identities, institutions, biographies, or confidential knowledge.

## Review Rules

- Do not invent actual reviewer feedback.
- Be critical but fair.
- Ground comments in the draft, matrices, experiments, and venue heuristics.
- Separate fatal issues from fixable issues.

Give every substantive concern a stable ID, manuscript or claim pointer, evidence pointer, severity, blocking status, and actionable revision path. Mark an issue blocking only when the manuscript cannot establish its central case without resolution.

Audit methods, statistics, reproducibility, ethics, figures/tables, citations, reporting guidance, novelty, significance, and internal consistency within the provided source boundary.

## Rebuttal Rules

A good rebuttal:

- thanks reviewers briefly;
- answers directly;
- provides evidence;
- admits real limitations;
- states exact manuscript changes;
- does not sound defensive;
- does not promise impossible new experiments.

For every reviewer comment, record the response position, evidence, action owner, exact manuscript change and location, status, and unresolved dependency in `templates/rebuttal_matrix.md`. Reconcile the response letter, clean manuscript, redline, figures, supplement, and declarations before delivery.

## Output

Use:

- `templates/simulated_review.md`;
- `templates/rebuttal_matrix.md`.
