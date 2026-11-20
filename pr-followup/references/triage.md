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

1. Look for a thread titled `Follow-up <owner>/<repo>#<number>` with
   `t3_thread_list` or `t3_thread_search`. When a live one exists, it owns this
   PR: report its link, and stop changing the PR or its checkout here.
2. Read this thread's model selection with `t3_thread_configure`; it becomes the
   acting model, passed to `delegate_task` as `target` with its `instanceId` as
   `providerInstanceId`, and its model and options unchanged.
3. Choose the triage model from `orchestrator_capabilities`: search `luna` and
   take the newest `luna` model of an enabled Codex provider, the newest being
   the highest version in its ID. Otherwise search `haiku` and take the newest
   Claude Haiku. Set its lowest effort option. When neither is offered, arm the
   watch here as [ci-and-observation.md](ci-and-observation.md#t3-code) says.
4. Write the ledger to its absolute path, including the Drive start time, the
   stopping point, any user deadline, and every authority and limit in force,
   such as keep-draft or do-not-merge.
5. Run `t3_thread_launch` with that `modelSelection`, this thread's workspace
   (`existing_worktree` with its path when this thread runs in a worktree,
   otherwise `root`), that title, and a message that names the PR URL, the
   actor, the ledger and state file paths, both complete helper commands, this
   file's absolute path, the acting model, and: "Arm `watch_pull_request` for
   this PR, then follow Route a wake once. Do not load the whole skill."
6. Report the thread's link: it now owns the watch, the checkout and every later
   Drive turn, and a failed arming is reported there. If the launch fails,
   report why and arm the watch here.

## Route a wake

1. A wake saying T3 stopped watching, or a helper command that exits nonzero:
   unwatch if the watch is still on, report the exact message, and end the turn.
2. While this thread's Drive child is running, end the turn with one line; its
   completion wakes you.
3. A message from the user: delegate it as below, with the user's words in the
   task.
4. Otherwise run `triage` and follow its verdict:
   - `quiet`: end the turn without a message; the watch stays on.
   - `act` or `stop`: delegate one Drive turn.
5. Delegate with `delegate_task`: `mode: async`, `role: implementation`,
   `isolation: shared`, the acting model as `target`, and a task naming the PR
   URL, the actor, the ledger and state file paths, the `record` command, the
   triage reasons, and: "Continue `pr-followup` Drive for this PR from a fresh
   snapshot, with the authority and limits the ledger records, and keep the
   ledger current. Leave the watch to the parent. When the turn ends waiting,
   run `record` immediately before the final snapshot. Return the `record`
   result and whether Drive ends waiting or for the user; end with
   `PR <URL>, head <SHA>, checks and reviews <state>`."
6. On its completion, relay its result. When Drive ends for the user, the child
   failed, or a turn that ends waiting returned no `record` result, unwatch
   first and report. Otherwise run `triage` once more and follow its verdict,
   which covers events that arrived during the turn.

A T3 tool can load late or under another namespace, such as
`t3-code-direct.delegate_task`: search for it and call it once before reporting
it absent, and quote the exact error when the call fails.

This thread only routes: it never edits, commits, pushes, replies or changes PR
state.
