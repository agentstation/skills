---
name: autoreview
description: Run an isolated second-model review immediately before publishing a PR with substantive code changes, at a configured plan checkpoint, or when the user explicitly requests autoreview.
---

# Autoreview

Use the bundled helper as an advisory closeout gate. It freezes and scans the
review bundle, isolates the reviewer from repository instructions and host
files, validates structured findings, and stops after one clean result.

## Pre-PR gate

When an agent is about to push or publish a PR, finish verification and commit
the intended change, then run:

```bash
export AUTOREVIEW="${AGENTS_HOME:-$HOME/.agents}/skills/autoreview/scripts/autoreview"
"$AUTOREVIEW" --gate pre-pr --mode auto
```

The default cadence is exactly this pre-PR checkpoint. It reviews the complete
branch diff and exits successfully without a model call when the PR changes
only documentation, configuration, metadata, generated files, or locks. A dirty
worktree fails the pre-PR gate because it would make the branch review
incomplete.

If an accepted finding changes code, verify and commit the fix, then rerun the
gate before publishing the PR.

## Configured checkpoints

Global and repository config can move the automatic cadence to `item`, `task`,
`phase`, or `step`. At that plan boundary, run the matching gate:

```bash
"$AUTOREVIEW" --gate phase --mode auto
```

The helper skips mismatched checkpoints and non-code-only automatic
checkpoints. A manual request always runs regardless of cadence:

```bash
"$AUTOREVIEW" --mode local
"$AUTOREVIEW" --mode branch --base origin/main
"$AUTOREVIEW" --mode commit --commit HEAD
```

Read [`CONFIG.md`](CONFIG.md) when adding a global, repository, or profile
configuration.

## Reviewer selection

With no explicit reviewer, the `auto` profile scores configured candidates,
keeps only installed isolation-safe harnesses, and avoids recursively invoking
the current host agent. The built-in profiles are:

```bash
"$AUTOREVIEW" --profile sol
"$AUTOREVIEW" --profile opus
"$AUTOREVIEW" --profile cross-lab
"$AUTOREVIEW" --profile value
"$AUTOREVIEW" --profile budget
"$AUTOREVIEW" --profile fable
```

Opus 5 high is the default Claude-side code reviewer. Fable requires manual
approval through an explicit CLI profile, model, or reviewer request; reserve it
for architecture-sensitive or exceptionally complex change review. Fable is
never selected automatically, approved by config or environment defaults, or
used as a fallback. Built-in Claude policy caps effort at `high`; a config can
consciously change that cap. Other supported models and harnesses can be
registered as candidates in config.

Read [`MODEL_SELECTION.md`](MODEL_SELECTION.md) when changing score axes,
candidate defaults, effort policy, or benchmark inputs.

## Findings

- Verify each advisory finding against the real code path.
- Accept concrete defects introduced by the reviewed change.
- Reject speculative edge cases, unrelated cleanup, and broad redesigns.
- Keep fixes inside the original task, changed owner boundary, and public
  contract.
- Stop on a clean helper exit. Add another reviewer only when the selected
  profile requires one.

The reviewer classifies every concrete actionable defect from P0 through P3;
deterministic post-processing then applies the requested output threshold. The
default threshold is P0. Widen it only when requested:

```bash
"$AUTOREVIEW" --max-priority P1
```

Pause and report when a finding requires a new protocol, schema, storage layout,
public API, release process, or owner boundary, or when two review-triggered
patch cycles have not converged.

## Safety

- TruffleHog scans the exact changed content before model invocation and fails
  closed on verified or unknown credentials.
- Codex receives the bundle in an empty read-only workspace with user config
  and repository rules disabled.
- Claude runs in safe mode with project skills, hooks, plugins, MCP servers,
  memory, filesystem, and shell access disabled.
- Explicit prompt, dataset, and repository config inputs remain inside the
  reviewed repository unless the user passes a trusted config path.
- The helper never pushes, commits, or mutates the reviewed repository.

Report the selected profile/reviewer, focused proof, accepted and rejected
findings, and the final clean result or consciously rejected remaining finding.
