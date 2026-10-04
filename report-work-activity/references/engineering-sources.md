# Engineering sources

Read for Git, PRs, tickets or incident work. Discover read-capable MCP/CLI surfaces
and inspect their actual schemas/help. Use provider account identity and the
specific tenant; never expose tokens. Paginate through the declared scope. Search
results are candidates until action timestamps and roles are inspected.

## Git and pull requests

Use connected GitHub tools or `gh` when available, across the known accounts and
repositories rather than only the current checkout. Query authored PRs, merges,
submitted reviews and comments as distinct workstreams. Keep full IDs and URLs.
Filter merges by merge time and author; track merge actor separately. Retrieve
review records and their `submitted_at`, author and state. `reviewed-by`,
`involves`, `updated` and notification searches alone cannot date a review. Draft
reviews have no submitted event. Comments can be meaningful work without being
a formal submitted review.

Check pagination and search caps. Split a capped interval or repository scope;
keep any remaining gap visible. Contribution graphs, GitHub event feeds and JQL
totals can cross-check retrieval, but their distinct scopes are not substitutes
for actor-linked event inventories. Do not switch account state blindly or read
tokens into output; use the host's established account-selection mechanism.

Local Git is an additional source when relevant roots are known. Preserve canonical
repository, full SHA, author email/date and committer date. Exact-match verified
aliases after retrieval; avoid regex surprises in author filters. Git's date
limiting can use committer time, so it cannot alone establish an author-date
report. Retrieve a sufficient history range and post-filter the chosen action
time, recording shallow/inaccessible history. Exclude merge commits from authored
commit metrics. Mark unpushed/local-only work accurately; a commit is not release
evidence. Coauthor trailers describe another role, not the main author.

## Jira, Linear and reviews of tickets

Use available Jira/JSM or Linear read tools. For completed-ticket counts retrieve
the actual completion transition and its actor; current `Done`, `updatedAt`,
`completedAt` or `statusCategoryChangedDate` alone may omit prior transitions or
their authors. Keep assignee-at-transition distinct from current assignee. For
comments/reviews, use the comment/review event's author and creation time.

Read current open assignments independently of the historical window. Keep
reopened or reassigned work, explicit requests and commitments traceable. Preserve
tenant plus native issue ID/key, ticket links and any explicit PR relationship.
Custom status workflows require the project's actual completed-state meaning.

## JSM, PagerDuty and equivalent incident systems

Discover incident and timeline/log-entry retrieval; ticket access does not imply
access to the incident timeline. Read response/resolution actors and times,
service, impact, outcome and linked follow-up actions. Distinguish scheduled
on-call duty, notification, acknowledgment, active response and resolution.
Team resolution does not automatically credit the user. Keep unsupported roles
as context and explain the missing actor evidence.

An incident linked from JSM, PagerDuty, Slack and a postmortem is one incident
only when stable links or IDs establish that relationship. Preserve source event
IDs and a canonical incident entity for distinct response and resolution counts.
Use a non-repository service row when appropriate. Do not run incident-response
commands or mutate tickets to produce the report.

## Primary documentation checked during authoring

- GitHub review authors, timestamps and pending-state behavior:
  https://docs.github.com/en/rest/pulls/reviews
- Source skills and immutable revisions are recorded in `origin.txt`; runtime
  access, query limits and provider-specific fields must be checked on the host.
