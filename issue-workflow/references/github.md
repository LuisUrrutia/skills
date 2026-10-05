# GitHub issues and Projects

GitHub issue open/closed state and a Project's Status field are different. Resolve
the exact issue repository and, for a board transition, the project owner/number,
item, Status field and option IDs. Inspect current fields/options and current CLI
help or connector schema rather than assuming one command version. An issue can
belong to multiple Projects: update only the configured project and item.

If the issue is not in that Project, report the missing membership. Synchronizing
status does not authorize creating a board, adding an item, inventing a status or
using labels as an improvised board. Honor an existing label-based convention
only when the policy explicitly chooses that state representation and its effects.
Change only the designated state labels and preserve unrelated labels.

Before any authenticated GitHub write, follow the active actor-verification rules.
Read the field/state before editing and re-read that same object afterward. Project
access can require permissions separate from issue/PR access; report a scope
failure without automatically expanding permissions.

Closing keywords such as `Fixes` or `Closes` can close linked issues when a PR
merges into the default branch. A custom Project Status update alone does not
prevent that closure. When merge should leave the issue open for QA, use the
policy's non-closing relation and inspect existing auto-close links or board
workflows for conflicts. Do not automatically reopen an issue to compensate.

When built-in or external automation owns a state change, verify the relevant
rule and result. Do not infer that issue closure and the desired Project option
are equivalent or automatically synchronized.

Primary references:

- https://cli.github.com/manual/gh_project_item-edit
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations
