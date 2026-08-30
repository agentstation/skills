# Modern Go Agent Skill

This Agent Skill guides Go code changes through three sources of truth:

- the repository's target Go version and local contracts.
- the version-aware Modern Go Guidelines CLI.
- the repository's active ago policy when its command is available.

The skill writes modern Go inside the form that the project selects. An ago
restriction wins when modern guidance recommends a construct that the active
project policy rejects.

## Install

Install the skill globally with the skills CLI:

```sh
npx skills add agentstation/skills --skill use-modern-go -g \
  -a codex -a claude-code -y
```

The bundled wrapper pins version `v0.1.1` of the Modern Go Guidelines CLI. It
requires Go 1.25 or automatic toolchain switching. Its first run also needs
network access and permission to write to a user cache.

The skill does not install ago. It uses `go tool ago` when `go.mod` declares
the ago module tool. The pinned version supplies built-in defaults without a
policy file. The command resolves a custom policy when `.ago.yml` or
`.ago.yaml` exists. The skill uses a global command only when repository
instructions require that command.

## Agent contract

[`SKILL.md`](SKILL.md) directs the coding agent to:

1. Read the module's declared Go version and the affected contracts.
2. Load the complete modern-guideline list for that version.
3. Resolve the active ago policy before it selects a Go form.
4. Make the smallest behavior-preserving change.
5. Format and test the affected code.
6. Run the repository-owned ago command when it is available.

[`UPSTREAM.md`](UPSTREAM.md) records the source version and local differences.
