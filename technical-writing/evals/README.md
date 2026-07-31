# Technical-writing evaluations

`evals.json` follows the Agent Skills evaluation shape. It adds categories,
smoke markers, protected literals, and forbidden trap claims.

The suite covers developer responses, READMEs, API errors, technical web pages,
procedures, PRs, release notes, exact content, mode selection, and glossary
terms.

## Cadence

- Run `validate.py` after each skill change.
- Run the eight smoke cases against Codex and Claude before an ordinary PR.
- Run the full set and a blind baseline comparison for a material rule, linter,
  glossary, or bootstrap change.
- Test the global bootstrap in a fresh session with a technical prompt that
  does not name the skill.

## Method

Run each case in a clean context against the candidate and the previous version
or no-skill baseline. Apply the hard gates and scoring rules in `rubric.md`.

Do not commit one response as golden prose. Store run artifacts outside the
skill directory. Record factual failures, terminology failures, linter results,
pairwise preference, tokens, and duration.
