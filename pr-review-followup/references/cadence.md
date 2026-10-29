# Cadence

Read when starting or resuming the follow-up, and when a tick ends. Report a
recurring blocker, such as an incomplete review, an uncertain write or a thread
waiting on the user, once per change, not on every tick.

## T3 Code watch

In T3 Code, wait with `watch_pull_request`; an interval the user names selects
the schedule below instead. Each wake runs one `pr-review-followup` tick; reread
this skill first if it is no longer in context.

- When a tick ends waiting and no watch is on, arm it right after the tick's final
  read and end the turn. End that report with the PR URL, reviewer, state file
  path and "each T3 watch wake runs one `pr-review-followup` tick", and say that a
  comment posted after that read, and the events below, wait for another wake or
  invocation.
- It wakes on others' comments and reviews, check results, a push without checks,
  conflicts and closure. It never wakes on a thread resolved without a comment or
  push, a base change, a merge, comments by the account T3 Code reads with
  (normally the reviewer), or time passing. Each tick rechecks them; a merge ends
  the watch silently, so report it when next invoked.
- A watched thread stays out of the user's inbox, so unwatch before reporting a
  tick that ends for the user: approval, `done`, a closed PR, a new blocker that
  needs the user, such as an incomplete review, the reviewer's unsubmitted review
  or a thread waiting on the user, or progress that waits only on time or an event
  the watch never reports, such as retrying a review that failed before recording
  or clearing an uncertain write. A blocker already reported and unchanged since
  the user's reply ends the tick waiting instead.
- If arming fails, report why and schedule ticks as below.
- Its comment-only stop is a loop guard: find the cause, such as a bot answering
  each reply, before re-arming. After a stop for read failures, re-arm once reads
  work.
- A delegated child does not arm it; it returns its tick result to its parent.

## Schedule

Where the T3 Code watch does not apply, run one tick every 30 minutes or at the
interval the user names. Use the host's recurring scheduler and keep its
identifier with the follow-up:

- T3 Code: `schedule_task` with `{"type":"interval","everyMs":<interval in ms>}`
  bound to the current thread.
- Claude Code: the `loop` skill or a cron trigger at the same interval.
- A host without a recurring scheduler: report that unattended follow-up is not
  available and run ticks only when invoked. Do not keep the model in a polling loop.

The tick prompt must be self-contained: the PR URL, the reviewer actor, the state
file path, the instruction to run one `pr-review-followup` tick, and the
schedule's own title so the tick can find and delete it.

A full review can outlast one interval. A tick that finds a review in progress on
the current head skips the review step and still settles threads; it does not
start a second review.

Delete the schedule after a verified approval, a merged or closed PR, or `done`.
A recurring blocker keeps the schedule running.
