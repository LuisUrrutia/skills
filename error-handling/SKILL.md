---
name: error-handling
description: Design, implement, or review error contracts and recovery behavior across software boundaries.
---

# Error handling

Make failures explicit to their callers and recover only when the operation's
contract supports it. Apply the language, runtime and framework already in use.
Keep the requested boundary: a review or design request produces findings or a
proposal; implementation requires the active task's authority.

## Establish the contract

Read the affected operation, callers, existing error types, adapters and tests.
Find the requirement or established contract for each material failure: what the
caller can observe, which effects may already have happened, and who can decide
the next action. Current behavior alone does not settle an unclear product policy.

Distinguish expected domain outcomes, invalid input or denied access, dependency
failures, broken internal invariants, and cancellation or deadline expiry when
they require different handling. Classify by the actual operation and runtime
semantics, not message matching or a blanket rule for an entire status range.
Separate known failure from an unknown outcome after a lost response.

Preserve public codes, response shapes, exit status, queue acknowledgement,
exception identity and other caller-visible behavior unless the requested change
revises that contract. Reuse the project's representation; do not introduce a
universal error superclass, result type, transport envelope or dependency merely
to follow this skill. Resolve an undecided fallback, data-loss or retry policy
before implementing the affected behavior; continue independent work.

## Propagate to an owner that can act

Place validation and translation at the boundary that owns them. Keep domain
behavior independent of transport details where the existing structure permits.
Rely on an established invariant only while its evidence holds: persisted data,
concurrent changes and lifecycle transitions can invalidate a prior check.

Handle a failure where code can recover, add useful context, translate its
representation, or perform required cleanup. Otherwise preserve propagation.
Retain the cause and useful classification when wrapping; keep diagnostic detail
separate from the public response. A catch that only logs does not establish
recovery. An empty value, default result or successful exit must not conceal an
unfulfilled operation.

Use runtime-supported cleanup and ownership mechanisms on success, failure and
cancellation. Keep the primary failure identifiable if cleanup also fails; expose
the secondary failure through the project's supported reporting mechanism. Treat
cancellation as control flow when the runtime does; do not turn it into success
or an automatic retry. Ensure asynchronous work has an owner that observes its
completion and failures, including work outside a request or UI render boundary.

## Choose recovery from the operation's semantics

Before adding retries, fallback, restart, rollback, compensation or a circuit
breaker, read [references/recovery.md](references/recovery.md). That reference
owns replay safety, partial effects, limits and recovery transitions.

Prefer existing retry and recovery mechanisms over another nested loop. A fallback
must satisfy an approved reduced contract and make partial or stale results clear.
If the intended result cannot be established, return the supported failure or
uncertainty rather than manufacture success. Do not add resilience infrastructure
without a concrete failure mode that needs it.

## Make failures understandable and testable

Give the user or caller an accurate outcome and a next action that is actually
available. Preserve localization and accessibility conventions. Do not advise
resubmitting a mutation whose outcome is unknown unless replay is safe. Keep
technical causes out of public messages while retaining appropriate internal
evidence for investigation.

Choose the reporting owner so one failure remains traceable without duplicate
alerts at every layer. Record useful operation, correlation, classification and
attempt context using the project's logging or telemetry conventions. Filter
secrets, payloads and personal data before recording them; raw exception text and
cause chains can contain sensitive values too. A public generic message does not
justify logging unrestricted internal data.

Exercise the real error boundary through observable behavior. Cover the relevant
failure, successful or permitted recovery path, and effects that must not repeat.
Use controllable dependencies and time where needed to exercise partial progress,
exhaustion, cancellation and cleanup. Verify result/state as well as reporting;
absence of a side effect is meaningful when tied to the observed failure contract.
Do not replace the behavior under test with a mock or use elapsed waiting as proof.

Run the project's applicable checks after implementation. Use available `verify`
for application-level evidence when the change needs it; existing direct checks
remain useful if that skill is unavailable. `debug` owns a wider investigation
of an observed symptom; error-handling supplies the failure-contract decisions.

## Return the result

Report the boundary and contract, changes or findings, observed outcomes and
remaining uncertainty. For recovery work, include what was retried or reconciled,
its stopping condition and the evidence that effects were not duplicated. Keep
proposed behavior and tested behavior distinct. The active caller owns further
delivery; this skill does not start publication or PR monitoring.

For a requested check or update of this skill's sources, read
[references/upstream-updates.md](references/upstream-updates.md).
