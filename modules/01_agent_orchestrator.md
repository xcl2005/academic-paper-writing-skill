# 01 Agent Orchestrator

## Purpose

Coordinate the workflow without loading every module.

## Standard Reasoning Flow

1. Classify the user's project context:
   - research paper;
   - undergraduate thesis;
   - hybrid capstone research;
   - standalone research task;
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
4. Detect the capability or capabilities in `capability_registry.yaml`.
5. Load the minimal internal modules required and resolve any suitable installed provider through `modules/22_capability_provider_router.md`.
6. Create/update `project_state.yaml` and record active capabilities, provider decisions, assumptions, and artifact status.
7. Produce structured artifacts before final prose when the task is complex.
8. Run the relevant stage gate, integrity checks, and artifact-specific QA before final output.

## Orchestration Rules

- A project stage does not force every module to load.
- A provider is bound to a capability for one task or handoff, not permanently to the whole project.
- Keep provider handoffs explicit with `templates/capability_handoff.yaml` when more than one capability is involved.
- Preserve existing evidence artifacts and statuses across handoffs.
- Do not mark a stage complete because prose or an export exists; check the underlying evidence and acceptance contract.

## Do Not Over-Ask

Ask only high-value clarifying questions. If the next step can be done with assumptions, proceed and record assumptions in `assumption_register.md`.

## Output Priority

Prefer:

1. decisions and next actions;
2. matrices and checklists;
3. concise explanations;
4. full prose only when the structure is ready.

For provider-backed work, also report the selected provider, fallback status, unresolved checks, and output acceptance result.
