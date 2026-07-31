# Model selection

The built-in score is:

```text
0.45 × intelligence
+ 0.25 × taste
+ 0.20 × (DeepSWE v1.1 pass rate ÷ 10)
+ 0.10 × (10 − cost)
```

`intelligence`, `taste`, and benchmark performance are higher-is-better.
`cost` is literal: 0 is free and 10 is the most expensive candidate. The
formula inverts cost so lower-cost candidates score higher. DeepSWE provides
both the pass rate and measured task cost under `mini-swe-agent`. It is not a
direct code-review benchmark, so pass rate receives 20% rather than controlling
selection.

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

## Selected sweet spots

No Anthropic model/effort pair above `high` is eligible. For other providers,
higher effort remains eligible when the capability gain justifies its marginal
cost. The table intentionally includes only useful review operating points, not
every measured effort.

Rows are ordered by owner intelligence score descending; pass rate and then
cost break ties. Model and candidate ID come first so each row is identifiable.
A layered configuration can retain the same candidate ID while overriding its
effort and matching benchmark inputs.

| model | candidate ID | intelligence | taste | harness | effort | when to use | cost/task | manual approval required |
| --- | --- | ---: | ---: | --- | :---: | --- | ---: | :---: |
| Opus 5 | `opus5` | 9 | 9 | Claude Code CLI | high | Default automatic reviewer when the host is Codex | $6.08 | no |
| GPT-5.6 Sol | `sol` | 9 | 8.5 | Codex CLI | xhigh | Complex or high-risk review; Nimbus Codex candidate | $4.70 | no |
| Opus 5 | `opus5` | 9 | 9 | Claude Code CLI | medium | Layered Claude value override when cost matters | $3.29 | no |
| GPT-5.6 Sol | `sol` | 9 | 8.5 | Codex CLI | high | Default automatic reviewer when the host is Claude | $3.47 | no |
| Fable 5 | `fable5` | 9 | 9 | Claude Code CLI | high | Only when the user explicitly requests and approves Fable | $9.18 | yes |
| GPT-5.6 Terra | `terra` | 8 | 8 | Codex CLI | max | `value` profile for near-frontier quality at lower cost | $3.96 | no |
| GPT-5.6 Luna | `luna` | 6 | 7 | Codex CLI | max | `budget` profile for low-cost or high-volume review | $0.61 | no |

The built-in automatic pool uses Opus 5 high, Sol high, Terra max, and Luna max:

- Opus 5 high is the quality sweet spot. It matches xhigh at 73% while saving
  $2.99 per task, and stays within the Anthropic ceiling.
- Sol high remains the standard Codex reviewer. Sol xhigh is the complex-task
  sweet spot and is used by Nimbus; max buys only two more pass points for
  another $3.69 over xhigh.
- Terra max is the value profile: 70% at $3.96.
- Luna max is the budget profile: 67% at only $0.61. Its lower efforts remain
  on the mathematical cost/pass frontier, but are not credible PR review
  defaults.
- Opus 5 medium is a documented Claude value alternative for layered config,
  but automatic Codex-hosted review retains high for the stronger quality gate.
- Fable high remains available only by manual approval and never participates
  in automatic selection or fallback.

Opus 4.8, Sonnet 5/4.6, GPT-5.5/5.4, Kimi, Grok, Muse, Gemini, and GLM do not
enter the built-in pool. Their supplied rows are dominated on pass rate and
cost by a selected operating point, or they lack a justified isolation-safe
default harness. Anthropic xhigh and max rows are excluded by policy regardless
of benchmark result.

Update procedure:

1. Recompute the allowed model/effort frontier from the current DeepSWE release.
2. Recompute selected-effort average cost per task and normalized cost.
3. Revisit owner scores for unsupervised capability and taste.
4. Keep the benchmark version and snapshot date in this file.
5. Run the helper self-tests and hardening suite.
6. Change built-ins only when the evidence affects a fresh install; put
   machine- or project-specific opinions in layered config.
