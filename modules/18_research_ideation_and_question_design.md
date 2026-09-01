# 18 Research Ideation and Question Design

## Purpose

Generate, challenge, and prioritize research directions without presenting ideas as findings. Use this module for topic selection, proposal scoping, gap discovery, hypothesis generation, and choosing among candidate directions.

## Boundary

Brainstorming proposes possibilities. It does not establish novelty, validate a mechanism, approve ethics or dual-use risk, or prove that a study will work. Hand those questions to literature, study-design, integrity, and authorized human review.

## Input Contract

Record what is known before generating ideas:

- decision context and intended audience;
- field, population or system, and unit of analysis;
- available data, equipment, compute, time, and expertise;
- target contribution type: empirical, methodological, theoretical, resource, replication, or engineering;
- non-negotiable constraints and known ethical, privacy, safety, or dual-use concerns;
- evidence anchors and explicit assumptions.

Unknowns remain unknown. Do not silently convert a preference, analogy, or plausible mechanism into evidence.

## Operating Standard

1. Frame the problem in more than one way: phenomenon, mechanism, measurement, intervention, application, replication, and failure mode.
2. Generate candidate ideas independently before discussion when multiple agents or reviewers are used. This reduces premature convergence and social anchoring.
3. Give each candidate a testable research question, a proposed mechanism or rationale, a falsifiable prediction, a minimum viable study, expected evidence, and a failure interpretation.
4. Search for the nearest prior work before assigning a novelty label. Record the source boundary and use `needs_evidence` when the search is incomplete.
5. Run an adversarial pass against each candidate: duplication, confounding, data leakage, weak measurement, unavailable data, infeasible sample size, hidden cost, ethical risk, and a result that would not change the conclusion.
6. Evaluate candidates transparently. Suggested dimensions are importance, evidence for the gap, testability, expected information gain, feasibility, resource fit, ethical acceptability, and publication or graduation fit.
7. Keep criteria and weights visible. Do not hide judgment inside a single unexplained score.
8. Select a portfolio rather than one brittle idea when uncertainty is high: one primary direction, one lower-risk fallback, and one high-upside option.
9. Record why candidates were selected, deferred, merged, or rejected in `templates/research_idea_portfolio.csv`.

## Handoff Gate

An idea is ready for study design only when it has:

- a specific question and unit of analysis;
- an observable outcome or evaluation target;
- at least one plausible falsifier or disconfirming result;
- a minimum viable evidence plan;
- a preliminary nearest-work check;
- named feasibility and integrity risks;
- a decision status and rationale.

Use `templates/research_idea_portfolio.csv` and keep `decision_status` as `needs_evidence` until the nearest-work and feasibility checks are reviewable.
