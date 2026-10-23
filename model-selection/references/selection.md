# Assignment selection

A role and a task class describe different constraints.
Roles are `worker`, `reviewer`, `coordinator`, and `specialist`.
Task classes are `mechanical`, `simple`, `implementation`, `design`, and `browser`.
Task defaults set minimum benchmark capability and owner taste requirements.
Selection chooses the cheapest eligible pair that meets those requirements.

Pass the host's observed capabilities as JSON:

```json
{"gpt-6.1-sol": ["medium", "high", "xhigh"], "claude-opus-5-5": ["high"]}
```

```bash
export MODEL_SELECTION="${AGENTS_HOME:-$HOME/.agents}/skills/model-selection/scripts/model-selection"
"$MODEL_SELECTION" select --task simple --available-json host-models.json
"$MODEL_SELECTION" check --model fable --effort high --role coordinator
"$MODEL_SELECTION" check --model astra --effort high \
  --role specialist --complexity high --focused
```

The coordinator must maximize independent parallel work and manage worker completion.
The coordinator remains accountable for delivery, code quality, readability,
maintainability, robustness, deployment, PR acceptance, and merge readiness.
The user's authorization still governs external actions.
A worker or isolated reviewer cannot use Fable.
A specialist brief must define the narrow problem and verifiable acceptance criteria.
An `--ultracode` flag asserts observed multi-agent support, not greater reasoning effort.

An absent availability file produces a policy suggestion only.
Before dispatch, check actual host access and supported flags.
An unavailable pair never causes an automatic downgrade to a prohibited model.
