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

## Prompts, tools, and agent messages

- State the actor, action, object, condition, and expected result when they
  affect behavior.
- For a tool, define its inputs, outputs, state changes, errors, and stopping
  condition.
- For an agent message, separate observed results from inferred status.
- Preserve machine-readable values and required project terms exactly.
- Do not refer to private reasoning or context that the receiving agent cannot
  access.

## PRs, issues, and release notes

- State the changed behavior and its boundary.
- Name unchanged behavior when the boundary matters.
- Do not claim performance, compatibility, or safety without measurements.
- Use exact issue numbers, identifiers, versions, and flags.

## Comments and docstrings

- Add prose only when the task or project convention requires it.
- Explain a contract, intent, invariant, or non-obvious constraint.
- Do not narrate visible code.
- Run the linter on a supported source file or source directory. It extracts
  comments and docstrings before it applies prose rules.
- Do not pass a complete source file through a plain-text prose path.
- Keep code identifiers, commands, directives, and structured examples exact.
