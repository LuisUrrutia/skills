# Recovery, replay and partial effects

Read before designing or changing retry, fallback, rollback, compensation,
restart or circuit-breaker behavior. Use the operation's existing contract and
the dependency's actual guarantees; names such as "timeout" or "idempotent"
do not establish those guarantees on their own.

## Establish whether repeating work is safe

A lost response can occur after a mutation committed. Determine whether the
operation was rejected, completed, partly completed or remains unknown before
choosing a recovery action. Query or reconcile existing state when that can
establish the outcome. If it cannot, preserve uncertainty for the caller.

An idempotency key protects replay only if the receiving system enforces the
contract. Check its operation scope, payload binding, retention, atomic recording
with the effect, and behavior under concurrent attempts. Preserve the identity
across retries and restarts of the same logical operation. A new key per attempt,
an in-memory flag or a read-before-write check does not establish durable deduplication.

Trace all effects, including those before the retried call. Retrying a transaction
or workflow may repeat notifications, writes or other operations outside its
atomic boundary. Preserve confirmed progress and resume missing work where the
contract permits. Reconcile concurrent results against the current state.

## Bound retries and respect control flow

Retry only failures classified as transient for this operation when replay is
safe. Respect server retry guidance and distinguish rate limits, conflicts,
authentication, malformed input and programming failures by their contracts;
neither all client errors nor all server errors share one policy.

Choose one layer to own retries and account for retries already performed by a
client, proxy or queue. Bound attempts and elapsed time by the caller's deadline
and configured policy. Backoff, a delay cap and jitter can reduce synchronized
load; preserve a server's minimum wait rather than shortening it to fit a budget.
If that wait cannot fit, return or defer under the existing contract.

Check cancellation and deadline expiry before another attempt and during waits.
An outer timeout does not prove the underlying work stopped. Settle or account
for in-flight work before replaying a mutation. Invalid retry settings must fail
clearly rather than run forever or report a successful operation that never ran.
After exhaustion, propagate a useful terminal result with the final cause and
relevant attempt context. Logs alone are not that result.

## Preserve state through recovery

Use rollback only for effects the transaction can actually undo. Compensation
is a separate operation that can fail or race with other work; apply only an
established, authorized compensation policy. Do not invent refunds, deletion,
message acknowledgement, skipped records or reduced durability as error handling.
Keep recoverable state and the next reconciliation step explicit.

Use fallback only when it preserves the required guarantees or an approved
degraded contract. Identify stale, incomplete or unavailable data. Failures in
authorization, validation or integrity checks must not become permission to
proceed. A fail-fast or fail-closed choice still needs the system's actual policy.

Add a circuit breaker only for a demonstrated need to contain dependency failure.
Prefer the existing implementation. Establish what counts toward opening, how
bounded recovery probes work, when the state closes, and what callers observe
while it is open. Isolate unrelated operations or tenants where the contract
requires it; verify recovery as well as rejection while open.

## Verify the recovery decision

Inject failure before an effect, after an effect but before its acknowledgement,
and at a relevant partial-progress boundary. Check the observable state and result
across retry or restart, including exhaustion and cancellation when applicable.
Exercise concurrent attempts if deduplication is the guarantee being claimed.
Use a real local implementation for the mechanism under test and a controllable
fake only beyond that claim. State which external guarantees remain untested.
