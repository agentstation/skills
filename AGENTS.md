# AgentStation Skills

Canonical reusable skills live under `skills/<name>/SKILL.md`.

- Keep global skills product-agnostic.
- Put project-specific profiles in the owning project's skills repository.
- Keep `SKILL.md` concise and move conditional reference material behind direct
  pointers.
- Prefer executable enforcement for security and model-selection boundaries.
- Record derivative skill provenance and upstream commit IDs.
- Validate changes with `scripts/validate-skills` and each skill's own tests.
