---
name: codex-delegation
description: Delegate a scoped task to Codex, prepare a Codex handoff, or manage an existing Codex plugin job. Use for explicit Codex delegation, rescue, delegated implementation or investigation, and Codex job status, results, or cancellation. Do not use for ordinary local work, generic model advice, Codex product questions, or structured autoreview.
compatibility: Requires the model-selection skill and a host with a supported Codex delegation interface. Claude Code uses openai/codex-plugin-cc.
---

# Codex delegation

Keep task ownership in the parent session. Delegate only work that the user or
active workflow authorizes. Preserve the distinction between investigation and
implementation.

## Prepare the assignment

1. Read the repository instructions and inspect the worktree status.
2. Define the task, allowed files, public behavior, acceptance evidence, and
   stopping condition.
3. Select the model and effort with the installed `model-selection` skill.
4. Run its assignment check before dispatch:

   ```bash
   "${AGENTS_HOME:-$HOME/.agents}/skills/model-selection/scripts/model-selection" check --model gpt-6.1-sol --effort high --role worker
   ```

5. Check the selected host's current model catalog and supported effort values.
6. Pass the accepted model and effort through the host's native parameters.

The assignment check validates policy. It does not prove host availability or
change the active session model. If the host cannot express the accepted pair,
select another eligible pair or report the limitation. Do not silently change
the model or effort.

Use the checker for worker, reviewer, coordinator, and specialist assignments.
It rejects Haiku and Fable workers or reviewers. Astra requires a focused,
narrow, highly complex specialist task. Opus coordination or highly complex
work requires multi-agent Ultracode. Read the installed `model-selection` skill
for its current rules and exception flags.

## Dispatch

For Claude Code, read [the native plugin procedure](references/native-plugin.md)
before the first dispatch. Use `openai/codex-plugin-cc` through
`codex:codex-rescue` or its slash commands. Do not write a custom shell wrapper
or launcher.

For another host, inspect its exposed tools and model parameters before dispatch.
Do not invent plugin commands, model switching, or message channels for that host.

If the native plugin cannot express the task, read
[the companion constraints](references/companion.md) before direct companion use.
If an existing local stop wrapper applies, read
[the conditional stop-hook note](references/local-stop-hook.md).

For browser work, use the owner's existing permissions for every site the task
requires. Read [the browser procedure](references/native-plugin.md#browser-tasks).

Give each worker one concept or independent task. Include repository paths,
constraints, checks, and the required result. For long prompts, save the task
in a file and tell Codex to read that file first.

Require the worker to report changed files, check commands, results, and unknowns.
Require a manual repository-grounded audit at the end. A Codex job never runs
the structured `autoreview` helper or nested reviewers.

## Manage and verify

Use the native completion result for foreground work. Do not poll a foreground
job. For an explicit background job, use the host's status and
result interfaces when needed. Do not create a liaison subagent to watch it.

Never infer job state from a timeout. File modification times can show worktree
activity. A command log can stay stale while work lands. Neither proves that a
job finished. The plugin has no mid-turn inbox for a liaison to query.

The parent session independently verifies the diff and required checks before
delivery. It owns commits, salvaged work, structured autoreview, and publication.
Do not ask a delegated worker to commit early. Run required structured
autoreview in the parent session before a push or pull request.

Keep pushes, pull requests, deployments, and merges within the user's authority.
Report the verified result and remaining uncertainty to the user.
