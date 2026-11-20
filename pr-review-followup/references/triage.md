# Triage thread

Read in T3 Code before arming the watch, and on each wake of a triage thread.
Most wakes change nothing a tick must judge, so a thread on a cheap model owns
the watch, routes each wake with the helper's `triage` command, and hands every
tick that needs judgment to the model that started the follow-up.

## Start it

When a tick ends waiting, no watch is on and this thread is not a triage thread:

1. Read this thread's provider instance, model and options with
   `t3_thread_configure`; they become the acting model.
2. Choose the triage model from `orchestrator_capabilities`: search `luna` and
   take the newest `luna` model of an enabled Codex provider, the newest being
   the highest version in its ID. Otherwise search `haiku` and take the newest
   Claude Haiku. Set its lowest effort option. When neither is offered, arm the
   watch here as [cadence.md](cadence.md) says.
3. Run `t3_thread_launch` with that `modelSelection`, this thread's workspace
   (`existing_worktree` with its path when this thread runs in a worktree), the
   title `Follow-up <owner>/<repo>#<number>`, and a message that names the PR
   URL, the reviewer, the state file, the complete `triage` command under the
   reviewer's binding, this file's absolute path, the acting model, and: "Arm
   `watch_pull_request` for this PR and end the turn. On each wake, follow Route
   a wake in the triage file; do not load the whole skill."
4. Report the thread's link and that its watch replaces one here. If the launch
   fails, report why and arm the watch here.

## Route a wake

1. While this thread's tick child is running, reply in one line and end the
   turn; its completion wakes you.
2. Run `triage` and follow its verdict:
   - `quiet`: reply in one line and end the turn; the watch stays on.
   - `stop` or `report`: run `state`, unwatch, and report the reasons, open
     optional threads and anything `state` shows that needs the user.
   - `act`: delegate one tick.
3. Delegate with `delegate_task`: `mode: async`, `role: review`, `isolation:
   shared`, the acting model as `target`, and a task naming the PR URL, the
   reviewer, the state file, the triage reasons, and: "Run one
   `pr-review-followup` tick from Run one tick. You may use `pr-review`'s T3
   child-task transport. Leave the watch to the parent. End with `apply`, using
   an empty plan when nothing is written. Return the tick report and whether the
   follow-up ends waiting or for the user."
4. On its completion, relay the tick report. When it ends for the user, or the
   child failed, unwatch first as cadence.md says. Otherwise run `triage` once
   more and act on its verdict, which covers events that arrived during the tick.

This thread only routes: it never runs `begin`, `record`, `settle` or `apply`,
and never writes to GitHub.
