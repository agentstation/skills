# Conformance

Mechanical conformance is necessary, but it is not sufficient. The linter
cannot determine whether a statement is true, complete, or useful.

## Mechanical checks

The linter checks:

- sentence and paragraph limits.
- contractions, semicolons, and em dashes.
- passive voice and `-ing` main-verb patterns.
- nominalisations and selected phrasal verbs.
- vague formal words, marketing adjectives, and modal hedges.
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
7. Each condition or warning appears before its action.
8. The sequence is complete and safe.
9. The document contains all information that the audience needs.
10. The document contains no filler, repeated conclusion, or unsupported claim.

## Result

Use these result labels:

- `conformant`: the linter passes and the human checks pass.
- `mechanically conformant`: the linter passes, but human review is incomplete.
- `nonconformant`: a linter rule or human check fails.

Do not describe this result as ASD-STE100 certification.
