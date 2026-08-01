# AgentStation Skills

Reusable Agent Skills for Claude Code, Codex, and compatible hosts.

## Skills

- `autoreview`: isolated, structured second-model review with layered model
  profiles and a substantive-code pre-PR gate.
- `technical-writing`: controlled, lintable developer writing for
  agent responses, documentation, prompts, tool descriptions, technical web
  pages, procedures, and other technical prose.

Install globally with the shared canonical directory:

```bash
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code
```

Install the default writing style for Codex, Claude Code, and Goose:

```bash
npx skills add agentstation/skills --skill technical-writing -g \
  -a codex -a claude-code -a goose -y
```
Installation makes a skill available but does not make its use unconditional.
Add this small bootstrap to each harness's persistent user instructions:

```markdown
## Default writing style

Use the installed `technical-writing` skill for all
developer-facing prose. Apply `developer` mode to every response for a
technical user. Use `strict` mode for procedures, safety text, and tightly
controlled errors. Preserve facts, uncertainty, glossary terms, identifiers,
commands, code, logs, and structured data.
```

Use `~/.codex/AGENTS.md` for Codex, `~/.claude/CLAUDE.md` for Claude Code, and
`~/.config/goose/.goosehints` for Goose. Other harnesses need the equivalent
persistent user-instruction file. The shared `~/.agents/skills` directory still
provides one canonical skill copy.

The agent flags create the harness links. A manual link for each skill is not
required. Compatible harnesses that read `~/.agents/skills` can use the same
canonical copy.

## Technical-writing setup

The linter requires Python 3.11 or later. Set its path after installation:

```bash
export TECHNICAL_WRITING="${AGENTS_HOME:-$HOME/.agents}/skills/technical-writing/scripts/technical-writing"
```

Copy the example to set a user-wide default:

```bash
mkdir -p ~/.config/agentstation
cp ~/.agents/skills/technical-writing/config.example.toml \
  ~/.config/agentstation/technical-writing.toml
```

A repository can override that file with
`.agents/technical-writing.toml`. Create and review the project glossary:

```bash
"$TECHNICAL_WRITING" glossary init
"$TECHNICAL_WRITING" glossary check
"$TECHNICAL_WRITING" glossary update --check
```

The initializer adds draft candidates. A person must define and approve each
real project term. Put reviewed scanner noise in `ignored_candidates`.

To migrate from the earlier name, install `technical-writing`,
update the persistent instruction, verify a fresh session, and then remove the
old skill:

```bash
npx skills remove writing-clearly -g -y
```

Install from the GitHub source shown above for normal use. Local-path installs
are useful during development, but they do not record updateable GitHub source
metadata in the global skill lock.

Update installed global skills with:

```bash
npx skills update -g
```

The global skill lock records source and content metadata. It does not pin a
GitHub commit. Review upstream changes before a global update when
reproducibility matters.

The repository uses the Agent Skills `<name>/SKILL.md` layout at its root. The
`skills` CLI discovers this flat collection and verifies that each frontmatter
name matches its directory. See each skill's `UPSTREAM.md` for derivative
provenance.
