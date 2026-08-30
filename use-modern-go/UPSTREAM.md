# Upstream

AgentStation derives this skill from:

- Repository: https://github.com/JetBrains/go-modern-guidelines
- Path: `plugin/skills/use-modern-go`
- Reviewed commit: `c17350498ae6a8f50e0d3882cd0d7fc132b5a233`
- Pinned CLI version: `v0.1.1`
- Reviewed: 2026-08-30
- License: Apache-2.0

The bundled `scripts/run-tool.sh`, `scripts/run-tool.ps1`, and
`scripts/VERSION` files match the reviewed upstream files. The upstream
license appears in `LICENSE.upstream`.

AgentStation rewrites the skill instructions around a project-selected Go
form. The local workflow adds repository contract discovery, behavior
preservation, focused verification, and optional ago policy enforcement.

Modern guidance applies inside the target Go version and the active project
policy. This rule resolves known conflicts. For example, modern guidance can
recommend expression-based `new`, while an active ago policy can reject it.

To update this skill:

1. Review a specific upstream commit and pinned CLI version.
2. Compare the upstream skill, wrapper scripts, CLI behavior, and license.
3. Update the pinned wrapper files and provenance fields together.
4. Preserve the project-policy and ago integration rules.
5. Run `scripts/validate-skills` and the technical-writing linter.
