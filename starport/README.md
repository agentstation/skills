# starport Agent Skill

This Agent Skill teaches a coding agent to install, start, query, and
diagnose a self-hosted [Starport](https://github.com/agentstation/starport)
LLM inference gateway.

The canonical copy lives in the Starport repository at
`skills/starport/SKILL.md` and ships inside the released binary. This
directory mirrors that copy for skill installers.

## Install

The primary path is the CLI itself, which installs the skill written for
its own commands:

```sh
brew install agentstation/tap/starport
starport agent setup
```

Run `starport agent setup` again after a CLI upgrade, so the installed
skill tracks the installed commands.

Install the mirrored copy with GitHub CLI:

```sh
gh skill install agentstation/skills starport --agent codex --scope project
```

Change `--agent` for another supported host. Use `--scope user` to make the
skill available across repositories.

## Provenance

The Starport repository owns this skill. Update the mirror from
`skills/starport/SKILL.md` there, and record the upstream commit in the
mirror commit message.
