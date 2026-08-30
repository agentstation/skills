# Glossary

| Term | Definition | Avoid | Status | Evidence |
|---|---|---|---|---|
| `@earendil-works/pi-coding-agent` | The npm package that provides the Pi CLI used by autoreview. | | Approved | `autoreview/CONFIG.md` |
| ago | The restriction-only Go linter that rejects selected legal Go constructs. | | Approved | `ago/SKILL.md` |
| Agent Skill | A reusable directory of agent instructions with a `SKILL.md` entry point. | | Approved | `AGENTS.md` |
| AgentStation | The organization that maintains this skills collection. | | Approved | `README.md` |
| ASD-STE100 | The international standard for technical documentation in Simplified Technical English. | | Approved | `technical-writing/UPSTREAM.md` |
| autoreview | An isolated second-model code review that runs at a configured gate. | auto review | Approved | `autoreview/SKILL.md` |
| code-like | Describes prose content that matches the form of a source identifier, command option, or dotted name. | | Approved | `technical-writing/CONFIG.md` |
| coding agent | A program that runs ago through its command, JSON catalogue, and exit status. | | Approved | `ago/SKILL.md` |
| control plane | The durable plan file that holds current state, routing, and progress for one outcome. | | Approved | `plans/references/structure.md` |
| execution log | The append-only plan table that records dated actions with commits and evidence. | | Approved | `plans/references/structure.md` |
| fail-before evidence | Proof that a check failed before the change that makes it pass. | | Approved | `plans/references/structure.md` |
| findings ledger | The plan table that records discovered defects and routes each one to an owning task. | | Approved | `plans/references/structure.md` |
| goal block | The paste-ready prompt inside a plan that starts autonomous execution. | goal prompt | Approved | `plans/references/execution.md` |
| DeepSWE | The benchmark data used to rank default autoreview models. | | Approved | `autoreview/MODEL_SELECTION.md` |
| developer mode | The technical-writing mode for developer collaboration and documentation. | developer-mode | Approved | `technical-writing/SKILL.md` |
| formulaic style | Stock wording or structure that adds rhetoric without adding technical meaning. | | Approved | `technical-writing/references/formulaic-style.md` |
| finding | One reported violation of an ago rule. | | Approved | `ago/SKILL.md` |
| Go | The Go programming language and its standard toolchain. | Golang | Approved | `use-modern-go/SKILL.md` |
| `cursor-agent` | The Cursor command-line executable that autoreview uses as a review harness. | | Approved | `autoreview/CONFIG.md` |
| markup-aware | Describes extraction that distinguishes visible prose from protected elements and attributes in a markup document. | | Approved | `technical-writing/CONFIG.md` |
| mechanical conformance | A result that confirms only the deterministic writing rules. | lint compliance | Approved | `technical-writing/references/conformance.md` |
| Modern Go Guidelines CLI | The version-aware command that lists and explains modern Go forms. | | Approved | `use-modern-go/SKILL.md` |
| multi-word noun | A noun group that contains more than one word and functions as one noun. | noun cluster | Approved | `technical-writing/references/asd-ste100.md` |
| MCP | Model Context Protocol, which connects an AI application to external tools and data. | | Approved | `autoreview/SKILL.md` |
| OpenCode | A coding-agent CLI that autoreview can use as an isolated review harness. | | Approved | `autoreview/SKILL.md` |
| plans | The skill identifier for the AgentStation durable-plan system. | | Approved | `plans/SKILL.md` |
| pre-PR gate | The autoreview gate that runs before authors publish or update a pull request. | | Approved | `autoreview/SKILL.md` |
| project glossary | The repository-level `GLOSSARY.md` file that defines approved technical terms. | terminology list | Approved | `technical-writing/references/glossary.md` |
| proof root | The directory beside a plan that holds its evidence artifacts, one file per task. | | Approved | `plans/references/structure.md` |
| seam | A language-native boundary that owns one domain concept and its contract. | | Approved | `plans/references/architecture.md` |
| status ledger | The plan table that holds one status row per task. | task ledger | Approved | `plans/references/structure.md` |
| stale ignore | An `//ago:ignore` directive that suppressed no finding in the run. | | Approved | `ago/SKILL.md` |
| protected content | Source text, code, identifiers, quotations, or approved terms that must remain exact. | | Approved | `technical-writing/references/formulaic-style.md` |
| restricted vocabulary | A controlled list of words that require a precise common replacement in technical prose. | | Approved | `technical-writing/references/formulaic-style.md` |
| strict mode | The technical-writing mode for procedures, runbooks, safety text, and controlled errors. | strict-mode | Approved | `technical-writing/SKILL.md` |
| technical writing | Developer-facing prose that explains technical behavior or guides a technical task. | | Approved | `technical-writing/SKILL.md` |
| technical-writing | The skill identifier for the AgentStation technical-writing system. | | Approved | `technical-writing/SKILL.md` |
