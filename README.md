# AgentStation Skills

Reusable Agent Skills for Claude Code, Codex, and compatible hosts.

## Skills

| Skill | What it does | Details |
|---|---|---|
| `ago` | Runs and remediates the ago restriction-only Go linter. | [ago/README.md](ago/README.md) |
| `autoreview` | Runs an isolated second-model code review at a pre-PR gate or a configured checkpoint. | [autoreview/README.md](autoreview/README.md) |
| `plans` | Keeps a durable plan that owns one outcome, with a status ledger, verifiable task criteria, and autonomous execution. | [plans/README.md](plans/README.md) |
| `technical-writing` | Applies controlled, lintable writing rules to developer-facing prose. | [technical-writing/README.md](technical-writing/README.md) |

## Install

Each skill installs into the shared `~/.agents/skills` directory:

```bash
npx skills add agentstation/skills --skill ago -g -a codex -a claude-code -y
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code -y
npx skills add agentstation/skills --skill plans -g -a codex -a claude-code -y
npx skills add agentstation/skills --skill technical-writing -g \
  -a codex -a claude-code -a goose -y
```

The agent flags create the harness links. A manual link for each skill is not
required. Compatible harnesses that read `~/.agents/skills` use the same
canonical copy.

Update every installed global skill with:

```bash
npx skills update -g
```

The global skill lock records source and content metadata. It does not pin a
GitHub commit. Review upstream changes before a global update when
reproducibility matters.

Install from the GitHub source shown above for normal use. A local-path
install helps during development, but it records no updateable GitHub source
metadata.

## Make a skill unconditional

Installation makes a skill available. It does not make the skill's use
unconditional. Add a bootstrap rule to each harness's persistent user
instructions:

```markdown
## Default writing style

Use the installed `technical-writing` skill for all developer-facing prose.
Apply `developer` mode to every response for a technical user. Use `strict`
mode for procedures, safety text, and tightly controlled errors. Preserve
facts, uncertainty, glossary terms, identifiers, commands, code, logs, and
structured data.
```

Use `~/.codex/AGENTS.md` for Codex, `~/.claude/CLAUDE.md` for Claude Code, and
`~/.config/goose/.goosehints` for Goose. Other harnesses need the equivalent
persistent user-instruction file.

## Repository layout

The repository uses the Agent Skills `<name>/SKILL.md` layout at its root. The
`skills` CLI discovers this flat collection and verifies that each frontmatter
name matches its directory. `SKILL.md` addresses the agent. Each `README.md`
addresses a person. `GLOSSARY.md` holds the approved terms for this
repository.

Validate every skill after a change:

```bash
./scripts/validate-skills
```

See each skill's `UPSTREAM.md` for derivative provenance.
