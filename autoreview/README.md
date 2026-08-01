# Autoreview

Autoreview runs an isolated second-model code review before you publish a pull
request. It freezes and scans the review bundle, then isolates the reviewer
from repository instructions and host state. It validates the structured
findings and stops after one clean result.

[`SKILL.md`](SKILL.md) holds the agent-facing contract. This page covers
install, the commands a person runs, and the documents that own each setting.

## Install

```bash
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code -y
```

Set the helper path:

```bash
export AUTOREVIEW="${AGENTS_HOME:-$HOME/.agents}/skills/autoreview/scripts/autoreview"
```

## Quickstart

Run the pre-PR gate after the final checks and the intended commit:

```bash
"$AUTOREVIEW" --gate pre-pr --mode auto
```

The gate reviews the complete branch diff. It exits successfully without a
model call when the branch changes only documentation, configuration,
metadata, generated files, or locks. A dirty worktree fails the gate, because
a branch review of uncommitted work is incomplete.

Other modes run on request:

```bash
"$AUTOREVIEW" --mode local
"$AUTOREVIEW" --mode branch --base origin/main
"$AUTOREVIEW" --mode commit --commit HEAD
```

Configuration can move the automatic cadence to an `item`, `task`, `phase`, or
`step` checkpoint. Run the matching gate at that plan boundary:

```bash
"$AUTOREVIEW" --gate phase --mode auto
```

## Reviewer selection

The default profile scores the configured candidates, keeps the installed
isolation-safe harnesses, and avoids the current host agent. A named profile
selects a fixed roster instead:

```bash
"$AUTOREVIEW" --profile sol
"$AUTOREVIEW" --profile cross-lab
"$AUTOREVIEW" --list-harnesses
"$AUTOREVIEW" --install-harness <name>
```

Fable needs an explicit request. It never enters automatic selection or
fallback.

## Findings

The reviewer returns structured findings at priority `P0` through `P3`. Fix
every `P0` and `P1` finding, or record the reason to accept it. Raise the
threshold to see less:

```bash
"$AUTOREVIEW" --max-priority P1
```

## Documents

- [`SKILL.md`](SKILL.md): gates, modes, selection, findings, and safety.
- [`CONFIG.md`](CONFIG.md): automation, profiles, candidates, and policy.
- [`MODEL_SELECTION.md`](MODEL_SELECTION.md): cost basis, allocation policy,
  and the selected sweet spots.
- [`AGENTS.md`](AGENTS.md): maintenance rules for this skill.
- [`UPSTREAM.md`](UPSTREAM.md): upstream source and provenance.

## Maintenance

Run from the repository root:

```bash
python3 autoreview/scripts/autoreview_test.py
python3 -m pytest autoreview/tests/
./scripts/validate-skills
```
