# Triage thread

Read in T3 Code before arming a Drive watch for a single PR, and on each wake of
a triage thread. Most wakes change nothing a Drive turn must judge, so by the
user's standing decision Drive waits in its own thread on a cheap model. That
thread owns the watch, routes each wake with `scripts/triage.py`, and hands every
turn that needs judgment to the model that started Drive. A stack keeps its
batch arming in the `stacked-pr` owner's thread, and Feedback scope never arms.

Both helper commands run as
`GH_TOKEN="$(gh auth token --hostname "$PR_HOST" --user "$ACTOR" || echo none)" python3 "$SKILL_DIR/scripts/triage.py" <triage|record> --pr "$PR_URL" --actor "$ACTOR" --state-file "$TRIAGE_FILE"`,
naming `GH_ENTERPRISE_TOKEN` instead on a GitHub Enterprise Server host. `$ACTOR`
is the verified publication actor, and the state file lives beside the ledger in
ignored task storage. `triage` writes nothing. `record` saves the PR state a
Drive turn judges: run it immediately before collecting the final snapshot of a
turn that ends waiting, so anything later reads as new.

## Start it

When a Drive turn ends waiting, no watch is on, and this thread is neither a
triage thread nor a delegated child:

1. Look for a thread titled `Drive as <actor>: <PR URL>` with `t3_thread_list`
   or `t3_thread_search`. When a live one exists, it owns this PR: report its
   link, and stop changing the PR or its checkout here.
2. Read this thread's model selection with `t3_thread_configure`; it becomes the
   acting model, passed to `delegate_task` as `target` with its `instanceId` as
   `providerInstanceId`, and its model and options unchanged.
3. Choose the triage model from `orchestrator_capabilities`: search `luna` and
   take the newest `luna` model of an enabled Codex provider, the newest being
   the highest version in its ID. Otherwise search `haiku` and take the newest
   Claude Haiku. Set its `medium` effort. When neither is offered, arm the
   watch here as [ci-and-observation.md](ci-and-observation.md#t3-code) says.
4. Write the ledger to its absolute path, including the Drive start time, the
   stopping point, any user deadline, and every authority and limit in force,
   such as keep-draft or do-not-merge.
5. Run `t3_thread_launch` with that `modelSelection`, this thread's workspace
   (`existing_worktree` with its path when this thread runs in a worktree,
   otherwise `root`), that title, and a message that names the PR URL, the
   actor, the ledger and state file paths, both complete helper commands, this
   file's absolute path, the acting model, and: "Follow Route a wake. Do not load
   the whole skill."
6. Wait with `t3_thread_wait` until that first run ends, waiting again after a
   timeout, then list its pull requests with `list_thread_pull_requests`. When
   this PR shows `watching: true`, report the link: that thread now owns the
   watch, the checkout and every later Drive turn. Otherwise report the link,
   that run's result, and that nothing watches the PR, and arm nothing: that
   thread may already hold a stop from the user, and no T3 call hands the watch
   back atomically. Arm the watch here, and report why, only when the launch
   failed before it created a thread.

## Route a wake

The launch message is not a user message: the first turn starts at step 5.
Its last call is `watch_pull_request` for this PR whatever the verdict, unless
the route ended Drive.

1. A message from the user that only asks for status: answer from the ledger
   and a read of the PR, and leave any child and the watch alone. Any other
   message: cancel a running child with `task_cancel`, since a cancelled child
   never wakes you, and record any new limit in the ledger. Then unwatch and
   report for a stop; otherwise delegate the message now as below, with the
   user's words.
2. A wake saying T3 stopped watching: report its exact message and end the turn.
3. While this thread's Drive child is running, end the turn with one line; its
   completion wakes you. When the wake is one of step 4's events, say so in that
   line, so the completion step delegates it.
4. A wake saying no checks started, the PR left the merge queue, or a workflow
   awaits approval: delegate one Drive turn.
5. Otherwise run `triage`. When it exits nonzero, run it once more; a second
   failure unwatches and reports the exact message. Then follow its verdict:
   - `quiet`: end the turn without a message; the watch stays on. A quiet
     verdict never delegates.
   - `act` or `stop`: delegate one Drive turn.
6. Delegate with `delegate_task`: `mode: async`, `role: implementation`,
   `isolation: shared`, the acting model as `target`, and a task naming the PR
   URL, the actor, the ledger and state file paths, the `record` command, the
   wake or triage reasons, and: "Continue `pr-followup` Drive for this PR from a
   fresh snapshot, with the authority and limits the ledger records, and keep
   the ledger current. Leave the watch to the parent. When the turn ends
   waiting, run `record` immediately before the final snapshot; when it fails
   because the head moved, judge the new head once and record again. Return the
   `record` result and whether Drive ends waiting or for the user; end with
   `PR <URL>, head <SHA>, checks and reviews <state>`."
7. On its completion, relay its result. When Drive ends for the user, the child
   failed, or a turn that ends waiting returned no `record` result, unwatch
   first and report. Otherwise delegate a step 4 event noted during the turn, or
   run `triage` once more and follow its verdict, which covers the other events
   that arrived during the turn.

After delegating, end the turn at once, arming the watch first in the first
turn. The child's completion wakes you, so never wait on it with
`t3_thread_wait` or `task_status`, and never delegate again while it runs: a
cheap model that waited and then re-delegated started a second acting turn on
the same PR.

A T3 tool can load late or under another namespace, such as
`t3-code-direct.delegate_task`: search for it and call it once before reporting
it absent, and quote the exact error when the call fails.

This thread only routes: it never edits, commits, pushes, replies or changes PR
state.
