---
name: technical-writing
description: Use this skill before you write or edit developer-facing prose. Artifacts include a response, README, docstring, comment, error message, PR, issue, release notes, runbook, API text, prompt, tool description, technical web page, and agent message. Use it when a request asks to write, rewrite, tighten, shorten, or proofread technical text. Use it when a draft reads like generated filler or AI slop. Do not use it for marketing, fiction, or other voice-led prose.
---

# Technical writing

Use a controlled writing system instead of a vague request to "write clearly."
The linter verifies mechanical rules. A human or agent must still verify facts,
meaning, terminology, and audience fit.

Protect source content. Reproduce text exactly. During an edit, preserve every
fact, unknown, value, identifier, and behavior. Keep conforming text unchanged
unless the user requests another change. Support new claims with evidence and
mark each inference or unknown.

Start with the answer. Use direct claims instead of assistant scaffolds, stock
phrases, restricted vocabulary, invented contrasts, or decorative conclusions.
Report each configured occurrence.

Write dead prose. Dead prose carries the facts and no voice. It has no rhythm,
emphasis, or persuasion. Each sentence states a fact, an instruction, or a
condition. Measure a draft by what the reader can verify, not by how the text
sounds.

## Workflow

1. Identify the audience, artifact, and mode.
2. Load the nearest `.agents/technical-writing.toml` and its `GLOSSARY.md`.
   Read [`CONFIG.md`](CONFIG.md) before a configuration change.
3. For long-lived text without a glossary, read
   [`references/glossary.md`](references/glossary.md).
4. For a rewrite or edit, read
   [`references/rewrite.md`](references/rewrite.md) before changing the source.
5. Draft with [`references/rules.md`](references/rules.md). Read
   [`references/technical-artifacts.md`](references/technical-artifacts.md)
   when the artifact needs specific structure.
6. Read [`references/formulaic-style.md`](references/formulaic-style.md) when
   revising stock prose or changing a formulaic-style rule.
7. Read [`references/asd-ste100.md`](references/asd-ste100.md) before changing
   this skill's rules or making an ASD-STE100 conformance claim.
8. Set the helper path:

   ```bash
   export TECHNICAL_WRITING="${AGENTS_HOME:-$HOME/.agents}/skills/technical-writing/scripts/technical-writing"
   ```

9. For a file or substantive draft, run:

   ```bash
   "$TECHNICAL_WRITING" lint <path> --format text
   ```

10. Revise until the linter exits with status `0`.
11. Complete the human checks in
   [`references/conformance.md`](references/conformance.md).

For short technical conversation, apply the rules and final check without a
tool call. For durable prose, run the linter until it passes.

## Modes

- `developer`: technical collaboration and developer-facing artifacts.
- `strict`: procedures, runbooks, safety text, and tightly controlled error
  messages. Apply every configured limit and treat warnings as failures.

Project configuration can change a mechanical rule. Record the technical or
terminology reason. Do not weaken factual or terminology checks.

## Acceptance

A durable artifact or conformance claim passes only when:

- The linter exits with status `0`.
- The text preserves protected content and approved terms.
- A rewrite preserves precision or states why a rule cannot apply.
- A reviewer completes the conformance checks.

The linter is not an ASD-STE100 certification tool. It checks the deterministic
subset that this skill defines.
