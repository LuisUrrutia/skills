---
name: pr
description: "Create, update, or inspect a pull request; prepare its title, description, review evidence, and metadata; publish a branch for review."
---

# Pull request

Make one change understandable to a human reviewer: the problem, delivered
behavior, consequential decisions, and evidence needed to assess it.

This skill owns publication and PR presentation. `commit` owns atomic commits;
`stacked-pr` owns stack topology, submit and cascading rebases; `pr-followup`
owns feedback, CI repair and the transition from draft to ready for review. Use
those owners only for work included in the active request or standing instructions.
Returning to an authorized caller continues its workflow; completing this phase does not cancel the enclosing task.
`issue-workflow` owns linked-ticket synchronization under the consuming project's
canonical transition policy.

## Resolve the operation

- **Create:** publish the intended commits and open a PR when requested and no
  exact PR exists. Default to draft unless the user's preference says ready.
  A request to create a PR also invokes `pr-followup` in Drive mode after
  publication, including when an exact open PR already satisfies creation.
- **Update:** refresh an existing open PR under existing authorization. Rewrite
  the whole body from the final published diff; preserve still-valid evidence
  and required template content. A request to update does not need a second approval.
- **Draft-only:** provide requested copy or inspection without a commit, push,
  or GitHub mutation. Use only the reads needed for that deliverable.

An exact closed or merged PR is historical state. Show its URL and state; do not
edit, reopen or replace it unless the user has chosen that operation. Ask only for
unresolved material decisions, never for an action already authorized. A blocker
pauses its dependent work; finish independent preparation when useful.

## Establish identity and scope

Read current branch, status, remotes, upstream and HEAD. Resolve:

1. **Push repository, remote and ref:** use the branch's verified upstream or the
   requested destination; map remote URLs to actual GitHub repositories. Remote
   names are hints. A branch's upstream is a push destination, never the PR base.
2. **Target repository:** prefer the supplied PR URL or explicit target. For an
   upstream contribution from a fork, use the verified parent, not the fork by
   accident. Ask if fork versus parent remains materially ambiguous.
3. **Exact PR:** query all relevant results with
   `gh pr list --repo <target> --state all --head <branch> --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`.
   `--head` takes the branch here, not `owner:branch`; filter by both branch and
   head repository identity. A failed or incomplete query is not an empty result.
   Inspect a supplied URL directly. Multiple exact matches need disambiguation.
4. **Base:** retain an existing PR's actual base. For a new PR, use an explicit
   verified base or the target repository's default. Detect dependent branches
   and pass topology decisions to `stacked-pr`. Use the target's SSH remote to
   fetch the chosen base; verify its identity rather than trusting local `main`.
5. **Revision:** identify the head actually being described: selected local
   commits for creation/publication, published head for metadata-only work.
   Record base and head SHAs. Preserve unrelated working and staged changes;
   they do not block a metadata-only update and do not belong in its claims.

Honor the host's checkout ownership and PR-linking requirements. When switching
checkouts is necessary, use the host handoff and `worktrunk` owner. Register the
actual PR with the host when it provides that capability.

## Understand the change and repository

Read [references/claims.md](references/claims.md) before making substantive
claims. Inspect every commit in `<base-ref>..<head>` and the full
`<base-ref>...<head>` diff, then trace the important behavior through current code,
gates and failure paths. Account for generated, binary, dependency and migration
changes. Do not equate tests present with tests passed or issue intent with delivery.

Check whether independent concerns can be reviewed and reverted separately.
Recommend a split when it materially helps; do not rewrite published history,
reorder a stack or separate a behavior from its regression test just to shorten
the diff. Necessary generated output is not automatically noise.

When the request, project rules or task record sets a PR size cap, measure additions
plus deletions in the full `<base-sha>...<head-sha>` diff, including tests, generated
text and lockfiles. Use Git's `--shortstat` for totals and `--numstat` to identify
binary entries; do not use net growth, sums of commits or excluded paths. Record
the exact revisions, count, cap and any binary review burden. For a stack layer,
the base is its immediate PR base. An unavailable diff blocks publication of the
capped work until it can be measured. If over the cap, stop code publication and
PR creation, and use `task-breakdown` to revise the units;
do not silently waive the cap or rewrite published history. Draft-only and
metadata-only work can still report the violation without shipping more code.

Before composing a body, read:

- Written PR rules in repository instructions and `CONTRIBUTING.md`.
- Templates on the resolved base in root, `docs/`, `.github/` and their
  `PULL_REQUEST_TEMPLATE/` directories. A template changed by this branch does
  not establish existing convention. Choose the applicable template from the
  change and repository rules; ask only if a remaining choice matters.
- Up to ten recent merged PRs; read three bodies, or all when fewer exist.
  Use relevant recent examples for style, not as authority over written rules.

Record inaccessible required evidence as unknown with the exact failed lookup.
Continue what the available evidence supports; do not invent missing conventions.

## Compose for review

When the task, branch, commits or PR body reference a ticket, use `issue-workflow`
in Inspect mode before composing its PR relation. Pass the supplied ticket or
lookup hint, exact repository, base and your evidence for a completing or
contributing relation. It verifies the ticket identity and relation, returning
`not applicable` if none is linked. For a verified ticket it returns the
project's permitted link form and event policy; preserve valid links on Update.
This also applies to Draft-only without authorizing tracker writes. Do not invent
a ticket or use closing keywords when the policy requires the issue open for QA.

Read [references/review-packet.md](references/review-packet.md) for every title
or body. Read [references/visual-evidence.md](references/visual-evidence.md) when
a changed interface, flow or structure would be easier to assess visually.
Use the smallest useful diagram, genuine screenshots or measured comparison.
Ordinary small changes can be explained in a sentence.

For visible UI changes, capture and attach the relevant app states when the app,
capture tool and upload route are available. Use existing verified captures when
they match the revision. Follow [references/attachments.md](references/attachments.md)
to upload them into the PR body; a local screenshot path is not an attachment.
If a prerequisite is inaccessible, report which one and the evidence retained.

Follow repository requirements and preserve meaningful template fields. When a
style convention leaves useful context out, a small addition is appropriate;
explain a material departure. An exact enforced format still applies unless the
user explicitly overrides it. Keep the body proportional to the review decision.

For Update, draft from the complete published change and replace obsolete claims,
rather than appending a history of successive fixes. Revalidate useful links,
screenshots and completed checklist claims before carrying them forward. Use
`communicate-clearly` when available for clear prose without weakening technical meaning.

## Publish and verify

For any Git or GitHub mutation, read
[references/publication.md](references/publication.md). It owns identity checks,
SSH publication, non-interactive commands, draft state and post-write verification.
Recheck any review-size cap against the selected publication revisions immediately
before pushing or creating the PR; changed base or head invalidates an earlier count.
Complete the reviewable title/body and necessary validation before asking for a
remaining authorization. Existing request and standing authorization take precedence
over source workflows that require blanket confirmation.

A successful phase has the exact PR URL, expected head and base, verified title
and body, intended state, and only requested metadata changes. Included captures
have verified uploaded references and a recorded rendering/access result. A failed
write is unknown until inspected; avoid duplicate creation or claims of success on timeout.
For a creation request with a linked ticket, invoke `issue-workflow` with the
verified `pr-created` event, ticket URL, exact PR/head/base, draft state and
completion relation. Include drafts. If the project instead selects `pr-ready`
and this verified PR is already non-draft, reconcile `pr-ready` now; do not wait
for a draft-to-ready transition that will never occur. Otherwise leave that
configured ready event pending. This applies when an exact open PR already
satisfies creation, using current state guards rather than blindly replaying an
old transition. Standalone
Update does not synthesize a creation event. Return the synchronization result
separately; a blocked tracker transition does not undo publication or stop
independent follow-up. If `issue-workflow` is missing, report that gap and retain
the event for resumption without guessing a state.
For a creation request, continue with `pr-followup` in Drive mode before returning:
pass the exact PR URL, head/base SHAs, draft state, validation and known pending work.
Also pass the verified ticket relation, transition result and merge-delivery owner
or uncovered event from `issue-workflow` when relevant.
That phase owns feedback/CI repair, readiness and post-ready observation under the
same request; do not stop at the creation summary. Honor an explicit create-only
instruction by returning after publication. Pass an explicit keep-draft instruction
to `pr-followup`, which runs Drive without the ready transition.
An Update that satisfies a creation request also continues into Drive. Standalone Update and Draft-only do not start Drive;
an Update called by follow-up returns to that existing loop. Never merge as
a side effect of publication. If `pr-followup` is unavailable, report the verified
publication result and the missing skill as a blocker to continuation.

## Return

Report `created`, `updated`, `draft-only` or `blocked`, with the PR URL when known,
head/base, draft state, relevant validation and remaining work. Include actual
commands and outcomes, distinguishing current execution from historical evidence.
For draft-only, provide the requested copy and state that no mutation occurred.
For a blocker, name its failed prerequisite or decision and retain completed work.
Hand verified identity, revision and publication state back to an authorized caller.

For requested source maintenance, use `agent-instructions` with `origin.txt` and
[references/upstream-updates.md](references/upstream-updates.md).
