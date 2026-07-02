# 15 Self-Update and Maintenance

## Purpose

Keep the skill useful as models, tools, venues, and academic practices change.

## Philosophy

This skill is not sacred text. Future agents may simplify, delete, merge, or rewrite parts to improve usability. The protected core is the invariant set, not exact wording.

## When to Update

Update when:

- venue rules changed;
- new model/tool generation appears;
- better high-quality external skills/tools exist;
- modules become duplicated;
- workflow is too long for agents to follow;
- templates are hard to parse;
- file structure is confusing;
- user workflow changes.

## Allowed Changes

- shorten prose;
- split large modules;
- merge duplicate modules;
- delete stale recommendations;
- replace tool names;
- add schemas or templates;
- change file layout;
- update routing rules;
- add new project types;
- add external-skill adapters.

## Forbidden Changes

- weakening no-fabrication rules;
- weakening integrity guard;
- treating Excel/Word as the only source of truth;
- inventing school or venue requirements;
- removing claim-to-evidence mapping;
- removing requirement discovery for undergraduate thesis;
- pretending unverified SOTA is current;
- giving external skills permission to silently rewrite core files.

## Update Procedure

1. Read `SKILL.md`, `skill_manifest.yaml`, and this module.
2. Identify duplication/staleness.
3. Check external high-quality skills/tools if relevant via `03_external_skill_gateway.md`.
4. Modify minimal necessary files.
5. Update `CHANGELOG.md`.
6. Run `scripts/validate_skill.py`.
7. State what changed and why.
