# 05 Venue Intelligence

## Purpose

Adapt research-paper strategy to the target venue.

## Rule

Do not hard-code current venue policies as permanent facts. NeurIPS, ICML, CVPR, ACL/ARR, AAAI, and journal requirements can change. Always verify current official author instructions, checklist, page limits, anonymity rules, ethics requirements, rebuttal process, and formatting rules before final decisions.

## Venue Preference Heuristics

Use these as starting hypotheses, not final facts.

### NeurIPS / ICML / ICLR-like ML venues

Commonly value:

- strong motivation and clear contribution;
- rigorous baselines and ablations;
- reproducibility and code/data transparency;
- statistics or repeated runs when stochastic;
- limitations and ethics/societal impact where relevant;
- convincing novelty beyond engineering combination.

### CVPR / ICCV / ECCV-like vision venues

Commonly value:

- strong empirical results on accepted benchmarks;
- clear method figures;
- visual qualitative evidence;
- fair comparison with recent methods;
- dataset and metric rigor;
- clear ablation and failure cases.

### ACL / EMNLP / NAACL / ARR-like NLP venues

Commonly value:

- task motivation and linguistic/empirical soundness;
- dataset quality and evaluation appropriateness;
- error analysis and qualitative examples;
- ethics, annotation, data leakage, and reproducibility;
- clear difference from recent LLM/SOTA work.

### AAAI / IJCAI-like AI venues

Commonly value:

- broad AI relevance;
- technical soundness;
- clarity for a general AI audience;
- evaluation breadth;
- responsible AI and reproducibility where relevant.

## Venue Fit Output

For each target venue, produce:

- fit score as a cautious estimate, not a promise;
- missing evidence;
- likely reviewer concerns;
- required formatting/policy checks;
- backup venues.
