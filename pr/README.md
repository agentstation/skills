# PR

The `pr` skill is the local gate before a pull request in a repository with no
remote pull-request CI. It rebases the branch and runs the static check, the
affected tests, the drills and autoreview. Then it writes the pull-request
body, pushes with an explicit refspec and opens the pull request. A scheduled
batch run tests the base branch later and moves the promoted branch to a green
commit.

[`SKILL.md`](SKILL.md) holds the agent-facing contract. This page covers
install, the repository configuration and one worked case.

## Install

```bash
npx skills add agentstation/skills --skill autoreview -g -a codex -a claude-code -y
npx skills add agentstation/skills --skill pr -g -a codex -a claude-code -y
```

The gate uses the GitHub CLI (`gh`) and the `autoreview` skill.

## Configure a repository

Add the `pr.*` keys to the repository `AGENTS.md` or to the workspace
`AGENTS.md`. A repository value overrides a workspace value. This example
configures a batch model with a `develop` base and a promoted `main`:

```markdown
## Pull requests

- `pr.base`: `develop`
- `pr.promoted`: `main`
- `pr.check`: `npm run verify:static`
- `pr.test`: `npm run test:affected -- --base {base}`
- `pr.drills`: `node scripts/select-drills.mjs --base {base}`
- `pr.run-now`: `gh workflow run batch.yml --ref main`
```

The labels default to `ci-batch-red` and `ci-main-audit`, and the CI workflow
defaults to `ci.yml`. [`SKILL.md`](SKILL.md#configuration) lists every key. The
skill stops when a required key has no value.

## Quickstart

Commit the change, then ask the agent to open the pull request. The agent runs
the gate in order:

1. Rebase on `origin/develop`.
2. Run `pr.check`, `pr.test` and the drills.
3. Run `autoreview --gate pre-pr --mode auto --base origin/develop`.
4. Write the body with a summary, the evidence and the merge danger.
5. Refuse when a `ci-batch-red` issue is open, unless the change is a revert
   or fix that names the issue.
6. Push with `git push origin HEAD:refs/heads/<branch>`.
7. Run `gh pr create --base develop`.

A hotfix, a merge-back and a sign-off have their own sections in
[`SKILL.md`](SKILL.md).

## Worked case: a Dependabot security update

Dependabot opens pull request 412, a security update of one npm package.
Security updates always target the default branch, so the pull request has
base `main`. The repository orchestrator session owns it.

1. Retarget the pull request to the pull-request base:

   ```bash
   gh pr edit 412 --base develop
   ```

2. Check out the branch. Do not run `npm install`, the tests or the build. The
   change does not get a local install:

   ```bash
   gh pr checkout 412
   ```

3. Run autoreview on the diff only. The diff holds only `package.json` and
   `package-lock.json`, and the pre-PR gate skips that diff. Use the manual
   branch mode:

   ```bash
   export AUTOREVIEW="${AGENTS_HOME:-$HOME/.agents}/skills/autoreview/scripts/autoreview"
   "$AUTOREVIEW" --mode branch --base origin/develop
   ```

4. Make sure that no `ci-batch-red` issue is open:

   ```bash
   gh issue list --label ci-batch-red --state open --json number --jq length
   ```

5. Merge the pull request to `develop` with the repository merge method:

   ```bash
   gh pr merge 412 --merge
   ```

The next batch run installs and tests the change on a runner. If that run is
red, the red path applies to the change like any other commit.
