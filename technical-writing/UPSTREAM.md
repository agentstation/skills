# Provenance

This source inspired the skill:

- Repository: https://github.com/woosal1337/blog
- Path: `videos/ep01-the-cure-for-ai-slop`
- Reviewed commit: `1de95f861304d71f028f7cc6ef3f171bb2c59f05`
- Reviewed: 2026-07-30

This later exemplar informed the rewrite workflow and agent-message scope:

- Repository: https://github.com/danyuchn/asd-ste100-skill
- Reviewed commit: `8564f8985f15104c2184f90531bfd1bbb25f3d5b`
- Reviewed: 2026-07-31
- License: MIT

This adaptation copies no exemplar prose or code. The review compared rule
coverage, examples, preservation boundaries, and agent-facing artifact scope.

The source experiment compared a banned-word list, Orwell's rules, and an
ASD-STE100-inspired skill. It motivated testing a coherent writing policy
instead of treating individual words as the main problem.

The experiment provides limited evidence. It used six tasks, two model
families, and a heuristic that evaluated surface features similar to the
prompted rules. It did not measure factual preservation, naturalness, voice,
or human preference.

AgentStation's skill is a developer-focused adaptation. It adds project
configuration, glossary enforcement, glossary maintenance, deterministic
conformance results, and explicit human review. The default mode targets
technical collaboration and documentation. The strict mode targets procedures
and safety text.

The linter adapts the upstream source code under the MIT License. The adapted
file retains attribution. `LICENSE.upstream` contains the upstream license.
This repository contains no source prose or ASD-STE100 standard text.

The block scanner diverges from the upstream one. A documentation tag line
starts its own block, so a `@param` run reads as one entry per line instead of
one sentence. Upstream measures the whole run as a single sentence, which
reports every documented parameter list of a normal size as too long.

The code mask diverges from the upstream one. It masks an escaped-brace type
literal, the form a documentation generator emits for a TypeScript object
type: `\{ `a`: `number`; `b`: `string`; \}`. The inline mask covers each
backticked member and leaves the separators, so upstream reports every such
signature as prose punctuation. The mask needs a backtick inside the braces,
which keeps an escaped brace pair in ordinary prose visible.

The ASD Simplified Technical English Maintenance Group maintains ASD-STE100.

Issue 9 became an international standard on January 15, 2025. Use the official
standard as the authority for conforming work:

- https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf

## Vocabulary research

The restricted vocabulary and phrase rules use these sources for candidate
selection:

- Juzek and Ward, “Why Does ChatGPT Delve So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models”: https://aclanthology.org/2025.coling-main.426/
- Kobak et al., “Delving into LLM-assisted writing in biomedical publications through excess vocabulary”: https://arxiv.org/abs/2406.07016

Frequency alone does not create a rule. The built-in list also requires a
controlled-writing rationale, a direct replacement, and low technical
ambiguity. The linter reports each configured occurrence without a
document-level vocabulary gate.
