# Model selection

Autoreview uses [model-selection](../model-selection/SKILL.md) policy version 2.
The shared policy owns model aliases, role limits, and approved frontier pairs.
Autoreview loads its canonical sibling script. Repository configuration cannot
replace that script or disable its checks.

## Reviewer eligibility

Every selected model and fallback must pass the shared policy with the
`reviewer` role. The same checks apply to explicit CLI models, exact profiles,
environment defaults, layered configuration, and `--no-config` runs. Known catalog
aliases normalize before invocation. Supplied OpenCode and Pi provider namespaces
stay unchanged. Caps apply to the resolved model identity.

- Fable can only coordinate work. It cannot review code, including through
  an explicit request or fallback.
- Astra can only handle a focused specialist task with high complexity.
  It cannot act as an autoreview reviewer.
- Haiku cannot handle any assignment.
- Known routine reviewer pairs must belong to the frozen approved frontier.
- Opus 5.5 high remains the default Claude reviewer.
- Claude effort defaults to a `high` cap. A higher configured cap still
  requires an approved model and effort pair.

Automatic selection checks eligibility before score ranking or harness
installation. It keeps the existing host avoidance and isolation checks.
Explicit third-provider catalog models remain available through external
adapters. They do not enter scored selection without shared-policy approval.
Unresolved catalog defaults need an explicit concrete model name. Aliases for
reserved families cannot use the third-provider exception.

## Configuration migration

Policy version 2 is separate from TOML configuration schema `version = 1`.
Existing schema version 1 files still load. The built-in `value` profile now
selects GPT-6.1 Sol high. The built-ins no longer include Terra or Fable.

An existing file that overrides `value` with Terra must remove that override
or select an approved pair. Legacy prohibited candidates do not enter scored
selection. An exact profile or final override that selects one fails with a
policy error. Approval fields cannot grant a prohibited reviewer role.

The loader completes partial legacy score overlays with their historical
identity fields. That migration preserves configuration layering. It does not
restore reviewer eligibility.

Install both skills together. If the sibling `model-selection` script does not exist, selection fails with an installation recovery message.

## Automatic score

After eligibility checks, automatic selection uses this formula:

```text
0.45 × intelligence
+ 0.25 × taste
+ 0.20 × (DeepSWE v1.1 pass rate ÷ 10)
+ 0.10 × (10 − cost)
```

Owners calibrate `intelligence` and `taste` from model use. These values do not
represent benchmark rank. DeepSWE measures pass rate and task cost under
`mini-swe-agent`. It does not directly measure code review.

The historical normalization reference remains $9.18. That reference preserves
existing score inputs after Fable leaves the candidate pool:

```text
cost = 10 × model/effort average cost per task ÷ $9.18
```

Lower `cost` improves the score. Eligibility and role restrictions take
precedence over every score.

## Built-in review pairs

The table uses the September 2026 owner scores and provisional DeepSWE inputs.
It does not replace the shared frontier data.

| model | candidate ID | intelligence | taste | DeepSWE Pass@1 | selection score | harness | effort | when to use | cost/task | manual approval required |
| --- | --- | ---: | ---: | ---: | ---: | --- | :---: | --- | ---: | :---: |
| Opus 5.5 | `opus5` | 9 | 9 | 73% | 8.43 | Claude Code CLI | high | Default when the host is Codex | $3.07 | no |
| GPT-6.1 Sol | `sol` | 7.5 | 7 | 75.2% | 7.52 | Codex CLI | high | Default when the host is Claude, plus `sol` and `value` profiles | $1.05 | no |
| GPT-6 Luna | `luna` | 5 | 5.5 | 67% | 5.93 | Codex CLI | max | `budget` profile | $0.23 | no |

The `cross-lab` profile selects Sol high and Opus high. Each reviewer receives
only the frozen review bundle. Model policy does not change harness isolation,
secret scanning, reviewer counts, or attestation requirements.

## Historical benchmark evidence

These snapshots explain the retained score inputs. They do not grant current
reviewer eligibility. Current frontier evidence belongs to
[model-selection](../model-selection/SKILL.md).

### Provisional September 22 and 29, 2026 inputs

DeepSWE had no measured rows for the selected new models at these efforts.
A provisional cost uses the predecessor cost times its same-effort AA cost
ratio. Vendor cost claims do not set that ratio.

- Sol high uses the vendor-reported DeepSWE v1.1 pass rate of 75.2%.
  Its provisional cost is $2.66 × ($0.319 ÷ $0.808) = $1.05.
- Opus high keeps the predecessor pass rate of 73%.
  Its provisional cost is $6.08 × ($1.823 ÷ $3.613) = $3.07.
- Luna max keeps the predecessor pass rate of 67%.
  Its provisional cost is $0.61 × ($0.068 ÷ $0.178) = $0.23.

Replace provisional inputs when measured data becomes available.

### AA snapshot from September 2026

The September 22 snapshot contains the measured AA Intelligence Index and
cost per task. The Sol 6.1 row comes from September 29. Bold cells identify
the frontier in that historical snapshot.

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


### DeepSWE v1.1 snapshot from September 22, 2026

The [DeepSWE v1.1 data](https://deepswe.datacurve.ai/data/v1.1) supplied these
pass rates and task costs. Bold cells identify the historical frontier.

| model | low | medium | high | xhigh | max |
| --- | --- | --- | --- | --- | --- |
| GPT-6 Astra | 67% $1.60 | **73% $3.08** | 73% $3.92 | **74% $4.43** | 73% $7.50 |
| Opus 5 | 58% $1.66 | 69% $3.29 | 73% $6.08 | 73% $9.07 | 74% $11.84 |
| GPT-5.6 Sol | 45% $0.82 | 61% $1.42 | **69% $2.66** | 71% $3.60 | 73% $6.46 |
| Fable 5 | 60% $3.76 | 65% $6.09 | 69% $9.18 | 70% $13.41 | 70% $21.63 |
| GPT-5.6 Luna | **2% $0.01** | **11% $0.04** | **44% $0.16** | **57% $0.31** | **67% $0.61** |
| Sonnet 5 | 31% $2.19 | 40% $4.08 | 48% $7.43 | 50% $11.89 | 54% $26.40 |


## External review adapters

Explicit concrete model names remain available through Kimi Code, OpenCode,
Cursor Agent, and Pi. Runtime catalogs own third-provider names. Reserved model
aliases still receive role checks through these adapters. An external adapter
does not make Fable, Astra, Haiku, or a dominated known pair eligible.

## Maintenance

1. Update shared frontier evidence in the model-selection skill.
2. Recompute score inputs when measured DeepSWE rows change.
3. Keep the benchmark version and snapshot date with each data table.
4. Run helper self-tests, Python tests, and the skill validator.
5. Keep machine and project preferences in layered configuration.

Known catalog models need an explicit supported effort on external adapters.
Cursor cannot establish effort for known catalog pairs, so those selections fail.
Concrete third-provider catalog models remain available through Cursor.
