---
name: autoreview
description: Run an isolated second-model review of a local, branch, or commit diff when the user explicitly asks for autoreview or a pre-ship review.
disable-model-invocation: true
---

# Autoreview

Run the bundled helper as an advisory closeout review. It builds and scans the
review bundle, isolates the reviewer from repository instructions and host
files, validates structured findings, and stops after one clean result.

This AgentStation skill is derived from
[`openclaw/agent-skills`](https://github.com/openclaw/agent-skills/tree/main/skills/autoreview).
Its model policy is intentionally narrower.

## Model policy

Use exactly one of:

- Codex: `gpt-5.6-sol`, `high` effort by default.
- Claude: `claude-opus-5`, `high` effort by default.

Use `xhigh` for a review whose correctness depends on architecture, concurrency,
cryptography, security boundaries, migrations, protocols, public APIs, or a
large cross-module change. The helper rejects other engines, models, effort
levels, and fallback chains. In particular, this review lane does not use
Fable.

## Run

Set the helper path once:

```bash
export AUTOREVIEW="${AGENTS_HOME:-$HOME/.agents}/skills/autoreview/scripts/autoreview"
```

Choose the reviewer:

```bash
# Default: GPT-5.6 Sol, high
"$AUTOREVIEW" --mode auto

# Complex review: GPT-5.6 Sol, xhigh
"$AUTOREVIEW" --mode auto --thinking xhigh

# Opus 5, high
"$AUTOREVIEW" --mode auto --engine claude

# Opus 5, xhigh
"$AUTOREVIEW" --mode auto --engine claude --thinking xhigh
```

Target explicitly when auto-selection is not appropriate:

```bash
"$AUTOREVIEW" --mode local
"$AUTOREVIEW" --mode branch --base origin/main
"$AUTOREVIEW" --mode commit --commit HEAD
```

Use `--prompt`, a repository-relative `--prompt-file`, or repository-relative
`--dataset` for extra review criteria. Use `--dry-run` to inspect target and
reviewer selection without invoking a model.

## Findings

- Treat findings as advisory and verify each against the real code path.
- Accept concrete defects introduced by the reviewed change.
- Reject speculative edge cases, unrelated cleanup, and broad redesigns.
- Keep fixes inside the original task, changed owner boundary, and public
  contract.
- If an accepted finding changes code, rerun focused tests and one review.
- Stop on a clean helper exit. Do not add another reviewer merely to reconfirm.

The default threshold is P0. Widen it only when the user asks:

```bash
"$AUTOREVIEW" --max-priority P1
```

## Scope breaks

Pause and report instead of patching when a finding requires a new protocol,
schema, storage layout, public API, release process, or owner boundary. Also
pause when two review-triggered patch cycles have not converged or the review
would more than double the original files or non-test LOC.

## Safety and isolation

- The helper runs TruffleHog against the exact changed content before model
  invocation and fails closed on verified or unknown credentials.
- Codex receives the validated bundle in an empty read-only workspace with user
  config and repository rules disabled.
- Claude runs in safe mode from an empty workspace with project skills, hooks,
  plugins, MCP servers, memory, filesystem, and shell access disabled.
- Explicit prompt and dataset inputs must remain inside the reviewed repository.
- The helper never pushes, commits, or mutates the reviewed repository.

Large safe bundles are split into bounded complete passes and merged before the
exit decision. Heartbeats indicate a healthy long-running review; allow up to
30 minutes while they continue.

## Result

Report:

- command and reviewer used;
- focused tests or other proof;
- accepted and rejected findings, briefly;
- final clean result, or the consciously rejected remaining finding.

Do not run another review solely to improve report wording.
