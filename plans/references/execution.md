# Plan execution

This reference defines the goal block, the execution loop, recovery, stop
states, and closure. The premise for all of it: chat history is not
progress state. Compaction erases conversation context. The plan file, the
status ledger, the execution log, and the git worktree are the durable
state. Resume from them rather than restarting.

## The goal block

The goal block is a paste-ready prompt inside the plan. It lets a cold
agent start or resume the plan from the file alone. The in-plan copy is
authoritative. Keep any companion prompt file in sync with it.

A plan runs autonomously when its status is `active` and its goal block is
complete. Template:

```text
Execute <plan path> to completion. This is a whole-plan goal, not a
single-task goal. Read the plan fully, then read: <required documents>.
Work in <worktree path> on branch <branch>. Chat history is not progress
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
<invariants and non-goals>. Commit policy: <commit policy>. Stop only at
a valid stop state from the plans skill. Before you stop, update the
ledger and the log, and record the next action in the status line. The
goal is met when <completion gate>.
```

Fill every placeholder. Name the documents to read, the worktree, the
branch, and the completion gate exactly.

## Execution loop

1. Read the status line, the ledger, and the tail of the execution log.
2. Confirm the worktree and branch from the goal block.
3. Inspect `git status`. Attribute each dirty file to the `in_progress`
   task or to prior user work that you must preserve. Stop on dirty files
   you cannot attribute.
4. Resume the `in_progress` task first. Otherwise set the first eligible
   `todo` task to `in_progress`.
5. Read the task's files before you edit. Implement at the owning seam.
6. Capture fail-before evidence, then run the task's verification
   commands.
7. Commit the work per the commit policy in the goal block.
8. Write the task's proof file. Append an execution log entry with the
   work commit and the test counts.
9. Set the task terminal with evidence in the ledger row. Commit the
   plan update per the commit convention.
10. Task completion is a checkpoint, not the goal. Continue with the
    next task until the plan reaches a valid stop state.

When a verification fails, capture the exact failure in the proof file.
Reduce it to a focused command, and fix the root cause at the owning seam.
Rerun the focused check, the task verification, and the verifier before
you continue.

## Commit convention

Record each ledger transition as its own plan commit, right after the
work commit it records. The subject encodes the transition and the next
active task:

```text
plan: <ID> done (PR #N); <NEXT> in_progress
```

A separate plan commit can cite the work commit and pull request it
records. It also makes `git log` a readable execution timeline and a
resume marker that survives any context loss.

Both commits follow the goal block's commit policy. When the policy
withholds commits, keep the plan edits in the worktree and cite the
verification counts as evidence.

## Discoveries and scope

- Record each discovery in the findings ledger with a classification and
  evidence. Route an in-scope discovery to a new task at the owning seam.
  Route an out-of-scope discovery to a follow-up ticket with a named
  owner.
- Apply the scope tripwire: when implementation reveals about twice the
  planned scope, stop and re-scope in the ledger.
- Record each design refusal in the rejected designs section with a
  re-open condition.

## Valid stop states

Stop only when one of these holds:

1. Every ledger row except cleanup is terminal, and the completion gate
   holds. The cleanup row waits as `todo` on the merge. The plan stays
   `active` until cleanup runs.
2. A real blocker needs owner input. Record the exact command and error
   evidence in the ledger row.
3. The owner interrupts.
4. Continuing requires a re-scope or a plan split first.

Before you stop: update the ledger, append the log, leave at most one task
`in_progress`, and record the exact next action in the status line.

## Verification gates

Run review gates only where the plan's acceptance criteria name them. A
pre-PR review gate, such as `autoreview`, runs after final checks per the
repository's own rules. Record each review verdict in the evidence cell.

## Closure and cleanup

The final ledger task is cleanup, and its trigger is the merge of the
plan's final pull request. A later session runs the cleanup task after
the merge, not an automated hook. When the merge lands:

- Default: delete the plan file, its proof root, and its index entry.
- Archive alternative: when the repository keeps an archive, move the plan
  into it. Flip the status line to `complete` with the date and the pull
  request range. Name the successor owner for any residual tickets.
  Replace the index entry with a one-paragraph retrospective that points
  at the archived plan. Keep the proof root.

Archive a plan as `complete` only when every ledger row is terminal.
Otherwise archive it as `superseded(<successor>)` or `abandoned(<reason>)`
so the archive stays honest. If the session ends before the merge, leave
the cleanup task `todo` with the merge named as its trigger, so any later
session can finish it.
