# Cadence

Read when starting, resuming or stopping the follow-up.

## T3 Code watch

In T3 Code, wait with `watch_pull_request` unless the user names an interval;
then schedule ticks as below. Each wake runs one tick.

- Arm the watch right after the first tick's final read, then end the turn. A
  tick that ends waiting keeps the watch; do not call it again on a wake.
- It wakes on new comments and reviews by others, failed checks, checks passing
  on a new head (on GitHub, also when no check reports 15 minutes after a push),
  conflicts and closure. It never wakes on a thread resolved without a comment or
  push, a re-requested review, a merge, or comments by the GitHub account T3 Code
  reads with. Each tick rechecks these; a merge ends the watch silently, so report
  it when next invoked.
- A watched thread stays out of the user's inbox. Unwatch before a tick that ends
  for the user: approval, `done`, a closed PR, or a blocker that needs the user,
  such as an incomplete review, the reviewer's unsubmitted review or a thread
  waiting on the user. When the user replies, run a tick and re-arm unless the
  follow-up is done.
- Ten comment-only wakes in a row stop the watch, for example when a bot answers
  each reply. Find the cause before re-arming. After a stop for read failures,
  re-arm once reads work.
- Only the thread that runs the follow-up arms the watch; a delegated child
  returns its tick result to that thread.

## Schedule

Elsewhere, or when the user names an interval, run one tick every 30 minutes
unless the user names another interval. Use the host's recurring scheduler and
keep its identifier with the follow-up:

- T3 Code: `schedule_task` with `{"type":"interval","everyMs":1800000}` bound to
  the current thread.
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
A recurring blocker, such as an incomplete review, an uncertain write or a thread
waiting on the user, keeps the schedule running and is reported once per change,
not on every tick.
