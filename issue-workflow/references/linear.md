# Linear

Resolve the issue's workspace and team before listing workflow states. State names
and IDs are team-specific. Discover the available tool schema, fetch the issue,
inspect its team states and update only the configured state ID. Preserve labels,
assignee and other fields. Re-fetch the issue to verify the result.
Use connection metadata or the available account-identity read to verify the
acting account and workspace under the shared actor rule before a write.

Inspect the GitHub integration's event and branch rules when it owns transitions.
Draft/open/ready/review/merge events can map differently, including by target branch.
Do not infer that a connected integration has the desired rule enabled. Verify
the relevant linked PR and whether its relation is completing or contributing;
that distinction affects merge automation. Check relevant additional linked PRs
against the project's completion rule.

If automation is configured, observe its result without an additional agent write.
If its settings are inaccessible, report the missing evidence. Neither a ticket
link nor a successful PR creation proves that the state transition occurred.

Primary provider reference: https://linear.app/docs/github
