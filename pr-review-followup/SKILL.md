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

Resolve `pr-review` and `comment-style` by registered name, and use
`comment-style` before wording any reply. A missing dependency blocks the phase
that needs it. Every write below is published immediately; none waits as a draft.

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
   It is bound to that PR and reviewer and holds the recorded review, the head
   and base on which each resolved thread was last verified, and any uncertain
   write.
3. If `pr-review` just reviewed the current head, record it from that run (step 3
   of a tick); otherwise the first tick performs the full review.
4. Schedule the ticks as [cadence.md](references/cadence.md) describes, then run
   the first tick immediately.

## Run one tick

1. **Read the state** with `state`. It reports the PR author, state, head and
   base branch; whether the recorded review covers this head and base, was
   complete, and left required findings outside the reviewer's threads or open
   decisive questions; the `approval_blockers`; whether a review is in progress;
   the reviewer's unsubmitted or approving reviews; any uncertain write; and
   every thread the reviewer started, with each comment's role (`author`,
   `reviewer` or `other`), who resolved it and whether the reviewer can resolve
   or reopen it. It writes nothing and refuses a partial view of threads or
   comments.
2. **Stop or wait.**
   - `done` (the reviewer approved this head and the approval gate is clear), or
     a merged or closed PR: delete the schedule and report the outcome.
   - An unsubmitted review by the reviewer, or a `pending_operation`: report it
     and write nothing. Clear an uncertain operation only after reading back the
     thread or review it names.
3. **Review a new head.** When `review_current` is false and no review is in
   progress, run `begin --head "$HEAD"`, then `pr-review` on the current head as
   a full review. Tell it that this follow-up owns approval, so it publishes
   with `--max-event COMMENT` or publishes nothing. Then record what it covered:

   ```bash
   python3 "$SKILL_DIR/scripts/followup.py" record --pr "$PR_URL" --actor "$REVIEWER" \
     --state-file "$STATE_FILE" --snapshot "$SCRATCHPAD/inputs/snapshot.json" \
     --complete true --standing 0 --questions 0
   ```

   `--complete` is true only when every requested engine succeeded. `--standing`
   counts supported required findings that still stand outside the reviewer's
   threads, such as body findings or points continued in another reviewer's
   thread; accepted deferrals are not counted. `--questions` counts decisive
   questions the review left open. An incomplete review is recorded as
   such, is not rerun on the same head, and blocks approval until the user
   decides. A review that fails before recording is reported once; the next tick
   retries it after the in-progress window. Re-read the state before settling threads.
4. **Settle the reviewer's threads.** Act on each thread where the author or
   another participant spoke last, on every unresolved thread after a new head
   or base (a push can fix it without a reply), and on each resolved thread
   listed in `needs_verification`: a resolution counts only once it is confirmed
   on the current head and base, so every resolved thread is checked again after
   a new head or base. Read the whole thread, check its claims on the current
   head, and choose the action in
   [thread-settlement.md](references/thread-settlement.md). Reassess the
   review's standing findings and open questions too: a fixed PR title, an
   answered question or a ticket confirmed elsewhere lowers them with `settle
   --standing N --questions N`, which only updates the review of the current
   head.
5. **Apply** with `apply --plan "$PLAN" --receipt "$RECEIPT"`, a new plan and
   receipt per tick. The plan is `{"expected_head": SHA, "expected_base_ref":
   BRANCH, "replies": [{"thread_id", "body"}], "resolve": [ids], "unresolve":
   [ids], "verified": [ids], "approve": bool}`, with the head and base `state`
   reported; `verified` marks resolved threads the current head confirms. Before
   any write the helper validates the whole plan, rejects threads the reviewer
   did not start or cannot resolve, and rechecks the actor, open state, head,
   base branch and unsubmitted reviews before each write. It skips a reply
   identical to the reviewer's last comment and a resolution already in place,
   reads back every write, and keeps an uncertain write in the state file so no
   later tick repeats it.
6. **Approve through the gate.** `state` lists `approval_blockers`: an
   unreviewed or incomplete review of this head and base, standing required
   findings, open decisive questions, unresolved threads, or resolved threads
   not verified on this head and base. Set `approve` when this plan clears them.
   For an approving plan the helper checks the same gate before any write and
   again on the read that immediately precedes the approval; `done` uses it too.
   After a verified approval, delete the schedule.
7. **Report the tick** in the user's language: resolved/total, each reply,
   resolution or reopening with its reason, a new review's outcome, and
   blockers. A tick with no change is one line.
