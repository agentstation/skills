# Conformance

Mechanical conformance is necessary, but it is not sufficient. The linter
cannot determine whether a statement is true, complete, or useful.

## Mechanical checks

The linter checks:

- sentence and paragraph limits.
- contractions, semicolons, and em dashes.
- passive voice, complex verb forms, and `-ing` main-verb patterns.
- nominalisations and selected phrasal verbs.
- vague formal words, marketing adjectives, and modal hedges.
- selected stock phrases, assistant scaffolds, and negative parallelism.
- restricted words when they occur.
- glossary aliases that conflict with an approved term.

The linter must exit with status `0`. Review each suppression or configuration
exception. An exception must protect technical accuracy or a required project
convention.

## Human checks

Confirm each item:

1. Available sources support every statement.
2. Unknown information stays unknown.
3. Each concept uses one approved glossary term.
4. Each glossary term has one meaning in this document.
5. Required identifiers, commands, values, and units are exact.
6. Each instruction contains one action.
7. Multiple actions in one instruction occur at the same time.
8. Each condition or warning appears before its action.
9. Each sentence keeps its necessary subject, verb, and articles.
10. Each multi-word noun has no more than three words, or it is an approved
    technical noun.
11. A longer approved technical noun has a clear shorter form when applicable.
12. Each descriptive sentence has one subject.
13. The sequence is complete and safe.
14. The document contains all information that the audience needs.
15. The document contains no imaginary misconception or invented contrast.
16. The document contains no rhetorical fragment or ornamental copula.
17. The document contains no near-synonym triad used only for rhythm.
18. The document contains no filler, repeated conclusion, or unsupported claim.
19. A reviewer checked each contextual vocabulary choice in its technical use.
20. Each intentional rule exception states the accuracy or terminology reason.

## Result

Use these result labels:

- `conformant`: the linter passes and the human checks pass.
- `mechanically conformant`: the linter passes, but human review is incomplete.
- `nonconformant`: a linter rule or human check fails.

Do not describe this result as ASD-STE100 certification.
