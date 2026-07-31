# Autoreview maintenance

- Upstream implementation: `openclaw/agent-skills`, `skills/autoreview`.
- Record the imported upstream commit in `UPSTREAM.md`.
- Sync upstream into a clean branch, then reapply and test the AgentStation
  model policy and any accepted hardening patches.
- Keep repository-specific criteria out of this skill. Profiles such as Nimbus
  belong in their owning repository and invoke this helper with explicit
  criteria.
- Keep Fable behind manual approval and unavailable to automatic selection or
  fallback.
- Keep built-in Claude effort at or below `high`; higher caps must be conscious
  configuration.
- Keep the default automatic cadence at the substantive-code pre-PR gate.
- Update `MODEL_SELECTION.md` whenever built-in scores or benchmark inputs
  change.
- Run the helper self-tests, Python tests, and repository skill validator after
  every change.
