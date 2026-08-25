# ago Agent Skill

This Agent Skill teaches a coding agent to discover, run, and remediate the
[ago](https://github.com/agentstation/ago) restriction-only Go linter.

The skill separates two workflows:

- Use the pinned tool and existing policy in an adopted repository.
- Add the pinned tool, starter policy, agent instruction, and CI when the user
  requests adoption.

The skill does not enforce policy. The adopting repository owns enforcement
through `go.mod`, `.ago.yml`, `AGENTS.md`, and CI.

## Install

Install for one repository with GitHub CLI:

```sh
gh skill install agentstation/skills ago --agent codex --scope project
```

Change `--agent` for another supported host. Use `--scope user` to make the
skill available across repositories.

Install through the skills CLI when that tool owns your Agent Skills:

```sh
npx skills add agentstation/skills --skill ago -a codex -a claude-code -y
```

## Agent contract

[`SKILL.md`](SKILL.md) directs the coding agent to:

1. Prefer `go tool ago` from the repository's module tool directive.
2. Discover the active rules as JSON.
3. Treat exit status 2 as an incomplete run.
4. Fix source without weakening `.ago.yml`.
5. Use a reasoned suppression only for a local exception.
6. Run the same command after each repair pass.
