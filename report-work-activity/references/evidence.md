# Evidence and counting contract

Read before collection. `bundle.md` defines the helper's input fields; these rules
define their meaning. The primary accepts records only after the checks below.

## Time and attribution

Use `[start, end)` in the user's timezone, converted to precise instants for each
provider. A search date, file modification time, session creation time or object's
last update is a candidate filter. The underlying action timestamp decides
inclusion. Unknown times remain contextual evidence and do not enter period
counts. Record query scope, retrieval time and timestamp semantics.

Match stable user IDs within the provider tenant/account; keep verified email
aliases for Git and mail. Normalize aliases to the same verified provider ID in
identities and records before counting. Prefer immutable IDs; apply casing rules
only when that provider establishes them, never lowercase every ID or address.
If a mismatch could be an unresolved alias, keep the role unknown until checked;
known other actors remain excluded. Do not use a display-name match or infer a historical
assignee from the current one. Preserve source roles: author, merger, reviewer,
responder, resolver, assignee, sender, participant. Tool execution by an agent
working for the user is an assisted contribution; it does not prove personal
typing, deployed results or time spent. Do not count bots' independent actions
as the user's actions.

## Metric definitions

Choose the metrics that help this report. Never sum different units into a
productivity score. The helper provides these fixed definitions:

| Key | Counting unit and evidence |
| --- | --- |
| `authored_prs_merged` | Unique PRs authored by the user, merged during the period; merger can be someone else. |
| `prs_merged_by_you` | Unique PRs whose merge actor is the user. |
| `prs_opened` | Unique PRs created by the user during the period. |
| `prs_reviewed` | Unique PRs with a submitted review by the user in the period. |
| `reviews_submitted` | Distinct submitted review events by the user. |
| `tickets_closed` | Unique tickets with a completed-state transition performed by the user in the period. |
| `assigned_tickets_completed` | Unique tickets completed while assigned to the user, supported by the assignee at that transition. This does not credit the user as closer. |
| `incidents_attended` | Unique incidents with an evidenced response action by the user. Being on call, paged or assigned is insufficient. |
| `incidents_resolved` | Unique incidents with a resolution action attributable to the user. |
| `commits_authored` | Distinct canonical-repository/full-SHA commits authored by a verified user alias; local-only status remains visible. |
| `emails_sent` | Distinct sent messages attributable to the user, excluding drafts, incoming quotes and automated mail. |
| `meetings_attended` | Unique meeting occurrences with participation evidence; scheduled/accepted meetings remain narrative context. |

Keep a ticket closed then reopened in its historical closure count and explicitly
show its current state and any renewed assignment. Repeated closures count once
per ticket, not once per transition. Similar titles and patch IDs alone do not
establish identical events. Squashed/rebased commits can be linked to one story
without redefining distinct commit counts. A PR review and the PR merge are
different events with one shared entity ID.

Classify by confirmed work context, including employer open-source repositories.
Apply repository exceptions before organization/container defaults. Record the
mapping evidence and any assumption. Link a cross-repository ticket to all
affected repositories, but put its metric in one explicit home or the
non-repository/multiple-repository row; do not duplicate it into each total.

## Coverage and obligations

For every source/workstream keep its account/container scope, query, retrieval
time, pagination outcome, inaccessible portions and retention limits. A complete
result means complete only within that declared scope. A source's failure is not
an empty result. Counts with incomplete relevant retrieval are observed lower
bounds; when none were observed, show unknown rather than an apparent zero total.
Missing classification can also make a bucket total incomplete. Do not derive
counts from just the interesting items a summarizer selected.

Pending work is an as-of snapshot, independent of historical date filtering.
Collect open assignments even when created before the period. For promises and
requests, search accessible prior unresolved threads or an earlier report's open
items, then check subsequent context. If that backlog is not fully searchable,
state its lookback and gap. Distinguish an explicit promise by the user from a
suggested action or an unanswered request. Require an owner, original evidence,
known status and check time; normalize relative due dates against the original
message and timezone, never against report generation. Unclear owners/dates stay
unclear. Suggestions are not added to the user's commitments.
