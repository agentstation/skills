# Technical writing

The skill applies a controlled writing system to developer-facing prose
instead of a vague request to write clearly. A linter verifies the mechanical
rules. A person or agent still verifies facts, meaning, terminology, and
audience fit.

[`SKILL.md`](SKILL.md) holds the agent-facing contract. This page covers
install, setup, and the documents that own each rule.

## Install

```bash
npx skills add agentstation/skills --skill technical-writing -g \
  -a codex -a claude-code -a goose -y
```

The linter needs Python 3.11 or later. Set its path after installation:

```bash
export TECHNICAL_WRITING="${AGENTS_HOME:-$HOME/.agents}/skills/technical-writing/scripts/technical-writing"
```

## Quickstart

```bash
"$TECHNICAL_WRITING" lint README.md --format text
"$TECHNICAL_WRITING" lint . --format text
echo "The parser reads the file." | "$TECHNICAL_WRITING" lint -
```

The linter exits with status `0` when the text conforms, `1` for a conformance
failure, and `2` for invalid configuration or input.

A directory scan skips vendored, generated, and boilerplate paths, such as
`node_modules` and `LICENSE`. An explicitly named path always lints.
[`CONFIG.md`](CONFIG.md) lists the built-in exclusions and the `[files]` table
that adjusts them.

## Modes

- `developer`: technical collaboration and developer-facing artifacts. A
  configured warning can pass within the density limit.
- `strict`: procedures, runbooks, safety text, and controlled errors. Every
  warning becomes an error.

## Configuration

Copy the example to set a user-wide default:

```bash
mkdir -p ~/.config/agentstation
cp ~/.agents/skills/technical-writing/config.example.toml \
  ~/.config/agentstation/technical-writing.toml
```

A repository overrides that file with `.agents/technical-writing.toml`.
Command-line options override both.

## Project glossary

Create and review the project glossary:

```bash
"$TECHNICAL_WRITING" glossary init
"$TECHNICAL_WRITING" glossary check
"$TECHNICAL_WRITING" glossary update --check
```

The initializer adds draft candidates. A person must define and approve each
real project term. Put reviewed scanner noise in `ignored_candidates`.

## Documents

- [`SKILL.md`](SKILL.md): the workflow, the modes, and acceptance.
- [`CONFIG.md`](CONFIG.md): configuration layers, rule severity, exclusions,
  and glossary discovery.
- [`references/rules.md`](references/rules.md): the writing rules.
- [`references/rewrite.md`](references/rewrite.md): the edit and preservation
  boundary.
- [`references/technical-artifacts.md`](references/technical-artifacts.md):
  structure for each artifact type.
- [`references/formulaic-style.md`](references/formulaic-style.md): stock
  prose and restricted vocabulary.
- [`references/asd-ste100.md`](references/asd-ste100.md): standard scope and
  conformance claims.
- [`references/conformance.md`](references/conformance.md): the human checks.
- [`references/glossary.md`](references/glossary.md): the glossary method.
- [`evals/README.md`](evals/README.md): the evaluation set and its cadence.
- [`UPSTREAM.md`](UPSTREAM.md): upstream sources and licenses.

The linter is not an ASD-STE100 certification tool. It checks the
deterministic subset that this skill defines.

## Migration

To migrate from the earlier name, install `technical-writing`, update the
persistent instruction, verify a fresh session, and then remove the old skill:

```bash
npx skills remove writing-clearly -g -y
```

## Maintenance

Run from the repository root:

```bash
python3 -m pytest technical-writing/tests/
./scripts/validate-skills
```
