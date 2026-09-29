# Upstream

AgentStation derives this skill from:

- Repository: https://github.com/openclaw/agent-skills
- Path: `skills/autoreview`
- Imported commit: `4d1f51be0f0ea3f8806ef18259348631a731e6f8`
- Imported: 2026-08-10

AgentStation intentionally diverges in model policy, skill instructions, and
selected false-positive hardening. Update by importing a newer upstream tree on
a branch, reapplying these local changes, and running the complete test suite.

Local divergences to reapply on import:

- AgentStation owns the scored profile, model, effort, Fable approval, and
  harness installation policy.
- AgentStation keeps runnable, isolated OpenCode and Cursor adapters. Upstream
  fails those engines closed.
- AgentStation reuses a recent clean pre-PR result when the exact substantive
  diff and review contract have not changed. The private attestation does not
  bypass secret scanning or prompt validation.
- `scripts/autoreview` treats `.astro`, `.cjs`, `.cts`, `.mjs`, and `.mts` as
  substantive code. The `".config." in name` guard still excludes related
  configuration files from automatic code gates.
- `scripts/autoreview` omits `docs` from `NONSUBSTANTIVE_PATH_PARTS`. A
  documentation directory holds handwritten files, and a `docs` path component
  also appears inside real source trees as a route segment. Markup suffixes stay
  outside `SUBSTANTIVE_CODE_SUFFIXES`, so prose is still excluded.
- Secret scanning recognizes the plain `synthetic` placeholder and simple
  TypeScript generic annotations. It still scans their initializers.
- The helper also redacts deleted credential fragments from removed lines in a
  modified file. It still refuses those fragments in retained text, additions,
  and extra review inputs.
- `--max-passes` accepts an explicit budget from 1 through 64. The default is
  eight. Per-pass bytes, complete-content checks, and isolation do not change.
- The prompt-boundary test derives its input from the configured byte ceiling.
- Committed branch and commit reviews decode regular `.json.gz` files before
  review and secret scanning. Input limits are 8 MiB compressed, 32 MiB decoded,
  64 MiB formatted, 64 nesting levels, and sixteen files per target. Only one
  gzip member with no optional header fields is accepted. JSON tokens and key
  order stay unchanged. Git object IDs and file metadata remain in the diff.
  Local binary review and other binary formats still fail closed.
