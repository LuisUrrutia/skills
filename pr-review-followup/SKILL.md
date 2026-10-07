---
name: pr-review-followup
description: Use when following up on a GitHub PR you reviewed, until your threads are settled and the PR is approved.
---

# PR review follow-up

Carry a PR you reviewed to approval: answer the author in your own threads, settle
what is resolved, re-review new commits and approve once nothing remains. When the
verified `gh` actor is the PR's author, use `pr-followup` instead; producing a
review belongs to `pr-review`. This skill never edits the reviewed code, requests
changes, or touches other reviewers' threads.

Resolve `pr-review` and `comment-style` by registered name, and read
`comment-style`'s PR review reference before wording any reply. A missing
dependency blocks the phase that needs it. Every write below is published
immediately; none waits as a draft.

All helper commands run from any directory as
`python3 "$SKILL_DIR/scripts/followup.py" <command> --pr "$PR_URL" --actor "$REVIEWER" --state-file "$STATE_FILE"`,
plus the arguments named below. Each prints JSON; a nonzero exit is a stopped
step to report, never a success.

## Start the follow-up

1. Resolve the PR URL, its target repository and the reviewer actor: explicit user
   direction, or the path-effective Git email matched to an authenticated `gh`
   account. Verify it with `gh api user --jq .login` on the PR's host and switch
   to an already authenticated intended account when needed. Ask only when the
   identity stays ambiguous.
2. Choose one state file per PR in the reviewed project's permitted scratch area.
   It is bound to that PR and reviewer and holds the recorded review, threads
   verified after someone else resolved them, and any uncertain write.
3. If `pr-review` just reviewed the current head, record it from that run (step 3
   of a tick); otherwise the first tick performs the full review.
4. Schedule the ticks as [cadence.md](references/cadence.md) describes, then run
   the first tick immediately.

## Run one tick

1. **Read the state** with `state`. It reports the PR author, state, head and
   base branch; whether the recorded review covers this head and base, was
   complete, and left required findings outside the reviewer's threads; whether a
   review is in progress; the reviewer's unsubmitted or approving reviews; any
   uncertain write; and every thread the reviewer started, with each comment's
   role (`author`, `reviewer` or `other`), who resolved it and whether the
   reviewer can resolve or reopen it. It writes nothing and refuses a partial
   view of threads or comments.
2. **Stop or wait.**
   - `done` (the reviewer approved this head and no reviewer thread is open), or a
     merged or closed PR: delete the schedule and report the outcome.
   - An unsubmitted review by the reviewer, or a `pending_operation`: report it
     and write nothing. Clear an uncertain operation only after reading back the
     thread or review it names.
3. **Review a new head.** When `review_current` is false and no review is in
   progress, run `begin --head "$HEAD"`, then `pr-review` on the current head as a
   full review. Tell it that this follow-up owns approval, so it publishes COMMENT
   or nothing. Then record what it covered:

   ```bash
   python3 "$SKILL_DIR/scripts/followup.py" record --pr "$PR_URL" --actor "$REVIEWER" \
     --state-file "$STATE_FILE" --snapshot "$SCRATCHPAD/inputs/snapshot.json" \
     --complete true --standing 0
   ```

   `--complete` is true only when every requested engine succeeded. `--standing`
   counts supported required findings that still stand outside the reviewer's
   threads, such as body findings or points continued in another reviewer's
   thread; accepted deferrals are not counted. An incomplete review is recorded as
   such, is not rerun on the same head, and blocks approval until the user
   decides. A review that fails before recording is reported once; the next tick
   retries it after the in-progress window. Re-read the state before settling threads.
4. **Settle the reviewer's threads.** Act on each thread where the author or
   another participant spoke last, whose code changed in a new head, or listed in
   `needs_verification` because someone else resolved it. Read the whole thread,
   check its claims on the current head, and choose the action in
   [thread-settlement.md](references/thread-settlement.md).
5. **Apply** with `apply --plan "$PLAN" --receipt "$RECEIPT"`, a new plan and
   receipt per tick. The plan is `{"expected_head": SHA, "replies": [{"thread_id",
   "body"}], "resolve": [ids], "unresolve": [ids], "verified": [ids], "approve":
   bool}`; `verified` marks threads someone else resolved that the current head
   confirms. Before any write the helper validates the whole plan, rejects
   threads the reviewer did not start or cannot resolve, and rechecks the actor,
   open state, head and unsubmitted reviews before each write. It skips a reply
   identical to the reviewer's last comment and a resolution already in place,
   reads back every write, and keeps an uncertain write in the state file so no
   later tick repeats it.
6. **Approve through the gate.** Set `approve` when the recorded review covers
   this head and base, was complete and left no standing required finding, and
   every reviewer thread is resolved and verified, counting this plan. The helper
   enforces the same gate before approving the current head. After a verified
   approval, delete the schedule.
7. **Report the tick** in the user's language: resolved/total, each reply,
   resolution or reopening with its reason, a new review's outcome, and blockers.
   A tick with no change is one line.
