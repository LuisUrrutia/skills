# Retirement across versions, state, and resources

Read when retirement reaches stored data, independently deployed consumers, or
external resources. Keep only the conditions relevant to this target.

## Versions and consumers

Identify old and new readers, writers, clients, workers, and in-flight operations.
Use their actual support and release constraints to choose a coordinated cutover
or a compatibility period. Cached and offline clients can outlive the release
that hides a feature. Backend enforcement and intentional responses for retired
operations must match the contract, not merely the current UI.

A legacy path may remain necessary while another consumer moves. Give it a
responsible owner and an evidence-based removal condition; a deadline does not
prove a consumer has upgraded. Before closure, reconcile unresolved consumers,
disabled entry points, and work already accepted against that condition.

## Persistent data

Separate ending a feature from deleting its records. Determine required access,
exports, retention, and audit history before choosing a data-disposal operation.
Where those requirements are unresolved, retain the affected records and pause
their destructive removal while completing independent changes.

For a changing data contract, establish which versions can read and write every
intermediate shape. Where coexistence requires it, expand the schema, keep new
writes compatible, migrate existing data, verify convergence, switch consumers,
and contract only when old consumers and recovery requirements permit it.
Use the actual database or service documentation for locks, transactions, and
tool behavior; an additive change is not automatically safe for live traffic.

Bound long data moves, make partial progress observable and resumable, and
define how concurrent writes stay consistent. Merely writing twice does not
establish atomicity or recovery after one write fails. Preserve real false,
zero, empty, and missing-value distinctions when changing formats or defaults.

Define recovery for each stage from its completed effects. Reverting code,
reversing a schema operation, restoring records, and correcting forward are
different actions. A command named `down`, a feature flag, or an existing backup
does not prove recovery. Use the delivery and verification owners for the actual
restore or compatibility evidence, including irreversible effects and constraints.

## External resources

Inventory dedicated and shared credentials, services, infrastructure, published
packages, contracts, and integrations only where the retirement reaches them.
Deleting repository files does not disable an external endpoint, recall an
installed client, or erase an already deployed smart contract.

Separate application retirement from external revocation, destruction, retention,
and billing changes. Verify shared usage and the active task's authority before
performing those operations. Record a deliberately retained external resource
and its reason; do not report it removed because its local wrapper disappeared.
