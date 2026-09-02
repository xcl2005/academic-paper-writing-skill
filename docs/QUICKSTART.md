# Validation Runtime

The skill instructions are plain text. The Python helpers additionally need Python
3.10 or 3.12 and the pinned dependency in `requirements.txt`. Python 3.12 is the local
development baseline; CI checks Windows and Ubuntu on both versions.

Use an environment outside the skill directory. Keep research output outside the
installed skill so updating the skill cannot replace project data.

## macOS / Linux

```bash
SKILL_ROOT="$HOME/.agents/skills/academic-paper-writing-skill"
python3 -m venv "$HOME/.local/share/academic-skill-venv"
PY="$HOME/.local/share/academic-skill-venv/bin/python"
"$PY" -m pip install -r "$SKILL_ROOT/requirements.txt"
"$PY" "$SKILL_ROOT/scripts/init_project.py" --out "$HOME/research/paper-workspace" --type research_paper
"$PY" "$SKILL_ROOT/scripts/check_stage_gate.py" "$HOME/research/paper-workspace" --gate literature --allow-empty
"$PY" "$SKILL_ROOT/scripts/pre_prose_check.py" "$HOME/research/paper-workspace" --expect-block
```

## Windows PowerShell

```powershell
$SkillRoot = "$HOME\.agents\skills\academic-paper-writing-skill"
python -m venv "$HOME\.academic-skill-venv"
$Py = "$HOME\.academic-skill-venv\Scripts\python.exe"
& $Py -m pip install -r "$SkillRoot\requirements.txt"
& $Py "$SkillRoot\scripts\init_project.py" --out "$HOME\research\paper-workspace" --type research_paper
& $Py "$SkillRoot\scripts\check_stage_gate.py" "$HOME\research\paper-workspace" --gate literature --allow-empty
& $Py "$SkillRoot\scripts\pre_prose_check.py" "$HOME\research\paper-workspace" --expect-block
```

The structure check reports `structure_valid`. The blank workspace's prose check
reports `blocked`; `--expect-block` exits successfully precisely because blocking is
expected. Remove that flag during normal readiness checks. Add actual sources and
reviewed support records following [Evidence Contract](EVIDENCE_CONTRACT.md).

For Claude Code, substitute its actual user/project installation path for `SKILL_ROOT`.
Provider discovery supports `.claude/skills`, `.agents/skills`, legacy `.codex/skills`,
and explicit repeated `--skill-root` arguments. No external provider is needed for the
internal baseline, and none is installed by these commands.

Examples elsewhere use `python scripts/...` as shorthand: activate this environment
and run those commands from the skill root, or use the absolute paths shown above.
To check the maintained package from any working directory:

```text
<environment-python> <skill-root>/scripts/check.py
```

Read [Migration](MIGRATION.md) before updating an existing research workspace.
