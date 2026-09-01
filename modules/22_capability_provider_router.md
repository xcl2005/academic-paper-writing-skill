# 22 Capability Provider Router

## Purpose

Resolve each research capability to the strongest available specialist without making the workflow depend permanently on one external skill. The registry is `capability_registry.yaml`.

## Resolution Protocol

1. Identify one or more capabilities from the user's request.
2. Preserve an explicit user choice of provider unless it violates a higher-priority rule or cannot satisfy the task.
3. Run `python scripts/resolve_capability.py <capability>` or emulate the same registry lookup.
4. Prefer an installed provider whose tags fit the target and whose required companion skills are present.
5. If a provider is selected, read its `SKILL.md` completely and read the provider resources it requires for the chosen workflow. The registry summary is not a substitute for the provider's detailed instructions.
6. Normalize the task into `templates/capability_handoff.yaml`. Pass only the inputs and permissions needed for that capability.
7. Write provider outputs to the project workspace or an isolated provider-output directory. Do not let a provider silently edit this skill's modules or unrelated project files.
8. Validate the output against the registry acceptance contract, `modules/17_external_skill_acceptance_tests.md`, and the relevant stage gate.
9. If the provider is absent, incomplete, unsafe, incompatible, or fails acceptance, use the internal fallback module and report the limitation.

## Provider Selection

Provider order is a preference, not a permanent binding. Consider:

- target venue, discipline, artifact format, and language;
- task depth and provider specialization;
- installed state and required companion skills;
- source and data handling constraints;
- the user's selected tool or backend;
- output acceptance criteria and observed provider performance.

Do not install an unknown provider silently. Use the external skill gateway when discovery or installation is needed.

## Composition

Use more than one provider only when the task genuinely spans distinct capabilities, such as search followed by synthesis or analysis followed by figure production. Keep each handoff explicit. Do not create a long provider sequence by default, and do not ask a polishing provider to change evidence or analysis decisions owned by another capability.

## Invariant Precedence

Provider detail should control domain execution, formatting, and QA when selected. This skill still controls evidence status, no-fabrication rules, authorization boundaries, provenance, and final human accountability.
