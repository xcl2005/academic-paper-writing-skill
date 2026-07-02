# Contributing

Thanks for helping improve Academic Paper Writing Skill.

This project exists to make academic writing assistance more grounded, modular, and honest. Contributions should strengthen evidence tracking and reduce hallucination risk.

## Useful contribution types

- Improve modules for literature review, novelty checks, experiments, figures, rebuttals, or thesis workflows.
- Add templates for claim ledgers, review matrices, project state, or defense preparation.
- Add schema validation for project artifacts.
- Improve support for undergraduate thesis and graduation project requirements.
- Add examples that show evidence-first academic workflows.
- Improve README clarity and installation instructions.

## Non-negotiable contribution rules

- Do not weaken no-fabrication rules.
- Do not add instructions to invent citations, SOTA, benchmark results, school requirements, or local rules.
- Do not blur planned, preliminary, and achieved results.
- Do not make final submission, authorship, ethics, or compliance decisions without human review.
- Do not silently let external tools override this skill's core invariants.

## Before opening a pull request

Run:

```bash
python scripts/validate_skill.py
python -m py_compile scripts/*.py
```

If you change a module, explain:

- which project type it affects;
- which stage it improves;
- which templates or schemas it uses;
- how it preserves no-fabrication and claim-to-evidence rules.

## Good pull request titles

- `Add defense preparation checklist`
- `Improve novelty verification matrix`
- `Add reviewer rebuttal example`
- `Tighten external skill acceptance tests`
