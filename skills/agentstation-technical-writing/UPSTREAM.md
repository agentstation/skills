# Provenance

This source inspired the skill:

- Repository: https://github.com/woosal1337/blog
- Path: `videos/ep01-the-cure-for-ai-slop`
- Reviewed commit: `1de95f861304d71f028f7cc6ef3f171bb2c59f05`
- Reviewed: 2026-07-30

The source experiment compared a banned-word list, Orwell's rules, and an
ASD-STE100-inspired skill. It motivated testing a coherent writing policy
instead of treating individual words as the main problem.

The experiment is directional, not proof of writing quality. It used six tasks,
two model families, and a heuristic that scores surface features similar to the
prompted rules. It did not measure factual preservation, naturalness, voice, or
human preference.

AgentStation's skill is a developer-focused adaptation. It adds project
configuration, glossary enforcement, glossary maintenance, deterministic
conformance results, and explicit human review. The default mode targets
technical collaboration and documentation. The strict mode targets procedures
and safety text.

The linter adapts the upstream source code under the MIT License. The adapted
file retains attribution. `LICENSE.upstream` contains the upstream license.
This repository contains no source prose or ASD-STE100 specification text.

The ASD Simplified Technical English Maintenance Group maintains ASD-STE100.
The official specification remains the authority for conforming work:
https://www.asd-ste100.org/
