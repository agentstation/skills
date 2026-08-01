# Rewrite workflow

Use this workflow when the user asks to edit, simplify, clarify, or compare
existing technical prose.

## Preserve the source

Read the complete source before changing a sentence. Record these protected
items:

- Facts, measurements, values, and units.
- Conditions, exceptions, limits, and scope qualifiers.
- Known causes, unknown causes, and confidence levels.
- Identifiers, commands, code, quotations, and citations.
- Required project terms and deliberate wording.

Do not trade technical precision for a shorter sentence. Keep necessary text
when a rule conflicts with accuracy. State the conflict in the result.

## Rewrite

1. Identify each sentence that needs a change.
2. Name the applicable rule.
3. Rewrite only the necessary text.
4. Compare the result with the protected items.
5. Run the linter.
6. Complete the human conformance checks.

If the source conforms and satisfies the request, return it unchanged. Do not
add a preamble or a restatement.

## Explain changes

Give a comparison only when the user requests one or needs it to review the
edit. Use this table:

| Rule | Original | Revised |
|---|---|---|
| Simple tense | Source sentence | Revised sentence |

Put intentionally nonconforming examples in fenced text blocks. The linter
then treats them as protected source text.

After the table, list only the text that remains intentionally unsimplified.
Give the precision or project-term reason for each item.
