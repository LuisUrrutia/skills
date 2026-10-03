---
name: pr
description: "Create, update, or inspect a pull request; prepare its title, description, review evidence, and metadata; publish a branch for review."
---

# Pull request

Make one change understandable to a human reviewer: the problem, delivered
behavior, consequential decisions, and evidence needed to assess it.

This skill owns publication and PR presentation. `commit` owns atomic commits;
`stacked-pr` owns stack topology, submit and cascading rebases; `pr-followup`
owns requested feedback and CI repair. Use those owners only for work included
in the active request or standing instructions. Returning to an authorized caller
continues its workflow; completing this phase does not cancel the enclosing task.

## Resolve the operation

- **Create:** publish the intended commits and open a PR when requested and no
  exact PR exists. Default to draft unless the user's preference says ready.
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

Read [references/review-packet.md](references/review-packet.md) for every title
or body. Read [references/visual-evidence.md](references/visual-evidence.md) when
a changed interface, flow or structure would be easier to assess visually.
Use the smallest useful diagram, genuine screenshots or measured comparison.
Ordinary small changes can be explained in a sentence.

Follow repository requirements and preserve meaningful template fields. When a
style convention leaves useful context out, a small addition is appropriate;
explain a material departure. An exact enforced format still applies unless the
user explicitly overrides it. Keep the body proportional to the review decision.

For Update, draft from the complete published change and replace obsolete claims,
rather than appending a history of successive fixes. Revalidate useful links,
screenshots and completed checklist claims before carrying them forward. Use
`humanize` when available for clear prose without weakening technical meaning.

## Publish and verify

For any Git or GitHub mutation, read
[references/publication.md](references/publication.md). It owns identity checks,
SSH publication, non-interactive commands, draft state and post-write verification.
Complete the reviewable title/body and necessary validation before asking for a
remaining authorization. Existing request and standing authorization take precedence
over source workflows that require blanket confirmation.

A successful phase has the exact PR URL, expected head and base, verified title
and body, intended state, and only requested metadata changes. A failed write is
unknown until inspected; avoid duplicate creation or claims of success on timeout.
Do not start monitoring, respond to reviews, change ready state on an existing PR,
or merge solely because this phase succeeded.

## Return

Report `created`, `updated`, `draft-only` or `blocked`, with the PR URL when known,
head/base, draft state, relevant validation and remaining work. Include actual
commands and outcomes, distinguishing current execution from historical evidence.
For draft-only, provide the requested copy and state that no mutation occurred.
For a blocker, name its failed prerequisite or decision and retain completed work.
Hand verified identity, revision and publication state back to an authorized caller.

For requested source maintenance, use `agent-instructions` with `origin.txt` and
[references/upstream-updates.md](references/upstream-updates.md).
