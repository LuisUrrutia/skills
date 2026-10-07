# Cadence

Read when starting or stopping the follow-up schedule.

Run one tick every 30 minutes unless the user names another interval. Use the
host's recurring scheduler and keep its identifier with the follow-up:

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
