# AgentStation Skills

Reusable Agent Skills for Claude Code, Codex, and compatible hosts.

## Skills

- `autoreview`: isolated, structured second-model review with layered model
  profiles and a substantive-code pre-PR gate.
- `writing-clearly`: clear, direct prose for every coding-agent response and
  durable technical artifact, with a stricter mode for procedures and errors.

Install globally with the shared canonical directory:

```bash
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code
```

Install the default writing style for Codex, Claude Code, and Goose:

```bash
npx skills add agentstation/skills --skill writing-clearly -g \
  -a codex -a claude-code -a goose
```

Installation makes a skill available but does not make its use unconditional.
Add this small bootstrap to each harness's persistent user instructions:

```markdown
## Default writing style

For every task, invoke the installed `writing-clearly` skill before drafting
prose. Apply it to all original prose, including progress updates and final
answers. Higher-priority user and repository instructions override it.
```

Use `~/.codex/AGENTS.md` for Codex, `~/.claude/CLAUDE.md` for Claude Code, and
`~/.config/goose/.goosehints` for Goose. Other harnesses need the equivalent
persistent user-instruction file. The shared `~/.agents/skills` directory still
provides one canonical skill copy.

The repository uses the standard `skills/<name>/SKILL.md` layout. See each
skill's `UPSTREAM.md` for derivative provenance.
