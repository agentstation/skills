# Autoreview configuration

Configuration is layered in this order, with later values replacing earlier
ones:

1. built-in defaults;
2. `${XDG_CONFIG_HOME:-~/.config}/autoreview/config.toml`;
3. `<repo>/.agents/autoreview/config.toml`;
4. each explicit `--config PATH`;
5. environment and CLI reviewer overrides.

Set `AUTOREVIEW_CONFIG` to replace the default global path. Use `--no-config`
for a reproducible built-in-only run.

## Automation

```toml
version = 1
default_profile = "auto"

[automation]
cadence = "pre-pr"
substantive_only = true
```

Cadence values are `manual`, `pre-pr`, `item`, `task`, `phase`, and `step`.
Manual CLI invocations always run. Other gates run only when their value equals
the configured cadence. With `substantive_only = true`, automatic gates skip
when no changed path is classified as source code.

## Profiles

A scored profile chooses the highest-scoring available candidate per harness:

```toml
[profiles.auto]
strategy = "score"
reviewers = 1
```

An exact profile names candidates:

```toml
[profiles.security-panel]
candidates = ["sol", "opus5"]
```

Select it with `--profile security-panel`. Exact profiles fail closed if a
required harness is unavailable. A candidate marked
`manual_approval_required = true` requires an explicit `--profile`; it cannot
become an automatic default.

## Candidates

```toml
[candidates.local-opus]
engine = "claude"
model = "claude-opus-5"
effort = "high"
manual_approval_required = false
cost = 6.6
intelligence = 9
taste = 9
deepswe_pass_rate = 73
deepswe_avg_cost_usd = 6.08
```

`engine` identifies the isolation harness: `claude` means the Claude Code CLI
and `codex` means the Codex CLI. `model` is the model invoked through that
harness. The candidate table name is a stable ID for the complete reviewer
configuration, not another model field.

`cost` is literal on a 0–10 scale derived from DeepSWE's measured average cost
per high-effort task: 0 is free and 10 is the most expensive candidate. Preserve
the underlying measurement in `deepswe_avg_cost_usd`. Lower cost improves the
automatic-selection score. `manual_approval_required` is a separate safety gate
and does not affect the score. See
[`MODEL_SELECTION.md`](MODEL_SELECTION.md) for the normalization formula and
source data.

Supported engines remain governed by the helper's isolation checks. At present,
Codex, Claude, and a sufficiently recent Pi CLI can be automatic candidates.
Other bundled adapters fail closed until their CLIs can prove equivalent
isolation.

Fable candidates must set `manual_approval_required = true`. Approval is
granted by an explicit `--profile`, `--model`, or `--reviewers` request. Fable
is also refused in fallback chains because fallback invocation is automatic.
The legacy `manual_approval`, `explicit_only`, and `automatic = false` fields
remain recognized when reading older config, but new config should use
`manual_approval_required`.

## Policy

```toml
[policy]
avoid_same_host = true
anthropic_max_effort = "high"
```

`avoid_same_host` keeps automatic selection from nesting Codex inside Codex or
Claude inside Claude. Exact CLI selections and explicit profiles are owner
choices and may select the host engine.

The Anthropic effort cap applies to every Claude reviewer. Raise it only when
your own evaluations justify the additional spend.
