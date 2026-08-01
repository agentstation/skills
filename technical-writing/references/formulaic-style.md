# Formulaic style

Use these controls to make technical prose direct, specific, and verifiable.
The rules prescribe output style.

## Decision order

1. Preserve each fact, technical meaning, and exact source form.
2. Preserve an approved project term.
3. Apply an explicit project exception.
4. Replace a prohibited phrase or restricted word with precise prose.
5. Review a rhetorical pattern that the linter cannot evaluate in context.

## Prohibited phrases

The `formulaic_phrase` rule checks selected phrases in these groups:

- inflated importance, such as `plays a pivotal role` and
  `underscores the importance`.
- abstract exploration, such as `delve into` and `in the realm of`.
- decorative metaphor, such as `rich tapestry` and
  `serves as a testament`.
- unsupported consequence, such as `far-reaching implications` and
  `a significant milestone`.
- generic understanding or change, such as `valuable insights` and
  `a significant step forward`.
- empty framing, such as `at its core` and `when it comes to`.
- canned context, such as `in today's fast-paced world`.

The linter reports the first occurrence and each later occurrence. Replace the
phrase with the relevant mechanism, measurement, scope, or causal relationship.
Delete it when it adds no information.

The `assistant_scaffold` rule reports each canned preamble and closing. Examples
include `certainly, here is`, `I would be happy to`, `hope this helps`, and
`let me know if you want`. Start with the answer. End after the last useful
fact or action.

## Restricted vocabulary

The `restricted_vocabulary` rule reports each restricted word. The built-in
list contains words with a direct controlled-writing replacement and a low
risk of technical ambiguity:

- `boast`, `delve`, `garner`, and their listed inflections.
- `groundbreaking`, `meticulous`, `multifaceted`, `paramount`, and
  `transformative`.
- `intricate`, `intricacy`, `profound`, `showcase`, `surpass`, `tapestry`, and
  their listed inflections.
- `vibrant` and `vibrantly`.

Replace the word with a precise common term or state the exact fact. Use
`[restricted_vocabulary].additional` for project-specific restrictions. Use
`[restricted_vocabulary].exceptions` for exact technical forms that the
project permits.

Do not place a word in the built-in list when it has a common technical use.
Handle contextual terms through a precise phrase rule, human review, a project
restriction, or a glossary. Examples include `align`, `advancement`, `beacon`,
`comprehend`, `critical`, `elevate`, `emphasize`, `ensure`, `environment`,
`framework`, `harness`, `landscape`, `lens`, `realm`, `roadmap`, `robust`,
`significant`, and `underscore`.

For example, `statistically significant` is precise. `Significant improvement`
needs a measurement. `Critical section` is a software term. `Critical
capability` needs evidence. `Underscore` can name an identifier character.

## Rhetorical patterns

The `negative_parallelism` rule reports each configured form:

- `not just X, but also Y`.
- `not only X, but also Y`.
- `it is not X. It is Y`.
- `no X, no Y, just Z`.

Keep a contrast when the source, user, or technical distinction requires it.
Otherwise, state the direct claim. Add an exact exception when a required
contrast repeatedly triggers the rule.

The linter cannot reliably evaluate these patterns. Review them manually:

- an imaginary misconception that no source or user stated.
- three near-synonyms used for rhythm instead of precision.
- a question fragment such as `The catch?` or `The result?`.
- a significance cue that tells the reader what to find important.
- a vague concession that precedes an unsupported benefit or challenge.
- an ornamental copula such as `serves as` or `stands as`.
- a repeated conclusion or staged closing verdict.
- an invented label that has no defined mechanism.
- repeated bold-label bullets or headings that do not improve navigation.

Also review these context-dependent forms when they add unsupported emphasis:

- `quietly` before a claim about change, power, collapse, or reinvention.
- metaphorical relabeling with `in disguise`, `hiding behind`, or
  `wearing a different hat`.
- conversational pivots such as `here is the thing` or `plot twist`.
- staged reactions such as `what surprised me most` or `what struck me`.
- unsupported cues such as `this matters because` or
  `the insight everyone is missing`.
- clipped trailing negations such as `no guessing` or `no wasted motion`.

## Protected content

The linter protects these forms:

- fenced code, inline code, and code-like identifiers.
- Markdown block quotations and paired double quotations.
- commands and logs formatted as code or a recognized log record.
- Markdown tables and front matter.
- approved glossary terms.
- exact configured exceptions.

Format an exact identifier or command as code. Format exact source prose as a
quotation. A protected term does not suppress a larger prohibited phrase that
contains it.

## Source comments

The linter extracts comments and docstrings from supported source files. It
masks executable code, string literals, directives, and structured values. It
does not process an unsupported source file as prose.

Python uses its tokenizer and syntax tree. C-like languages use a comment-aware
scanner for line and block comments. Shell and Ruby use full-line hash comments.
TOML and YAML use quote-aware hash comments. HTML uses markup-aware extraction
for visible text and comment blocks.

## Research use

Corpus vocabulary research supplies candidates for controlled-writing rules.
A candidate enters the built-in restricted list only when it also has a clear
prescriptive reason, a direct replacement, and low technical ambiguity. The
research does not change rule severity. Each configured occurrence remains a
separate conformance finding.

The source record is in [`../UPSTREAM.md`](../UPSTREAM.md).
