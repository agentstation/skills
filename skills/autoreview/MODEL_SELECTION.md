# Model selection

The built-in score is:

```text
0.45 × intelligence
+ 0.25 × taste
+ 0.20 × (DeepSWE v1.1 pass rate ÷ 10)
+ 0.10 × cost
```

Every axis is higher-is-better. `cost` describes the owner's effective credits
and limits, not vendor list price. DeepSWE is evidence about long-horizon
implementation under `mini-swe-agent`; it is not a direct code-review
benchmark, so it receives 20% rather than controlling selection.

The July 30, 2026 built-in snapshot uses high effort for review defaults:

| candidate | harness/model | cost | intelligence | taste | DeepSWE v1.1 |
| --- | --- | ---: | ---: | ---: | ---: |
| `sol` | Codex / GPT-5.6 Sol | 9 | 9 | 8.5 | 69% |
| `opus5` | Claude / Opus 5 | 4 | 9 | 9 | 73% |
| `terra` | Codex / GPT-5.6 Terra | 9 | 8 | 8 | 54% |
| `luna` | Codex / GPT-5.6 Luna | 10 | 6 | 7 | 44% |
| `opus48` | Claude / Opus 4.8 | 4 | 7 | 8 | 52% |
| `sonnet5` | Claude / Sonnet 5 | 5 | 5 | 7 | 48% |
| `fable5` | Claude / Fable 5 | 2 | 9 | 9 | 69% |

Fable's score never participates in automatic selection because its candidate
is explicit-only. The default Claude cap stays at high: DeepSWE shows Opus 5
high and xhigh effectively tied while Anthropic documents substantially higher
token use above high. Sol can be selected explicitly at xhigh for unusually
hard, high-risk review.

Update procedure:

1. Recompute the high-effort benchmark column from the current DeepSWE release.
2. Revisit owner scores for actual credits, unsupervised capability, and taste.
3. Keep benchmark version and date in this file.
4. Run the helper self-tests and hardening suite.
5. Change built-ins only when the evidence affects a fresh install; put
   machine- or project-specific opinions in layered config.
