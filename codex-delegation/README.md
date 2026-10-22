# Codex delegation

This Agent Skill prepares scoped Codex assignments and keeps verification in
the parent session. It covers the native Claude Code plugin, job results, and
the direct companion fallback.

## Requirements

- A host with a supported Codex delegation interface.
- The `model-selection` skill from `agentstation/skills`.
- For Claude Code, the `openai/codex-plugin-cc` plugin and authenticated Codex.
- Codex CLI 0.159.0 or later for the delegated workflow.
- Node.js 18.18 or later for the Claude Code plugin.
- Python 3.10 or later to run the static contract tests.

Use the [upstream plugin setup](https://github.com/openai/codex-plugin-cc#install)
to install the plugin. Run `/codex:setup` to check its local requirements and
readiness. This skill does not install a runtime or change model defaults.

## Install

Install both skills from the canonical repository:

```bash
npx skills add agentstation/skills --skill model-selection -g -a codex -a claude-code -y
npx skills add agentstation/skills --skill codex-delegation -g -a codex -a claude-code -y
```

The CLI installs canonical copies under `~/.agents/skills` and creates harness
links. Installation makes the skills available. It does not switch the current
model or authorize an external write.

## Use

Ask the agent to delegate a scoped investigation or implementation task to Codex.
Specify the allowed changes and required evidence. For an existing job, include
its identifier and the requested status, result, continuation, or cancellation.

The agent checks model policy and host support before dispatch. It uses native
model and effort parameters. The parent session verifies changes and runs any
required structured autoreview before publication.

Browser jobs inherit the owner's existing permissions. They do not need a
per-task site list. Read [the browser procedure](references/native-plugin.md#browser-tasks)
for global origin access and runtime failures.

Read [SKILL.md](SKILL.md) for the workflow. Read
[UPSTREAM.md](UPSTREAM.md) for provenance.

## Check the skill

Run these commands from the repository root:

```bash
python3 -m unittest discover -s codex-delegation/tests -v
./scripts/validate-skills
"${AGENTS_HOME:-$HOME/.agents}/skills/technical-writing/scripts/technical-writing" lint codex-delegation --format text
```

The tests check reference links, command transport constraints, and eval fixture structure. The validator checks Agent Skills frontmatter. The linter
checks durable prose. Each command must exit with status `0`.

The [trigger cases](evals/evals.json) contain positive and negative examples for
future host evaluation. Static checks validate their structure and coverage.
They do not measure model trigger accuracy. These automated checks do not start
Codex jobs or make paid model calls.

For a live browser check, explicitly delegate a read-only task to the selected
Codex model. Ask it to open two public sites outside `[origins].allowed` with
its browser tools. Require URLs, page titles, and visible headings. Check that
the browser configuration stays unchanged. This check starts a real model job.
It must report missing browser tools or denied access without substituting HTTP
requests or web search.
