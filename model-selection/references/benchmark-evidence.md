# Model selection evidence

The owner policy is in `~/.agents/AGENTS.md`.
This reference records the evidence for its worker table.

## Sources and dates

- Policy and AA verification date: October 22, 2026.
- [Slopalytics](https://slopalytics.com/) benchmark snapshot:
  October 13, 2026, at 20:47:14.735 UTC.
- Slopalytics publishes AA data, so these sources share benchmark evidence.
- The AA model pages matched all 14 frontier scores and costs during verification.
- AA identifies this benchmark as Intelligence Index v4.3.2.

The comparison uses the current families in the owner's chart, with Haiku excluded.
It also includes the newer Claude Sonnet 5.5.
The compared families are:

- GPT-6 Luna
- GPT-6.1 Sol
- Claude Opus 5.5
- Claude Fable 5.1
- GPT-6 Astra
- Gemini 4 Argon
- Muse Wonder
- Grok 4.7
- Claude Sonnet 5.5

This scope does not cover every model in the AA catalog.

Current model identifiers follow the
[Anthropic catalog](https://platform.claude.com/docs/en/models/overview) and
[OpenAI catalog](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

## Frontier calculation

A pair qualifies when no compared pair has both equal-or-lower cost and
equal-or-higher intelligence, with at least one strict improvement.
The calculation uses unrounded values.
The global table rounds intelligence to one decimal and cost to four decimals.

AA cost/task is a weighted average across the Intelligence Index evaluations.
It includes input, cache read, cache write, reasoning, and answer costs.
The source field is `intelligenceIndexCostPerTask.cost.total`.
This measure differs from total index cost divided by total task count.
See the [AA methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking).

| Model and effort | AA intelligence, unrounded | USD/task, unrounded |
| --- | ---: | ---: |
| [Luna 6 low](https://artificialanalysis.ai/models/gpt-6-luna-low) | 21.5261980080866 | 0.004516607569410252 |
| [Luna 6 medium](https://artificialanalysis.ai/models/gpt-6-luna-medium) | 29.9251773515762 | 0.017476906067835942 |
| [Luna 6 high](https://artificialanalysis.ai/models/gpt-6-luna-high) | 32.9282054150837 | 0.02903157640372802 |
| [Luna 6 xhigh](https://artificialanalysis.ai/models/gpt-6-luna-xhigh) | 34.5587320217785 | 0.042183547923951084 |
| [Luna 6 max](https://artificialanalysis.ai/models/gpt-6-luna) | 38.1245186869738 | 0.06782295669812205 |
| [Sol 6.1 low](https://artificialanalysis.ai/models/gpt-6-1-sol-low) | 42.0835618555848 | 0.13075190869859377 |
| [Sol 6.1 medium](https://artificialanalysis.ai/models/gpt-6-1-sol-medium) | 47.7833271274065 | 0.21370088267875537 |
| [Sol 6.1 high](https://artificialanalysis.ai/models/gpt-6-1-sol-high) | 50.2377777519769 | 0.31914442375664703 |
| [Sol 6.1 xhigh](https://artificialanalysis.ai/models/gpt-6-1-sol-xhigh) | 51.0377679093761 | 0.39286117158850653 |
| [Sol 6.1 max](https://artificialanalysis.ai/models/gpt-6-1-sol) | 51.8332597011541 | 0.7241670655535033 |
| [Opus 5.5 high](https://artificialanalysis.ai/models/claude-opus-5-5-high) | 53.5831959822067 | 1.822504718771704 |
| [Opus 5.5 xhigh](https://artificialanalysis.ai/models/claude-opus-5-5-xhigh) | 55.9873505840139 | 3.459110175822289 |
| [Sonnet 5.5 max](https://artificialanalysis.ai/models/claude-sonnet-5-5) | 56.0001286580794 | 5.4608525948098325 |
| [Opus 5.5 max](https://artificialanalysis.ai/models/claude-opus-5-5) | 57.6223698102963 | 5.982012019521066 |

Sonnet 5.5 max exceeds Opus 5.5 xhigh by about 0.0128 index points.
It costs about 58% more per index task.
Both display as 56.0 after rounding, but both qualify under the exact calculation.
This difference does not establish a practical quality advantage.

Opus 5.5 medium scores 51.2435 at $1.3360 per task.
Sol 6.1 max scores 51.8333 at $0.7242 per task, so it dominates Opus medium.
Sonnet 5.5 low, medium, high, and xhigh also fall below the frontier.
The [Sonnet release](https://www.anthropic.com/claude-sonnet-5-5) confirms substantial
improvements over Sonnet 5, but model age alone does not establish frontier membership.

## Interpretation limits

The frontier measures aggregate benchmark capability and API cost.
It does not measure coordination, PR acceptance, deployment management, or code-review accuracy.
The owner's Fable, Astra, and Opus role limits come from use and explicit instructions.
They do not represent conclusions from the AA index.
Ultracode refers to the owner's multi-agent workflow, not a measured AA variant.

Subscription allocation, task duration, harness support, and task-specific quality
can change the practical choice among eligible pairs.
A frontier pair can require more time for a small capability gain.
Eligibility therefore does not set the default effort.

The public [DeepSWE leaderboard](https://deepswe.datacurve.ai/) still reports
a September 22, 2026 update.
It lacks measured rows for Sonnet 5.5 and Sol 6.1.
Predecessor scores and vendor reports cannot replace independent measurements for those models.

The autoreview helper retains separate review scores and historical evidence.
Its [selection reference](../../autoreview/MODEL_SELECTION.md) describes that configuration.
Those settings do not authorize Fable worker or isolated reviewer assignments under the current owner policy.

## Owner taste estimates

These estimates preserve the earlier owner calibration.
They measure interface design, code quality, API design, and copy on a 1-to-10 scale.
They are separate from the AA intelligence index.

| Model | Owner taste | Evidence limit |
| --- | ---: | --- |
| GPT-6 Luna | 5.5 | Earlier owner estimate |
| GPT-6.1 Sol | 7 | Provisional estimate inherited from GPT-6 Sol |
| Claude Opus 5.5 | 9 | Earlier owner estimate |
| Claude Sonnet 5.5 | 7 | Provisional estimate inherited from Sonnet 5 |
| GPT-6 Astra | 8 | Earlier owner estimate |
| Claude Fable 5.1 | 10 | Owner estimate for code and architecture; interface design remains unverified |
