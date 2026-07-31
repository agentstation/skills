# Evaluation rubric

Compare the candidate skill with the previous version or a no-skill baseline.
Hide the candidate label during pairwise review.

## Hard gates

An output fails if it:

- adds or strengthens a fact during an edit without authorization or evidence.
- changes protected technical content.
- violates a glossary term or higher-priority instruction.
- omits a required condition, action, limit, or boundary.
- selects technical-writing rules for a nontechnical task.

## Score

| Dimension | Range | Standard |
|---|---:|---|
| Factual integrity | 0-3 | Preserves each fact and unknown |
| Terminology | 0-3 | Uses exact identifiers and approved glossary terms |
| Instruction quality | 0-3 | Orders conditions and actions correctly |
| Clarity | 0-3 | Uses direct sentences and useful structure |
| Mechanical conformance | 0-2 | Meets the configured deterministic rules |
| Audience fit | 0-2 | Serves a technical reader and selects the correct mode |

A passing output scores at least 13 of 16 and passes each hard gate.

Record evidence for each score. Name each failed invariant. Use deterministic
checks for protected content, glossary aliases, parseability, limits, and
ordering. Use human review for truth, completeness, meaning, and usefulness.

Treat each `protected_literals` value as an exact, case-sensitive substring.
Treat each `forbidden_literals` value as a case-insensitive whole term or
phrase. Letters, numbers, underscores, and hyphens are term characters. Thus,
`repo` matches `the repo` but not `repository`, `mono-repo`, or `repo-sync`.

The linter score cannot replace the hard gates or human review.
