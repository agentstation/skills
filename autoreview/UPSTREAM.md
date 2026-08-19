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
