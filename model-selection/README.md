# Model selection

This skill selects and validates model assignments without invoking a provider.
Its shared Python contract serves autoreview and the native delegation workflow.

## Install

Install the dependency before callers that use it:

```bash
npx skills add agentstation/skills --skill model-selection -g -a codex -a claude-code -y
```

The checker requires Python 3.11 or later.
It uses the dated catalog in `data/catalog.json` and role policy in `data/policy.json`.
It makes no network requests when it selects a model.

```bash
export MODEL_SELECTION="${AGENTS_HOME:-$HOME/.agents}/skills/model-selection/scripts/model-selection"
"$MODEL_SELECTION" check --model gpt-6.1-sol --effort high --role worker
"$MODEL_SELECTION" frontier
"$MODEL_SELECTION" table --check ~/.agents/AGENTS.md
```

The catalog uses AA identifiers for comparison and runtime identifiers for dispatch.
For example, `gpt-6-1-sol` maps to `gpt-6.1-sol`.

## Version 2 policy

Config schema versions and policy versions are separate contracts.
Policy version 2 reserves Fable for coordination and rejects Haiku.
It restricts Astra to narrow, highly complex, focused specialist work.
It requires multi-agent Ultracode for Opus coordination or high-complexity work.
These restrictions also govern explicit profiles and fallback.

The autoreview `value` profile now selects Sol high.
Fable review profiles stop with a role-policy error.
Existing version 1 autoreview config remains readable.
Reserved or dominated candidates cannot regain eligibility through that config.
External review adapters require a concrete model identity.
Adapters without an effort control may omit effort for a concrete external model.

## Claude agent profiles

`assets/claude/` holds scoped explorer, implementer, and designer definitions.
They use Opus high because Claude Agent definitions cannot select native Codex models.
Use native Codex for the preferred Sol exploration route when the host supports it.
The explorer is a read-only fallback when native Codex exploration is unavailable.

Install reviewed definitions in `~/.claude/agents/` after comparing existing files.
The skill installer copies these assets into the skill, not the agent-definition directory.
Global role restrictions still govern each profile.

## Verification

Run from the collection root:

```bash
python3 -m unittest discover -s model-selection/tests -v
./scripts/validate-skills
```

The trigger fixtures in `evals/` are examples, not measured trigger accuracy.
