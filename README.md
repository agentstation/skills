# AgentStation Skills

Reusable Agent Skills for Claude Code, Codex, and compatible hosts.

## Skills

- `autoreview`: isolated, structured second-model code review using GPT-5.6 Sol
  or Claude Opus 5.

Install globally with the shared canonical directory:

```bash
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code
```

The repository uses the standard `skills/<name>/SKILL.md` layout. See each
skill's `UPSTREAM.md` for derivative provenance.
