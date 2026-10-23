# Autoreview maintenance

- Upstream implementation: `openclaw/agent-skills`, `skills/autoreview`.
- Record the imported upstream commit in `UPSTREAM.md`.
- Sync upstream into a clean branch, then reapply and test the AgentStation
  model policy and any accepted hardening patches.
- Keep repository-specific criteria and named project profiles in their owning
  repositories.
- Invoke this helper with explicit criteria from those repositories.
- Enforce the canonical sibling model-selection policy for reviewers and fallbacks.
- Keep Fable coordinator-only, Astra specialist-only, and Haiku prohibited.
- Check frontier eligibility before ranking candidates or installing harnesses.
- Keep external adapters explicit and require concrete model identities.
- Keep Opus 5.5 high as the default Claude-side code reviewer.
- Keep built-in Claude effort at or below `high`.
- Require conscious configuration for higher caps.
- Keep the default automatic cadence at the substantive-code pre-PR gate.
- Update `MODEL_SELECTION.md` whenever built-in scores or benchmark inputs
  change.
- Run the helper self-tests, Python tests, and repository skill validator after
  every change.
