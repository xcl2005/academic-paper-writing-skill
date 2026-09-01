# 12 Writing Style Adapter

## Purpose

Adapt writing style to project type, venue, school template, and user needs.

## Select the Writing Operation

- `draft`: create new prose from a verified source and evidence packet.
- `rebuild`: reorganize existing material around a stronger argument while preserving facts.
- `polish`: improve clarity, flow, grammar, and academic tone without adding claims.
- `translate`: preserve meaning, numbers, citations, equations, and technical terms across languages.
- `compress_or_expand`: change length while preserving the source boundary and claim strength.

Do not use polishing to perform unlogged scientific revision. Route evidence, method, or analysis changes back to their owning capability.

## General Rules

- Clarity before decoration.
- Preserve meaning when editing.
- Do not invent results, citations, or contributions.
- Make claims proportional to evidence.
- Prefer concrete academic wording over vague praise.

Before editing, freeze protected facts: numbers, signs, units, sample sizes, p-values or intervals, equations, model and dataset names, citations, figure/table pointers, limitations, and claim strength. Maintain `templates/terminology_ledger.csv` for substantial or multilingual work.

After editing, run a consistency pass and summarize material changes and unresolved author checks. A smoother sentence is not allowed to become a stronger scientific claim.

## Research Paper Style

- Strong motivation.
- Explicit gap.
- Concrete contributions.
- Related work by theme, not paper-by-paper list.
- Experiments written around research questions.
- Honest limitations.

## Top-Tier Style

- Use precise claims.
- Make novelty and evidence easy for reviewers to find.
- Avoid hype without numbers.
- Figure 1 and contribution bullets must align with experiments.

## Undergraduate Thesis Style

- Follow school template first.
- Emphasize background, requirement analysis, design, implementation, testing, results, and summary.
- Avoid pretending ordinary engineering work is top-tier research.
- Show concrete work through modules, screenshots, tests, logs, and diagrams.

## Venue/School Specificity

If target venue/school is known, verify official instructions. If unknown, write in a safe general academic style.

Select the applicable reporting guideline or study-specific checklist when relevant. Use a resolved provider such as `nature-writing`, `scientific-writing`, or `nature-polishing` for deeper section, submission, language, LaTeX, or formatting rules; preserve this module's fact invariants across the handoff.
