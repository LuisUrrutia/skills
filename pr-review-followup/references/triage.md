# Triage thread

Read in T3 Code before arming the watch, and on each wake of a triage thread.
Most wakes change nothing a tick must judge, so by the user's standing decision
each follow-up waits in its own thread on a cheap model. That thread owns the
watch, routes each wake with the helper's `triage` command, and hands every tick
that needs judgment to the model that started the follow-up.

## Start it

When a tick ends waiting, no watch is on, and this thread is neither a triage
thread nor a delegated child:

1. Look for a thread titled `Review follow-up as <reviewer>: <PR URL>` with
   `t3_thread_list` or `t3_thread_search`. When a live one exists, it owns this
   follow-up: report its link, and answer here only status questions.
2. Read this thread's model selection with `t3_thread_configure`; it becomes the
   acting model, passed to `delegate_task` as `target` with its `instanceId` as
   `providerInstanceId`, and its model and options unchanged.
3. Choose the triage model from `orchestrator_capabilities`: search `luna` and
   take the newest `luna` model of an enabled Codex provider, the newest being
   the highest version in its ID. Otherwise search `haiku` and take the newest
   Claude Haiku. Set its lowest effort option. When neither is offered, arm the
   watch here as [cadence.md](cadence.md) says.
4. Run `t3_thread_launch` with that `modelSelection`, this thread's workspace
   (`existing_worktree` with its path when this thread runs in a worktree,
   otherwise `root`), that title, and a message that names the PR URL, the
   reviewer, every limit the user set on this follow-up (such as no approval),
   the absolute state file path, the full helper command form under the
   reviewer's binding, this file's absolute path, the acting model, and: "Follow
   Route a wake once, then arm `watch_pull_request` for this PR as your last
   call unless the route ended the follow-up. Do not load the whole skill."
5. Wait for that first run with `t3_thread_wait`, then list its pull requests
   with `list_thread_pull_requests`. When this PR shows `watching: true`, report
   the link: that thread now owns the watch and every later tick. When that run
   ended the follow-up, report its result and arm nothing. Otherwise, or when
   the launch fails or times out, call `unwatch_pull_request` with that thread's
   ID, then arm the watch here and report why.

## Route a wake

1. A message from the user: cancel a running child with `task_cancel`, since a
   cancelled child never wakes you. Then unwatch and report for a stop;
   otherwise delegate the message now as below, with the user's words, and carry
   any new limit into every later task.
2. A wake saying T3 stopped watching: report its exact message and end the turn.
3. While this thread's tick child is running, reply in one line and end the
   turn; its completion wakes you.
4. Run `triage`. When it exits nonzero, run it once more; a second failure
   unwatches and reports the exact message. Then follow its verdict:
   - `quiet`: reply in one line and end the turn; the watch stays on.
   - `stop` or `report`: run `state`, unwatch, and report the reasons, open
     optional threads and anything `state` shows that needs the user.
   - `act`: delegate one tick.
5. Delegate with `delegate_task`: `mode: async`, `role: review`, `isolation:
   shared`, the acting model as `target`, and a task naming the PR URL, the
   reviewer, the user's limits, the state file, the full helper command form,
   the triage reasons, and: "Run one `pr-review-followup` tick from Run one tick
   within those limits. You may use `pr-review`'s T3 child-task transport. Leave
   the watch to the parent. Return the tick report, the `apply` result, and
   whether the follow-up ends waiting or for the user; end with
   `PR <URL>, head <SHA>, checks and reviews <state>`."
6. On its completion, relay the tick report. When it ends for the user, failed,
   or returned no `apply` result, unwatch first and report. Otherwise run
   `triage` once more and follow its verdict, which covers events that arrived
   during the tick.

A T3 tool can load late or under another namespace, such as
`t3-code-direct.delegate_task`: search for it and call it once before reporting
it absent, and quote the exact error when the call fails.

This thread only routes: it never runs `begin`, `record`, `settle` or `apply`,
and never writes to GitHub.
