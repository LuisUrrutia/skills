# Work units and dependencies

Read when one plan needs separately executable units, a staged migration, or
tickets. Keep a small cohesive change together when splitting would add handoffs
without independently useful results.

## Find boundaries that can be verified

Name each unit by the behavior or capability it delivers. Prefer an end-to-end
path through the layers involved over separate database, backend, frontend, and
testing tickets. A unit may rely on completed prerequisites; after those land,
its own result should be demonstrable without a later unfinished unit.

Size for a fresh executor to acquire the needed context, implement, and verify.
Supply the outcome, constraints, relevant entry points, required inputs and
outputs, acceptance scenarios, and deciding checks. A short schema or interface
excerpt can preserve an agreed contract more precisely than prose; a full
implementation transcript usually commits details too early. Recheck paths and
signatures when resuming a plan written against an older revision.

Define a dependency by what must be available before another unit can execute or
be verified. Record that prerequisite and the work that supplies it. Distinguish
dependencies from preferred order and coordination needs. Shared files, test
environments, data, or release targets may prevent concurrent execution even when
the functional dependencies are satisfied. Name those constraints; leave dispatch,
isolation, and integration mechanics to the active execution workflow.

Resolve cycles by finding a smaller shared contract or keeping inseparable work
together. Prioritize a risky assumption before work that relies on it. Explain
any enabling refactor by the current change it permits and its behavior-preserving
check; planning is not a reason to add a cleanup campaign.

Include a check of the combined capability after integration. Per-unit checks
cannot establish that independently built contracts connect correctly.

## Stage broad changes honestly

When every small edit would break existing consumers, consider an expand,
migrate, contract sequence: introduce compatibility, migrate bounded consumer
groups, then retire the old form after checking all required consumers have moved.
Include deployed clients and data where they matter; an empty repository search
does not establish that an external contract is unused.

For each stage, name the intermediate supported behavior and its verification.
If units cannot pass independently, identify the coupled group, the integration
prerequisite, and where the first passing whole-system check is possible. Do not
present those units as independently releasable. A migration or release dependency
remains explicit even when its code has already merged.

## Prepare or publish tickets

Use the user's requested destination and the project's tracker conventions.
Preparing a breakdown does not publish it. When publication is authorized, inspect
existing items for this work, preserve stable identities, and create or update
only the requested records. Write prerequisites before dependents and use native
blocking relations when available; otherwise record explicit linked blockers.
Read back the results and distinguish drafted, published, and failed items.

Each ticket needs its outcome, applicable constraints, acceptance evidence, true
blockers, and accessible links to the relevant plan and decisions. Keep one
authoritative task record and a compact index when multiple files or a tracker
are useful. Do not require one file per task, duplicate progress in two places,
change implementation states, or close a parent merely because planning finished.
If a write's outcome is uncertain, reconcile the existing record before retrying
so a retry does not create duplicate work.
