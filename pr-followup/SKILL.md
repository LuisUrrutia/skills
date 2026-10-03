---
name: pr-followup
description: Follow an existing pull request, evaluate human and AI review feedback, and resolve authorized feedback, CI failures, and base conflicts.
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
  Use this for requested babysitting; do not start it merely because a PR was created.

Resolve scope from the request and standing instructions. Record whether commits,
publication, replies and thread resolution are authorized. Code repair alone does
not authorize messages to reviewers. Do not require approval again for covered work.
Set a finite observation window for Drive: use the user's limit, otherwise state a
30-minute window. Reaching it returns current evidence and pending work, not success
or an automatic extension. Persistent scheduling requires a separate explicit request.

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

## Stop with an honest result

Feedback work is accounted for when every observed item is applied or reported
with its reason for remaining unapplied and any required decision. Distinguish
locally fixed, verified, published, replied and resolved; none implies the next.

Drive is settled only after a fresh coherent snapshot has the expected head/base,
required checks satisfied, observed failures and feedback accounted for, and no
known active required reviewer left unobserved. Assess merge readiness separately:
required approvals, review decisions, draft state and platform merge requirements
must also be satisfied. Silence, an old green run, a quiet interval or API failure
does not establish readiness. Never merge, enable auto-merge, mark an existing
draft ready, or approve a gated workflow merely to make this loop finish.

Return the PR URL and current head, applied work summary with relevant commits,
actual verification commands/results, current checks, and remaining items. For
each unapplied item give the evidence-based reason; for a user decision include
choices and recommendation. State `complete for requested scope`, `waiting`, or
`blocked` and what would allow continuation. Retain the ledger only while needed
for resumption, then remove owned scratch. Stop any watcher owned by this run.

For requested source maintenance, use `agent-instructions` with `origin.txt` and
[references/upstream-updates.md](references/upstream-updates.md).
