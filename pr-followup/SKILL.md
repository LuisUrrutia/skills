---
name: pr-followup
description: Follow an existing pull request through feedback, CI and conflict repair, and move a settled draft PR to ready for review.
---

# PR follow-up

Bring an existing PR to the requested stopping point with evidence for its current
revision. Evaluate feedback before changing code; keep every observed item accounted
for. Use this directly with a PR URL or as a phase of an authorized delivery task.

## Choose scope and establish state

- **Check:** inspect and report. No edits, reruns, replies, publication or state changes.
- **Feedback:** collect all feedback channels, evaluate each item, apply clear
  improvements within the request, and verify the resulting change. A request to
  review PR comments includes acting on correct observations unless it says read-only.
- **Drive:** repair feedback, CI and necessary base conflicts, publish when authorized,
  and observe the new revision until settled, blocked, or the observation limit is reached.
  Use this for requested babysitting and the continuation of a PR creation request.

Resolve scope from the request and standing instructions. Record whether commits,
publication, replies and thread resolution are authorized. Code repair alone does
not authorize messages to reviewers. A PR creation request covers Drive repairs,
verification, commits, publication and the conditional ready transition below;
explicit read-only, create-only or keep-draft instructions constrain that scope.
Do not require approval again for covered work.
Set a finite observation window for Drive and for post-ready observation entered
from Feedback: use the user's limit, otherwise state a 30-minute window. Start it
on entry to Drive, or at the ready transition for Feedback. Reaching it returns
current evidence and pending work, not success or an automatic extension.
Persistent scheduling requires a separate explicit request.

Resolve exact PR URL, target repository, head repository/ref/SHA, base ref/SHA,
open/closed state, draft state and repository merge requirements. Match the local
checkout to that head before editing; preserve unrelated work and index state.
Use host checkout ownership and `worktrunk` for necessary checkout operations;
`stacked-pr` owns stack topology and rebases. Keep one mutation owner per PR or stack.
Register the PR with the host when supported. Stop on a closed or merged target
unless the user requested a specific historical operation.

## Observe and evaluate

Read [references/feedback.md](references/feedback.md) for collection, judgment and
reviewer communication. It includes [references/github-collection.md](references/github-collection.md)
for GitHub pagination and channels. Inspect review threads, formal review bodies,
conversation comments, check annotations/summaries and reviewer output in CI logs.
A green job can still contain feedback. Record inaccessible channels as unknown.

Keep a small local ledger when multiple items or cycles need continuity: source
IDs/URLs, updated version, claim, evidence, decision, correction, verification,
published revision and any pending reply/resolution. Use ignored task storage.
Deduplicate one causal issue while retaining all its source IDs. Re-read edited
comments and new replies, including resolved or outdated threads; prior disposition
does not settle new content. Remote state remains authoritative on resume.

Trace each claim through current code, requirements and caller behavior. Accept a
clear improvement because its reasoning holds, not because a bot or reviewer said
it. Disprove a claim with concrete evidence, not preference or a vote. Uncertainty
is a question to investigate, not automatic permission to change behavior.

Ask immediately when a critical choice remains unresolved and plausible answers
would change the contract or validity of a repair. Pause that repair, continue
independent work, and report the choices with a recommendation. Do not let pending
CI, an inaccessible channel or one disputed item freeze unrelated supported fixes.

## Repair, verify and publish

Group related feedback by root cause; make the smallest coherent correction that
preserves the intended contract. Add a regression test when it exercises the failure.
Do not implement optional redesigns or change product policy just to clear a thread.

Load support only at the boundary that needs it:

| Need | Owner |
| --- | --- |
| Uncertain defect or CI failure | `debug` for causal investigation. |
| Bounded review claim that needs deeper audit | `review-code-changes` in read-only mode. |
| A deciding indirect consequence | `analyze-change-effects`. |
| Workflow or agent-instruction changes | `github-actions` or `agent-instructions`. |
| Applicable execution evidence | `verify` and the local application recipe. |
| Atomic commits | `commit`; carry existing authorization and preserved work. |
| Push and complete PR description refresh | `pr`; pass exact identity and verified revision. |
| Dependent PR topology or cascading rebase | `stacked-pr`, retaining one writer. |

For CI, base updates and observation, read
[references/ci-and-observation.md](references/ci-and-observation.md). Before GitHub
writes or publication, use `pr`'s publication procedure for actor identity, SSH,
exact destination and post-write checks. Standalone follow-up needs those same
checks; it does not require having created the PR with `pr`.

Run applicable behavioral checks, compile/build and broader smoke evidence under
project instructions. If a prerequisite is unavailable, report the exact limitation;
do not treat it as passed. Commit at coherent boundaries and publish a batch of
verified fixes when authorized. Re-read the actual remote head after publication,
invalidate prior CI/readiness evidence, and update the whole PR body through `pr`.
Do not republish merely to wake a bot. Continue collecting feedback for the new head.

## Move a settled draft to review

In Feedback or Drive scope, mark an open draft ready without another permission
prompt when a fresh snapshot of the current head/base establishes all of these:

- All applicable CI/CD has passed, with no active jobs or unexplained failures,
  cancellations or unknown results. Optional failures also block this transition
  unless the user explicitly accepts an exception. Explain legitimate policy-based
  skips; jobs skipped only because the PR is a draft must be checked after the
  transition.
- Observed feedback has been resolved: accepted fixes are verified and published,
  reviewer questions are answered visibly or settled by the user, decisions are
  settled, and required thread resolutions are complete
  under the authority in `references/feedback.md`. Merely listing an unresolved
  item in the final report does not satisfy this gate. If a required reply or
  thread resolution lacks authorization, keep the draft and report that prerequisite.
- No known repair, conflict, active automated reviewer or other actionable work
  remains. Inaccessible evidence blocks the transition. A future human review or
  missing approval alone does not: ready for review is distinct from ready to merge.

Honor an explicit keep-draft instruction and leave Check scope read-only. Recheck
identity, head/base and readiness immediately before using `pr`'s publication
identity checks and `gh pr ready <url>`. Verify `isDraft` is false; inspect remote
state before retrying an uncertain write. If the revision moved, reassess it.

The transition starts a new observation phase even if the SHA is unchanged.
Invalidate the draft-era completion snapshot, discover workflows and automated
reviewers triggered or unblocked by ready state, and collect every feedback channel
again. Continue the repair/verify/publish loop for new failures and comments. Do not
infer completion from the old green checks or a momentarily empty queue; verify
expected post-ready work has run or report it as pending. Use the existing bounded
observation window and host notifications, without silently resetting the window.
Always attempt a fresh post-ready snapshot before returning, even at the deadline;
report an inaccessible snapshot as blocked rather than claiming completion.

Human feedback arriving during observation or on host resumption enters the same
loop. If human review is still pending when observation stops, report that fact
separately from completed technical work; never claim approval or merge readiness.

## Stop with an honest result

Feedback work is accounted for when every observed item is applied or reported
with its reason for remaining unapplied and any required decision. Distinguish
locally fixed, verified, published, replied and resolved; none implies the next.

Drive is settled only after a fresh coherent snapshot has the expected head/base,
required checks satisfied, observed failures and feedback accounted for, and no
known active required reviewer left unobserved. Assess merge readiness separately:
required approvals, review decisions, draft state and platform merge requirements
must also be satisfied. Silence, an old green run, a quiet interval or API failure
does not establish readiness. A draft eligible for the transition above is not
finished until that transition and the post-ready checks are accounted for. Report
an unmet draft-readiness gate as waiting or blocked, even if required checks pass.
Never merge, enable auto-merge or approve a gated workflow merely to make this loop finish.

Return the PR URL and current head, applied work summary with relevant commits,
actual verification commands/results, current checks, and remaining items. For
each unapplied item give the evidence-based reason; for a user decision include
choices and recommendation. State `complete for requested scope`, `waiting`, or
`blocked` and what would allow continuation. Retain the ledger only while needed
for resumption, then remove owned scratch. Stop local watchers owned by this run;
retain a host-managed watch when the host requires it to resume pending review work.

For requested source maintenance, use `agent-instructions` with `origin.txt` and
[references/upstream-updates.md](references/upstream-updates.md).
