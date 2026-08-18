# Configuration

The CLI reads TOML configuration in this order:

1. Built-in defaults.
2. `~/.config/agentstation/technical-writing.toml`.
3. The nearest `.agents/technical-writing.toml`.
4. Command-line options.

Later layers override earlier layers. An explicit `--config` path replaces
automatic project discovery. It still inherits the global configuration.
The invocation directory remains the project root for relative glossary and
scan paths. When the directory is inside a Git worktree, the worktree root
takes precedence.

Copy `config.example.toml` to create a project configuration:

```bash
mkdir -p .agents
cp ~/.agents/skills/technical-writing/config.example.toml \
  .agents/technical-writing.toml
```

## Modes

`developer` is the default for technical collaboration, documentation, and
developer-facing web content. Configured warnings can pass when their density
does not exceed `max_warnings_per_100_words`.

The modes control enforcement severity.

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
of each document is within the configured limit. One failing document makes a
multi-file invocation fail. The linter exits with status `1` for a conformance
failure. It exits with status `2` for invalid configuration or input.

## Terms

`additional_banned` adds project-specific terms. `allowed` suppresses an exact,
case-insensitive mechanical phrase match. List each required inflection. For
example, allowing `ensure` does not also allow `ensures` or `ensuring`.

Use the glossary for concept aliases. The linter applies avoided aliases from
approved glossary rows. It does not apply aliases from draft rows.

## Formulaic style

The formulaic-style rules enforce direct and specific technical prose.

- `formulaic_phrase` reports selected stock phrases.
- `negative_parallelism` reports selected rhetorical contrast forms.
- `assistant_scaffold` reports canned assistant preambles and closings.
- `restricted_vocabulary` reports each restricted word.

Configure project vocabulary with `[restricted_vocabulary]`:

- `additional` adds exact project-specific words or phrases.
- `exceptions` permits an exact restricted form for a technical reason.

`[terms].allowed` suppresses an exact mechanical match across rule groups. An
approved glossary term is also protected. List each permitted inflection.

Term protection suppresses a finding on the approved term itself. A larger
formulaic phrase or rhetorical pattern that contains the term can still
produce a warning.

The linter protects code, code-like identifiers, block quotations, paired
double quotations, recognized log records, Markdown tables, front matter,
URLs, approved glossary terms, and explicit exceptions. See
`references/formulaic-style.md` for the review boundary.

## Source comments

Directory scans include supported source files and lint only extracted comments
or docstrings. The linter does not process executable code as prose.

- Python uses token and syntax-tree parsing for comments and docstrings.
- C-like languages use line-comment and block-comment parsing.
- Shell and Ruby use full-line hash comments.
- TOML and YAML use quote-aware hash comments.
- HTML uses markup-aware extraction for visible text and comment blocks. It
  protects code, quotation, script, style, and table elements.

A documentation tag line starts its own block, as a list item does. A run of
`@param`, `@returns`, or `@throws` entries is therefore measured entry by
entry, not as one sentence. A single entry that passes the sentence limit
still reports.

An explicitly named source file needs a supported parser. The command exits
with status `2` instead of processing an unsupported source or structured-data
file as prose. Pass extracted prose on standard input when no parser exists.

## Automatic exclusions

A directory scan skips paths that the project did not write and cannot
rewrite. An explicitly named path always lints, so
`technical-writing lint LICENSE` still reports diagnostics.

The linter skips these directories and everything under them:

```text
.bundle .cache .dart_tool .git .gradle .mypy_cache .next .nox .nuxt
.pytest_cache .ruff_cache .svelte-kit .terraform .tox .venv Pods
__fixtures__ __pycache__ __snapshots__ bower_components build coverage
dist fixtures htmlcov node_modules site-packages target testdata
third_party vendor venv
```

It skips these files by name pattern:

- Legal and community boilerplate: `LICENSE*`, `LICENCE*`, `COPYING*`,
  `NOTICE*`, `PATENTS*`, `AUTHORS*`, `CONTRIBUTORS*`, `CODE_OF_CONDUCT*`.
- Release output: `CHANGELOG*`.
- Dependency locks: `*.lock`, `*-lock.json`, `*-lock.yaml`, `*.lock.json`,
  `go.sum`.
- Build output: `*.min.js`, `*.min.css`, `*.bundle.js`.
- Generated code: `*.d.ts`, `*.pb.go`, `*_pb2.py`, `*_pb2_grpc.py`,
  `*.g.dart`, `*.freezed.dart`, `*.gen.go`, `*_generated.go`,
  `*.generated.*`.

It also skips any discovered file whose first 4096 characters contain
`@generated` or a `Code generated ... DO NOT EDIT` marker.

The `[files]` table adjusts the list:

```toml
[files]
exclude = ["docs/vendor-guide.md"]
exceptions = ["CHANGELOG.md"]
```

- `exclude` adds project patterns to the built-in list.
- `exceptions` restores a path that an exclusion removes. It wins over every
  exclusion. It also restores a file inside an excluded directory and a file
  with a generated marker.

Each pattern matches the project-relative path, any path segment, or the file
name. A wildcard crosses a path separator. Write `vendor/docs/**` to name a
whole subtree, because a pattern with a separator matches no path below
itself. A pattern that names a path inside an excluded directory makes the
scan descend into that directory.

`[glossary].exclude` still applies to glossary candidate scans. Those scans
use the same automatic exclusions.

## Glossary discovery

The `[glossary].path` value is relative to the project configuration
directory's parent. The default `.agents/technical-writing.toml` therefore
resolves `GLOSSARY.md` from the repository root.

The configured path must stay inside the project root. Use the explicit
`--glossary` option when you intentionally need another path. The linter fails
when that explicit path does not exist.

Set `[glossary].required = true` in a project that enforces its glossary. A
missing required glossary makes `lint` exit with status `2`. The built-in and
example global configurations leave this setting `false`, so projects can use
the writing rules before they create a glossary.

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
