---
name: design-code-structure
description: Use when designing, comparing, or improving data models, interfaces, and module boundaries for a software change.
---

# Design code structure

Resolve a structural problem with a usable interface, clear ownership of data
and invariants, and evidence for the chosen shape. Start from real callers and
the change they need; carry the decision through implementation when authorized.

Establish the work area and requested outcome. A design request ends with a
recommendation and sketch. An implementation request continues through the
authorized change and its checks. Honor an explicit request to stop before
implementing. If the structure is settled and only its enforcement is missing,
use [references/structural-checks.md](references/structural-checks.md) for that
contract without reopening the design.
Neither a local decision nor an enforcement gap expands the task into a
repository-wide audit, cleanup, or tooling rollout.

For requested source maintenance, read
[references/upstream-updates.md](references/upstream-updates.md).

## Ground and select the change

Identify the behavior to support, the decision still open, and the constraints
already settled. Inventory source and documentation inside the bounded work area
with ignore filtering disabled. With a filesystem and ripgrep, use:

```sh
rg --files --hidden --no-ignore <scope>
```

Set `<scope>` to the relevant subsystem or supplied input directory. Exclude
dependency and cache directories when necessary; keep local contracts and
generated documentation discoverable. Other tools need the equivalent setting
or a direct listing. A filtered inventory cannot establish a contract's absence.

Read the implementation, callers, tests, domain terms, and recorded decisions.
Trace a concrete use from entry point to result, including state ownership and
who may change it. Reuse a current relevant trace; filenames and proposed diagrams
alone do not establish how the system works.

When the caller has named the decision or boundary, address it. When asked to
choose among structural improvements, first inspect representative history in
the authorized area and connect substantive changes to current friction. Discount
generated files, bulk formatting, and renames; commit counts alone do not measure
design quality. If history is unavailable, use current callers, tests, and recorded
requirements, and state the evidence gap.

When choosing among improvements, rank them before designing alternatives. Name
each opportunity's location, affected callers, current requirement or supported
upcoming change, the knowledge that would become local, correctness risk, and
migration and verification costs. Frequent coordinated edits can expose scattered
ownership; a consequential low-frequency failure can still take priority.
Select the opportunity the evidence justifies
now, scoped to the smallest change that delivers it, and explain why material
alternatives were deferred. A named decision needs no opportunity ranking;
speculative cleanup does not become an automatic backlog.

Use available specialists by registered name when their evidence is needed:

- `explain-code`: establish the current mechanism and ownership.
- `explain-decisions`: recover a consequential constraint before replacing the
  ownership or layering it motivated; distinguish recorded reasons from inference.
- `analyze-change-effects`: investigate a deciding compatibility or indirect-consumer
  assumption.
- `prototype`: resolve an empirical uncertainty; supply the alternatives,
  constraints, and deciding observation, and retain the result's limits.

Resolve skills through the host's catalog or supplied named context. Do not claim
an unavailable specialist ran. Perform optional bounded work directly when useful
and state material evidence gaps. If requested help or evidence is essential and
inaccessible, report the blocker and continue only independent work.

Separate requirements from preferences and assumptions. If undecided behavior
or a conflicting term changes the public contract, ask before choosing the
affected design. Continue only work common to the plausible answers. Do not guess
a business rule to make a type sketch look complete.

## Shape the interface from usage

Write a representative caller interaction first: inputs, result, and a material
failure or lifecycle case. Derive public types and operations from that use. Show
what existing callers would change, keeping usage and signatures consistent.

Choose data structures from valid domain states and dominant access patterns.
Name who owns each invariant and how it is enforced. Group behavior around the
knowledge it protects, rather than giving every execution stage its own module.
Avoid storing values that can be derived reliably.

An interface includes everything callers must know: types, ordering, errors,
configuration, cancellation, and relevant resource costs. Prefer a small surface
that hides substantial decisions and coordination. A short signature that leaves
callers managing internal rules is not a simple interface.

For persistent state, concurrent actors, external protocols, or changes to domain
meaning, read [references/state-and-boundaries.md](references/state-and-boundaries.md).
Use the project's language, terminology, and module conventions. Introduce terms
or abstractions only when they clarify a real distinction.

## Compare and choose

For an unsettled structural choice, sketch at least two materially different ways
to meet the same requirements. Vary ownership, the data model, or the caller's
interaction; renaming the same design is not an alternative. Include the current
shape when viable. Use an established pattern or a design forced by constraints
without manufacturing options; explain the deciding constraint.

Compare correctness, caller effort, change locality, state and reading effort,
and implementation, migration, verification, and relevant runtime costs. Check
whether an edit made from one caller or example would stay correct across the
subsystem. Unknown performance or provider guarantees remain assumptions until
measured or established from evidence.

Screen for pass-through layers, exposed private representations, duplicated
policy, parallel routes for the same contract, hand-maintained registry copies,
and callers coordinating internal stages. Try removing a suspect layer: does
complexity disappear or spread into consumers? Access control, isolation,
adaptation, or ownership can justify a boundary with one implementation; counts
of files, adapters, or callers do not settle its value.

Prefer one maintained route for the same contract. Preserve supported protocol
surfaces, platform variants, and compatibility paths while consumers need them;
retire them only within an authorized migration that accounts for those consumers.
Derive related registries from an authority or check their
defined relationship; independently meaningful lists need not be identical.

For each material boundary, name the failure it must prevent, its owner, and the
existing structural, type, lint, test, or build mechanism that can enforce it.
Read [references/structural-checks.md](references/structural-checks.md) when
designing, adding, or changing a check, or when a boundary change exceeds an
existing check's demonstrated coverage. Reuse current evidence for an unchanged
check only if it still covers the affected paths and contract. Proposed
enforcement and demonstrated enforcement are different completion states.

Use `compare-solutions` for requested independent attempts, or when independent
complete designs justify the work and delegation is authorized. Give candidates
the same grounded task and constraints with this skill as their design specialist.
It owns isolation, judgment, synthesis, and execution evidence. A participant
produces its assigned design without starting another comparison; one agent's
sketches are alternatives, not independent attempts.

Recommend the simplest coherent option that meets the requirements. Give the
decisive evidence, accepted costs, and reasons meaningful alternatives lost.
Combine useful ideas only when they preserve the chosen ownership and invariants.

## Carry the decision through and verify

Trace usage through the chosen shape, including the deciding failure or lifecycle
case. Check types, ownership, invariants, and dependencies agree. Name observable
checks through the interface callers use; internal tests can supplement them.
Retain useful coverage when merging or replacing modules.

For a design-only request, return the shape, representative usage and signatures,
data or module flow, alternatives and costs, unresolved assumptions, and the
implementation and validation plan. Run existing commands on an executable
sketch only when they establish a material claim. A type check proves type
consistency, not runtime correctness. Keep disposable sketches in permitted
scratch storage, outside product code; do not leave throwing stubs or claim an
unexecuted check passed.

During authorized implementation, prove one cohesive caller-to-result slice
before generalizing a wider migration. Preserve supported behavior and constraints,
connect the selected boundary checks to the project's actual verification path,
remove obsolete structure where justified, and verify the resulting behavior.
Repeated caller knowledge of hidden rules, type escapes, duplicated policy, or
unexpected shared writes can invalidate the model: revisit the affected
assumptions and compare a revised shape before
adding workarounds. A necessary edge case alone does not justify a rewrite.

Scale the handover to the decision. Use diagrams when relationships are clearer
visually. Create a glossary or decision record only within the documentation scope
or established convention; record a consequential, non-obvious choice when real
alternatives were considered. Report the implemented slice, actual checks and
outcomes, and any remaining migration or enforcement gap. Return to the caller's
larger task when its authorized work remains.
