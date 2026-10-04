# State, domain meaning, and boundaries

Read this when the decision involves persistent state, concurrent actors,
external protocols, or a change to domain meaning. Apply the relevant parts.

## Model the domain

Use concrete scenarios to distinguish concepts that share a name. Read the
project's glossary or context map when present. Check terms against actual
behavior; neither an old document nor current code automatically establishes
the desired new rule. Surface a conflict that affects correctness rather than
silently renaming it away.

Describe valid states and transitions, identity, and the data needed for each
operation. Encode known invariants in types or storage constraints when the
project can enforce them. A discriminated union may eliminate synchronized
booleans; a map may express keyed ownership. Prefer plain data when it already
expresses the rule. Types cannot establish facts about unvalidated input or
mutable state held by another actor.

## Establish ownership and lifecycle

Trace create, read, update, retry, cancellation, and cleanup only where they can
change the decision. For shared mutable state, ask whether actors can own
independent data and combine it at a read boundary. When they require one
canonical invariant, name the structural enforcement: a transaction, unique
constraint, single writer, or another mechanism supported by the real system.
Splitting state must not discard a cross-actor invariant.

For operations subject to retries or crashes, examine duplication and partial
completion. Say what is atomic, which identity deduplicates work, and how a later
attempt distinguishes completed work from uncertain effects. Do not promise
exactly-once behavior from a process-local flag or invent external guarantees.
Keep legitimate validation of current authorization and mutable state at the
operation where it is needed; an earlier parse does not make those facts timeless.

## Define external boundaries and migration

Separate domain meaning from private storage, transport, and framework details
when callers should not depend on them. A protocol library may intentionally
expose protocol concepts: that is part of its contract, not automatically leakage.
Retain tenant identity, cancellation, security, and observable errors when they
are part of the caller's obligation. Hiding them is not interface simplification.

Use a replaceable dependency where real variation, ownership, isolation, or
testability needs it. Prefer real collaborators or lightweight substitutes for
local behavior. A fake at an external boundary cannot prove the remote service's
transaction, timing, or failure semantics; name the integration evidence needed.

When changing a persisted or public contract, identify the readers and writers,
versions that must coexist, and when old behavior may be retired. Define a
compatible transition or establish that an atomic cutover is actually available.
Distinguish a proposed migration from one exercised against real consumers.
Let `analyze-change-effects` own a deeper investigation when that evidence decides
between designs; keep its result separate from a code review verdict.
