---
name: use-modern-go
description: Use this skill for any task that writes, modifies, reviews, fixes, or refactors Go source, tests, module files, or tooling. Invoke it when the user requests a Go feature, bug fix, migration, performance change, code review, test change, dependency update, or cleanup, even if they do not mention Go style. Do not invoke it only to read, explain, or answer questions about existing Go code.
license: Apache-2.0. See LICENSE.upstream for complete terms.
compatibility: Requires Go 1.25 or automatic toolchain switching. The modern-guidelines wrapper needs network access and writes to a user cache on its first run.
metadata:
  author: agentstation
  upstream: https://github.com/JetBrains/go-modern-guidelines
  upstream-commit: c17350498ae6a8f50e0d3882cd0d7fc132b5a233
  upstream-cli-version: v0.1.1
---

# Modern Go

Write Go in one project-selected form. Use modern Go only inside the
repository's compatibility, behavior, and policy boundaries.

## Establish the contract

1. Read the nearest `AGENTS.md` and repository instructions.
2. Locate the applicable `go.work` and `go.mod` files.
3. Record the target Go version for each affected module.
4. Read the affected source, tests, callers, interfaces, and recent changes.
5. State the current behavior and the behavior that the task requires.

Do not use a feature only because the local toolchain accepts it. The affected
module's declared Go version is the default compatibility boundary.

For a review or diagnosis, inspect and report. Do not edit unless the request
includes a change.

## Read modern Go guidance

Run the bundled [modern-guidelines wrapper](scripts/run-tool.sh) before you
review or edit Go code. Resolve `<skill-directory>` to this installed skill's
directory.

On Linux or macOS, run:

```sh
sh "<skill-directory>/scripts/run-tool.sh" list --file-path path/to/file.go
```

On Windows PowerShell, run:

```powershell
& '<skill-directory>\scripts\run-tool.ps1' list --file-path path\to\file.go
```

The first run installs the pinned Modern Go Guidelines CLI in a user cache.
Use the host's approval flow when the install needs network or write access.

If no target file exists, pass the known version:

```sh
sh "<skill-directory>/scripts/run-tool.sh" list --go-version 1.24
```

Read the complete output. Do not filter or truncate it. Older entries can
still apply to the target version.

Request details only for a relevant guideline:

```sh
sh "<skill-directory>/scripts/run-tool.sh" explain guideline-id
```

If files use different module versions, run `list` once for each version. If
the command is unavailable, use repository evidence and report the skipped
guidance check.

## Resolve the ago policy

Before a Go code change or review, inspect `go.mod` for this module tool:

```text
tool github.com/agentstation/ago/cmd/ago
```

Use `go tool ago` when the module declares the tool. Use a global `ago`
command only when repository instructions require it. Read the nearest
`.ago.yml` or `.ago.yaml` when one exists.

An ago policy file is optional. The pinned ago version supplies built-in
defaults when no policy file exists.

Do not install ago or add a policy unless the user requests adoption. If the
`ago` Agent Skill is available, use its complete remediation workflow.

When the repository owns an ago command, discover the resolved policy before
you choose a Go form:

```sh
go tool ago -list -format json
```

Use each `rules[].enabled` value as the active restriction set. With ago 0.2.0
or later, also read `policy.ruleSource`, `policy.configPath`, `policy.tests`,
and `policy.exclude`. A `built-in` rule source is a complete policy, not a
missing policy. A `config` rule source records the selected policy file.

An active ago restriction takes priority over a modern form. For example, do
not use expression-based `new` when `no-new-expr` is active. Keep a generic
operation as a package function when `no-generic-methods` is active.

## Make the change

- Use the newest applicable form that the target version and policy accept.
- Keep new code consistent with the selected project policy.
- Prefer the simplest form that keeps control flow, ownership, and data visible.
- Preserve behavior, exported APIs, wire formats, and error identity unless
  the task changes them.
- Keep the smallest coherent change. Do not modernize unrelated code.
- Prefer the standard library when it provides the required contract.
- Keep ownership with the package or type that owns the domain concept.
- Do not edit generated, vendored, or third-party code directly.
- Add a regression test when an automated test can reproduce a defect.

Skip a relevant modern guideline only when it would fail to compile, change
required behavior, or violate project policy. Read its `explain` output before
you skip it.

## Verify the result

1. Run `gofmt` on each changed handwritten Go file.
2. Run the affected package tests.
3. Run the repository's complete Go check when the task scope permits it.
4. Run race or platform checks when the changed behavior depends on them.
5. Run ago when the repository owns an available command.

Use the same ago command form that supplied the policy:

```sh
go tool ago -stale-ignores -format json ./...
```

Status 0 means the run completed without findings. Status 1 means the run
found a violation or stale ignore. Status 2 means the run was incomplete.
Read the JSON `errors` field before you change source after status 2.

Fix source when the selected ago policy reports a finding. Do not weaken the
policy or add a suppression only to make the check pass.

Report the checks, results, skipped checks, and remaining uncertainty.
