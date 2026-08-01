# Plans

A plan is one durable file that owns one outcome. The plan file, its status
ledger, and the git worktree hold the progress, so any agent resumes from them
without chat history. Compaction erases conversation state. The plan and the
repository do not.

The default artifact is a self-contained HTML file. Its overview shows the
outcome, the progress, and the before and after architecture. Markdown is the
fallback when the repository requires it.

[`SKILL.md`](SKILL.md) holds the agent-facing contract. This page covers
install, the lifecycle a person drives, and the documents that own each rule.

## Install

```bash
npx skills add agentstation/skills --skill plans -g -a codex -a claude-code -y
```

## Quickstart

Ask the agent for a plan when work spans several sessions or pull requests,
changes architecture across seams, or must survive context compaction. The
agent copies a template and completes the required sections:

- [`assets/plan-template.html`](assets/plan-template.html): the default
  artifact.
- [`assets/plan-template.md`](assets/plan-template.md): the Markdown fallback.

A plan with status `active` and a complete goal block runs without further
prompting. Paste the goal block to start or resume execution. The agent keeps
one task `in_progress`, verifies each task, records the evidence, and stops
only at a valid stop state.

## How a plan works

- The status ledger holds one row per task, with one status token per cell and
  the proof beside it.
- Each task states verifiable success criteria: named tests, exact commands,
  or a measurable observation.
- The execution log records dated actions, so a new session resumes from the
  ledger, the log, and git state.
- Evidence records exact counts and names. A check that could not run is
  `UNVERIFIED` instead of green.
- Execution repairs the pockets of complexity it reveals at their owning
  seams, and routes each repair through the ledger.
- The last task deletes the plan when its final pull request merges. A
  repository that keeps an archive can archive the plan instead.

## Documents

- [`SKILL.md`](SKILL.md): the workflow, the core rules, and autonomous
  execution.
- [`references/structure.md`](references/structure.md): vocabulary, statuses,
  required sections, ledger rules, and evidence rules.
- [`references/execution.md`](references/execution.md): the goal block, the
  execution loop, the commit convention, the stop states, and closure.
- [`references/architecture.md`](references/architecture.md): seam quality,
  complexity repair, and diagrams.
- [`references/html-format.md`](references/html-format.md): the file and
  editing rules for the HTML artifact.

## Maintenance

Run from the repository root:

```bash
./scripts/validate-skills
```
