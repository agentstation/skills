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
`node_modules` and `LICENSE`. An explicitly named path always lints. The
`[files]` table adjusts the list.

## Commands

| Command | What it does |
|---|---|
| `lint <paths>` | Lints files, directories, globs, or `-` for standard input. |
| `glossary init [path]` | Creates an absent glossary with draft candidates. |
| `glossary update --check` | Reports project terms that the glossary omits. |
| `glossary update --write` | Appends those terms to the glossary as draft rows. |
| `glossary check [path]` | Validates glossary structure and approved rows. |

Options:

- `--config <path>`: layer one TOML file over the user and project files.
- `--mode developer|strict`: override the configured mode for one `lint` run.
- `--format text|json`: select readable output or machine output.
- `--glossary <path>`: override the glossary path for one run.

## What the linter checks

Each rule reports at its configured severity:

- Length: `long_sentence` for instructions and descriptive sentences, plus
  `long_paragraph`.
- Word choice: `banned_word`, `marketing_adjective`, `modal_hedge`, and
  `restricted_vocabulary`.
- Verbs: `passive_voice`, `complex_verb`, `ing_main_verb`, `nominalization`,
  and `phrasal_verb`.
- Formulaic style: `formulaic_phrase`, `negative_parallelism`, and
  `assistant_scaffold`.
- Punctuation: `semicolon`, `contraction`, and `em_dash`.
- Terminology: `glossary_term` applies the avoided aliases of approved rows.

The linter protects code, code-like identifiers, block quotations, paired
double quotations, log records, Markdown tables, front matter, URLs, approved
glossary terms, and configured exceptions.

A directory scan also reads supported source files and lints only their
comments and docstrings. Parsers exist for Python, C-like languages, shell,
Ruby, TOML, YAML, and HTML. Pipe extracted prose through standard input when
no parser exists.

## Modes

- `developer`: technical collaboration and developer-facing artifacts. A
  configured warning can pass within the density limit.
- `strict`: procedures, runbooks, safety text, and controlled errors. Every
  warning becomes an error.

## Configuration

The CLI merges four layers. A later layer overrides an earlier layer:

1. Built-in defaults.
2. `~/.config/agentstation/technical-writing.toml`.
3. The nearest `.agents/technical-writing.toml`.
4. Command-line options.

Copy the example to set a user-wide default:

```bash
mkdir -p ~/.config/agentstation
cp ~/.agents/skills/technical-writing/config.example.toml \
  ~/.config/agentstation/technical-writing.toml
```

Copy the same file into a repository to set a project default:

```bash
mkdir -p .agents
cp ~/.agents/skills/technical-writing/config.example.toml \
  .agents/technical-writing.toml
```

[`config.example.toml`](config.example.toml) lists every table with its
default value. Each table owns one part of the system:

| Table | What it customizes |
|---|---|
| `mode` | The default enforcement mode. |
| `[limits]` | Sentence, paragraph, and warning-density limits. |
| `[rules]` | The severity of each rule: `off`, `warning`, or `error`. |
| `[files]` | Directory-scan exclusions and the exceptions that restore a path. |
| `[terms]` | Project banned terms and permitted mechanical matches. |
| `[restricted_vocabulary]` | Extra restricted words and technical exceptions. |
| `[glossary]` | Glossary path, enforcement, and candidate discovery. |

A project configuration that changes the defaults looks like this:

```toml
mode = "developer"

[limits]
instruction_words = 20
descriptive_words = 25
max_warnings_per_100_words = 1.5

[rules]
passive_voice = "error"
phrasal_verb = "off"

[terms]
additional_banned = ["synergy"]
allowed = ["ensure", "ensures"]

[restricted_vocabulary]
additional = ["seamless"]
exceptions = ["delve"]

[files]
exclude = ["docs/vendor-guide.md"]
exceptions = ["CHANGELOG.md"]
```

Record the technical or terminology reason for each relaxed rule. Do not
weaken a factual or terminology check.

Read [`CONFIG.md`](CONFIG.md) for the severity semantics, the built-in
exclusions, the pattern syntax, and the source-comment parsers.

## Project glossary

The project glossary gives one approved term to each concept. The linter reads
it, protects each approved term, and reports an avoided alias as a
`glossary_term` finding. Rows use five columns:

| Term | Definition | Avoid | Status | Evidence |
|---|---|---|---|---|
| retry budget | The maximum retries for one operation | retry limit | draft | `src/retry.ts` |

Only an approved row changes linter behavior. A draft row waits for a person.

```bash
"$TECHNICAL_WRITING" glossary init
"$TECHNICAL_WRITING" glossary update --check
"$TECHNICAL_WRITING" glossary update --write
"$TECHNICAL_WRITING" glossary check
```

The initializer adds draft candidates. A person must define and approve each
real project term. Put reviewed scanner noise in `ignored_candidates`.

The `[glossary]` table controls the file and its candidates:

- `path`: the glossary location, resolved from the project root.
- `required`: makes a missing glossary fail `lint` with status `2`.
- `scan` and `exclude`: the candidate search patterns.
- `candidate_min_occurrences`: removes one-off identifier noise.
- `ignored_candidates`: drops reviewed scanner noise by exact term.
- `require_approved_definitions`: rejects an approved row without a definition.

Read [`references/glossary.md`](references/glossary.md) for the method and the
maintenance cadence.

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
