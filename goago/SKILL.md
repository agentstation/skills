---
name: goago
description: Run and remediate the goago restriction-only Go linter. Use when a Go repository declares the goago module tool, invokes goago in repository checks, contains a goago policy file, reports goago findings, or needs goago adoption or setup.
license: MIT OR Apache-2.0
compatibility: Requires Go 1.25 or later. Adoption changes go.mod and go.sum. A custom policy also adds .goago.yml. Recognizes projects that still use the former ago name.
metadata:
  author: agentstation
---

# goago

Pronounce `goago` as **go ago**. Use the repository's pinned command and
resolved rule policy.

## Find the contract

1. Read the nearest `AGENTS.md`.
2. Inspect `go.mod` for this tool directive:

   ```text
   tool github.com/agentstation/goago/cmd/goago
   ```

3. Read the nearest `.goago.yml` or `.goago.yaml` when one exists.
4. Use `go tool goago` when the directive exists.
5. Use `goago` only when the repository documents a global installation.
6. Do not install or add goago unless the user requests adoption or setup.

A goago policy file is optional. The pinned version's built-in defaults are the
resolved policy when no policy file exists.

## Run the check

Discover the active rule policy before the first repair pass:

```sh
go tool goago -list -format json
```

Use each `rules[].enabled` value as the active restriction set. Also read
`policy.ruleSource`, `policy.configPath`, `policy.tests`, and `policy.exclude`.

Do not infer that the repository has no policy when `.goago.yml` is absent. The
pinned goago version supplies the built-in defaults.

Run the complete coding-agent check:

```sh
go tool goago -stale-ignores -format json ./...
```

Interpret the exit status with the JSON document:

- Status 0 means the run completed with no findings or stale ignores.
- Status 1 means the run found a violation or stale ignore.
- Status 2 means the run was incomplete. Read `errors` before changing source.

Do not treat an empty `findings` array as clean when `errors` is not empty.

## Repair findings

1. Group findings by `rule` and file.
2. Read each catalogue `rationale` or run `go tool goago -explain <rule>`.
3. Change the smallest source region that violates the selected policy.
4. Preserve behavior unless the user requested a behavior change.
5. Delete each stale ignore after confirming that it suppresses no finding.
6. Run the same JSON command again.
7. Report the exit status, finding count, stale-ignore count, and incomplete errors.

Do not add or change `.goago.yml` only to remove a finding. A policy change
needs an explicit project decision.

Do not add a suppression only to make the run pass. Use a suppression for a
local exception with a concrete reason:

```go
//goago:ignore no-goto -- hand-written state machine, see docs/parser.md
goto retry
```

goago never rewrites source. Fixes belong to the coding agent or developer.

## Adopt goago

Use this procedure only when the user requests adoption or setup.

1. Add the pinned module tool.

   ```sh
   go get -tool github.com/agentstation/goago/cmd/goago@latest
   ```

2. Inspect the built-in policy.

   ```sh
   go tool goago -list -format json
   ```

3. Run `go tool goago -stale-ignores -format json ./...`.
4. Add the goago command to the repository's existing check target and CI.
5. Add the required command to `AGENTS.md`.
6. Commit `go.mod`, `go.sum`, and the authorized integration files.

If the user requests a custom policy, run `go tool goago -init`. Review the new
`.goago.yml`, then commit it. The command writes at the `go.mod` or `go.work`
root and refuses to create a competing child policy.

## Projects that still use ago

Before v0.3.0, the tool used the name `ago`. If `go.mod` still pins
`github.com/agentstation/ago/cmd/ago`, use `go tool ago` for the commands above
until the user requests migration. Versions before v0.2.0 do not include the
`policy` JSON metadata. Report that limitation.

Read legacy `.ago.yml` and `.ago.yaml` policies too. goago accepts these files
and `//ago:ignore` directives so migration does not remove restrictions or
exceptions. Do not create a second policy file.

When the user requests migration, follow the
[migration guide](https://github.com/agentstation/goago/blob/main/docs/migration.md).
Replace the old module tool, commands, policy filenames, and suppression
prefixes. Preserve the policy and each suppression reason.

## Boundaries

- goago always skips `vendor/` and `testdata/`.
- Exclude patterns are project policy, not a repair shortcut.
- Exit status 2 blocks a clean result.
- The versioned JSON fields and rule catalogue are the machine contracts.
- CI enforces the policy. This skill guides the local workflow.
