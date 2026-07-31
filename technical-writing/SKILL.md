---
name: technical-writing
description: Use this skill for developer-facing technical writing and communication. Apply it to responses for technical users, documentation, READMEs, API text, runbooks, PRs, issues, release notes, error messages, technical web pages, comments, and docstrings. Use developer mode by default and strict mode for procedures, safety text, and tightly controlled errors. Do not apply it to marketing, fiction, or other voice-led prose.
---

# Technical writing

Use a controlled writing system instead of a vague request to "write clearly."
The linter verifies mechanical rules. A human or agent must still verify facts,
meaning, terminology, and audience fit.

Protect source content:

- When reproducing text, preserve it exactly.
- When editing or rewriting, change only the requested aspects. Preserve every
  fact, unknown, value, identifier, and behavior.
- When authoring new text, support claims with available evidence. Mark an
  inference or unknown. Never invent precision.

## Workflow

1. Identify the technical audience and artifact.
2. Use `developer` mode unless the artifact needs `strict` mode.
3. Load the nearest `.agents/technical-writing.toml` and its `GLOSSARY.md`.
   Read [`CONFIG.md`](CONFIG.md) when you create or change configuration.
4. If the project has no glossary, read
   [`references/glossary.md`](references/glossary.md) and create a reviewed
   draft before long-lived documentation work.
5. Draft with the rules in [`references/rules.md`](references/rules.md). Read
   [`references/technical-artifacts.md`](references/technical-artifacts.md)
   when the artifact needs specific structure.
6. Set the helper path:

   ```bash
   export TECHNICAL_WRITING="${AGENTS_HOME:-$HOME/.agents}/skills/technical-writing/scripts/technical-writing"
   ```

7. For a file or substantive draft, run:

   ```bash
   "$TECHNICAL_WRITING" lint <path> --format text
   ```

8. Revise until the linter exits with status `0`.
9. Complete the human conformance checks in
   [`references/conformance.md`](references/conformance.md).

For short technical conversation, apply the rules and final check without a
tool call. For durable prose, run the linter until it passes.

## Modes

- `developer`: technical explanations and collaboration, documentation,
  READMEs, API text, PRs, issues, release notes, and technical web pages.
- `strict`: procedures, runbooks, safety text, and tightly controlled error
  messages. Apply every configured limit and treat warnings as failures.

Project configuration can change a mechanical rule when the audience,
repository, locale, or required terminology demands it. Record the reason in
the configuration or glossary. Do not weaken factual or terminology checks.

## Acceptance

A durable artifact or explicit conformance claim passes only when all
conditions hold:

- The linter exits with status `0`.
- Each concept uses its approved glossary term.
- The text preserves facts, uncertainty, identifiers, values, units, versions,
  commands, and code.
- Instructions contain one action and put conditions before commands.
- The text has one topic per paragraph and no empty preamble or conclusion.
- A reviewer confirms that the prose is accurate, complete, and useful.

The linter is not an ASD-STE100 certification tool. It checks the deterministic
subset that this skill defines.
