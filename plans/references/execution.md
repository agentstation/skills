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
single-task goal. Read the compact plan fully, then the in-progress task
contracts and relevant current proof. Required reference owners:
<documents by scope>. Work in <worktree path> on branch <branch>. Chat history
is not progress state. Resume from Current resume state, the ledger, and
verified git state.
Read history only for a named evidence question.
If compaction happens, continue from the plan and git state rather than
restarting. Loop: run independent tasks in parallel. Mark each running task
in_progress with its named owner and its own worktree and branch. A task
starts only when its dependencies are terminal. For each task, implement at
the owning seam, capture fail-before evidence, run the verification commands,
commit the work per the commit policy, write the proof file, append the
execution log with the work commit, mark the task terminal with
evidence, commit the plan update the same way, then start the next eligible
task. Decide rather than ask. Mark a
wrong or already-satisfied task no-action with a one-line reason. Record
a blocker and continue with the next eligible task. Binding constraints:
<invariants and non-goals>. Commit policy: <commit policy>. Stop only at
a valid stop state from the plans skill. Before you stop, update the
ledger and the log, and replace Current resume state. The status line links
to its exact next action. The
goal is met when <completion gate>.
```

Fill every placeholder. Name the documents to read, the worktree, the
branch, and the completion gate exactly.

## Execution loop

1. Read the compact plan, including Current resume state and the ledger.
2. Confirm the worktree and branch from the goal block.
3. Inspect `git status`. Attribute each dirty file to an `in_progress`
   task or to prior user work that you must preserve. Stop on dirty files
   you cannot attribute.
4. Resume every `in_progress` task first. Then start every eligible `todo`
   task, per [Parallel execution](#parallel-execution).
5. Read the task's files before you edit. Implement at the owning seam.
   Load the task contract and relevant proof, not the whole history.
6. Capture fail-before evidence, then run the task's verification
   commands.
7. Commit the work per the commit convention.
8. Write the task's proof file. Append a short execution entry with a proof
   link, work commit, and test counts. Update Current resume state.
9. Set the task terminal with evidence in the ledger row. Commit the
   plan update per the commit convention.
10. Task completion is a checkpoint, not the goal. Continue with the
    next task until the plan reaches a valid stop state.

When a verification fails, capture the exact failure in the proof file.
Reduce it to a focused command, and fix the root cause at the owning seam.
Rerun the focused check, the task verification, and the verifier before
you continue.

## Parallel execution

Prioritize parallelism. Start every eligible task at once.

- A `todo` task is eligible when each dependency that its contract names is
  terminal. Tasks that change the same files or the same shared state are
  dependent. Run them in sequence.
- Give each running task a named owner (an agent or a session) and its own
  worktree and branch. Record both in its evidence cell. Current resume
  state lists every `in_progress` task with its owner.
- The orchestrator is the session that drives the plan. It reviews
  delegated work before merge. It keeps the ledger and Current resume state
  current. It deletes the local and remote branches and worktrees of merged
  work.
- A peer orchestrator owns each other plan. Coordinate with it. Never drive
  its plan.

## Commit convention

The goal block's commit policy governs every commit this skill names.
When the policy withholds commits, keep the work and the plan edits in
the worktree, and cite the verification counts as evidence.

Under a policy that permits commits, record each ledger transition as its
own plan commit, right after the work commit it records. The subject
encodes the transition and the tasks that it starts:

```text
plan: <ID> done (PR #N); <NEXT IDs> in_progress
```

A separate plan commit can cite the work commit and pull request it
records. It also makes `git log` a readable execution timeline and a
resume marker that survives any context loss.

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

Before you stop: update the ledger, append the log, leave `in_progress` only
on tasks that a named owner still runs, and replace Current resume state.
Check the [context budget](context-budget.md) before a handoff or stop.

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
