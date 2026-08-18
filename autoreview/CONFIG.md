# Autoreview configuration

The helper layers configuration in this order. Later values replace earlier
values:

1. built-in defaults.
2. `${XDG_CONFIG_HOME:-~/.config}/autoreview/config.toml`.
3. `<repo>/.agents/autoreview/config.toml`.
4. each explicit `--config PATH`.
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
when the changed paths contain no source code.

Clean pre-PR reviews use a private 24-hour attestation cache. The cache key
includes the base commit, exact substantive diff, reviewer settings, priority
threshold, explicit prompt and dataset content, and helper revision. Changes to
those inputs require a new model review. Non-substantive proof changes can reuse
the prior result after secret scanning and prompt validation pass. Set
`AUTOREVIEW_NO_REVIEW_CACHE=1` or pass `--no-review-cache` to bypass the cache.

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
required harness is unavailable. A candidate with
`manual_approval_required = true` requires an explicit `--profile`. It cannot
become an automatic default.

## Candidates

```toml
[candidates.local-opus]
engine = "claude"
model = "claude-opus-5"
effort = "high"
manual_approval_required = false
cost = 6.6
intelligence = 8
taste = 8.5
deepswe_pass_rate = 73
deepswe_avg_cost_usd = 6.08
```

`engine` identifies the review harness. Supported runnable engines are
`claude`, `codex`, `pi`, `kimi`, `opencode`, and `cursor`. The helper also
accepts `cursor-agent` as an alias. `model` identifies the model that the
harness invokes. Kimi accepts a model alias from its configuration. OpenCode
expects a provider-qualified `provider/model` name. Cursor accepts model names
from the account catalog.

The candidate table name is a stable ID for the complete reviewer
configuration, not another model field.

`cost` uses a literal 0–10 scale. The scale derives from DeepSWE's measured
average task cost at the candidate's configured effort. Zero is free, and 10 is
the most expensive candidate. Preserve the underlying measurement in
`deepswe_avg_cost_usd`. Lower cost improves the automatic-selection score.
`manual_approval_required` is a separate safety gate and does not affect the
score. See
[`MODEL_SELECTION.md`](MODEL_SELECTION.md) for the normalization formula and
source data.

The helper's isolation checks govern every supported engine. You can configure
Codex, Claude, a sufficiently recent Pi CLI, Kimi Code 0.30.0 or newer,
OpenCode, and Cursor Agent as automatic candidates. The adapters give each
reviewer only the frozen prompt bundle. They run from empty workspaces. The
adapters disable repository, filesystem, shell, edit, plugin, MCP, and
project-instruction capabilities.

Inspect the installed harnesses before choosing a profile:

```bash
autoreview --list-harnesses
```

The capability table distinguishes `cli_installed`, `desktop`, and
`automatic_eligible`. A desktop app never substitutes for the CLI command used
by autoreview. Installers are opt-in:

```bash
autoreview --install-harness pi
autoreview --install-harness opencode
autoreview --install-harness cursor
autoreview --engine cursor --model grok-4.5 --install-if-missing
```

`--install-harness` installs and verifies the requested CLI, then exits. The
`--install-if-missing` flag permits installation only for an explicitly selected
engine, reviewer panel, or profile. If scored selection lacks reviewer quorum,
the flag installs the best missing isolation-safe harness. Without the flag,
scored selection never installs software. Pi uses the current
`@earendil-works/pi-coding-agent` package. The installer rejects the deprecated
`@mariozechner/pi-coding-agent` package.

Autoreview does not install Kimi Code. Install it separately, then confirm it
with `autoreview --list-harnesses`.

| harness | canonical installer used |
| --- | --- |
| [Codex CLI](https://help.openai.com/en/articles/11096431) | `npm install -g @openai/codex` |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started) | `npm install -g @anthropic-ai/claude-code` |
| [Pi](https://pi.dev/docs/latest) | `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` |
| [OpenCode](https://opencode.ai/docs/) | `npm install -g opencode-ai` |
| [Cursor Agent](https://docs.cursor.com/en/cli/installation) | Official `https://cursor.com/install` script, downloaded to a bounded temporary regular file before execution |

Explicit model examples:

```bash
autoreview --engine kimi --model kimi-k2 --thinking on
autoreview --engine cursor --model grok-4.5
autoreview --engine cursor --model glm-5.2
autoreview --engine cursor --model kimi-k3
autoreview --engine opencode --model opencode/kimi-k3 --thinking max
autoreview --engine opencode --model opencode/glm-5.2 --thinking max
autoreview --engine opencode --model opencode/grok-4.5 --thinking high
```

Model names are deliberately not rewritten by autoreview. Use
`opencode models <provider>` for OpenCode and the Cursor model catalog for
Cursor, because provider and hosted-catalog identifiers can change.

Fable candidates must set `manual_approval_required = true`. An explicit CLI
selection grants approval only when it names Fable. Valid selections include
`--profile`, `--model`, and an inline model in `--reviewers`. Scored profiles,
config defaults, environment defaults, automatic gates, and unrelated arguments
cannot grant approval. The helper also refuses Fable in fallback chains because
fallback invocation is automatic.

The helper recognizes the legacy
`manual_approval`, `explicit_only`, and `automatic = false` fields in older
config. New config should use `manual_approval_required`.

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
