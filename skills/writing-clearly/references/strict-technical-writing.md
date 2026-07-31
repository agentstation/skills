# Strict technical writing

Use this mode for safety text, procedures, error messages, and requests for
ASD-STE100-style writing. It is an operational subset of Simplified Technical
English, not a certified ASD-STE100 check.

## Terms

- Use one name for one thing.
- Give each word one meaning in the same passage.
- Prefer a short common word when it preserves the technical meaning.
- Keep approved technical terms, product names, API names, and commands exact.
- Use American spelling unless the user or repository requires another form.

## Verbs

- Use active voice when the actor is known.
- Express an action with a verb, not a noun phrase.
- Prefer a simple tense.
- Avoid stacked auxiliary verbs and vague modal hedges.
- Do not replace a precise technical verb only to make it shorter.

## Sentences and procedures

- Put one instruction in each sentence.
- Aim for at most 20 words in an instruction and 25 words in a descriptive
  sentence. Split a longer sentence unless the split would reduce accuracy.
- Put a condition before the instruction that depends on it.
- Use a numbered vertical list for a sequence.
- Start each procedure step with an imperative verb.
- Do not use contractions or semicolons.
- Keep each paragraph on one topic and at most six sentences.

## Final check

1. Does each instruction perform one action?
2. Does each condition appear before its action?
3. Is the actor clear?
4. Can a verb replace a nominalization?
5. Does one concept have more than one name?
6. Did any simplification change the technical meaning?

The official ASD-STE100 specification contains more rules and an approved-word
dictionary. Consult the current issue for conforming or safety-critical work:
https://www.asd-ste100.org/
