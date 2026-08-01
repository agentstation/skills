# Plan title

Status: `draft` | Owner: this plan | Created: 2026-01-01
Baseline: main @ 0000000
Proof root: `proof/plan-slug/`
Next action: complete the promotion gate

## Outcome

> One quotable paragraph that states the invariant this plan delivers. A
> reviewer holds the whole plan against it.

## Architecture

Before:

```text
[component-a: owns policy and transport]
```

After:

```text
[component-a] -> [policy seam: owns the contract]
```

## Scope

- Owns: the concrete workstream this plan delivers.
- Does not own: adjacent work, with the owning plan named for each
  exclusion.
- Non-goals: work this plan refuses, so scope cannot drift into it.

## Promotion gate

Promote this plan to `active` only when every item holds:

- Scope and non-goals are complete.
- Every task states verifiable acceptance criteria.
- The baseline commit and the proof root exist.
- The goal block names real documents, paths, and gates.
- The owner approves activation.

## Invariants

1. A numbered condition the implementation cannot trade away.

## Status ledger

| ID | Task | Status | Evidence |
|---|---|---|---|
| AB0 | Baseline: pin the baseline commit, create the proof root, author the verifier red, capture fail-before evidence. No production behavior changes. | `todo` | |
| AB1 | First implementation task. | `todo` | |
| AB9 | Cleanup after the final pull request merges: delete this plan, its proof root, and its index entry. Archive instead only when the repository keeps an archive. | `todo` | |

## Tasks

### AB0 Baseline

- Problem: the plan needs a pinned baseline, a red verifier, and
  fail-before evidence.
- Owning seam and paths: this plan and `proof/plan-slug/`.
- Steps: pin the baseline commit, create the proof root, author the
  verifier red, capture fail-before evidence.
- Acceptance: the verifier reports its failing baseline count with no
  production behavior change.
- Fail-before: the verifier reports red before any implementation task.
- Verification: run the verifier and record its summary line.

### AB1 First implementation task

- Problem: the defect or gap this task closes.
- Owning seam and paths: module and files.
- Steps: numbered actions.
- Acceptance: named tests or measurable state assertions.
- Fail-before: the check that must fail before the change.
- Verification: exact commands.

### AB9 Cleanup

- Problem: a merged plan must not linger as a stale control plane.
- Owning seam and paths: this plan file, its proof root, and the plans
  index.
- Steps: confirm the merge of the final pull request, then delete the
  plan, the proof root, and the index entry.
- Acceptance: the repository holds no reference to this plan, or the
  archive holds the completed plan.
- Fail-before: not applicable, because the ledger row records the merge.
- Verification: search the repository for the plan slug and confirm the
  end state.

## Goal

```text
Execute this plan to completion. This is a whole-plan goal, not a
single-task goal. Read the plan fully, then read: [required documents].
Work in [worktree path] on branch [branch]. Chat history is not progress
state. Resume from the status ledger, the execution log, and git state.
If compaction happens, continue from the plan and git state rather than
restarting. Loop: keep one task in_progress, implement at the owning
seam, capture fail-before evidence, run the verification commands,
commit the work per the commit policy, write the proof file, append the
execution log with the work commit, mark the task terminal with
evidence, commit the plan update the same way, then advance to the next
task. Decide rather than ask. Mark a
wrong or already-satisfied task no-action with a one-line reason. Record
a blocker and continue with the next eligible task. Binding constraints:
[invariants and non-goals]. Commit policy: [commit policy]. Stop only at
a valid stop state from the plans skill. Before you stop, update the
ledger and the log, and record the next action in the status line. The
goal is met when [completion gate].
```

## Execution log

Append rows at the end. This section stays last.

| Date | Item | Action | Evidence |
|---|---|---|---|
| 2026-01-01 | meta | authored | Plan authored. No implementation started by this step. |
