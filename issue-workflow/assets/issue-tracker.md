# Issue tracker

Policy status: **Unconfigured**. This template authorizes no transition until
the relevant scope and row are filled from project decisions and verified service
data. Save the configured document at the policy path the applicable
instructions designate, defaulting to the consuming project's
`docs/agents/issue-tracker.md`, and drop fields and guidance that change no
decision there.

## Tracker

- Provider and canonical URL: unresolved.
- Code repository and final integration branch: unresolved.
- Ticket lookup and branch/PR linking convention: unresolved.
- Completing versus contributing PR relation: unresolved.
- Closing keywords and their effects, for GitHub issues: unresolved.
- Default project and issue type for published tasks, if any: unresolved.

## Workflow scopes

| Scope | Selector (fields of the fetched ticket) |
| --- | --- |
| Unresolved | Unresolved: Jira project key and issue type IDs; Linear team; or GitHub issue repository, plus Project when used |

Excluded scopes: unresolved.

## Scope: unresolved

Copy this section for each scope. Record each state with its provider ID where
one exists; the ID governs. `Any` means any verified branch of the target code
repository the policy was selected for. Name allowed source states explicitly
and remove unused rows.

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

These apply to every scope unless a scope section states its own value for an
item.

- Evidence that this PR completes the ticket: unresolved.
- Other required PRs/subtasks and how their completion is checked: unresolved.
- Partial contributions and intermediate stack merges: unresolved.
- Manual progress/source-state exceptions: unresolved.
- Rework or reopening policy, if needed: unresolved.
- GitHub issue closure versus Project Status changes, if applicable: unresolved.
- Required transition fields and their approved values, if applicable: unresolved.

## Delivery ownership

- Identity of each automation rule that owns a transition: unresolved.
- For agent-owned merge events, how an agent is invoked after merge: unresolved.
