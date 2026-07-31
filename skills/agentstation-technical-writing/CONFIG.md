# Configuration

The CLI reads TOML configuration in this order:

1. Built-in defaults.
2. `~/.config/agentstation/technical-writing.toml`.
3. The nearest `.agents/technical-writing.toml`.
4. Command-line options.

Later layers override earlier layers. An explicit `--config` path replaces
automatic project discovery. It still inherits the global configuration.
The invocation directory remains the project root for relative glossary and
scan paths.

Copy `config.example.toml` to create a project configuration:

```bash
mkdir -p .agents
cp ~/.agents/skills/agentstation-technical-writing/config.example.toml \
  .agents/technical-writing.toml
```

## Modes

`developer` is the default for technical collaboration, documentation, and
developer-facing web content. Configured warnings can pass when their density
does not exceed `max_warnings_per_100_words`.

The density calculation uses a 100-word minimum. One warning in a short reply
therefore counts as one warning per 100 words.

`strict` promotes each warning to an error and sets the warning threshold to
zero. Use it for procedures, runbooks, safety text, and controlled errors.

## Rules

Each rule has one severity:

- `off`: do not report the rule.
- `warning`: report the rule and include it in warning density.
- `error`: fail the lint command.

The linter exits with status `0` when it finds no error and the warning density
is within the configured limit. It exits with status `1` for a conformance
failure. It exits with status `2` for invalid configuration or input.

## Terms

`additional_banned` adds project-specific terms. `allowed` suppresses a
mechanical term match when the term is technically required.

Use the glossary for concept aliases. The linter applies avoided aliases from
approved glossary rows. It does not apply aliases from draft rows.

## Glossary discovery

The `[glossary].path` value is relative to the project configuration
directory's parent. The default `.agents/technical-writing.toml` therefore
resolves `GLOSSARY.md` from the repository root.

The configured path must stay inside the project root. Use the explicit
`--glossary` option when you intentionally need another path.

The `[glossary]` table controls candidate discovery:

- `candidate_min_occurrences` removes one-off identifier noise.
- `ignored_candidates` excludes reviewed scanner noise by exact term.
- `scan` lists project-relative glob patterns.
- `exclude` removes generated, vendored, or private paths.
- `require_approved_definitions` makes glossary validation reject an approved
  row without a definition.

Generated candidates always start as `draft`. A person must approve them.
Add a false positive to `ignored_candidates` instead of keeping it as a
glossary term.
