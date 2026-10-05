# Jira

Resolve the site, issue key and project. Fetch the issue and currently available
workflow transitions, including required field metadata. Match the policy's
destination to an allowed transition, then pass that transition's ID and required
values through the available connector/API. A status ID is not a transition ID.
Verify the acting account and site through connection metadata or the available
account-identity read before writing, under the shared actor rule.

Different workflows can use the same status name, and more than one operation can
reach a destination. Resolve required fields or materially different transition
effects before writing; do not choose the first result, guess an ID or bypass the
workflow with a direct status edit. Re-fetch the issue after the operation.

Connected development tools can deliver PR-created and PR-merged automation events.
Inspect the actual rule, issue linkage, project filters and branch conditions
before treating automation as the owner. Merge is distinct from deployment or QA
completion; the project policy decides its target state.

Primary provider reference:
https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/
