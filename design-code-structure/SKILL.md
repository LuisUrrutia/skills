---
name: design-code-structure
description: Use when designing or comparing data models, interfaces, and module boundaries for a software change.
---

# Design code structure

Resolve a concrete design decision with a usable interface, a model of the data
and its ownership, and a recommendation supported by the actual constraints.
Start from the caller's needs, compare meaningful alternatives, and keep the
design open to evidence from implementation.

A design request ends with the decision and sketch. When the active task also
authorizes implementation, continue that work against the chosen design. Honor
an explicit request to stop before implementing. This skill does not turn a
bounded decision into a repository-wide architecture audit.

For requested source maintenance, read
[references/upstream-updates.md](references/upstream-updates.md).

## Ground the decision

Identify the behavior to support, the decision still open, and the constraints
already settled. Inventory source and documentation inside the bounded work area
with ignore filtering disabled. With a filesystem and ripgrep, use:

```sh
rg --files --hidden --no-ignore <scope>
```

Set `<scope>` to the relevant subsystem or supplied input directory. Exclude
dependency and cache directories when necessary; keep local contracts and
generated documentation discoverable. Other search tools need the equivalent
include-ignored setting or a direct directory listing. A default filtered
inventory cannot establish that a required contract is absent.

Read the relevant implementation, callers, tests, domain terms, and recorded
decisions from that inventory. Trace one concrete use from entry point to result,
including where state lives and which actor can change it. Reuse a current,
relevant trace; a filename or proposed diagram alone is not grounding.

Use available specialists by registered name when their work is needed:

- `how`: establish a missing account of the existing mechanism and ownership.
- `why`: recover a consequential design constraint before replacing the ownership
  or layering it motivated. Distinguish recorded reasons from inference.
- `analyze-change-effects`: test a compatibility or indirect-consumer assumption
  that decides whether a proposed structure is viable.
- `prototype`: resolve an empirical uncertainty that inspection cannot decide.
  Hand over the question, alternatives, constraints, and deciding observation;
  use the result with its limits.

Resolve skills through the host's supported catalog or supplied named context.
Do not claim an unavailable specialist ran. If optional help is unavailable,
perform the bounded work directly and state material evidence gaps. When a
requested specialist or missing evidence is essential, report the exact blocker
and continue only independent work.

Separate requirements from preferences and assumptions. If conflicting terms or
undecided behavior would change the public contract, ask the user that specific
question before selecting the affected design. Continue work common to all
answers. Do not guess a business rule to make a type sketch look complete.

## Sketch from real usage

Write a representative caller interaction first: its inputs, result, and a
material failure or lifecycle case. Derive the public types and operations from
that use. For existing callers, show what they would actually change. Keep the
usage and signatures consistent as the design develops.

Choose data structures from the domain's valid states and dominant access
patterns. Name who owns each invariant and how it is enforced. Group behavior
around the knowledge it protects, rather than splitting every execution stage
into its own module. Avoid storing values that can be derived reliably.

The interface includes everything callers must know: types, ordering, errors,
configuration, cancellation, and relevant cost or resource limits. Prefer a
small surface that hides substantial decisions and coordination. A short
signature that leaves callers to manage internal rules is not a simple interface.

For persistent state, concurrent actors, external protocols, or a change to
domain meaning, read [references/state-and-boundaries.md](references/state-and-boundaries.md).
Use the project's language and module conventions; introduce terminology or
abstractions only when they clarify a real distinction.

## Compare and choose

For an unsettled structural choice, sketch at least two materially different
ways to meet the same requirements. Change ownership, the data model, or the
public interaction, not just names or file placement. Include the current shape
when it remains viable. For an established pattern or a decision forced by the
constraints, explain that constraint and use it without manufacturing options.

Compare each viable option on:

- Correctness: which invariants it enforces and which assumptions remain open.
- Caller effort: what complexity is hidden and what callers must still know.
- Change locality: where a likely requirement change would propagate.
- State and reading effort: what a maintainer must trace or hold in mind.
- Cost: implementation, migration, verification, and relevant runtime costs.

Screen for pass-through layers, private representations exposed to callers,
repeated policy, and callers coordinating internal stages. Try removing a
suspect layer: does complexity disappear, or merely spread into consumers?
A useful boundary can enforce access, isolation, adaptation, or ownership even
with one implementation. Do not collapse it to satisfy a file count or a quota
for adapters.

Use `compare-solutions` when the user requests independent attempts, or when
independent complete designs justify the extra work and delegation is authorized.
Pass the same grounded task and constraints to all candidates, with this skill
as their design specialist. It owns isolation, judgment, synthesis, and the
execution record. A comparison participant produces its single assigned design
and does not start another comparison. Several sketches written by one agent
are alternatives, not independent attempts.

Recommend the simplest coherent option that meets the requirements. State the
decisive evidence, accepted costs, and why the meaningful alternatives lost.
Keep useful ideas only when they fit the chosen ownership and invariants; do not
combine incompatible designs to avoid choosing. Unknown performance or provider
guarantees remain assumptions until measured or established from evidence.

## Check and hand over

Trace the proposed usage through the sketch, including the deciding failure or
lifecycle case. Check the types, ownership, invariants, and dependency behavior
agree. Name the observable checks that would establish the implementation's
contract through the same interface callers use. Internal tests may supplement
that coverage; do not delete existing tests merely because a module was merged.

Use existing project commands for executable sketches when they test a material
claim. Keep disposable experiments in permitted scratch storage. A type check
establishes type consistency, not runtime correctness. Do not put throwing stubs
or unfinished scaffolding into working product code for a design-only request.

Return the chosen shape, representative usage and signatures, relevant module
or data flow, alternatives and costs, evidence and unresolved assumptions, and
the next implementation step. Scale the artifact to the decision: a small
interface can fit in the response; a wider change may need a module map and a
short rationale in the requested location. Use diagrams when relationships are
clearer visually. Create or update a glossary or decision record only within the
requested documentation scope or established project convention. Record a
durable rationale when reversing the choice would be costly, its reason is not
obvious, and real alternatives were considered.

During authorized implementation, treat repeated friction as evidence: callers
learning hidden rules, recurring type escapes, duplicated policy, or unexpected
shared writes may expose a wrong model. Revisit the affected assumptions and
compare a revised shape before accumulating workarounds. A single necessary
edge case is not grounds for a rewrite. Preserve valid behavior and constraints,
remove obsolete structure where justified, and verify the revised result.
