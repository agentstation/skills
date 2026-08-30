# AgentStation Skills

Canonical reusable skills live under `<name>/SKILL.md`.

- Follow the current Agent Skills specification at https://agentskills.io.
- Keep global skills product-agnostic.
- Put project-specific profiles in the owning project's skills repository.
- Keep `SKILL.md` concise and move conditional reference material behind direct
  pointers.
- Prefer executable enforcement for security and model-selection boundaries.
- Record derivative skill provenance and upstream commit IDs.
- Validate all skills with `scripts/validate-skills` after each skill change.
- Run each changed skill's own tests.

## Technical writing

Use `GLOSSARY.md` for developer-facing prose. Run the installed
`technical-writing` linter on durable technical text.
