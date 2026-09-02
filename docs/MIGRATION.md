# Updating Existing Workspaces

Skill version 2.1.0 uses workspace schema 2. Existing command names, project types,
modules, and provider mappings remain available. Readiness checks are intentionally
stricter: older permissive output is not a guarantee that the same records will pass.

## Preview First

From the skill directory, with the validation environment active:

```bash
python scripts/migrate_workspace.py /path/to/research-workspace
```

This prints proposed changes without writing. It maps known legacy aliases such as
`claim` to `claim_text` and `evidence_pointer` to `evidence_source`, preserves extra
columns, and adds missing canonical columns. Conflicting aliases or malformed CSV
require manual resolution. Existing status values are never promoted or reinterpreted.

If the old initializer left the project type blank, explicitly supply the known type:

```bash
python scripts/migrate_workspace.py /path/to/research-workspace --project-type undergraduate_thesis
python scripts/migrate_workspace.py /path/to/research-workspace --project-type undergraduate_thesis --apply
```

The apply step stores originals and a change inventory under
`.academic-backups/<timestamp>/`. Gate scans exclude that directory. It then adds
the new records/columns; evidence IDs, actual evidence, source reviews, requirements,
and human sign-offs still need real input. An old `supported` row without evidence
remains blocked. A repeated migration is idempotent.

## Verify and Recover

```bash
python scripts/validate_evidence_status.py /path/to/research-workspace
python scripts/pre_prose_check.py /path/to/research-workspace
```

Blocking is expected until evidence gaps are resolved. Keep legitimate unknowns in
explicit limitation/assumption/proposal records or the excluded backlog.

To recover, inspect the backup's `migration.json`, compare any work done since the
migration, and restore only the intended original files from the same relative paths.
Newly created files are listed separately. Do not blindly replace newer research work.
The migrator does not delete existing research artifacts or run a destructive reset.

Before updating the skill installation itself, inspect `git status` and preserve local
edits. Use a named release tag for reproducibility or `main` for development; never
force-reset a locally modified installation. A previous skill version may read old
records, but downgrading is not a remedy for evidence-validation defects.
