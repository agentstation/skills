# AgentStation Skills

Reusable Agent Skills for Claude Code, Codex, and compatible hosts.

## Skills

- `autoreview`: isolated, structured second-model review with layered model
  profiles and a substantive-code pre-PR gate.

Install globally with the shared canonical directory:

```bash
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code
```

The repository uses the standard `skills/<name>/SKILL.md` layout. See each
skill's `UPSTREAM.md` for derivative provenance.
