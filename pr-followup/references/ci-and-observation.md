# CI, base maintenance and event-driven observation

## Investigate failures without blocking independent feedback

Identify required, optional and pending checks for the actual PR head, including
external providers. Read the failing job, command, error and relevant source before
editing. Separate product defects, workflow configuration, environment failures
and observed flaky behavior. A file outside this diff does not prove a stale-base
failure; a failure seen elsewhere does not automatically make it irrelevant.

Use `debug` for uncertain causes and `github-actions` when changing workflow code.
Prefer a root-cause repair over disabling a check, weakening an assertion or adding
blanket retries. Rerun once when evidence supports a transient infrastructure or
flaky failure and the request authorizes reruns. If it recurs, investigate or
report the blocker rather than burning an unbounded retry loop. A new code fix
starts new relevant checks, not a way to reset the same unexplained retry budget.

Required policy decides what must pass. Account for optional failures and cancelled
or skipped required jobs explicitly; do not label all non-failing statuses as
success. A manual approval gate is pending authorization, not permission to approve
it. Keep useful code-feedback repairs moving while unrelated jobs run.

## Update the base when necessary

Update when the user asks, conflicts prevent integration, repository policy requires
it, or evidence connects a failure to a needed base change. Mere base advancement
does not require repeatedly rebasing a working PR.

Resolve exact head/base repositories and refs and save recovery tips. Use SSH and
rebase for an ordinary PR under the user's standing policy; route a stack to
`stacked-pr`. Respect checkout ownership and other contributors' commits.
In conflicts, read both sides' intended behavior and preserve relevant callers,
contracts and tests. Compilation alone does not prove a correct conflict resolution.
Regenerate derived files with project tools when appropriate; do not hand-edit a
lockfile merely to remove conflict markers.

Verify the resulting revision, then use `pr`'s exact-lease publication procedure.
If head changed elsewhere, stop this publication and reconcile; do not overwrite
the new contributor work or silently turn rebase into a merge commit.

## Observe, resume and stop

Separate feedback collection from CI waiting. After a publication, collect a fresh
snapshot for the new head, check review applicability and required policy, and
refresh the PR description from that published diff. Previous results can explain
history but cannot prove the new revision passed.

Use a resumable host watch when available and finish the agent turn while waiting.
Keep one watch per PR and thread; reuse an active watch rather than restarting it
after every message or push. When cadence is configurable, use elapsed wall-clock
time since this PR's Drive task began to choose the default interval:

| Elapsed time | Check interval |
| --- | --- |
| Less than 1 hour | 10 minutes |
| From 1 hour to less than 3 hours | 30 minutes |
| 3 hours or more | 1 hour |

Retain the original start time across wakes, pushes and watch recovery; those
operations do not restart the cadence. Honor an explicit user cadence override.
Apply interval changes through the host watch's interval setting, not agent polling.
If the host fixes the interval or cannot apply the transitions, disclose that
limitation and use its watch without adding a second agent loop.
The host's ordinary GitHub checks should not invoke a model; each delivered event
starts agent work and consumes tokens for its context, investigation and response.
Return compact status deltas and actionable findings to the model; avoid loading
unchanged logs and bot summaries repeatedly. Reread the evidence needed for each
new decision and the final coherent snapshot. Do not replace the watch with
repeated agent turns, sleep loops or recurring AI checks. If the host cannot resume this task, report the coverage gap. Do not create
a separate recurring schedule as a side effect of Drive.

Inspect the host's wake coverage and stop conditions. Edited comments, delayed
publication of pending reviews, or terminal PR states may not generate a wake.
Disclose uncovered events; notifications are prompts to reread GitHub, not a
complete inbox or proof of approval. When first arming a watch, close any gap
between the initial collection and activation with a fresh snapshot if the host
allows it. If it requires immediate yielding, disclose the gap and reread all
channels at the next wake.

For a user time limit, use a host expiry or an authorized one-shot wake to stop
the watch at the deadline. If neither is available, report that unattended expiry
cannot be guaranteed; merely remembering a deadline cannot wake a quiet thread.

Inspect the host's stop conditions. A watch may stop on closure, access failures
or a notification-loop guard, and may pause when the app is offline or the thread
is settled. Report interruptions. Re-arm only after checking the cause and current
PR state: recover an access failure when access works again, and investigate a
loop guard before resuming it. Never blindly restart a repeating notification loop.
On an approval event, verify current review state. Unwatch only if the stopping
condition holds; otherwise retain the existing watch. Merge or closure may stop
the host watch silently, with no final agent turn.

For the post-ready pass, inspect workflow triggers and draft conditions, review
requests and available reviewer-app configuration to identify expected work. Use
current run and review state to establish what actually started; inaccessible
configuration remains unknown. Record the ready-transition time and the fresh
post-ready snapshot even when the head SHA did not change.

At each meaningful change, retain the Drive start time, PR identity, head/base,
feedback versions and decisions, outstanding checks/reviewers, authorized actions,
published fixes,
replies and retry counts. Retain an observation deadline only when the user set one.
On resume, inspect remote state before acting. Preserve others' watchers and scratch;
stop and remove only resources owned by this run.

A fresh pass must cover current channels and show whether known work is complete.
Apply the entrypoint's personal-repository merge policy when it matches: technical
completion triggers a verified merge, and approval alone does not end Drive.
Otherwise Drive remains waiting for merge or a current formal approval after
technical work finishes. A user-imposed deadline returns waiting with outstanding
IDs/URLs, not success. If required evidence is inaccessible, report the exact blocker
and completed independent work. No quiet interval, fixed pass count or lack of new comments proves
approval. Stop this PR's watch when the stopping condition is verified.
