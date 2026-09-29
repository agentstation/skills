# Plan context budget

The audience is an agent that must resume unfinished work from durable files.
Keep current state small enough to read in full. Keep detailed evidence
available through exact links.

## Review triggers

Check size at task transitions and before a handoff or stop. Use:

```bash
wc -l -w -c <plan-path>
```

Review the plan when any default trigger applies:

| Surface | Review trigger |
| --- | --- |
| Whole plan source | More than 4,000 words or 32,000 bytes. |
| Current resume state | More than 500 words. |
| Handoff | More than 250 words. |
| Execution log inside the plan | More than 10 entries. |
| Resume procedure | Requires full historical logs or repeated proof-root reads. |

These are maintenance defaults, not model token limits or product acceptance
gates. Count raw HTML too. Do not minify markup or shorten identifiers to
pass the check. Long table rows can hide growth from a line limit.

If required control content exceeds a default, record the reason and the
bounded read path. Do not remove requirements to satisfy a size target.
Split ownership only when the work has distinct outcomes.

## Information ownership

- The plan owns outcome, status, dependencies, invariants, and completion.
- Current resume state owns the next action and current worktree evidence.
- Each task contract owns its complete acceptance and verification procedure.
- Proof files own detailed results and dated observations.
- History owns prior execution entries and superseded decisions.

Give each fact one authoritative location. Link other uses to that location.
Keep active constraints and accepted decisions discoverable from the plan.
Record a decision's reason and re-open condition once. Do not re-open it
without changed evidence or owner direction.

Measure the required resume reading as well as the plan size. Include the
in-progress task contracts and current proof sections that the resume instructions
require. Record their paths, sections, and combined word or byte count after
compaction. Do not count unopened evidence as resume input.

Moving text into one large proof file does not reduce context if every resume
still reads that file. Link exact sections or split them by owning task.
Name the relevant prerequisite decisions too. A section link must not hide a
required invariant or acceptance condition.

## Safe document compaction

1. Finish the current safe operation or record its running process state.
2. Inspect git state and preserve unrelated changes.
3. Record task IDs, statuses, dependencies, invariants, and every completion requirement.
4. Move older log entries and detailed evidence unchanged to the proof root.
5. Keep exact links from each task to its complete contract and proof.
6. Replace Current resume state with verified current facts and the next action.
7. Change the goal and index to use the bounded read path.
8. Compare the protected content before and after the move.
9. Verify links, anchors, ledger statuses, and the plan's existing structural checks.
10. Run the cold-resume check below.
11. Append one short compaction entry with size, preservation, and resume results.

For large moves, compare counts and content hashes of the moved sections.
These checks prove preservation, not product correctness. Use existing tools
or a bounded local check. Do not create another verification framework.

Preserve failed, rejected, and inconclusive evidence. Preserve authorization
boundaries and unresolved work. Keep historical test results attached to their
tested source. Do not change a gate, status, or scope during mechanical
compaction. Record a separate decision when the owner authorizes such a change.

## Cold-resume check

After changing resume instructions, inspect the named read path without relying
on chat history. Confirm that it answers:

- Which task is active, and what exact action comes next?
- Which decisions, dependencies, and authorization limits govern that action?
- Which worktree and source do the test results cover, and which checks remain unverified?
- Which operation remains active, and what safe command reports its state?
- Which acceptance conditions still prevent task and whole-plan completion?

If an answer requires reconstructing history, repair its owning record or link.
Record the result in the existing maintenance entry. This checks resume
readability, not product correctness. It requires no additional reviewer,
new evidence framework, or test run against the product.

## Resume and handoff

Read the compact plan fully. Then read the in-progress task contracts, the relevant
current proof, repository instructions, and affected source. Read history only
for a named decision, failure, or verification question.

Before acting, check current git state and any recorded process. When evidence
disagrees with the resume record, correct that record first. Treat a former
next action in historical evidence as history.

A handoff contains the plan link and only unresolved facts needed to resume.
Update the durable record before handing off. Include only a new discrepancy
or volatile state that the durable record does not yet contain.
Do not paste task histories, tool transcripts, or full file inventories into
the handoff. Do not copy the previous handoff and append another turn.

Use this minimal shape:

```text
Plan: <path>#current-resume-state
In progress: <ID> (<owner>) for each task. Next action: follow the current resume record.
Unrecorded discrepancy or running operation: <exact fact, or none>.
```

Preserve unresolved safety or process details if a write fails before handoff.
Explain any budget exception. Never omit such details merely to shorten a handoff.

Bound tool output as well as document reads. Query filenames or headings
before reading large files. Print result counts and named failures instead of
whole reports. Budget the combined output of parallel calls. Complete every
required instruction-file read, but do not load unrelated references.

This procedure reduces repeated input. It cannot change the host application's
context limit, automatic compaction, or previously recorded chat messages.
