# Technical artifacts

## Agent responses

- Answer the technical question before you restate context.
- State the current result before the next action in a progress update.
- Name an unknown, assumption, or inference.
- Keep a short reply short. Do not omit a required condition for brevity.

## Documentation and technical web pages

- Define the audience and task before you draft.
- Introduce each concept before you use it in a procedure.
- Put prerequisites before setup steps.
- Use the project glossary in navigation, headings, body text, and examples.
- Keep marketing claims out of developer documentation.

## READMEs and getting-started guides

- State what the project does with concrete behavior.
- List prerequisites before installation commands.
- Give one tested path before alternatives.
- State the expected result of each verification step.

## API documentation

- Keep endpoint names, fields, types, values, and status codes exact.
- Separate required behavior from optional behavior.
- State limits and defaults only when a source defines them.
- Give an error cause only when the system can identify it.

## Procedures, runbooks, and errors

- Use `strict` mode.
- Put one action in each numbered step.
- Put a condition or warning before its command.
- State what failed, the known cause, and the supported recovery action.
- Keep an unknown cause unknown.

## PRs, issues, and release notes

- State the changed behavior and its boundary.
- Name unchanged behavior when the boundary matters.
- Do not claim performance, compatibility, or safety without measurements.
- Use exact issue numbers, identifiers, versions, and flags.

## Comments and docstrings

- Add prose only when the task or project convention requires it.
- Explain a contract, intent, invariant, or non-obvious constraint.
- Do not narrate visible code.
