---
name: plans
description: Use this skill to create, promote, execute, resume, or close a durable implementation plan that acts as a control plane with a status ledger, verifiable task criteria, and a goal block for autonomous execution. Use it when work spans several sessions or pull requests, changes architecture across seams, or must survive context compaction. Do not use it for a small change that one session delivers without coordination.
---

# Plans

A plan is one durable file that owns one outcome. The plan file, its status
ledger, and the git worktree hold progress, so any agent resumes from them
without chat history. Compaction erases conversation state. The plan and
the repository do not.

The default plan artifact is a self-contained HTML file whose overview
shows the outcome, the progress, and the before and after architecture.
Markdown is the fallback when the repository requires it.

## Workflow

1. Identify the request: create, promote, execute, resume, or close.
2. Read [`references/structure.md`](references/structure.md) for the
   vocabulary, statuses, sections, ledger rules, and evidence rules.
3. To create or promote, copy
   [`assets/plan-template.html`](assets/plan-template.html), or
   [`assets/plan-template.md`](assets/plan-template.md) when the
   repository requires Markdown, and complete the required sections. Read
   [`references/html-format.md`](references/html-format.md) for the file
   and editing rules.
4. To execute or resume, follow
   [`references/execution.md`](references/execution.md): the goal block,
   the execution loop, the stop states, and closure.
5. When execution reveals an architecture problem, apply
   [`references/architecture.md`](references/architecture.md).
6. Write plan prose with the technical-writing skill in developer mode.
7. Apply [`references/context-budget.md`](references/context-budget.md) when
   creating or revising resume instructions, or when repeated history crowds current work.

## Core rules

- One plan owns one outcome. Name the owner for everything out of scope.
- Give every task verifiable success criteria: named tests, exact
  commands, or a measurable observation.
- Keep one status token per ledger cell, with the proof in the evidence
  cell.
- Prioritize parallelism. Run independent tasks at the same time, each
  `in_progress` with a named owner and its own worktree. A task waits only
  on a real dependency.
- The orchestrator reviews delegated work before merge. It keeps the ledger
  and Current resume state current. It deletes merged local and remote
  branches and worktrees. It coordinates with peer orchestrators and never
  drives their plans.
- When the commit policy permits, record each ledger transition in a plan
  commit right after its work commit.
- Record evidence with exact counts and names. Mark checks that could not
  run `UNVERIFIED` instead of counting them green.
- Keep the plan a thin control plane. Move narrative evidence to the
  proof root. Keep one current resume state, separate from execution history.
- Repair the pockets of complexity that execution reveals at their owning
  seams, and route each repair through the ledger.
- End every plan with a cleanup task that triggers when its final pull
  request merges. Delete the plan by default, or archive it when the
  repository keeps an archive.

## Autonomous execution

A plan runs autonomously when its status is `active` and its goal block is
complete. Drive it to completion through the execution loop,
and stop only at a valid stop state defined in
[`references/execution.md`](references/execution.md).
