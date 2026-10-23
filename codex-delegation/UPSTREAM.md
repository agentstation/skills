# Provenance

This skill adapts the owner's existing `CODEX_DELEGATION.md` procedure. It
removes project details and moves machine paths into a conditional reference.
The source procedure sets the Codex CLI minimum at 0.159.0. Plugin setup checks
the requirements of the installed version.

The author checked the native plugin interface against
[`openai/codex-plugin-cc`](https://github.com/openai/codex-plugin-cc), commit
`db52e28f4d9ded852ab3942cea316258ae4ef346`, on 2026-10-22.

The plugin source uses Apache-2.0. This skill contains no copied plugin code.
Its command examples describe the native interface. Check installed help when
the plugin version changes.
