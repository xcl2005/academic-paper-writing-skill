# Thesis Outline Workflow

This example shows how to use the skill for an undergraduate thesis or graduation project without inventing local requirements.

## User request

```text
Use $academic-paper-writing-skill to turn my graduation project idea into a thesis outline, scope ladder, and evidence checklist.
```

## Expected workflow

1. Set `project_type` to `undergraduate_thesis`.
2. Ask for school template, advisor notes, rubric, and deadline if the user has them.
3. If local requirements are missing, mark them as unknown rather than inventing them.
4. Build a scope ladder that separates must-have, should-have, and stretch work.
5. Create a graduation evidence map before drafting the thesis outline.
6. Keep planned work, preliminary results, and completed results separate.

## Working artifacts

| Artifact | Purpose |
|---|---|
| `templates/requirement_discovery_log.md` | Tracks confirmed, missing, and assumed requirements |
| `templates/scope_ladder.md` | Keeps the project feasible under graduation constraints |
| `templates/graduation_evidence_map.csv` | Maps each thesis section to implementation, tests, screenshots, data, or official requirements |
| `templates/assumption_register.md` | Records assumptions that need advisor or school confirmation |

## Good output shape

```text
Confirmed: project topic, implementation target, current prototype state.
Unknown: school formatting template, defense rubric, advisor workload expectation.
Next artifact: scope_ladder.md with MVP, standard, and stretch tiers.
Draft status: thesis outline can proceed, but compliance language remains marked for human confirmation.
```

