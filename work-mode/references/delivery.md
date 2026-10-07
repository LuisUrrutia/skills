# Delivery and waiting

Read this when the selected task includes ticket publication, PR work, or another
external delivery phase. Keep the active request's endpoint and limits with the
responsible owner; this reference composes existing procedures.

## Select one delivery owner

- For requested publication of a prepared task breakdown, use `issue-workflow`
  in Publish mode with units, target tracker, existing IDs, and publication scope.
  A breakdown alone does not authorize creating tickets. Preserve useful artifacts
  and independent implementation when publication is blocked.
- For one PR, use `pr` with its exact operation, repository/head/base, verified
  changes, validation, linked ticket or lookup hint, and explicit create-only or keep-draft
  limits. Its Create operation normally continues into `pr-followup` Drive.
  Let that owner continue; do not start another follow-up loop on its return.
- For dependent branches or PRs, use `stacked-pr` with the selected units, actual
  dependencies, topology, and requested operation. Keep one stack mutation owner.
  Independent units do not become a stack merely because they share a project.
  Stack publication ends at that operation's verified result; it does not inherit
  single-PR Create's Drive default. Continue follow-up on layers when the request
  includes it, preserving `stacked-pr` as the topology and rebase owner.
- For an existing PR's requested feedback or monitoring, use `pr-followup` with
  the exact PR, current revision, feedback/CI evidence, permitted actions, and
  stopping condition. An Update performed by `pr` inside that loop returns to it.
- For a requested merge, release, or deployment beyond those results, resolve
  the project's existing owner and required authority. An approved or published
  PR does not establish those later actions or their evidence.

Require the owner's observed result: ticket IDs and verified state, or the exact
PR and expected head/base/state, with remaining work and current evidence. Local
commits do not prove publication. After an uncertain external write, let its
owner inspect the remote result before retrying; avoid duplicate effects.

## Carry the review budget

Pass the established review budget and any explicit numeric cap, with its source,
to the publishing owner. There is no default numeric ceiling. `pr` owns Check cap;
`stacked-pr` calls it for each layer's actual immediate base and selected head.
Use the owner's current verdict instead of copying the measurement procedure.

An over-cap or unverified result blocks capped publication. Return the scope and
source revision to `task-breakdown` for revised units, then to the execution owner
for authorized restructuring. A new plan or more commits does not itself shrink
the PR. Remeasure through Check cap after relevant base/head changes. Preserve
requirements and completed work; report a needed but unauthorized rewrite while
continuing independent ready work.

## Preserve continuation and waiting

Keep the owner's actual endpoint. Explicit create-only can end after verified
publication. Keep-draft constrains readiness while preserving authorized Drive
work. Green CI, an empty feedback queue, and merge-ready do not replace
`pr-followup`'s current formal-approval or merge stop. An enclosing task that also
requires a later result retains that work after follow-up returns.

While Drive is waiting, retain its PR identity, revision, pending event, and watch
owner. Use the host-supported watch and yield the current turn. On a wake, resume
that owner, refresh remote state, and reconcile earlier actions before continuing.
If a child cannot own the watch, return that responsibility to the parent. An
unavailable resumable watch is a specific coverage limit; do not replace it with
agent polling or an unrequested recurring schedule.

Keep ticket synchronization results separate from PR progress. `pr` and
`pr-followup` carry their configured events through `issue-workflow`. After a
stack operation, the coordinator checks which events were already handled and
invokes `issue-workflow` for any missing configured event. Pass verified per-layer
PR state and completing or contributing ticket relations; preserve native event
ownership and report blocked transitions separately. This invokes the existing
owner, not installation or modification of persistent hooks.

Formal approval does not emit a merge event. Preserve the configured durable
merge-event owner or report the uncovered event; do not promise a wake or continue
Drive beyond its stopping condition just to hide that gap.
