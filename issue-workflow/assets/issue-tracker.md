# Issue tracker

Policy status: **Unconfigured**. This template authorizes no transition until
the relevant row and scope are filled from project decisions and verified service
data. Save the configured document in the consuming project's
`docs/agents/issue-tracker.md`, or maintain its existing canonical policy path.

## Tracker and scope

- Provider and canonical URL: unresolved.
- Workspace, team or Jira project: unresolved.
- Code repository and final integration branch: unresolved.
- GitHub Project URL/ID and Status field, if used: unresolved.
- Ticket lookup and branch/PR linking convention: unresolved.
- Completing versus contributing PR relation: unresolved.
- Closing keywords and their permitted effects: unresolved.

## Transition rules

Use exact states from this scope. `Any` below means any verified branch in this
repository; it does not cross repository or ticket scope. Name allowed source
states explicitly and remove unused rows.

| Rule | Event | Target branch | Allowed source states | Destination | Conditions | Owner | Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | `work-started` | Any | Unresolved | Unresolved (intended: In Progress) | Implementation actually starts | Unresolved | No |
| Review | `pr-created` | Unresolved | Unresolved | Unresolved (intended: In Review) | PR exists; drafts included | Unresolved | No |
| Merge | `pr-merged` | Unresolved | Unresolved | Unresolved | Completion conditions below hold | Unresolved | No |

The Review event can explicitly be changed to `pr-ready`. Set one review event;
do not silently exclude drafts while keeping `pr-created`. Give each event one
owner: `agent`, or the exact native/external automation rule.

For example, a project might choose Ready for QA after a completing PR merges
into its final integration branch, while another chooses Done. Multiple branches
can have different rules. These examples do not choose this project's destination.

## Completion and exceptions

- Evidence that this PR completes the ticket: unresolved.
- Other required PRs/subtasks and how their completion is checked: unresolved.
- Partial contributions and intermediate stack merges: unresolved.
- Manual progress/source-state exceptions: unresolved.
- Rework or reopening policy, if needed: unresolved.
- GitHub issue closure versus Project Status changes, if applicable: unresolved.
- Required transition fields and their approved values, if applicable: unresolved.

## Delivery ownership

- Automation rule URL/ID, event filters, branches and enabled/configuration
  evidence for each automation-owned event: unresolved.
- For agent-owned merge events, how an agent is invoked after merge: unresolved.
- If no durable merge handler is configured, record: "Merge synchronization runs
  only when an agent observes the merged PR. Unattended delivery is not configured."

Execution procedure: use `issue-workflow` with this policy.
