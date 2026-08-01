# Plan structure

This reference defines the vocabulary, statuses, sections, and evidence rules
for a standard plan. The plan file is the control plane: it holds current
state, routing, and progress for one outcome.

## Vocabulary

| Term | Meaning |
|---|---|
| plan | One durable file that owns one outcome. |
| phase | An ordered group of tasks inside a plan. Phase 0 is the baseline. |
| task | The atomic unit of planned work. One ledger row, normally one pull request. |
| step | One numbered action inside a task body. A step has no ledger row. |
| item | Any ledger row, when the specific noun does not matter. |
| gate | A named condition that must hold before a lifecycle transition. |
| seam | A language-native boundary that owns one domain concept and its contract. |

Use a flat task list for a small plan. Add phases when the plan holds more
than about eight tasks or needs ordered groups. Map legacy nouns to this
vocabulary: a band becomes a phase, and a work row becomes a task. Keep
`lane`, `milestone`, and `checkpoint` out of plan vocabulary.

Three gate kinds cover the lifecycle:

- Promotion gate: conditions to move a plan from `draft` to `proposed` or
  `active`.
- Activation gate: the external trigger that schedules a `deferred` plan.
- Completion gate: the conditions that close the plan.

## Plan statuses

| Status | Meaning |
|---|---|
| `draft` | Records candidate work. Not an execution target. |
| `proposed` | Coherent enough to review. Needs an owner decision to start. |
| `deferred(<trigger>)` | Scoped, and parked until a named trigger. |
| `active` | Ready to execute or resume. |
| `complete` | Every ledger row is terminal and the completion gate holds. |
| `superseded(<successor>)` | Folded into a named successor plan. |
| `abandoned(<reason>)` | Closed without completion for a recorded reason. |

`complete`, `superseded`, and `abandoned` are terminal. Promote a draft only
after it has scope, a ledger, verification obligations, and a goal block.

## Task statuses

| Status | Meaning |
|---|---|
| `todo` | Eligible and not started. |
| `in_progress` | Under active work now. |
| `blocked(<reason>)` | Stopped on a recorded blocker. |
| `deferred(<decision>)` | Parked by an explicit owner decision. |
| `done` | Complete, with evidence in the ledger row. |
| `no-action(<reason>)` | The task was wrong or already satisfied. |
| `rejected(<evidence>)` | A gate or measurement refused the task. |

`done`, `no-action`, and `rejected` are terminal. A measured rejection is a
finished row, not a failure to record.

## Status line

Every plan opens with the status line:

```text
Status: `active` | Owner: this plan | Created: 2026-07-31
Baseline: main @ <sha>
Proof root: proof/<plan-slug>/
Next action: <the exact next step>
```

In a Markdown plan the status line fills the first lines of the file. In
an HTML plan it is the first content in the overview. A cold agent reads
it first. `Next action` is the durable resume pointer. Update it at every
task transition and before every stop.

## Required sections

An `active` plan contains these sections, in this order:

1. Status line.
2. Outcome: one quotable paragraph that states the invariant the plan
   delivers. A reviewer holds the whole plan against it.
3. Progress, in an HTML plan only: the bar and counts that the ledger
   drives.
4. Architecture: before and after diagrams when the plan changes structure.
5. Scope: what the plan owns, what it does not own with the owning plan
   named, and explicit non-goals.
6. Status ledger.
7. Tasks: one block per task, in the task template below.
8. Goal: the paste-ready block defined in
   [`execution.md`](execution.md).
9. Execution log, last, so a log append edits the end of the document
   instead of its middle.

Optional sections slot between Scope and the status ledger. A `draft`
plan needs only the status line, scope, a promotion gate, a draft ledger,
and an execution log.

## Task template

```text
### <ID> <task name>

- Problem: the defect or gap this task closes.
- Owning seam and paths: module and files.
- Steps: numbered actions.
- Acceptance: named tests or measurable state assertions.
- Fail-before: the check that must fail before the change.
- Verification: exact commands.
```

Write acceptance as falsifiable state assertions. Name literal test
functions where they exist. One task is one pull request unless its row
permits a mechanical split.

The final task of every plan is cleanup. Its trigger is the merge of the
plan's final pull request. [`execution.md`](execution.md) defines the
cleanup procedure.

## Status ledger rules

The status ledger is a table with columns `ID | Task | Status | Evidence`.

- The status cell holds one status token and nothing else.
- The evidence cell holds the proof: pull request, commit, date, exact test
  counts, and the proof file path.
- Give every task a stable ID: a plan prefix of two to four letters plus a
  number, with dotted subtasks. Never renumber.
- Keep one row per task and one line per row, so rebases cannot lose rows
  silently.
- Record what execution found that planning missed in the evidence cell.

## Execution log rules

The execution log is an append-only table with columns
`Date | Item | Action | Evidence`. It records dated actions with the
completing commit and test counts. It also records doc-only work such as a
re-scope or a dependency refresh, which produces no code commit. The ledger
answers "where are we". The log answers "what happened".

## Evidence rules

- Record exact counts and named checks. "Tests pass" is not evidence.
- Mark a check that could not run `UNVERIFIED`, with the reason and the
  merge source of truth. An absent verifier is not a pass.
- Capture fail-before evidence before the fix lands.
- Keep rejected and inconclusive runs in the proof root. They prove the
  method.
- For a measurement, split the raw data file from the verdict file.

## Proof root

The proof root is `proof/<plan-slug>/` beside the plan file. Derive the slug
from the plan filename so the mapping stays mechanical. Write one proof file
per task, named by the task ID in lower case. A closeout proof records the
branch, head commit, pull request, verification commands with output, and
the check roster.

## Size rules

Keep the plan a thin control plane and the proof root thick.

- Keep the status line, outcome, progress, and ledger in the first 120
  lines.
- Keep the plan under about 500 lines. Move narrative evidence to the proof
  root.
- Split the plan when a phase grows into its own outcome. An oversized plan
  cannot be re-read at resume, which defeats the ledger.

## Optional sections

Add these sections when the plan needs them:

- Invariants: a numbered list of conditions the implementation cannot trade
  away. Tasks may be re-scoped. Invariants may not.
- Findings ledger: `ID | Classification | Evidence | Owning task`. The
  classification carries severity and confidence. Every finding routes to an
  owning task or a follow-up ticket.
- Decisions: dated entries with stable IDs, evidence, consequence, and a
  re-open condition.
- Rejected designs: each rejection with the reason and a re-open condition,
  so the next agent does not re-litigate it.
- Patterns to preserve: an anti-regression list of existing behavior the
  plan must not break.
- Test matrix: `Dimension | Required cases` for broad behavioral coverage.
- Verifier contract: a named script with a fixed condition count and the
  output shape `Summary: N passed, M failed`. Author it red in phase 0,
  tabulate the expected count per phase, and state the terminal count that
  defines done.
- Coordination: precedence against sibling plans and specs. Name which
  document wins on disagreement.

## Campaign and single session modes

A campaign plan spans several pull requests. It requires phase 0: pin the
baseline commit, create the proof root, author the verifier red, capture
fail-before evidence, and change no production behavior. Commit the ledger
at every transition.

A single session plan delivers one pull request. It may use a flat task
list and update the ledger at completion. It keeps the same sections and
evidence rules.

## The plans index

When the repository keeps a plans directory, maintain an index README that
routes work. The index answers two questions: which plan owns the work, and
in what order the plans run. Keep exactly one owner plan per topic. Keep
history out of the index so it stays readable as the current control plane.
Update the index in the same commit as any plan lifecycle change.
