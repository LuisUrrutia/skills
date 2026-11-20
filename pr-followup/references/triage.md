# Triage thread

Read in T3 Code before arming a Drive watch for a single PR, and on each wake of
a triage thread. Most wakes change nothing a Drive turn must judge, so a thread
on a cheap model owns the watch, routes each wake with `scripts/triage.py`, and
hands every turn that needs judgment to the model that started Drive. A stack
keeps its batch arming in the `stacked-pr` owner's thread.

Both helper commands run as
`GH_TOKEN="$(gh auth token --hostname "$PR_HOST" --user "$ACTOR" || echo none)" python3 "$SKILL_DIR/scripts/triage.py" <triage|record> --pr "$PR_URL" --actor "$ACTOR" --state-file "$TRIAGE_FILE"`,
naming `GH_ENTERPRISE_TOKEN` instead on a GitHub Enterprise Server host. `$ACTOR`
is the verified publication actor, and the state file lives beside the ledger in
ignored task storage. `triage` writes nothing; `record` saves the PR state a
Drive turn has judged. A nonzero exit is a stopped step to report.

## Start it

When a Drive turn ends waiting, no watch is on and this thread is not a triage
thread:

1. Run `record` after the final snapshot.
2. Read this thread's provider instance, model and options with
   `t3_thread_configure`; they become the acting model.
3. Choose the triage model from `orchestrator_capabilities`: search `luna` and
   take the newest `luna` model of an enabled Codex provider, the newest being
   the highest version in its ID. Otherwise search `haiku` and take the newest
   Claude Haiku. Set its lowest effort option. When neither is offered, arm the
   watch here as [ci-and-observation.md](ci-and-observation.md#t3-code) says.
4. Run `t3_thread_launch` with that `modelSelection`, this thread's workspace
   (`existing_worktree` with its path when this thread runs in a worktree), the
   title `Follow-up <owner>/<repo>#<number>`, and a message that names the PR
   URL, the actor, the retained task state, both complete helper commands, this
   file's absolute path, the acting model, and: "Arm `watch_pull_request` for
   this PR and end the turn. On each wake, follow Route a wake in the triage
   file; do not load the whole skill."
5. Report the thread's link and that its watch replaces one here. If the launch
   fails, report why and arm the watch here.

## Route a wake

1. While this thread's Drive child is running, end the turn with one line; its
   completion wakes you.
2. Run `triage` and follow its verdict:
   - `quiet`: end the turn without a message; the watch stays on.
   - `act` or `stop`: delegate one Drive turn.
3. Delegate with `delegate_task`: `mode: async`, `role: implementation`,
   `isolation: shared`, the acting model as `target`, and a task naming the PR
   URL, the actor, the retained task state, the triage reasons, and: "Continue
   `pr-followup` Drive for this PR from a fresh snapshot, with the authority the
   retained state records. Leave the watch to the parent. When the turn ends
   waiting, run `record` after the final snapshot. Return the PR URL, head SHA,
   pending check and review state, and whether Drive ends waiting or for the
   user."
4. On its completion, relay its result. When Drive ends for the user, or the
   child failed, unwatch first as ci-and-observation.md says. Otherwise run
   `triage` once more and act on its verdict, which covers events that arrived
   during the turn.

This thread only routes: it never edits, commits, pushes, replies or changes PR
state.
