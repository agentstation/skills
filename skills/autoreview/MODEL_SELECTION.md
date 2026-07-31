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

Cost uses the average `cost_usd` of included, full-scope, high-effort trials in
the [DeepSWE v1.1 data](https://deepswe.datacurve.ai/data/v1.1). Normalize each
model's measured average to the most expensive candidate, Fable 5:

```text
cost = 10 × model average cost per task ÷ Fable average cost per task
```

The July 30, 2026 snapshot uses DeepSWE's current cost corrections and rounds
the normalized score to one decimal. Subscription scarcity is a separate policy
concern. Fable's current Claude plan treatment is unusually restrictive, but
that affects `manual_approval`, not its measured cost score.

## Candidate snapshot

The built-in snapshot uses high effort for review defaults:

Each candidate ID names a complete reviewer configuration: harness, model,
effort, scores, and approval policy. The harness and model are separate.
Candidates are ordered by intelligence descending; taste and pass rate break
intelligence ties:

| candidate ID | intelligence | harness | model | effort | avg cost/task | cost | manual approval | taste | DeepSWE pass |
| --- | ---: | --- | --- | :---: | ---: | ---: | :---: | ---: | ---: |
| `opus5` | 9 | Claude Code CLI | Opus 5 | high | $6.08 | 6.6 | no | 9 | 73% |
| `fable5` | 9 | Claude Code CLI | Fable 5 | high | $9.18 | 10 | yes | 9 | 69% |
| `sol` | 9 | Codex CLI | GPT-5.6 Sol | high | $3.47 | 3.8 | no | 8.5 | 69% |
| `terra` | 8 | Codex CLI | GPT-5.6 Terra | high | $0.91 | 1.0 | no | 8 | 54% |
| `opus48` | 7 | Claude Code CLI | Opus 4.8 | high | $4.28 | 4.7 | no | 8 | 52% |
| `luna` | 6 | Codex CLI | GPT-5.6 Luna | high | $0.16 | 0.2 | no | 7 | 44% |
| `sonnet5` | 5 | Claude Code CLI | Sonnet 5 | high | $7.43 | 8.1 | no | 7 | 48% |

Fable never participates in automatic selection because it requires manual
approval, independently of its cost score. The default Claude cap stays at
high: DeepSWE shows Opus 5 high and xhigh effectively tied while Anthropic
documents substantially higher token use above high. Sol can be selected
explicitly at xhigh for unusually hard, high-risk review.

Update procedure:

1. Recompute the high-effort benchmark column from the current DeepSWE release.
2. Recompute high-effort average cost per task and normalized cost.
3. Revisit owner scores for unsupervised capability and taste.
4. Keep the benchmark version and snapshot date in this file.
5. Run the helper self-tests and hardening suite.
6. Change built-ins only when the evidence affects a fresh install; put
   machine- or project-specific opinions in layered config.
