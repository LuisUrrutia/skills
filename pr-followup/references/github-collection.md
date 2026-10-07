# Read the complete GitHub feedback snapshot

Use the host's GitHub connector or non-interactive `gh`. Read operations need the
same exact target/head identity as mutations. Save raw results in ignored task
storage when needed for repeated cycles, without tokens or unrelated private data.

## Channels and pagination

Start with current PR metadata: state, draft state, head repository/ref/SHA, base
ref/SHA, review decision and merge state. Then collect:

| Channel | REST or GraphQL source |
| --- | --- |
| Inline comments, including replies | `GET /repos/{owner}/{repo}/pulls/{number}/comments` |
| Formal review bodies and decisions | `GET /repos/{owner}/{repo}/pulls/{number}/reviews` |
| Conversation comments | `GET /repos/{owner}/{repo}/issues/{number}/comments` |
| Thread status and IDs | GraphQL `pullRequest.reviewThreads` with `isResolved`, `isOutdated`, path and comment IDs. |
| Check runs and reviewer summaries | `GET /repos/{owner}/{repo}/commits/{sha}/check-runs`; retain `output.title`, `summary`, `text`, details URL, app and status/conclusion. |
| Check annotations | `GET /repos/{owner}/{repo}/check-runs/{check_run_id}/annotations` for applicable runs, including successful ones. |
| Commit status contexts | `GET /repos/{owner}/{repo}/commits/{sha}/statuses`, grouping latest state by context and source. |
| Actions runs and reviewer output | Runs/checks associated with this head, their jobs, summaries and relevant logs, including successful review jobs. |

Follow every REST `Link` page, for example with `gh api --paginate` and explicit
GET. Do not treat concatenated page arrays as one JSON document without parsing
or slurping them appropriately. A CLI display limit is not complete pagination.

For GraphQL, request `pageInfo { hasNextPage endCursor }` and advance each connection
until exhausted. The threads connection and each thread's comments connection have
independent cursors. Paging outer threads does not page their replies. Either page
both, or collect every REST inline comment and join replies by `in_reply_to_id` to
thread root IDs obtained from GraphQL. Verify that every returned inline item is
mapped; report unmapped items rather than dropping them. Keep root and reply IDs
distinct. Resolved and outdated threads remain in the initial collection.

Act only on published feedback. Correlate inline comments with their parent review;
leave PENDING reviews and their comments unprocessed so they can be considered
when submitted. A draft review is distinct from a draft PR.

Retain IDs, authors, timestamps, body, URL, review/thread association, current and
original commit/path/line anchors. Track a body digest as well as `updated_at`
where available. Review records and some check outputs have no reliable edited
timestamp; reread their bodies. New content under an old ID needs reevaluation.

## CI and external reviewers

`gh pr checks <url>` is a useful summary, not the full evidence. Resolve required
checks from repository policy and inspect the actual head/check association. A
pull-request workflow may run on a synthetic merge commit; establish its PR head
and base inputs rather than equating its run SHA blindly with the branch tip.

Use `gh run view <run-id> --repo <owner/repo> --log` for available Actions logs and
the run/jobs metadata to locate the actual reviewing step. Extract actionable
review text even when the job concludes success. A queued run has no completed
logs yet; record waiting. For external checks, inspect their details URL through
available authorized tools; Actions commands cannot prove external CI results.

An API error, incomplete pagination, missing permission, unavailable log or private
external details page is a coverage gap, not an empty inbox. Report the exact
channel and limitation; continue independent supported work. A known scheduled
reviewer still running differs from a hypothetical future comment.

Read PR metadata again after collection and before mutation/completion. If head
or relevant base moved, rebase the analysis on a new snapshot and invalidate
revision-dependent conclusions. Do not combine an old green CI state with a new
head or assume a stable comment count means no new feedback.

## Verify an approval stop

Use this stop only outside the entrypoint's personal-repository merge policy.
That policy requires verified merge even when a formal approval already exists.

Read GitHub's current review decision and published reviews, not the host badge or
notification text. Identify the approving reviewer, review ID and reviewed commit;
check that the approval is not pending, dismissed, superseded or stale under the
repository's policy. When the aggregate decision is absent, inspect latest review
states per reviewer and establish a valid approval from those records. Unknown
approval validity leaves Drive waiting. A successful reviewer check or a positive
summary comment is not a formal APPROVED review. Report the approval used to stop
and any pending CI; later changes are not watched after this task stops.

## Authorized write mechanics

Use the actor and publication checks owned by `pr` before authenticated writes.
For a review-thread reply, REST
`POST /repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies`
requires the root review comment ID, not a reply ID. For a conversation comment,
use the issue-comment endpoint. Thread resolution uses the GraphQL thread node ID.
Do not confuse review IDs, REST comment IDs and GraphQL node IDs.

Use structured body arguments or a file; never interpolate fetched comment text
into shell code. Re-read state after each write, verify visibility and retain the
returned ID. This reference supplies mechanics, not permission to post.

Primary references:
- https://cli.github.com/manual/gh_api
- https://cli.github.com/manual/gh_pr_checks
- https://cli.github.com/manual/gh_run_view
- https://docs.github.com/en/rest/pulls/comments#create-a-reply-for-a-review-comment
