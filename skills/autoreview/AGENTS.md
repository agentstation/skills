# Autoreview maintenance

- Upstream implementation: `openclaw/agent-skills`, `skills/autoreview`.
- Record the imported upstream commit in `UPSTREAM.md`.
- Sync upstream into a clean branch, then reapply and test the AgentStation
  model policy and any accepted hardening patches.
- Keep repository-specific criteria out of this skill. Profiles such as Nimbus
  belong in their owning repository and invoke this helper with explicit
  criteria.
- The executable policy must reject every reviewer except `gpt-5.6-sol` and
  `claude-opus-5`, and every effort except `high` and `xhigh`.
- Run the helper self-tests, Python tests, and repository skill validator after
  every change.
