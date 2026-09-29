# Model selection

The automatic-selection formula is:

```text
0.45 × intelligence
+ 0.25 × taste
+ 0.20 × (DeepSWE v1.1 pass rate ÷ 10)
+ 0.10 × (10 − cost)
```

Owners calibrate `intelligence` and `taste` from model use at the configured
effort. These values do not represent benchmark rank.

DeepSWE reports pass rate and measured task cost. It measures both under
`mini-swe-agent`.

`cost` is literal: 0 is free and 10 is the most expensive candidate, so the
formula inverts it. DeepSWE is not a direct code-review benchmark, so pass rate
receives 20% rather than controlling selection.

## Cost basis

Cost uses the average `cost_usd` of included, full-scope trials at the
selected effort. The source is the
[DeepSWE v1.1 data](https://deepswe.datacurve.ai/data/v1.1).
Normalize each model/effort pair to the $9.18 Fable high reference, the most
expensive selected pair:

```text
cost = 10 × model/effort average cost per task ÷ $9.18
```

The July 30, 2026 snapshot uses DeepSWE's current cost corrections and rounds
the normalized score to one decimal. Subscription scarcity is a separate policy
concern. Fable's current Claude plan treatment is unusually restrictive, but
that affects `manual_approval_required`, not its measured cost score.

### Provisional September 22 and 29, 2026 inputs

Opus 5.5, GPT-6.1 Sol, GPT-6 Luna, and Fable 5.1 do not have DeepSWE rows at
the selected efforts yet. Until DeepSWE publishes them, the built-ins use these
provisional inputs:

A provisional cost is the predecessor's DeepSWE cost at the same effort ×
the measured AA cost-per-task ratio at that effort (see
[AA cost per task](#aa-cost-per-task)). Vendor cost claims are not used.

- GPT-6.1 Sol uses the vendor-reported DeepSWE v1.1 pass rate at high: 75.2%.
  The cost uses the measured GPT-5.6 Sol high cost: $2.66 × ($0.319 ÷ $0.808)
  = $1.05 per task. The GPT-6 Sol provisional $1.23 × ($0.319 ÷ $0.375) gives
  the same $1.05.
- Opus 5.5 keeps the Opus 5 high pass rate of 73%. The cost is
  $6.08 × ($1.823 ÷ $3.613) = $3.07 per task. AA measures a 50% cost cut at
  high. Anthropic reports 40%.
- GPT-6 Luna keeps the GPT-5.6 Luna max pass rate of 67%. The cost is
  $0.61 × ($0.068 ÷ $0.178) = $0.23 per task.
- Fable 5.1 keeps the Fable 5 high pass rate and the $9.18 reference cost. AA
  publishes Fable 5 only at max, so no same-effort ratio exists.

Replace every provisional input with measured DeepSWE data when it is
available.

## Owner scores

Owner intelligence and taste use one scale in `~/.agents/AGENTS.md` and in this
file. The September 22, 2026 calibration uses these values:

| model | intelligence | taste | knee effort | AA index at knee | base |
| --- | ---: | ---: | :---: | ---: | ---: |
| Fable 5.1 | 10 | 10 | high | 51.2 | 8.3 |
| Opus 5.5 | 9 | 9 | high | 53.6 | 8.9 |
| GPT-6 Astra | 8 | 8 | high | 50.9 | 8.2 |
| GPT-6.1 Sol | 7.5 | 7 | medium | 47.8 | 7.5 |
| GPT-5.6 Terra | 6 | 6.5 | max | 42.1 | 6.0 |
| GPT-6 Luna | 5 | 5.5 | max | 37.3 | 4.8 |
| Sonnet 5 | 3.5 | 7 | high | 31.7 | 3.4 |

- Intelligence anchors to the Artificial Analysis (AA) Intelligence Index at
  each model's price/performance knee, not at max. The knee is the last effort
  before the cost of each extra index point rises about 3 times or more. For
  Anthropic models, the knee is also capped at `high`.
- `(index − 18) ÷ 4` sets the base, so 4 index points are about 1 score point.
  DeepSWE at the same effort corrects the base. Sonnet 5 high gets no
  correction, because it passes 48%.
- The GPT-6.1 Sol score is provisional from September 29, 2026. Its knee is
  medium: medium → high costs 2.9 times more per point, the same ratio that
  makes high the Astra knee. The base is 7.45. It gets no DeepSWE correction,
  because no pass rate exists at medium. The vendor-reported 75.2% at high is
  above Astra, so a measured row can raise the score. Its taste carries over
  from GPT-6 Sol until use verifies it. GPT-6 Sol had 6.5 and 7.
- Fable 5.1 is 10 by owner call for code and architecture. On AA, it is off
  the cost frontier at every effort. Its interface-design taste is not yet
  verified.
- Taste uses 1-point steps: Fable 5.1 > Opus 5.5 > GPT-6 Astra > GPT-6.1 Sol.
  Arena WebDev human votes rank Claude models above GPT-5.6 Sol for interface
  work. Opus 5.5 and GPT-6 Sol did not have Arena rows on September 22, 2026.
- A candidate uses its model's scores at every configured effort.

## AA cost per task

On September 22, 2026, the AA Intelligence Index model pages gave these
results. The GPT-6.1 Sol row is from September 29, 2026. Each cell is index points, then the measured USD cost to run the
index, divided by task count. JavaScript read the values from the embedded
data of the `artificialanalysis.ai/models/<model>-<effort>` pages. For a
model with no effort suffix, AA reports the max effort.

| model | low | medium | high | xhigh | max |
| --- | --- | --- | --- | --- | --- |
| Opus 5.5 | 42.3 $0.55 | 51.2 $1.34 | **53.6 $1.82** | **56.0 $3.46** | **57.6 $5.98** |
| Fable 5.1 | 46.8 $2.37 | 48.9 $2.98 | 51.2 $3.91 | 53.2 $5.98 | 53.4 $7.63 |
| GPT-6 Astra | 45.8 $0.82 | 49.6 $1.54 | 50.9 $1.73 | 52.4 $2.31 | 52.7 $3.26 |
| GPT-6.1 Sol | **42.1 $0.13** | **47.8 $0.21** | **50.2 $0.32** | **51.0 $0.39** | **51.8 $0.72** |
| GPT-6 Sol | 33.9 $0.13 | 39.8 $0.25 | 42.8 $0.37 | 44.1 $0.53 | 47.5 $1.06 |
| GPT-5.6 Terra | 27.5 $0.14 | 30.1 $0.18 | 34.2 $0.34 | 38.0 $0.63 | 42.1 $1.40 |
| GPT-6 Luna | **20.9 $0.004** | **29.5 $0.02** | **32.1 $0.03** | **33.9 $0.04** | **37.3 $0.07** |
| Sonnet 5 | 24.3 $0.51 | 28.1 $1.00 | 31.7 $1.79 | 34.4 $2.87 | 38.2 $5.09 |

Bold cells are on the cost frontier across all rows. The cost of each extra
index point at each effort step, from low to max, is:

| model | low→medium | medium→high | high→xhigh | xhigh→max |
| --- | ---: | ---: | ---: | ---: |
| Opus 5.5 | $0.09 | $0.21 | $0.68 | $1.54 |
| Fable 5.1 | $0.29 | $0.42 | $1.01 | $10.87 |
| GPT-6 Astra | $0.19 | $0.14 | $0.40 | $3.30 |
| GPT-6.1 Sol | $0.01 | $0.04 | $0.09 | $0.42 |
| GPT-6 Sol | $0.02 | $0.04 | $0.12 | $0.15 |
| GPT-5.6 Terra | $0.02 | $0.04 | $0.08 | $0.19 |
| GPT-6 Luna | $0.00 | $0.00 | $0.01 | $0.01 |
| Sonnet 5 | $0.13 | $0.22 | $0.40 | $0.59 |

- Opus 5.5 high is the knee. Xhigh costs 3.2 times more per point. Opus 5.5
  medium dominates Astra medium and high and Fable up to high. Opus 5.5 high
  dominates Fable xhigh and max.
- GPT-6.1 Sol dominates every GPT-6 Sol, GPT-5.6 Terra, and GPT-6 Astra row
  up to Astra high. GPT-6.1 Sol max also dominates Opus 5.5 medium: 0.6 more
  index points at 54% of the cost.
- GPT-6.1 Sol medium is the knee. See
  [GPT-6.1 Sol effort](#gpt-61-sol-effort) for the routed efforts.
- Terra keeps the `value` profile only for its measured 70% DeepSWE pass
  rate. GPT-6.1 Sol high beats it on AA and on the vendor-reported DeepSWE
  rate at 27% of its DeepSWE cost per task. Review that profile when DeepSWE measures GPT-6.1
  Sol.
- GPT-6 Luna max is on the frontier at $0.07 and is the cheapest route to 37
  index points.
- Sonnet 5 high scores below GPT-6 Luna high at about 60 times the cost.

The AA ratio of the new model to its predecessor at the same effort is 0.50
for Opus 5.5 high, 0.46 for GPT-6 Sol high, 0.85 for GPT-6.1 Sol high against
GPT-6 Sol high, and 0.38 for GPT-6 Luna max. The
provisional DeepSWE costs use these ratios.

## Task routing evidence

`~/.agents/AGENTS.md` routes each problem type to a model and effort. The AA
cost-per-task data supports each row:

- Escalate the model before the effort, except for GPT-6.1 Sol. Opus 5.5
  high → xhigh costs $0.68 per point. GPT-6.1 Sol high → xhigh costs $0.09
  per point, and xhigh matches Opus 5.5 medium at 29% of the cost.
- Do not use low effort for Opus 5.5 or GPT-6.1 Sol. Low → medium is the
  cheapest step on each curve: $0.09 per point for Opus and $0.01 for Sol.
- GPT-6.1 Sol medium is on the frontier at 47.8 points and $0.21. It fits
  high-volume simple work. It scores more than GPT-6 Sol xhigh at 41% of the
  cost.
- Opus 5.5 medium is on the frontier at 51.2 points and $1.34. It dominates GPT-6
  Astra at medium and high, Fable 5.1 up to high, and Sonnet 5 at high and
  above. Sol and Luna dominate Sonnet 5 at low and medium. It fits exploration, search, and short copy.
- Opus 5.5 high is the knee for feature work, debugging, refactors,
  architecture, interface design, and prose. It also has the second-highest
  taste score.
- Sonnet 5 has no routed job. At high, it scores 31.7 at $1.79. Opus 5.5
  medium scores 19.5 points more at 75% of the cost, with higher taste.

Claude Code sets a subagent's effort only from its agent definition. The
`explorer` agent runs Opus 5.5 medium, and the `implementer` agent runs Opus
5.5 high. The Codex plugin accepts `--effort` up to xhigh for each job.

### GPT-6.1 Sol effort

Use high by default and xhigh for a hard case. Never use max. The AA
September 29, 2026 data for each step is:

| step | index points | cost per task | cost per point | Terminal-Bench 4.0 | AutomationBench | time per task |
| --- | ---: | ---: | ---: | --- | --- | ---: |
| medium → high | +2.5 | +49% | $0.04 | 0.480 → 0.515 | 0.626 → 0.645 | +30% |
| high → xhigh | +0.8 | +23% | $0.09 | 0.515 → 0.540 | 0.645 → 0.666 | +29% |
| xhigh → max | +0.8 | +84% | $0.42 | 0.540 → 0.561 | 0.666 → 0.649 | +84% |

Time per task is the Terminal-Bench 4.0 time.

- High buys the largest agentic gain above medium for 49% more cost.
- Xhigh is the cheapest escalation on the chart. It costs $0.39 per task,
  against $1.34 for Opus 5.5 medium at the same index. It is 29% slower, so
  keep it for long flows, actions that cannot be undone, and retries.
- Max costs 4.5 times more per point than xhigh and nearly doubles the time.
  It loses 1.7 points on AutomationBench. On AA Briefcase it takes 2.6 times
  the xhigh time. Escalate to Opus 5.5 high instead: 53.6 points at $1.82.
- The medium knee sets the intelligence score only. Routed efforts follow the
  rows above.

### Computer and browser use

GPT-6.1 Sol replaces GPT-6 Astra for computer and browser use. No public
source reports OSWorld by effort. The only direct measure is the vendor
OSWorld 2.0 offline result at max: GPT-6.1 Sol scores 71.4% at $1.27 per task,
and Astra scores 73.5% at $9.44. The AA agentic evaluations below are the
per-effort proxies. None of them drives a GUI. MMMU-Pro measures the visual
reasoning that screenshot work needs. Each cell is score, cost per task, and
time per task.

| evaluation | Astra medium | Sol 6.1 medium | Sol 6.1 high | Sol 6.1 xhigh | Astra high |
| --- | --- | --- | --- | --- | --- |
| AA index | 49.6, $1.54 | 47.8, $0.21 | 50.2, $0.32 | 51.0, $0.39 | 50.9, $1.73 |
| AA Briefcase (Elo) | 1459, $3.94, 9.5m | 1365, $0.46, 5.1m | 1471, $0.84, 8.8m | 1507, $1.04, 11.2m | 1507, $4.76, 11.0m |
| GDPval-AA (Elo) | 1468, $1.82, 4.7m | 1433, $0.23, 2.7m | 1486, $0.43, 4.9m | 1510, $0.56, 6.6m | 1485, $2.43, 6.4m |
| AutomationBench | 0.646, $1.18, 2.8m | 0.626, $0.20, 2.0m | 0.645, $0.23, 2.4m | 0.666, $0.25, 2.7m | 0.666, $1.30, 3.1m |
| Terminal-Bench 4.0 | 0.495, $4.43, 10.7m | 0.480, $0.61, 8.7m | 0.515, $0.83, 11.3m | 0.540, $1.03, 14.6m | 0.540, $4.05, 10.4m |
| MMMU-Pro | 0.850 | 0.839 | 0.849 | 0.850 | 0.864 |

- Sol 6.1 high equals or beats Astra medium on every agentic proxy at 19% to
  24% of the cost per task, in about the same time. It is 0.001 below on
  AutomationBench and MMMU-Pro.
- Sol 6.1 xhigh ties Astra high on Briefcase, AutomationBench, and
  Terminal-Bench, and beats it on GDPval, at 19% to 25% of the cost. It is
  about 40% slower on Terminal-Bench and 1.4 points lower on MMMU-Pro.
- Sol 6.1 medium is below Astra medium on every proxy, by 94 Briefcase Elo
  and 2 AutomationBench points, at 12% to 17% of the cost.
- Screenshot loops send many input tokens. GPT-6.1 Sol input costs one fifth
  of Astra input, and cached input costs one tenth. The cost ratio holds or
  improves for screen work.
- Route computer and browser use to Sol 6.1 high. Use xhigh for long flows,
  actions that cannot be undone, and retries. Astra needs an explicit request.
  Recheck this choice when OSWorld publishes results by effort.

## DeepSWE effort frontier

The DeepSWE v1.1 leaderboard on September 22, 2026 had these rows for the
selected families. A frontier row has no other row with a higher or equal pass
rate at a lower or equal cost.

| model | low | medium | high | xhigh | max |
| --- | --- | --- | --- | --- | --- |
| GPT-6 Astra | 67% $1.60 | **73% $3.08** | 73% $3.92 | **74% $4.43** | 73% $7.50 |
| Opus 5 | 58% $1.66 | 69% $3.29 | 73% $6.08 | 73% $9.07 | 74% $11.84 |
| GPT-5.6 Sol | 45% $0.82 | 61% $1.42 | **69% $2.66** | 71% $3.60 | 73% $6.46 |
| Fable 5 | 60% $3.76 | 65% $6.09 | 69% $9.18 | 70% $13.41 | 70% $21.63 |
| GPT-5.6 Luna | **2% $0.01** | **11% $0.04** | **44% $0.16** | **57% $0.31** | **67% $0.61** |
| Sonnet 5 | 31% $2.19 | 40% $4.08 | 48% $7.43 | 50% $11.89 | 54% $26.40 |

Bold rows are on the frontier. The frontier is Luna up to 67%, then GPT-5.6 Sol
high, then Astra medium and xhigh. Opus, Fable, and Sonnet rows are not on the
frontier at any effort. Sol high is the knee of the Sol curve: xhigh adds 2
points for 35% more cost, and max adds 4 points for 2.4 times the cost.

OpenAI reports GPT-6.1 Sol high at 75.2%, above every measured row. The
estimated cost at high is $1.05. If DeepSWE confirms it, GPT-6.1 Sol high
becomes the frontier point above GPT-6 Luna. OpenAI reports GPT-6 Luna high at 66.6%, so GPT-6 Luna can move
the low-cost frontier when DeepSWE measures it.

Astra is not a review candidate. Use it only on explicit request, except for
the computer-use rule in `~/.agents/AGENTS.md`.

## Claude allocation policy

Treat the Claude subscription as two purpose-specific allocations:

- Reserve the limited Fable 5.1 allocation for manually requested review of
  architecture-sensitive or exceptionally complex changes.
- Use Opus 5.5 high for routine code review. It remains the default Claude-side
  reviewer because its code-review price/performance is stronger and its
  allocation is normally more available. Anthropic reports that Opus 5.5 high
  caught 72% of known bugs in code review, against 56% for Opus 5 high.

Fable's higher intelligence score does not make it the automatic code-review
default. Use-case policy and manual approval take precedence over score.

## Selected sweet spots

No Anthropic model/effort pair above `high` is eligible. For other providers,
higher effort remains eligible when the capability gain justifies its marginal
cost. The table intentionally includes only useful review operating points, not
every measured effort.

The table orders rows by descending owner intelligence score. Pass rate and then
cost break ties. Model and candidate ID come first so each row is identifiable.
A layered configuration can retain the same candidate ID while overriding its
effort and matching benchmark inputs. Candidate IDs name the model family, so
`opus5` selects Opus 5.5 and `fable5` selects Fable 5.1. `selection score` is
the result of the formula above. Eligibility, host isolation, profile
constraints, and manual approval apply before score ranking.

| model | candidate ID | intelligence | taste | DeepSWE Pass@1 | selection score | harness | effort | when to use | cost/task | manual approval required |
| --- | --- | ---: | ---: | ---: | ---: | --- | :---: | --- | ---: | :---: |
| Fable 5.1 | `fable5` | 10 | 10 | 69% | 8.38 | Claude Code CLI | high | Explicit manual profile for architecture-sensitive or exceptionally complex change review | $9.18 | yes |
| Opus 5.5 | `opus5` | 9 | 9 | 73% | 8.43 | Claude Code CLI | high | Built-in default code reviewer when the host is Codex, and second reviewer for a high-risk change | $3.07 | no |
| GPT-6.1 Sol | `sol` | 7.5 | 7 | 75.2% | 7.52 | Codex CLI | high | Built-in automatic reviewer when the host is Claude | $1.05 | no |
| GPT-5.6 Terra | `terra` | 6 | 6.5 | 70% | 6.30 | Codex CLI | max | Built-in `value` profile for near-frontier quality at lower cost | $3.96 | no |
| GPT-6 Luna | `luna` | 5 | 5.5 | 67% | 5.93 | Codex CLI | max | Built-in `budget` profile for low-cost or high-volume review | $0.23 | no |

The built-in automatic pool uses Opus 5.5 high, GPT-6.1 Sol high, GPT-5.6
Terra max, and GPT-6 Luna max:

- Opus 5.5 high is the default Claude-side code reviewer. It stays within the
  Anthropic ceiling and costs less than Opus 5 high.
- GPT-6.1 Sol high is the standard Codex reviewer. It needs Codex CLI 0.159.0
  or later. Do not raise Sol effort for a high-risk change. Add Opus 5.5 high
  as the second reviewer with the `cross-lab` profile.
- Terra max stays the value profile until OpenAI releases a GPT-6 Terra or
  DeepSWE measures GPT-6.1 Sol. On AA, GPT-6.1 Sol high already dominates it.
- GPT-6 Luna max is the budget profile.
- Fable 5.1 high remains available only through an explicit manual CLI request
  for architecture-sensitive or exceptionally complex change review. It never
  participates in scored selection, automatic review, config or environment
  defaults, or fallback.

The built-in pool excludes Opus 5, Opus 4.8, Fable 5, Sonnet 5/4.6,
GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol/Luna, GPT-5.5/5.4, Kimi, Grok, Muse, Gemini, and GLM.
Newer or selected operating points replace or dominate their rows, Astra is an
explicit-request model, and some lack owner-calibrated intelligence and taste
values for scored selection. They remain available through explicit or layered
Kimi Code, OpenCode, Cursor Agent, and Pi candidates.
Policy excludes Anthropic xhigh and max rows regardless of benchmark result.

## Security-review diversity

Model capability and provider policy are separate axes. For authorized security
review, add a heterogeneous second layer through Kimi Code, Cursor Agent,
OpenCode, or Pi. Use Grok 4.5, GLM-5.2, or Kimi K3 when available. These
combinations help with exploit-adjacent code, malware-analysis fixtures,
vulnerability reproduction, protocol abuse, and red-team tests. An OpenAI- or
Anthropic-hosted reviewer may refuse, truncate, or redirect this legitimate
analysis.

This is a diversity recommendation, not a claim that weaker safety policy
automatically produces a better reviewer. Alternative-provider models can have
different blind spots and false-positive rates. Keep review authorized and
defensive, preserve the isolated frozen-bundle boundary, and corroborate
high-impact findings with tests or a second model.

| security-review option | harness | when it adds the most value |
| --- | --- | --- |
| Grok 4.5 | Cursor Agent, OpenCode, or Pi | Adversarial reasoning, exploit-chain review, and code that triggers conservative provider refusals |
| GLM-5.2 | Cursor Agent, OpenCode, or Pi | Independent vulnerability analysis and implementation-level review from a different model family |
| Kimi K3 | Kimi Code, Cursor Agent, OpenCode, or Pi | Long-context security review, cross-file attack-surface tracing, and a third-provider tie-breaker |

These models remain explicit or layered candidates until owner-calibrated
intelligence, taste, and cost inputs justify scored automatic selection.
Cursor model names come from the account catalog. Kimi Code, OpenCode, and Pi
use their runtime model catalogs.

Update procedure:

1. Recompute the allowed model/effort frontier from the current DeepSWE release
   and the AA cost per task by effort.
2. Recompute selected-effort average cost per task and normalized cost.
3. Revisit owner scores for unsupervised capability and taste.
4. Recompute the displayed selection scores from the executable formula.
5. Review current Anthropic model guidance.
   - [Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
   - [Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
   - Check for Opus 5.5 and Fable 5.1 guides. On September 22, 2026, this
     file had no verified links for them.
   - [Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
6. Reconsider the Claude effort policy against that guidance.
7. Keep the benchmark version and snapshot date in this file. Replace the
   provisional inputs when DeepSWE publishes measured rows.
8. Run the helper self-tests and hardening suite.
9. Change built-ins only when evidence affects a fresh install.
10. Put machine- or project-specific opinions in layered config.
