# Jira

Resolve the site, then fetch the issue and take its project key and issue type ID
from the response. A moved issue keeps its old key as a redirect, so a key prefix
in a branch or PR does not establish the project. Fetch the currently available
workflow transitions, including required field metadata. Match the policy's
destination to an allowed transition, then pass that transition's ID and required
values through the available connector/API. A status ID is not a transition ID.
Verify the acting account and site through connection metadata or the available
account-identity read before writing, under the [shared actor rule](identity.md).

A ticket's workflow follows its project and issue type. Company-managed projects
map issue types to workflows through a workflow scheme that several projects can
share, and their statuses are site-wide objects reused across workflows.
Team-managed projects hold their own per-issue-type workflows with project-scoped
statuses. Sub-tasks often use a separate workflow. A company-managed board is a
saved filter with a column-to-status mapping: it can span projects and owns no
transitions, so it is not a scope.

Select a scope by project key and issue type ID; a project key alone
establishes one workflow only when the project has one issue type or a readable
scheme maps all of them to one workflow. When teams share one workflow
but follow different rules, add one stable ticket field that separates them, such
as the Team field, a component or a label their board filters use; record its
value in the selector and evaluate it against the fetched ticket. Sprint,
assignee and filter membership are not selectors. If no such field exists, the
policy must designate one or treat the teams as one scope.

Status and issue type names can be localized for the connected account, and
several statuses can share a name; record and match IDs. The workflow's full
state list is the project's statuses grouped by issue type
(`GET /rest/api/3/project/{projectIdOrKey}/statuses`), using the entry for the
ticket's issue type ID. Tools limited to issue, search and transition reads
cannot list it; to discover states during configuration, search per project and
issue type and read the transitions of representative issues.

More than one operation can reach a destination. Resolve required fields or
materially different transition effects before writing; do not choose the first
result, guess an ID or bypass the workflow with a direct status edit. Re-fetch
the issue after the operation.

Connected development tools can deliver PR-created and PR-merged automation events.
Inspect the actual rule, issue linkage, project filters and branch conditions
before treating automation as the owner. Merge is distinct from deployment or QA
completion; the project policy decides its target state.

Primary provider references:

- https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/
- https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-projectidorkey-statuses-get
