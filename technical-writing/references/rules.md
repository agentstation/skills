# Technical writing rules

Apply these rules to developer-facing prose. Required technical terms take
priority over short common words.

## Terms

- Use one approved term for each concept.
- Give each term one meaning in the same scope.
- Read `GLOSSARY.md` before you write long-lived project text.
- Keep code identifiers, API fields, commands, product names, and protocol
  terms exact.
- Prefer a short common word when it preserves the technical meaning.

Use these common replacements unless the glossary requires another term:

| Avoid | Prefer |
|---|---|
| `begin`, `commence`, `initiate`, `originate` | `start` or the exact source |
| `utilize`, `utilise`, `utilization`, `utilisation`, `leverage` | `use` |
| `facilitate` | `help` |
| `ensure` | the exact action that produces or verifies the result |
| `prior to` | `before` |
| `subsequent to` | `after` |
| `obtain`, `acquire` | `get` |
| `demonstrate` | `show` |
| `additionally`, `furthermore`, `moreover` | `also` |
| `comprehensive`, `comprehensively` | the exact scope |
| `aforementioned` | the exact subject |
| `henceforth` | `from now on` |
| `therein` | the exact location |
| `whilst`, `amongst` | `while`, `among` |
| `numerous`, `myriad`, `plethora` | an exact number or `many` |
| `in order to` | `to` |
| `a variety of` | the exact items or `several` |
| `in the event that` | `if` |
| `due to the fact that` | `because` |

Replace a modal preamble with the fact or condition. Examples include
`it is important to note`, `it should be noted`, and `please note that`.

Do not use promotional words as substitutes for evidence. Examples include
`seamless`, `robust`, `powerful`, `effortless`, and `enterprise-grade`.

## Verbs

- Use active voice when the text identifies a relevant actor.
- Use a verb for an action. Write `analyze the log`, not
  `perform an analysis of the log`.
- Prefer a simple tense.
- Avoid stacked auxiliary verbs.
- Replace an `-ing` main verb with a simple verb when the meaning stays exact.
- Replace a phrasal verb with one precise verb when possible.

## Sentences

- Put one instruction in each sentence.
- Put a condition before the instruction that depends on it.
- Keep an instruction at or below 20 words.
- Keep a descriptive sentence at or below 25 words.
- Do not use contractions in conforming text.
- Use articles when they make the subject unambiguous.

## Punctuation and structure

- Do not use semicolons.
- Do not use an em dash as a substitute for sentence structure.
- Keep one topic in each paragraph.
- Keep a paragraph at or below six sentences.
- Use a numbered vertical list for a sequence.
- Start each procedure step with an imperative verb.
- Put a prerequisite or warning before the affected action.
- Use a table only for repeated fields or direct comparisons.

## Content

- When reproducing existing material, keep it exact.
- When editing material, change only the authorized parts.
- Preserve every supplied fact, unknown, cause, guarantee, measurement, and
  level of confidence during an edit.
- When authoring new material, support each claim with an available source,
  verified result, or clearly marked inference.
- Do not invent precision, evidence, causes, guarantees, or certainty.
- Separate an observation from an inference or recommendation.
- Preserve code, commands, identifiers, logs, quotations, and structured data.
- Start with the information that the technical reader needs first.
- Do not add a preamble, repeated summary, or empty closing statement.

## Modes

`developer` mode uses the complete terminology, verb, sentence, punctuation,
structure, and content rules. It permits the full project glossary.

`strict` mode also requires a reviewed glossary, treats each linter warning as
a failure, and requires the human procedure checks in `conformance.md`.
Name the actor in a condition when this change preserves the source meaning.
