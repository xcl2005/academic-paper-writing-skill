# 01 Agent Orchestrator

## Purpose

Coordinate the workflow without loading every module.

## Standard Reasoning Flow

1. Classify the user's request:
   - research paper;
   - undergraduate thesis;
   - hybrid capstone research;
   - formatting-only;
   - literature-only;
   - experiment-only;
   - rebuttal/revision;
   - defense preparation.
2. Identify known inputs:
   - topic;
   - field;
   - target venue/school/template;
   - existing draft/code/data/results;
   - deadline;
   - available compute/resources.
3. Identify unknowns and risks.
4. Load the minimal modules required.
5. Create/update `project_state.yaml`.
6. Produce structured artifacts before final prose when the task is complex.
7. Run integrity checks before final output.

## Do Not Over-Ask

Ask only high-value clarifying questions. If the next step can be done with assumptions, proceed and record assumptions in `assumption_register.md`.

## Output Priority

Prefer:

1. decisions and next actions;
2. matrices and checklists;
3. concise explanations;
4. full prose only when the structure is ready.
