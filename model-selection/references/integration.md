# Caller integration

The canonical module is `model-selection/scripts/model_policy.py`.
Its data files are `data/catalog.json` and `data/policy.json`.
Callers load these installed files, not code or policy from the reviewed repository.

```python
validate_assignment(
    model,
    effort,
    role="reviewer",
    complexity="routine",
    focused=False,
    ultracode=False,
    require_frontier=True,
    allow_unknown=False,
)
```

The function returns a validated assignment or raises `PolicyError`.
Runtime model identifiers appear in `model`.
The `catalog_model` field retains the AA comparison identifier.
Dispatch the returned runtime identity, rather than the input alias.
Known catalog models require explicit effective effort at dispatch.

Automatic selection validates each candidate before scoring or installing a harness.
Exact profiles and final reviewers validate before dispatch.
Every fallback validates independently.
A missing dependency stops execution and identifies the installation command.
Review attestation keys include the module and both data files.

A concrete external review model may use `allow_unknown=True`.
Reserved-family checks still apply first.
Opaque aliases such as `auto`, `default`, and an empty model remain invalid.
A third-provider adapter without effort control may use `None`.
This allowance does not make unknown models eligible for automatic ranking.

Policy version 2 changes reviewer eligibility.
Autoreview config schema version 1 remains readable.
Its legacy `value` profile resolves to Sol high.
A Fable review request fails rather than changing the requested model silently.
Shared role restrictions take precedence over layered scores and explicit overrides.
