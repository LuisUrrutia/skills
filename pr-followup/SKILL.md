---
name: pr-followup
description: Inspect or repair feedback and CI on your own PR, move settled drafts to review, and babysit it through approval or an authorized merge.
---

# PR follow-up

Bring an existing PR to the requested stopping point with evidence for its current
revision. Evaluate feedback before changing code; keep every observed item accounted
for. Use this directly with a PR URL or as a phase of an authorized delivery task.
When the verified `gh` actor reviewed the PR rather than authoring it, use
`pr-review-followup` instead.

## Choose scope and establish state

- **Check:** inspect and report. No edits, reruns, replies, publication or state changes.
- **Feedback:** collect all feedback channels, evaluate each item, apply clear
  improvements within the request, and verify the resulting change. A request to
  review PR comments includes acting on correct observations unless it says read-only.
- **Drive:** repair feedback, CI and necessary base conflicts, publish when authorized,
  and follow the PR until merged or, outside the personal-repository merge policy
  below, a current formal approval is verified.
  Use this for requested babysitting and the continuation of a PR creation request.

Resolve scope from the request and standing instructions. In Feedback and Drive
scope, classify every review thread and bring it to one of the dispositions in
`references/feedback.md`: applied, not applicable, outside this PR with a tracking
ticket, or needs a confirmation from the user or from someone the user must ask.
The task is incomplete until each thread has one. A PR creation request covers Drive
repairs, verification, commits, publication and the conditional ready transition
below; explicit read-only, create-only or keep-draft instructions constrain that
scope. Do not require approval again for covered work.
Drive has no default elapsed-time cutoff. The user can set a time limit or stop
it explicitly. A formal approval must still be valid for the current revision
under repository policy; green checks and a bot's success comment are not approval.
A closed, unmerged PR ends observation with that outcome, not success. An access
blocker pauses affected work and must be reported, not treated as completion.
Use host-managed event notifications and end the agent turn while waiting.
A host watch notification resumes this skill and its retained task state. A
subagent unable to own the watch returns that responsibility to its parent. If no
resumable watch is available, report that limitation instead of keeping the model
in a polling loop or claiming unattended coverage. A separate recurring schedule
still requires an explicit request. Feedback scope does not become indefinite
babysitting merely because its repairs or ready transition finished.

Resolve exact PR URL, target repository, head repository/ref/SHA, base ref/SHA,
open/closed state, draft state and repository merge requirements. Match the local
checkout to that head before editing; preserve unrelated work and index state.
Use host checkout ownership and `worktrunk` for necessary checkout operations;
`stacked-pr` owns stack topology and rebases. Keep one mutation owner per PR or stack.
Register the PR with the host when supported. Stop on a closed or merged target
for repair work unless the user requested a specific historical operation. For
a verified merged target with a linked ticket, first handle the authorized
`pr-merged` synchronization below; Check scope remains read-only.
For a standalone request limited to feedback inspection or repair, use Inspect
for linked-ticket transitions unless the request or standing project instructions
also authorize lifecycle synchronization; the outside-scope tracking ticket still
uses Publish. An active delivery/Drive task retains its existing authority.

When first observing an open non-draft PR, or observing that another actor readied
it, reconcile `pr-ready` through `issue-workflow` if the linked ticket's policy
selects that event. Keep the scope rules above; do this before an approval stop.
Use current source-state guards rather than replaying an already settled event.
If the host cannot wake on an external ready change, report that coverage gap and
reconcile when next invoked.

## Observe and evaluate

Read [references/feedback.md](references/feedback.md) for collection, judgment and
reviewer communication. It includes [references/github-collection.md](references/github-collection.md)
for GitHub pagination and channels. Inspect review threads, formal review bodies,
conversation comments, check annotations/summaries and reviewer output in CI logs.
A green job can still contain feedback. Record inaccessible channels as unknown.

Keep a small local ledger when multiple items or cycles need continuity: source
IDs/URLs, updated version, claim, evidence, decision, correction, verification,
published revision, disposition, tracking-ticket URL and any pending
reply/resolution. Use ignored task storage.
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
| Wording any reviewer reply, before drafting or posting it | `comment-style` and its PR review reference; if missing, block the reply, not the repair. |
| Dependent PR topology or cascading rebase | `stacked-pr`, retaining one writer. |
| Linked-ticket transitions, and one tracking ticket per outside-scope thread | `issue-workflow`, using the project's policy and current remote evidence; Publish for the ticket. |

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
- All observed feedback is settled: every review thread has reached its
  disposition under `references/feedback.md`, reviewer questions across every
  collected channel are answered visibly or settled by the user, accepted fixes
  are verified and published, decisions are settled, and the resolutions each
  disposition requires are complete. Merely listing an unresolved item in the
  final report does not satisfy this gate. If a thread still needs a confirmation,
  or its reply, resolution or tracking ticket failed, keep the draft and report
  that prerequisite.
- No known repair, conflict, active automated reviewer or other actionable work
  remains. Inaccessible evidence blocks the transition. A future human review or
  missing approval alone does not: ready for review is distinct from ready to merge.

Honor an explicit keep-draft instruction and leave Check scope read-only. Recheck
identity, head/base and readiness immediately before using `pr`'s publication
identity checks and `gh pr ready <url>`. Verify `isDraft` is false; inspect remote
state before retrying an uncertain write. If the revision moved, reassess it.
When a linked ticket's policy selects `pr-ready`, pass the verified ready event
to `issue-workflow`. Do not repeat `pr-created` merely because draft state changed.
Report a blocked ticket transition separately and continue independent observation.

The transition starts a new observation phase even if the SHA is unchanged.
Invalidate the draft-era completion snapshot, discover workflows and automated
reviewers triggered or unblocked by ready state, and collect every feedback channel
again. Continue the repair/verify/publish loop for new failures and comments. Do not
infer completion from the old green checks or a momentarily empty queue; verify
expected post-ready work has run or report it as pending. Drive then keeps its
host-managed watch until its stopping condition is met; Feedback returns its
current result without starting indefinite observation.
Always attempt a fresh post-ready snapshot before returning;
report an inaccessible snapshot as blocked rather than claiming completion.

Human feedback arriving during observation or on host resumption enters the same
loop. If human review is still pending when the agent yields, report that fact
separately from completed technical work; never claim approval. Establish merge
readiness through the applicable policy, including the personal-repository rule below.

## Merge settled PRs in Luis Urrutia's personal repositories

In Feedback or Drive scope, merge an eligible PR directly without asking again or
waiting for human or bot approvals when its target repository belongs to Luis
Urrutia's personal GitHub account, `LuisUrrutia`. Verify the target repository's
owner login and `User` account type; PR authorship, a personal source fork or access
to an organization repository does not establish personal ownership. Unknown
ownership blocks this policy. Explicit read-only, create-only, keep-draft or
do-not-merge instructions take precedence. Check scope remains read-only.

This standing policy authorizes the merge; replies and thread resolutions follow
the disposition rules in `references/feedback.md`. Before merging, obtain
a fresh snapshot of the current head/base and establish all of these:

- The PR is open, non-draft and mergeable without conflicts. For a draft, complete
  the ready transition and its fresh observation phase first.
- Every enabled automated reviewer expected for this revision has finished,
  including CodeRabbit, Greptile, Codex or any other configured agent. Verify
  expected reviews actually ran; an empty comment list or a successful reviewer
  check alone does not prove all feedback is settled. Unknown reviewer enablement
  or completion blocks merge.
- All observed feedback across every collection channel is settled, including
  human comments: accepted fixes are verified and published, questions and
  decisions are settled, each thread's reply is visible, and every thread is
  resolved by its disposition, the reviewer or the user.
  Recheck new content in resolved or outdated threads. An unapplied item merely
  listed in a report, a finding deferred without its tracking ticket or a
  disputed disposition blocks merge.
- All applicable CI/CD has passed for this revision, including required and
  optional checks. Pending, failed, cancelled, unexplained skipped or unknown
  results block merge. Account for legitimate policy-based skips and workflows
  triggered by the ready transition; inaccessible evidence is a blocker.

For a stacked PR, let `stacked-pr` own bottom-up landing under this same standing
authorization, applying these gates to each in-scope layer and rebuilding evidence
after restacking or retargeting. Do not merge an upper layer into an unmerged parent
or require another approval for work covered by this policy.

Use `pr`'s publication identity checks, then recheck head/base, feedback and checks
immediately before the merge. Use the user or repository's established merge method;
otherwise prefer GitHub's `viewerDefaultMergeMethod` when allowed. Pass the chosen
allowed method as an explicit flag to
`gh pr merge <url> --match-head-commit <verified-sha>`. If the revision or relevant
base changed, rebuild the snapshot. Do not use
`--admin`, relax repository protections or approve a gated workflow to bypass a
requirement. If GitHub requires approvals despite this policy, report the enforced
requirement as a blocker. Do not substitute auto-merge for checking these gates.

Verify the remote merged state and merge revision before reporting success or
emitting `pr-merged`. If the command enabled auto-merge instead, disable that request,
verify its removal and rebuild the snapshot. A required merge queue is pending until
merge is verified. In Drive, keep the host watch until then; a formal approval alone does
not end this personal-repository task. Feedback scope attempts this merge when
eligible, otherwise reports the remaining gates without starting indefinite observation.

## Stop with an honest result

Feedback work is accounted for when every observed item is applied or reported
with its reason for remaining unapplied and any required decision, and, in Feedback
or Drive scope, every thread has its disposition and any reply it requires is
visible. Distinguish locally fixed, verified, published, replied and resolved;
none implies the next. Report a thread awaiting confirmation with the question
and who must answer it; report a thread still missing a reply, resolution or
ticket its disposition requires as unfinished work.

On each Drive wake, refresh PR state and reconcile an observed ready event as
above, then check for merge. Apply the personal-repository policy before considering
an approval stop; outside that policy, a current formal approval also ends
babysitting, after the unblocked disposition actions for observed threads are
complete and thread-specific blockers are reported. On verified merge with a
linked ticket, invoke `issue-workflow` for `pr-merged` before returning, passing
the ticket, exact PR/head, actual merge branch/revision/time and completing or
contributing relation. Use Inspect in
Check scope; otherwise carry the task's existing transition authority. Respect
the policy's single owner and completion guards. Report its result separately
from the PR outcome, including a missing skill or blocked tracker operation.
Formal approval alone never emits `pr-merged`: retain the pending merge event and
report its configured durable owner or the uncovered delivery gap. Stop the host
watch when the PR stopping condition holds; do not extend Drive to solve that gap.
A host may
stop silently on merge or closure; do not promise a final agent message without
a wake. Report that outcome when next invoked. Approval does
not establish merge readiness; report any remaining checks, feedback or conflicts
without claiming they passed. Otherwise collect a fresh coherent snapshot of the
head/base, checks and feedback, repair authorized issues, and yield to the host
watch. Technical completion triggers the authorized personal-repository merge;
otherwise it does not end Drive before approval or merge.
Honor an explicit stop or user time limit, and report closed-unmerged state or
access blockers separately. Outside the personal-repository policy or another
explicit merge authorization, never merge or enable auto-merge merely to make the
loop finish. Never approve a gated workflow merely to end observation.

Return the PR URL and current head, applied work summary with relevant commits,
actual verification commands/results, current checks, and remaining items. For
each unapplied item give the evidence-based reason; for a user decision include
choices and recommendation. State `complete for requested scope`, `waiting`, or
`blocked` and what would allow continuation. Retain the ledger only while needed
for resumption, then remove owned scratch. Stop local watchers owned by this run;
retain this run's host watch only while Drive is waiting for its stopping condition.
Outside the personal-repository policy, other pending reviews do not override an
already verified approval stop.

For requested source maintenance, use `agent-instructions` with `origin.txt` and
[references/upstream-updates.md](references/upstream-updates.md).
