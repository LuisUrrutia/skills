# Delivery boundaries

Read when delivery spans state, consumers, or recovery paths that a single
successful job cannot establish. Apply only the sections relevant to the product.

## Match the release unit to its consumer

For a service, verify the deployed candidate through meaningful requests or jobs,
its required dependencies, and release-specific signals. Process liveness and a
successful deployment API response prove less than functional readiness. Keep
liveness, readiness, and rollout acceptance distinct; making every dependency a
liveness requirement can turn a dependency outage into restart churn.

For a package or CLI, install and exercise the built or packed distribution in a
clean consumer environment across supported platforms. Check included files and
entrypoints, version identity, and publication state. Source-tree tests cannot
detect every packaging failure. Publishing a fixed version and moving a channel
pointer are separate effects; changing the pointer does not remove installed copies.

For mobile, firmware, or offline clients, account for signing, distribution review,
delayed adoption, and old clients that remain in use. A successful upload is not
proof of availability or adoption. Retain compatibility and a repair path where
recalling the installed release is impossible.

For infrastructure, bind approval to the reviewed plan and relevant target state.
Reconcile drift before applying; stale plans and an old configuration file are not
proof of a safe reversal. Treat plans and state as potentially sensitive artifacts.
Use an available infrastructure specialist or current primary provider documentation
for implementation and provider guarantees.

## Protect state during mixed-version operation

Trace schema, stored payloads, caches, queues, and configuration through the old
and new producers and consumers. Establish the deploy order and the compatibility
window, including in-flight work and a possible return to the prior application.
For independent services, avoid a coordinated release unless their contract needs it.

Use expansion, backfill, reader/writer transition, and eventual removal when the
data contract needs a staged migration. State what proves each transition safe;
elapsed time or a fixed number of releases alone does not prove old consumers
have retired. Serialize migrations where they share state and bound backfill load.

Record relevant invariants and read-only checks before and after the change, with
expected results. Distinguish repository evidence from live-state prerequisites
that still need observation. Verify restoration access and data-loss tolerance
when recovery depends on backups; a backup's existence is not a tested restore.

## Specify advancement and recovery

For a rolling deployment, prove mixed-version compatibility and capacity. For
blue-green, check shared data and traffic cutover behavior before promising a fast
switch back. Use a canary only with representative exposure, candidate-specific
signals, and enough observations to judge it. Choose thresholds and windows from
the service's requirements and baseline; do not copy arbitrary percentages or waits.

Keep success, failure, and inconclusive telemetry separate. Specify who investigates
an inconclusive result and how the rollout remains bounded. Feature flags can
separate deployment from exposure; they do not reverse writes, messages, or payments.
Give temporary flags an owner and a removal condition.

Define which operations can retry, how partial progress is discovered, and how a
timed-out request is reconciled before another attempt. Inspect completed effects
before deciding rollback, roll-forward, or repair. Verify the resulting state after
recovery; a command named "rollback" is not the evidence.

Keep a release record linking source, artifact, configuration identity, target,
checks, approvals where required, and actual outcome. Name the failure/incident
owner and preserve diagnostics without secrets. Clean up temporary environments
without deleting evidence or artifacts still needed for investigation or recovery.
