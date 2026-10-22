# Delivery and release evidence

The coordinator owns completion across workers, review, and delivery.
It verifies code quality, readability, maintainability, and robustness.
Use the installed `model-selection` skill when assigning these roles.
The coordinator retains accountability after it delegates a task.

## Acceptance

1. Match the final diff to the requested behavior and acceptance criteria.
2. Inspect each worker result and the combined change.
3. Check callers, public contracts, failure behavior, and deployment dependencies.
4. Run repository checks and any review gate that the task requires.
5. Resolve accepted findings and verify the resulting diff.
6. Record check commands, results, skipped checks, and remaining uncertainty.

A passing worker report does not prove that the combined change passes.
Require evidence from the final combined state.

## Compatibility and versioning

Read the project's customer, data, API, protocol, and release policies.
A low user count does not remove customer contracts or data migration requirements.
When the user permits a breaking change, identify affected consumers and version the public change.
Publish upgrade steps and preserve customer data through explicit migrations.

Keep support windows, rollback floors, and deployment order explicit.
Remove obsolete paths after their migration and support obligations end.
Project instructions own exact windows, formats, and migration mechanisms.

## Publication and rollout

Prepare a reviewable result before requesting any approval that remains necessary.
Keep commits, publication, deployments, charges, and merges within the user's authority.
Verify required PR checks, review findings, approvals, and merge conflicts before acceptance.
For an authorized deployment, verify configuration, migration order, recovery, and observable health.
Record the delivered revision and the evidence that proves the target behavior.
Keep unverified release work explicit when the task authorizes only local changes.
