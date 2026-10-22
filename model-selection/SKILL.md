---
name: model-selection
description: Select or validate models and effort levels for delegated work, review, coordination, or focused specialist problems. Use when changing routing, refreshing benchmark evidence, or diagnosing model-policy conflicts. Do not use for ordinary work under an already valid assignment.
compatibility: Python 3.11 or later. Runtime model access depends on the calling host.
metadata:
  policy-version: "2"
---

# Model selection

This skill owns model eligibility and benchmark evidence across projects.
The calling host owns dispatch and its available model catalog.
Global instructions retain the owner's visible model tables and role restrictions.

## Select an assignment

1. Identify the task class, role, complexity, and quality requirements.
2. Read the host's actual model and effort catalog.
3. Validate a proposed assignment with `scripts/model-selection check`.
4. For a comparison, pass host availability to `scripts/model-selection select`.
5. Give the validated assignment to the native dispatch adapter.

The checker does not invoke a model or change the current session.
A successful policy check does not prove host availability.
Read [`references/selection.md`](references/selection.md) for availability input and role evidence.

```bash
export MODEL_SELECTION="${AGENTS_HOME:-$HOME/.agents}/skills/model-selection/scripts/model-selection"
"$MODEL_SELECTION" check \
  --model gpt-6.1-sol --effort high --role worker
"$MODEL_SELECTION" select \
  --task implementation --available-json host-models.json
```

The role policy applies before explicit profiles, ranking, and fallback.
Fable only coordinates work. Do not use Haiku.
Astra requires a narrow, highly complex, focused specialist assignment.
Opus coordination or high-complexity work requires multi-agent Ultracode.
The caller must verify those task conditions before setting the corresponding flags.

## Refresh evidence

Read [`references/refresh.md`](references/refresh.md) before changing the catalog or policy.
Keep source dates, benchmark versions, unrounded measurements, and uncertainty.
Use `scripts/model-selection frontier` to recompute the frontier.
Use `scripts/model-selection table --check PATH` to verify the global instructions.
Do not substitute vendor claims for measured results.

## Integrate a caller

Import `scripts/model_policy.py` from the canonical installed sibling skill.
Call `validate_assignment` for the primary model and every fallback.
Missing policy data stops dispatch with an installation recovery message.
A CLI override cannot bypass a role restriction.
Read [`references/integration.md`](references/integration.md) for the API and migration contract.

Read [`references/benchmark-evidence.md`](references/benchmark-evidence.md) only for a benchmark evidence question.
Run `python3 -m unittest discover -s model-selection/tests -v` from the collection root after a change.
