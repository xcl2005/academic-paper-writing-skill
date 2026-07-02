# 17 External Skill Acceptance Tests

## Purpose

Decide whether a skill/tool found by the installer or by fallback search can actually be used in this workflow.

## Candidate Acceptance Checklist

A candidate must pass most relevant checks:

```text
[ ] Has a clear README or SKILL.md.
[ ] Task scope matches the current task.
[ ] Does not encourage fabricated citations/results.
[ ] Provides examples or usage instructions.
[ ] Has a clear source URL or local path.
[ ] Has license information or acceptable risk note.
[ ] Has recent maintenance or is stable enough for the task.
[ ] Can run in the current environment.
[ ] Does not require unsafe scripts without inspection.
[ ] Outputs inspectable files or logs.
[ ] Does not require modifying this skill's core files.
[ ] Does not conflict with official venue/school requirements.
```

## Scoring Rubric

Score out of 100:

```text
Task relevance:                 0-25
Documentation/examples:          0-15
Maintenance/stability:           0-15
Integrity compatibility:         0-15
Environment compatibility:       0-10
Output inspectability:           0-10
License/safety clarity:          0-5
Community signal:                0-5
```

Recommended interpretation:

- 85-100: strong candidate.
- 70-84: usable if task-relevant.
- 55-69: inspect manually; use only with caution.
- below 55: reject unless user explicitly requests.

## Decision Labels

Use one of:

- `accepted_primary`;
- `accepted_helper`;
- `deferred_needs_manual_check`;
- `rejected_low_relevance`;
- `rejected_integrity_conflict`;
- `rejected_safety_or_license`;
- `rejected_environment_incompatible`.

## Compatibility Report

For every external skill/tool selected or rejected, record:

- name;
- source/path;
- selected by installer or fallback search;
- score;
- decision;
- reason;
- risk;
- expected use;
- override rule if conflict occurs.
