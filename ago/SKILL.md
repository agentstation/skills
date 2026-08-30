---
name: ago
description: Run and remediate the ago restriction-only Go linter. Use when a Go repository declares the ago module tool, invokes ago in repository checks, contains an ago policy file, reports ago findings, or needs ago adoption or setup.
license: MIT OR Apache-2.0
compatibility: Requires Go 1.25 or later. Resolved-policy JSON metadata requires ago 0.2.0 or later. Adoption changes go.mod and go.sum. A custom policy also adds .ago.yml.
metadata:
  author: agentstation
---

# ago

Use the repository's pinned ago command and resolved rule policy.

## Find the contract

1. Read the nearest `AGENTS.md`.
2. Inspect `go.mod` for this tool directive:

   ```text
   tool github.com/agentstation/ago/cmd/ago
   ```

3. Read the nearest `.ago.yml` or `.ago.yaml` when one exists.
4. Use `go tool ago` when the directive exists.
5. Use `ago` only when the repository documents a global installation.
6. Do not install or add ago unless the user requests adoption or setup.

An ago policy file is optional. The pinned version's built-in defaults are the
resolved policy when no policy file exists.

## Run the check

Discover the active rule policy before the first repair pass:

```sh
go tool ago -list -format json
```

Use each `rules[].enabled` value as the active restriction set. With ago 0.2.0
or later, also read `policy.ruleSource`, `policy.configPath`, `policy.tests`,
and `policy.exclude`. For an earlier version, report that policy source
metadata is unavailable.

Do not infer that the repository has no policy when `.ago.yml` is absent. The
pinned ago version supplies the built-in defaults.

Run the complete coding-agent check:

```sh
go tool ago -stale-ignores -format json ./...
```

Interpret the exit status with the JSON document:

- Status 0 means the run completed with no findings or stale ignores.
- Status 1 means the run found a violation or stale ignore.
- Status 2 means the run was incomplete. Read `errors` before changing source.

Do not treat an empty `findings` array as clean when `errors` is not empty.

## Repair findings

1. Group findings by `rule` and file.
2. Read each catalogue `rationale` or run `go tool ago -explain <rule>`.
3. Change the smallest source region that violates the selected policy.
4. Preserve behavior unless the user requested a behavior change.
5. Delete each stale ignore after confirming that it suppresses no finding.
6. Run the same JSON command again.
7. Report the exit status, finding count, stale-ignore count, and incomplete errors.

Do not add or change `.ago.yml` only to remove a finding. A policy change
needs an explicit project decision.

Do not add a suppression only to make the run pass. Use a suppression for a
local exception with a concrete reason:

```go
//ago:ignore no-goto -- hand-written state machine, see docs/parser.md
goto retry
```

ago never rewrites source. Fixes belong to the coding agent or developer.

## Adopt ago

Use this procedure only when the user requests adoption or setup.

1. Add the pinned module tool.

   ```sh
   go get -tool github.com/agentstation/ago/cmd/ago@latest
   ```

2. Inspect the built-in policy.

   ```sh
   go tool ago -list -format json
   ```

3. Run `go tool ago -stale-ignores -format json ./...`.
4. Add the ago command to the repository's existing check target and CI.
5. Add the required command to `AGENTS.md`.
6. Commit `go.mod`, `go.sum`, and the authorized integration files.

If the user requests a custom policy, run `go tool ago -init`. Review the new
`.ago.yml`, then commit it. The command writes at the `go.mod` or `go.work`
root and refuses to create a competing child policy.

## Boundaries

- ago always skips `vendor/` and `testdata/`.
- Exclude patterns are project policy, not a repair shortcut.
- Exit status 2 blocks a clean result.
- The versioned JSON fields and rule catalogue are the machine contracts.
- CI enforces the policy. This skill guides the local workflow.
