# CI, base maintenance and bounded observation

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

Prefer host notifications or a short bounded watcher. Otherwise poll around once
per minute, respecting API rate limits and any known reviewer cadence; keep waits
interruptible and progress updates regular. Never claim a persistent background
process exists unless it actually does. Do not create a recurring app schedule as
a side effect of a one-session Drive request.

For the post-ready pass, inspect workflow triggers and draft conditions, review
requests and available reviewer-app configuration to identify expected work. Use
current run and review state to establish what actually started; inaccessible
configuration remains unknown. Record the ready-transition time and the fresh
post-ready snapshot even when the head SHA did not change.

At each meaningful change, retain the original observation deadline, PR identity,
head/base, feedback versions and decisions, outstanding checks/reviewers, authorized actions, published fixes,
replies and retry counts. On resume, inspect remote state before acting; a wake-up
does not reset the deadline. Preserve others' watchers and scratch; stop and remove only resources owned by this run.

A final fresh pass must cover current channels and show whether known work is
complete. If required checks or reviewers remain active at the observation limit,
return waiting with their IDs/URLs. If required evidence is inaccessible, return
the exact blocker and completed independent work. Approval, draft and merge
requirements remain separate from technical repair completion. No quiet interval,
fixed pass count or lack of newly visible comments proves human approval.
