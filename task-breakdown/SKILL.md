---
name: task-breakdown
description: Use when dividing a software plan or feature into small, testable tasks sized for human-reviewed pull requests.
---

# Task breakdown

Turn a defined feature or implementation plan into delivery units a person can
review and an executor can implement and verify. Normally, one unit becomes one
ticket and one PR. Keep a cohesive change in one unit when it already fits.

`wayfinder` owns direction; `planning` owns the overall approach and implementation
plan. This skill owns delivery boundaries, acceptance checks and dependencies.
`issue-workflow` owns authorized ticket publication; `pr` owns individual PR
publication; `stacked-pr` owns dependent branches and PR operations.
Resolve collaborators by registered name. If a needed
owner is unavailable, preserve the breakdown and report the missing phase.

A breakdown request authorizes its requested artifact, not implementation, ticket
publication, branch creation or deployment. Continue those phases when already
authorized. A review-only request returns findings without editing the record.

## Establish the input

Read the request, authoritative plan, decisions, existing tasks and project
instructions. Inspect the affected code, callers, tests and configured checks.
Keep settled scope and contracts; do not turn decomposition into a new design
exercise. A formal planning document is useful input, not a prerequisite.

Resolve routine details from evidence. If a missing decision materially changes
the behavior, contract or feasibility of a split, ask for that decision and keep
only the affected work pending. Return connected direction questions to
`wayfinder`, or an incomplete implementation approach to `planning`, with the
exact gap; continue independent units. Do not invent a contract just to fill a
ticket template.

Use the existing authoritative record and requested format. A table in the plan
or chat can be enough; no separate document or ticket per unit is mandatory.
When resuming, reconcile actual completed work, existing IDs and changed premises
before revising remaining units. Preserve unrelated work and stable identities.

## Choose functional boundaries

Start with the smallest useful behavior that can be demonstrated after its real
prerequisites land. Include the layers needed for that behavior: data access,
backend, frontend and behavioral tests where applicable. Add further capabilities
as separate units. Name each unit after what it delivers, not a file or widget.

For a statistics dashboard, a useful first unit might deliver the revenue card
with its real query, permissions, endpoint, UI states and checks. Another can add
active customers. Neither a button alone nor the entire dashboard's backend is
a default boundary. Prefer a small production-testable path when the project
supports it; defining that check does not authorize a production action.

Keep implementation, its regression tests and required generated output together.
Avoid separating tests to meet a size limit, unrelated cleanup, or tickets for
each technical layer by habit. A backend prerequisite or frontend contract test
can be a valid unit when a complete vertical slice would be impractical. Read
[references/staged-delivery.md](references/staged-delivery.md) for such splits,
migrations, or units that cannot yet pass an end-to-end check.

Record dependencies by the exact capability or contract a unit consumes. Shared
files or environments can need coordination without creating a functional blocker.
Distinguish both from a preferred execution order. Resolve cycles through a smaller
shared contract or a cohesive unit. Do not force independent units into a stack.

## Budget for human review

Each PR must contain at most **5,000 changed text lines: additions plus deletions**
in its complete base-to-head PR diff. This is a ceiling, not a target. Honor a
stricter project limit. Changing the ceiling needs an explicit user decision;
an estimate, deadline, draft state or generated-file label cannot waive it.

For each proposed unit, estimate a range from the affected code and comparable
changes, include tests, migrations, generated text and lockfiles, and state the
basis and uncertainty. Aim comfortably below the ceiling so implementation and
review fixes can fit. Do not report an estimate as a measured diff or invent
precision from unavailable code. If the credible upper bound exceeds the ceiling,
reduce the unit's scope or resolve the sizing uncertainty before calling it ready.

Carry the numeric cap and counting rule into every task's execution contract.
Require a fresh measurement before PR publication and after scope, base or head
changes: sum additions and deletions for the intended PR base and head, never net
growth, individual commits, or the whole stack against trunk. Include all changed
text, without path exclusions. Record binary changes separately; a line count does
not measure their review cost. An unavailable or incomplete diff is unverified.

The publishing owner (`pr` or `stacked-pr`) checks the actual diff. If it exceeds
the cap, stop publication of that unit and revise the split; retain independent
ready work. Splitting commits does not shrink a PR. Do not discard required
behavior, tests or files, rewrite published history without authority, or hide
changes through formatting to make the count pass. A small count still needs a
coherent review boundary.

For code already on an oversized branch, pass the revised unit map and preserved
source revision to the execution owner. `stacked-pr` owns rebuilding dependent
layers from that map; independent units need separate branches through the active
branch workflow. A revised plan alone does not change the existing diff. Complete
the authorized restructuring and remeasure before returning to publication; if
the needed rewrite lacks authority, retain the map and report that exact boundary.

## Make each unit executable

Use the project's task format and include only details the executor needs:

- Stable ID and the concrete outcome; included scope and likely scope confusion.
- Relevant source paths, authoritative decisions, and consumed/produced contracts.
- True prerequisites by unit ID, plus separate coordination or release constraints.
- Acceptance scenarios with observable expected results, deciding commands or
  interactions, and environment/data prerequisites. Mark checks to add separately
  from existing checks; planned checks are not passing evidence.
- Why new coverage is needed, using the plan's rationale and existing tests. Keep
  meaningful failure and compatibility cases with the behavior they protect.
- Estimated changed-line range, its basis and uncertainty, and the actual PR cap
  of 5,000 additions plus deletions (or the stricter applicable limit).
- Supported intermediate state, how to exercise it, and any integration dependency
  that prevents claiming it production-testable yet.

Enough context must travel with each unit for a fresh executor, including relevant
contract excerpts when links alone are insufficient. Keep one task authority;
link shared decisions rather than duplicating a large plan or progress log.

## Check the breakdown and continue

Trace every material requirement to a unit and its acceptance evidence. Check
that dependencies are real and acyclic, each proposed PR fits its review budget,
and a unit demonstrates its stated result without waiting for unfinished work
unless that limitation is explicit. Specify where the combined capability is
verified; separate unit checks do not prove integration. Preserve blocked scope.

Return the breakdown or its location, dependency order, ready and blocked units,
sizing uncertainty, and next action. No additional approval gate is needed for
already-authorized work. For a drafting-only request, stop with the artifact.

When ticket publication is requested, pass the prepared units, target tracker,
existing IDs, relationships, plan links and publication scope to `issue-workflow`
in Publish mode. Retain drafted units if publication is blocked. If implementation
is already authorized, continue ready units through the existing workflow with
their acceptance and review-size contracts. Do not select worker topology here.

For requested source maintenance, use `agent-instructions` with `origin.txt`.
