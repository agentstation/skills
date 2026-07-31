# Project glossary

Use `GLOSSARY.md` for project terminology. Keep only the instruction to use the
glossary in `AGENTS.md`.

This separation gives the glossary a stable, reviewable format. The linter can
read it, and people can update it without changing agent instructions.

## AGENTS.md instruction

Add a short project instruction:

```markdown
## Technical writing

Use `GLOSSARY.md` for developer-facing prose. Run the installed
`technical-writing` linter on durable technical text.
```

## Format

The glossary uses this table:

| Term | Definition | Avoid | Status | Evidence |
|---|---|---|---|---|
| repository | The version-controlled project tree | repo | approved | `README.md` |
| retry budget | The maximum retries for one operation | retry limit | draft | `src/retry.ts` |

Use these status values:

- `approved`: the linter enforces the preferred term and avoided aliases.
- `draft`: a person must review the term, definition, and aliases.
- `deprecated`: the term must not appear in new prose.
- `ignored`: the row documents a scanner exception without enforcing the term.

Separate multiple aliases or evidence paths with a comma.

## Create and update

Set the installed helper path:

```bash
export TECHNICAL_WRITING="${AGENTS_HOME:-$HOME/.agents}/skills/technical-writing/scripts/technical-writing"
```

Create a glossary when none exists:

```bash
"$TECHNICAL_WRITING" glossary init
```

The command scans configured project files. It adds candidate terms as `draft`.
It never treats generated definitions as approved.

Check for new codebase terms without changing the glossary:

```bash
"$TECHNICAL_WRITING" glossary update --check
```

Append new draft candidates:

```bash
"$TECHNICAL_WRITING" glossary update --write
```

Review each draft. Add an exact definition and avoided aliases. Change the
status to `approved` only after project review.

For scanner noise, remove the draft and add its exact term to the
`ignored_candidates` configuration. Use `ignored` only when the glossary
should record why the scanner exception exists.

Validate the table and alias mappings:

```bash
"$TECHNICAL_WRITING" glossary check
```

The update command preserves existing rows and never removes a term. Deprecate
an obsolete term explicitly.

## Maintenance

Run the update check when a change adds or renames:

- a public type, command, flag, API field, or protocol term.
- a product, component, service, or package.
- a domain concept in documentation or code.

Use this CI sequence for repositories that enforce terminology:

```bash
"$TECHNICAL_WRITING" glossary check
"$TECHNICAL_WRITING" glossary update --check
"$TECHNICAL_WRITING" lint README.md docs/
```
