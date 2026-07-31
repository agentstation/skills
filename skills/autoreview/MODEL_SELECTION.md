# Model selection

The automatic-selection formula is:

```text
0.45 × intelligence
+ 0.25 × taste
+ 0.20 × (DeepSWE v1.1 pass rate ÷ 10)
+ 0.10 × (10 − cost)
```

`intelligence` and `taste` are owner-calibrated from real model use at the
configured effort; they are not aliases for benchmark rank. DeepSWE separately
provides pass rate and measured task cost under `mini-swe-agent`. `cost` is
literal: 0 is free and 10 is the most expensive candidate, so the formula
inverts it. DeepSWE is not a direct code-review benchmark, so pass rate receives
20% rather than controlling selection.

## Cost basis

Cost uses the average `cost_usd` of included, full-scope trials at the selected
effort in the [DeepSWE v1.1 data](https://deepswe.datacurve.ai/data/v1.1).
Normalize each model/effort pair to Fable 5 at high, the most expensive selected
pair:

```text
cost = 10 × model/effort average cost per task ÷ $9.18
```

The July 30, 2026 snapshot uses DeepSWE's current cost corrections and rounds
the normalized score to one decimal. Subscription scarcity is a separate policy
concern. Fable's current Claude plan treatment is unusually restrictive, but
that affects `manual_approval_required`, not its measured cost score.

## Claude allocation policy

Treat the Claude subscription as two purpose-specific allocations:

- Reserve the limited Fable 5 allocation for manually requested review of
  architecture-sensitive or exceptionally complex changes.
- Use Opus 5 high for routine code review. It remains the default Claude-side
  reviewer because its code-review price/performance is stronger and its
  allocation is normally more available.

Fable's higher intelligence score does not make it the automatic code-review
default. Use-case policy and manual approval take precedence over score.

## Selected sweet spots

No Anthropic model/effort pair above `high` is eligible. For other providers,
higher effort remains eligible when the capability gain justifies its marginal
cost. The table intentionally includes only useful review operating points, not
every measured effort.

Rows are ordered by owner intelligence score descending; pass rate and then
cost break ties. Model and candidate ID come first so each row is identifiable.
A layered configuration can retain the same candidate ID while overriding its
effort and matching benchmark inputs. `selection score` is the result of the
formula above. Eligibility, host isolation, profile constraints, and manual
approval are applied before score ranking.

| model | candidate ID | intelligence | taste | DeepSWE Pass@1 | selection score | harness | effort | when to use | cost/task | manual approval required |
| --- | --- | ---: | ---: | ---: | ---: | --- | :---: | --- | ---: | :---: |
| Fable 5 | `fable5` | 10 | 9 | 69% | 8.13 | Claude Code CLI | high | Explicit manual profile for architecture-sensitive or exceptionally complex change review | $9.18 | yes |
| GPT-5.6 Sol | `sol` | 9 | 8 | 71% | 7.96 | Codex CLI | xhigh | Layered override for complex, high-risk, or intelligence-critical review | $4.70 | no |
| GPT-5.6 Sol | `sol` | 8.5 | 8 | 69% | 7.83 | Codex CLI | high | Built-in automatic reviewer when the host is Claude | $3.47 | no |
| Opus 5 | `opus5` | 8 | 8.5 | 73% | 7.52 | Claude Code CLI | high | Built-in default code reviewer when the host is Codex | $6.08 | no |
| GPT-5.6 Terra | `terra` | 8 | 7 | 70% | 7.32 | Codex CLI | max | Built-in `value` profile for near-frontier quality at lower cost | $3.96 | no |
| Opus 5 | `opus5` | 7.5 | 8.5 | 69% | 7.52 | Claude Code CLI | medium | Layered Claude value override when cost matters | $3.29 | no |
| GPT-5.6 Luna | `luna` | 6 | 6 | 67% | 6.47 | Codex CLI | max | Built-in `budget` profile for low-cost or high-volume review | $0.61 | no |

The built-in automatic pool uses Opus 5 high, Sol high, Terra max, and Luna max:

- Opus 5 high is the default code-review sweet spot. It matches xhigh at 73%
  while saving $2.99 per task, stays within the Anthropic ceiling, and uses the
  Claude allocation intended for code review.
- Sol high remains the standard Codex reviewer. Sol xhigh is the sweet spot
  when complexity, risk, or required reviewer intelligence justifies the
  additional cost; max buys only two more pass points for another $3.69 over
  xhigh.
- Terra max is the value profile: 70% at $3.96.
- Luna max is the budget profile: 67% at only $0.61. Its lower efforts remain
  on the mathematical cost/pass frontier, but are not credible PR review
  defaults.
- Opus 5 medium is a documented Claude value alternative for layered config,
  but automatic Codex-hosted review retains high for the stronger quality gate.
- Fable high remains available only through an explicit manual CLI request for
  architecture-sensitive or exceptionally complex change review. It never
  participates in scored selection, automatic review, config or environment
  defaults, or fallback.

Opus 4.8, Sonnet 5/4.6, GPT-5.5/5.4, Kimi, Grok, Muse, Gemini, and GLM do not
enter the built-in pool. Their supplied rows are dominated on pass rate and
cost by a selected operating point, or they lack a justified isolation-safe
default harness. Anthropic xhigh and max rows are excluded by policy regardless
of benchmark result.

Update procedure:

1. Recompute the allowed model/effort frontier from the current DeepSWE release.
2. Recompute selected-effort average cost per task and normalized cost.
3. Revisit owner scores for unsupervised capability and taste.
4. Recompute the displayed selection scores from the executable formula.
5. Review Anthropic's current model-specific guidance for
   [Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5),
   [Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5),
   and
   [Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
   before changing Claude prompt scaffolding or effort policy.
6. Keep the benchmark version and snapshot date in this file.
7. Run the helper self-tests and hardening suite.
8. Change built-ins only when the evidence affects a fresh install; put
   machine- or project-specific opinions in layered config.
