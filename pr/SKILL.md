---
name: pr
description: Run the local pull-request gate and open the pull request in a repository with no remote pull-request CI. Use before you push a branch or run gh pr create in a repository whose AGENTS.md sets pr.* keys. Also use for a Dependabot pull request, a hotfix to the promoted branch, a merge-back, or a sign-off that depends on a green batch. Do not use for a repository that runs CI on each pull request.
compatibility: Requires git, the GitHub CLI (gh), and the autoreview skill.
---

# Pull-request gate

The repository has no remote CI on a pull request. This gate is the only check
before the merge. A scheduled batch run tests the base branch later and moves
the promoted branch to a green commit.

Run every step in order. Stop and report when a step fails. Do not open the
pull request with a failed or skipped step.

## Configuration

Read the `pr.*` keys from the repository `AGENTS.md` first, then from the
workspace `AGENTS.md`. A repository value overrides a workspace value. Each key
is one list item:

```markdown
- `pr.base`: `develop`
- `pr.check`: `npm run verify:static`
- `pr.test`: `npm run test:affected -- --base {base}`
```

| Key | Required | Value |
|---|---|---|
| `pr.base` | Yes | The pull-request base branch. |
| `pr.check` | Yes | The static check command. |
| `pr.test` | Yes | The command that runs the tests that the change affects. |
| `pr.drills` | No | A drill selector command, or `<path>: <command>` items. |
| `pr.promoted` | No | The branch that only the batch run moves, for example `main`. |
| `pr.run-now` | Batch | The command that starts a batch run now. |
| `pr.ci-workflow` | No | The CI workflow file. The default is `ci.yml`. |
| `pr.red-label` | No | The red-batch issue label. The default is `ci-batch-red`. |
| `pr.audit-label` | No | The promoted-branch audit label. The default is `ci-main-audit`. |

- Replace `{base}` in a command value with the gate base ref. The gate base ref
  is `origin/<pr.base>`, or `origin/<pr.promoted>` for a hotfix.
- If a required key has no value, stop and report the key. Do not guess a
  command.
- The batch rules apply when `pr.promoted` has a value other than `pr.base`.
  Without that value, run only the [gate](#gate) and skip each batch rule.
  The batch rules are the red stop, the base check, "run now", sign-off,
  hotfix, and merge-back.
- In this file, `<base>` is the value of `pr.base`, and `<promoted>` is the
  value of `pr.promoted`.

## Gate

1. Inspect `git status`. Commit the intended change. The autoreview gate fails
   on a dirty worktree.
2. Rebase on the base:

   ```bash
   git fetch origin <base>
   git rebase origin/<base>
   ```

   Do not rebase a merge-back branch. It needs a true merge.
3. Run `pr.check`. Then run `pr.test`.
4. Run the drills. For a selector command, run it. For `<path>: <command>`
   items, run each command whose path the change touches. List the changed
   paths with `git diff --name-only origin/<base>...HEAD`.
5. Run autoreview with an explicit base:

   ```bash
   export AUTOREVIEW="${AGENTS_HOME:-$HOME/.agents}/skills/autoreview/scripts/autoreview"
   "$AUTOREVIEW" --gate pre-pr --mode auto --base origin/<base>
   ```

   Always pass `--base`. Without it and before a pull request exists, the
   helper reviews against `origin/main`.

   Every change gets a model review. If the gate prints `autoreview skipped`,
   run the manual branch review on the same diff:

   ```bash
   "$AUTOREVIEW" --mode branch --base origin/<base>
   ```

   The gate skips a diff with no substantive code path, for example a change
   to workflows, configuration, manifests, lock files, or documentation.
   Record in the pull-request body which mode ran. Follow the installed
   `autoreview` skill for findings. After a fix, commit it and run steps 3 to
   5 again.
6. Write the pull-request body. Use the [body form](#pull-request-body).
7. Apply the [red stop](#red-stop) when the batch rules apply.
8. Push with an explicit refspec:

   ```bash
   git push origin HEAD:refs/heads/<branch>
   ```

   A branch made from `origin/<base>` tracks `<base>`. With
   `push.default=upstream`, a bare `git push` updates `<base>` directly. After
   a rebase of a pushed branch, add `--force-with-lease`.
9. Open the pull request:

   ```bash
   gh pr create --base <base> --head <branch> --title "<title>" --body-file <file>
   ```

   `gh pr create` takes the bare branch name. Autoreview takes
   `origin/<base>`.
10. When the batch rules apply, apply the [base check](#base-check) before the
    merge. Run `pr.run-now` after the merge of a one-way-door change. A one-way-door change is a change that a revert
    cannot undo. Examples are a data migration, a wire or storage format
    change, and an external write.

Use the installed `gh` skill for `gh` output, pagination, and repository
targeting.

## Pull-request body

The body has three sections:

- **Summary:** what changes and why.
- **Evidence:** each gate command and its result, the test counts, and the
  drills that ran. List the autoreview mode and its result. The mode is the
  pre-PR gate or the manual branch review.
- **Merge danger:** what breaks if the change is wrong, whether the change is a
  one-way door, and the rollback.

## Red stop

A red batch issue is open when a batch run on `<base>` failed after its retry.
Before `gh pr create --base <base>`, run:

```bash
gh issue list --label ci-batch-red --state open --json number,title,url
```

Use the `pr.red-label` value when the repository sets one.

- If the command fails, refuse. A failed check does not show an empty list.
- If the list has an issue, refuse the pull request. Report the issue number
  and keep the branch.
- Exception: a revert or a fix whose body names the open issue, for example
  `Fixes #<n>`.
- The owner of a red issue is the agent that merged the culprit. If that agent
  is unknown, the owner is the repository orchestrator.
- An open `ci-main-audit` issue does not stop a pull request. The repository
  orchestrator owns that issue and reports it.
- The merge-back pull request is exempt. The batch run does not promote before
  the merge-back lands, so a stop would also block the fix.

## Base check

When the batch rules apply, an agent merges a pull request only to `<base>`.
Before each `gh pr merge <n>`, run:

```bash
gh pr view <n> --json baseRefName --jq .baseRefName
```

- Merge only when the output equals `<base>`.
- If the command fails or prints another branch, do not merge. Report the pull
  request and its base.
- Do not use the admin bypass. GitHub can apply the bypass to an admin merge
  with no `--admin` flag, so the base check is the guard.
- A person with merge authority merges each pull request to `<promoted>`.

## Dependabot

The orchestrator session of each repository owns its Dependabot pull requests.

1. Security updates always target the default branch. Dependabot applies
   `target-branch` only to version updates. Retarget each security-update pull
   request to the base:

   ```bash
   gh pr edit <n> --base <base>
   ```

2. Get the branch without an install. Do not install a Dependabot change on the
   local machine. Do not run the package manager, the tests, or the build:

   ```bash
   gh pr checkout <n>
   ```

3. Run autoreview on the diff only. A Dependabot diff holds only manifests,
   lock files, or workflows. The pre-PR gate skips it, so run the manual branch
   review directly:

   ```bash
   git fetch origin <base>
   "$AUTOREVIEW" --mode branch --base origin/<base>
   ```

4. Apply the red stop. While a red batch issue is open, do not merge.
5. Apply the [base check](#base-check). Then merge to the base with the
   repository merge method. The batch run tests the change on a runner.

## Sign-off

A sign-off that depends on CI uses the phrase "subject to a green batch that
contains the commit". Before you write that phrase for a commit, run:

```bash
git fetch origin <promoted>
git merge-base --is-ancestor <sha> origin/<promoted>
gh issue list --label ci-main-audit --state open --json title --jq '[.[]|select(.title|startswith("main audit: workflow change")|not)]|length'
```

The condition holds only when `merge-base --is-ancestor` exits 0 and the issue
count is `0`. The count ignores a workflow change issue, which reports a
workflow edit for review and not an outside update. Use the `pr.audit-label`
value when the repository sets one. A `promoted: <sha>` line in a run summary
is not evidence.

## Hotfix

A hotfix goes on top of the promoted branch. It does not start from a release
tag. A green hotfix does not go to `<promoted>` automatically. A person with
merge authority merges the hotfix pull request with a merge commit. The agent
never merges it.

1. Branch from the promoted tip:

   ```bash
   git fetch origin <promoted>
   git switch -c hotfix/<name> origin/<promoted>
   ```

2. Run the [gate](#gate) steps 1 to 6 with `origin/<promoted>` as the base.
   The manual review rule of step 5 applies:

   ```bash
   "$AUTOREVIEW" --gate pre-pr --mode auto --base origin/<promoted>
   ```

3. Push with `git push origin HEAD:refs/heads/hotfix/<name>`.
4. Open a ready pull request to the promoted branch, with the autoreview output
   in its body:

   ```bash
   gh pr create --base <promoted> --head hotfix/<name> --title "<title>" --body-file <file>
   ```

5. Start the CI workflow on the branch and watch it. A red `hotfix/*` run gets
   no retry and no issue:

   ```bash
   gh workflow run ci.yml --ref hotfix/<name>
   gh run list --workflow ci.yml --branch hotfix/<name> --event workflow_dispatch -L 1 --json databaseId,headSha,status,url
   gh run watch <run-id> --exit-status
   ```

   Use the `pr.ci-workflow` value when the repository sets one. If the run is
   red, fix the branch, run the gate again, push, and start a new run.
6. Make sure that the green run tested the merge result. The run `headSha`
   must equal the pull-request head. The promoted tip must be an ancestor of
   that head:

   ```bash
   gh pr view <n> --json headRefOid --jq .headRefOid
   git fetch origin <promoted>
   git merge-base --is-ancestor origin/<promoted> <head-sha>
   ```

   If `<promoted>` moved, merge `origin/<promoted>` into the hotfix branch.
   Then run gate steps 3 to 5, push, and start a new run. Do not push after
   the green run.
7. Ask the person with merge authority to merge the pull request with a merge
   commit. Give the run URL and the head SHA. The batch audit checks the merge
   commit. Its second parent must be the tested head, and its tree must equal
   the head tree.
8. After the merge, confirm the hotfix head with the [sign-off](#sign-off)
   commands.
9. Do the [merge-back](#merge-back).

## Merge-back

After a hotfix promotion, `<promoted>` holds commits that `<base>` does not
hold. The batch run skips until `<base>` contains the promoted tip.

1. Make the merge-back branch at the promoted tip:

   ```bash
   git fetch origin <promoted>
   sha=$(git rev-parse --short origin/<promoted>)
   git switch -c "merge/<promoted>-$sha" origin/<promoted>
   git push origin "HEAD:refs/heads/merge/<promoted>-$sha"
   ```

2. Open a pull request to the base. Apply the [base check](#base-check), then
   merge. Do not rebase and do not squash:

   ```bash
   gh pr create --base <base> --head "merge/<promoted>-$sha" --title "<title>" --body-file <file>
   gh pr view <n> --json baseRefName --jq .baseRefName
   gh pr merge <n> --merge
   ```

3. If GitHub reports a conflict, merge `origin/<base>` into the merge-back
   branch. Resolve the conflict, run gate steps 3 to 5, and push.
4. Run `pr.run-now`.
