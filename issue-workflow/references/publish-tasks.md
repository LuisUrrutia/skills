# Publish prepared tasks

Read for requested ticket creation, updates from a breakdown, or their read-only
preview. This route publishes an existing task contract; `task-breakdown` owns
dividing a feature into coherent, verifiable units. If it is needed but unavailable,
retain prepared work and report the missing decomposition phase.

## Resolve scope before writing

Use the requested provider and the project's canonical tracker convention. Read
its existing policy when present, but missing lifecycle-transition rows do not
block otherwise specified ticket creation. Publication does not configure those
rows or start implementation. Resolve the workspace/team/project or repository,
intended task set, existing ticket identities, and any requested parent or board.
Do not substitute a different tracker when lookup or publication fails.

A request to prepare tasks produces drafts. A request to create tickets authorizes
those tickets and the specified breakdown's relationships, not arbitrary backlog
changes, new projects, workflow configuration, assignments or comments. Before
any write, read [identity.md](identity.md) and verify the actor and target scope.

Inspect the available connector or CLI schema and actual required creation/update
fields. For Linear, verify the workspace/team and permitted fields; for Jira, the
site, project, issue type and its required fields; for GitHub, the issue repository
and any explicitly requested Project membership and field IDs. Discover technical
IDs from the service. Use explicit or documented project defaults for required
choices; ask only when an unresolved business choice materially changes the task.
Do not install integrations or change credentials as a fallback.

Preserve the provider's initial state unless the request or project creation
convention supplies another. Verify the resulting state. Never transition tasks
to In Progress, mark them done, or close a parent because a breakdown was published.

## Preserve the task contract

Keep each unit's outcome, scope, acceptance checks, relevant contract and source
links, prerequisites, integration limits and review-size budget. Retain the cap
and additions-plus-deletions counting rule in the ticket so a new executor can
enforce it before publishing the PR. Do not publish the whole project plan as one
implementation ticket when the supplied units are smaller delivery boundaries.

Before creating, inspect existing records for this work. Match stable IDs and
verified scope rather than assuming equal titles mean equal tasks. Preserve
existing identities, completed work, manual progress and unrelated fields. Update
an existing record only within the requested scope; an ambiguous match needs
resolution before that item's write. Do not create mirrors in a second tracker.

Publish prerequisites before dependents. Create a parent only when requested or
required by the verified project convention. Use supported native blocking and
parent/child relations for the specified tasks, verifying direction and identities;
otherwise record explicit linked blockers in their descriptions and report the
fallback. Do not impose a linear chain on independent units. Read back content,
scope and relationships after writing; a returned ID alone does not prove them.

## Reconcile partial outcomes

Retain a compact unit-ID to ticket-ID/URL map in the authoritative task record.
Record confirmed items before proceeding so a resumed run can reuse them. Keep
one source of progress; publication is not permission to maintain competing boards.

After a timeout or uncertain write, inspect the target service before retrying.
Use supported idempotency keys where available. If the item or link exists, verify
and reuse it; if absence is established, retry at most once for a transient error.
If the result cannot be determined, stop writes that could duplicate it and retain
the uncertainty. A dependent link waits for a verified prerequisite identity.
Continue independent requested items when their writes cannot duplicate or depend
on the uncertain one. Never delete confirmed tickets to conceal a partial result.

Return each unit as drafted, created, updated, unchanged, blocked or unknown, with
verified ticket URLs and relationships when available. Report exact failed fields,
lookups or writes and pending work. Creating tickets does not authorize a delivery
state transition; return to the caller's already-authorized next phase.
