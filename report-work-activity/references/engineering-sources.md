# Engineering sources

Read for Git, PRs, tickets or incident work. Discover read-capable MCP/CLI surfaces
and inspect their actual schemas/help. Use provider account identity and the
specific tenant; never expose tokens. Paginate through the declared scope. Search
results are candidates until action timestamps and roles are inspected.

## Git and pull requests

Use connected GitHub tools or `gh` when available. For `gh`, follow the account
procedure below before querying activity. Query authored PRs, merges,
submitted reviews and comments as distinct workstreams. Keep full IDs and URLs.
Filter merges by merge time and author; track merge actor separately. Retrieve
review records and their `submitted_at`, author and state. `reviewed-by`,
`involves`, `updated` and notification searches alone cannot date a review. Draft
reviews have no submitted event. Comments can be meaningful work without being
a formal submitted review.

Check pagination and search caps. Split a capped interval or repository scope;
keep any remaining gap visible. Contribution graphs, GitHub event feeds and JQL
totals can cross-check retrieval, but their distinct scopes are not substitutes
for actor-linked event inventories.

Local Git is an additional source when relevant roots are known. Preserve canonical
repository, full SHA, author email/date and committer date. Exact-match verified
aliases after retrieval; avoid regex surprises in author filters. Git's date
limiting can use committer time, so it cannot alone establish an author-date
report. Retrieve a sufficient history range and post-filter the chosen action
time, recording shallow/inaccessible history. Exclude merge commits from authored
commit metrics. Mark unpushed/local-only work accurately; a commit is not release
evidence. Coauthor trailers describe another role, not the main author.

### All configured GitHub CLI profiles

Inventory every configured account on every host with `gh auth status --json hosts`,
without `--active` or `--show-token`. Honor the effective `GH_CONFIG_DIR`; repeat
for other configuration directories explicitly known from the user's setup.
Record configuration context, hostname, login and each account's authentication
state. JSON mode can exit successfully with account errors: inspect every entry.
Include inactive accounts in the report's scope unless explicitly excluded.

Environment tokens override stored credentials. For the stored-profile inventory,
remove `GH_TOKEN`, `GITHUB_TOKEN`, `GH_ENTERPRISE_TOKEN` and
`GITHUB_ENTERPRISE_TOKEN`, plus `GH_HOST`, only from the inventory subprocess.
When token variables are present, also run status in the inherited environment
and retain entries whose `tokenSource` names an environment variable. This discovers
environment-only connections on known hosts without printing credentials. A failed entry without
a login is an unresolved connection, not an identified account.

Bind each retrieval to one configuration context, host and verified account.
Prefer an existing account-bound read tool. For a stored `gh` profile, capture
`gh auth token --hostname HOST --user LOGIN` inside a process. For an environment-
only connection, reuse its effective credential in memory with its known host;
it need not have a stored `--user` entry. Supply the credential only to that
process's `gh` subprocess environment. Keep the same configuration directory
through inventory, token lookup and retrieval. Use `GH_TOKEN` for `github.com`
and `*.ghe.com`, or `GH_ENTERPRISE_TOKEN` for other Enterprise hosts, clearing the
four inherited token overrides before setting the selected one. Set `GH_HOST`
to the selected host in that environment; commands such as `gh search prs` have
no hostname flag. Clear inherited `GH_REPO`; use `--repo HOST/OWNER/REPO` for
`gh pr` commands, or `--repo OWNER/REPO` for searches on the bound host.
Pass the same hostname explicitly in retrieval commands when supported, and record
it in query provenance. Resolve the login and stable user ID with `gh api user`
without `--hostname` in that environment so the identity check also tests
default-host resolution. For a stored profile, require the login to match the
inventory; check any previously verified ID too. Retrieve activity only after that
identity check, with the same binding.

Keep credentials out of tool output, command arguments, files, worker briefs and
logs; disable shell tracing and `GH_DEBUG`/`DEBUG`, and set `GH_PROMPT_DISABLED=1`.
Do not run `gh auth token` as a standalone visible tool call. Preserve the global
active account: `gh auth switch` is not an isolation mechanism for concurrent
workers. If a worker cannot use a safe binding, the primary fetches its scoped
records for Luna; if neither can, mark that profile's retrieval blocked.

The retrieving account is not necessarily the person who performed an action.
Confirm which discovered accounts belong to the user from existing mappings or
the user when unresolved. Put every confirmed login in `identities` as a separate
host-qualified stable user ID; merge aliases of one account, not different logins
owned by one person. Each bound profile queries all confirmed user identities on
its host across accessible repositories, rather than only its own login or `@me`.
A bot or shared credential does not make its actions the user's. Classify each
repository by confirmed work context, independently of which profile found it.
Record access failures, expired accounts,
SSO restrictions, rate limits and pagination gaps per profile/workstream; continue
the others and show incomplete coverage instead of zero activity.

Deduplicate sightings across profiles by hostname and native event/entity ID;
include the repository for repository-scoped numbers. Retain all retrieval
provenance. Do not put the retrieving login or config directory in the canonical
event ID. The same login, PR number or native ID on
different hosts remains distinct. Keep one canonical repository classification
when several profiles return the same event.

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
- GitHub CLI account inventory, credential selection and environment precedence:
  https://cli.github.com/manual/gh_auth_status
  https://cli.github.com/manual/gh_auth_token
  https://cli.github.com/manual/gh_help_environment
- Source skills and immutable revisions are recorded in `origin.txt`; runtime
  access, query limits and provider-specific fields must be checked on the host.
