---
name: ago
description: Run and remediate the ago restriction-only Go linter. Use when a Go repository contains .ago.yml, declares the ago module tool, reports ago findings, or needs ago adoption.
license: MIT OR Apache-2.0
compatibility: Requires Go 1.25 or later. Adoption changes go.mod, go.sum, and .ago.yml.
metadata:
  author: agentstation
---

# ago

Use the repository's pinned ago command and rule policy.

## Find the contract

1. Read the nearest `AGENTS.md` and `.ago.yml`.
2. Inspect `go.mod` for this tool directive:

   ```text
   tool github.com/agentstation/ago/cmd/ago
   ```

3. Use `go tool ago` when the directive exists.
4. Use `ago` only when the repository documents a global installation.
5. Do not install or add ago unless the user requests adoption or setup.

## Run the check

Discover the active rule policy before the first repair pass:

```sh
go tool ago -list -format json
```

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

Do not change `.ago.yml` only to remove a finding. A policy change needs an
explicit project decision.

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

2. Write the starter policy.

   ```sh
   go tool ago -init
   ```

3. Review `.ago.yml` with the user when the default policy is not sufficient.
4. Add the ago command to the repository's existing check target and CI.
5. Add the required command to `AGENTS.md`.
6. Run `go tool ago -stale-ignores -format json ./...`.
7. Commit `go.mod`, `go.sum`, `.ago.yml`, and the authorized integration files.

`ago -init` refuses to replace an existing `.ago.yml`. Preserve that file and
inspect it instead.

## Boundaries

- ago always skips `vendor/` and `testdata/`.
- Exclude patterns are project policy, not a repair shortcut.
- Exit status 2 blocks a clean result.
- The JSON fields and rule catalogue are the machine contracts.
- CI enforces the policy. This skill guides the local workflow.
