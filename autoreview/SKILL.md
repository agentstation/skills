---
name: autoreview
description: Run an isolated second-model review before a substantive-code PR, at configured checkpoints, or when the user explicitly requests autoreview.
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

A clean pre-PR review stores a private attestation for 24 hours. The key covers
the exact substantive diff, base commit, reviewer contract, threshold, prompt,
datasets, and helper revision. A later proof or documentation commit reuses the
attestation when the substantive diff has not changed. Secret scanning and prompt
validation still run before reuse. Pass `--no-review-cache` to require a fresh
model review.

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
approval through an explicit CLI profile, model, or reviewer request. Reserve it
for architecture-sensitive or exceptionally complex change review. Fable is
never selected automatically, approved by config or environment defaults, or
used as a fallback. Built-in Claude policy caps effort at `high`. A config can
consciously change that cap.

Config can register other supported models and harnesses as candidates.

The helper also supports Kimi Code, OpenCode, and Cursor Agent when their CLIs
exist:

```bash
"$AUTOREVIEW" --engine kimi --model kimi-k2
"$AUTOREVIEW" --engine opencode --model opencode/kimi-k3 --thinking max
"$AUTOREVIEW" --engine cursor --model grok-4.5
"$AUTOREVIEW" --reviewers cursor:grok-4.5,opencode:opencode/glm-5.2:max
"$AUTOREVIEW" --list-harnesses
```

Kimi model names use its configured model catalog. OpenCode model names use its
runtime `provider/model` catalog. Cursor model names use the Cursor account
catalog, including subscription-hosted models. A compatible Pi CLI enables Pi
as an explicit or configured candidate.

Desktop applications and headless review harnesses are separate capabilities.
For example, Cursor Desktop does not satisfy the `cursor-agent` requirement,
and Codex Desktop does not satisfy the `codex` requirement. A missing CLI is
never automatically eligible. Inspect or explicitly install harnesses with:

```bash
"$AUTOREVIEW" --list-harnesses
"$AUTOREVIEW" --install-harness cursor
"$AUTOREVIEW" --engine cursor --model grok-4.5 --install-if-missing
```

Installation is always explicit. Automatic scored selection skips missing
harnesses. It never downloads software unless the caller passes
`--install-if-missing`. With that opt-in, a profile lacking quorum installs the
best missing isolation-safe harness. An unavailable harness fails
with a machine-readable `harness_unavailable` or `profile_unavailable` marker,
desktop-versus-CLI diagnosis, canonical installation command, and recovery
options.

The helper does not install Kimi. Install Kimi Code separately before you
select it.

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

The default threshold is P0. The helper sends the selected threshold to the
reviewer and asks it to omit lower-priority findings. Deterministic
post-processing applies the same threshold as a final guard. Widen the
threshold only when requested:

```bash
"$AUTOREVIEW" --max-priority P1
```

Pause and report when a finding requires a new protocol, schema, storage layout,
public API, release process, or owner boundary. Also pause when two
review-triggered patch cycles have not converged.

## Safety

- TruffleHog scans the exact changed content before model invocation and fails
  closed on verified or unknown credentials.
- Codex receives the bundle in an empty read-only workspace with user config
  and repository rules disabled.
- Claude runs in safe mode with project skills, hooks, plugins, MCP servers,
  memory, filesystem, and shell access disabled.
- OpenCode runs from an empty workspace with project instructions, Claude
  compatibility, plugins, MCP servers, filesystem, shell, and edit tools
  disabled.
- Cursor Agent runs from an empty workspace with an isolated permission config.
- It uses Ask mode when supported and denies filesystem, shell, write, fetch,
  force-write, and MCP permissions.
- Pi runs without repository context files, extensions, skills, sessions, or
  tools.
- Kimi runs from an empty workspace with a staged configuration, no tools or
  subagents, and an empty skill directory. It requires Kimi Code 0.30.0 or
  newer.
- Each engine runs in an owned process group. An interrupt terminates the
  engine and its child processes.
- Explicit prompt, dataset, and repository config inputs remain inside the
  reviewed repository unless the user passes a trusted config path.
- The helper never pushes, commits, or mutates the reviewed repository.

Report the selected profile/reviewer, focused proof, accepted and rejected
findings, and the final clean result or consciously rejected remaining finding.
