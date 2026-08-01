# ASD-STE100 profile

ASD-STE100 Simplified Technical English is an international standard for
technical documentation. The current edition is Issue 9, dated January 15,
2025.

Use the official standard as the authority for ASD-STE100 rules and approved
words:

- [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf)
- [Official ASD-STE100 site](https://www.asd-ste100.org/)
- [Official tools guidance](https://www.asd-ste100.org/STEsoftware.html)

## AgentStation profile

This skill applies a verified subset of Issue 9 to developer-facing prose. It
also adds factual-preservation, project-glossary, and software-artifact rules.

The profile has these boundaries:

- It does not include the official controlled dictionary.
- It does not enforce American English when project or locale rules select
  another spelling.
- It lets project glossaries define approved technical nouns and technical
  verbs.
- It permits multiple actions in one instruction only when the actions occur
  at the same time.
- It does not assign `warning` or `caution` meanings when another industry or
  project defines different risk labels.
- It does not claim ASD approval, certification, or audited conformance.

The linter checks deterministic surface rules. It cannot determine whether a
sentence preserves meaning, uses the official dictionary, or applies every
Issue 9 rule. A writer must complete the human conformance review.
