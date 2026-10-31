---
name: pr
description: "Create, update, or inspect a pull request; prepare its title, description, review evidence, and metadata; publish a branch for review."
---

# Pull request

Make one change understandable to its reviewer: problem, delivered behavior,
consequential decisions and evidence.

This skill owns publication and presentation. Use `commit` for atomic commits,
`stacked-pr` for stack topology, submission and cascading rebases, `pr-followup`
for feedback, CI repair and readiness, and `issue-workflow` for ticket transitions.
Invoke owners within the request or standing authority; completing this phase
continues an authorized caller's workflow.

## Resolve the operation

- **Create:** publish the selected commits and open a requested PR when no exact
  PR exists. Default to draft unless the user prefers ready.
- **Update:** refresh an exact open PR under existing authority.
- **Draft-only:** return requested copy or inspection using only necessary reads;
  make no commit, push or GitHub mutation.
- **Check cap:** run only [the size check](#check-the-review-size-cap). Return its
  verdict; the caller retains remediation, publication and continuation.

An exact closed or merged PR is historical: report its URL/state and obtain the
user's chosen operation before editing, reopening or replacing it. Otherwise ask
only for unresolved material decisions, applying existing authority first.
A blocker pauses dependent work; continue useful independent preparation.

## Establish identity and scope

Before the first `gh` command, read
[GitHub account](references/publication.md#github-account).

Read branch, status, remotes, upstream and HEAD. Resolve:

1. **Push destination:** verified requested or configured repository, remote and
   ref. Map URLs to repositories; a remote name proves neither identity nor
   intent. The branch upstream is a push destination, never the PR base.
2. **Target:** supplied PR URL or explicit repository; an upstream contribution
   from a fork targets its verified parent. Ask about material ambiguity.
3. **Exact PR:** inspect a supplied URL, otherwise collect relevant results with
   `gh pr list --repo <target> --state all --head <branch> --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`.
   Here `--head` takes the branch, not `owner:branch`; match branch **and** head
   repository. Disambiguate multiple exact matches. Failed or incomplete lookups
   are unknown, not empty. `gh pr` commands use GraphQL; when `gh api rate_limit`
   shows GraphQL `remaining` at 0, use REST, whose primary limit is separate:
   `gh api -X GET repos/<target>/pulls --paginate -f head=<head-owner>:<branch> -f state=all`,
   matching `head.ref` and `head.repo.full_name`. GitHub ignores a `head` without
   its owner. Add `--hostname <target-host>` to every `gh api` call when the
   target is not on github.com.
4. **Base:** retain an existing PR's actual base; for creation use the explicit
   verified base or target repository's default. Fetch through the target's SSH
   remote and verify that ref's identity rather than trusting local `main`.
   Route dependent-branch topology to `stacked-pr`.
5. **Revision:** record exact base/head SHAs. Describe selected local commits for
   publication, the published head for metadata-only work. Preserve unrelated
   work/index entries; they neither block metadata work nor belong in its claims.

Honor host checkout ownership and PR linking. Use its handoff and `worktrunk` when
switching checkouts.

## Understand the change and repository

Before substantive claims, read [claims](references/claims.md). Inspect every
commit in `<base>..<head>` and the full `<base>...<head>` diff; trace important
behavior through current code, gates and failures, including generated, binary,
dependency and migration changes.

Recommend splitting independently reviewable/revertible concerns when useful.
Do not shorten the diff by rewriting published history, reordering a stack or
separating behavior from its regression test. Necessary generated output is not
automatically noise.

Before writing a title or body, read:

- Repository instructions and `CONTRIBUTING.md`.
- Templates on the resolved base in root, `docs/`, `.github/` and their
  `PULL_REQUEST_TEMPLATE/` directories. Choose by task and rules; ask only about
  a consequential unresolved choice.
- Recently merged PRs not authored by bots, for example with
  `gh pr list --repo <target> --state merged --search 'sort:updated-desc' --limit 50 --json author,title,body,mergedAt --jq '[.[] | select(.author.is_bot | not)] | sort_by(.mergedAt) | reverse | {titles: (.[:10] | map(.title)), chars: (map(select((.body | length) > 0)) | .[:10] | map(.body | length))}'`
  (plain `gh pr list` orders by creation; a PR's update time is never before its
  merge). When GraphQL is exhausted, query
  `gh api -X GET repos/<target>/pulls -f state=closed -f sort=updated -f direction=desc -f per_page=50`
  and keep entries with `merged_at` whose `user.type` is not `Bot`. Read up to ten titles and the base's commit subjects
  (`git log --no-merges --format=%s -20 <base>`) for the title convention when no
  written rule sets it. For a body, measure up to ten non-empty bodies for the
  review packet's length budget and read three, or all if fewer exist, for style
  rather than policy.

Record inaccessible required evidence and its failed lookup as unknown;
continue supported work without inventing conventions.

## Check the review-size cap

Apply when the request, project or task record sets a cap. Resolve exact base/head
SHAs and cap; missing inputs or an unavailable diff yield `unverified`.

Count additions **plus deletions** in the full `<base-sha>...<head-sha>` diff,
including tests, generated text and lockfiles: `git diff --shortstat` for totals,
`--numstat` for binaries. Do not use net growth, commit sums or path exclusions;
splitting commits cannot shrink a PR.

Return `within-cap`, `over-cap` or `unverified`, with revisions, count, cap and
binary review burden. Require a fresh `within-cap` immediately before pushing or
creating; changed base/head invalidates it. The publishing owner sends over-cap
work to `task-breakdown` to revise the units; never silently waive the cap or
rewrite published history.
Draft-only and metadata-only work may report violations without shipping code.

## Compose for review

When the task, branch, commits or body reference a ticket, invoke `issue-workflow`
Inspect before composing its relation, including Draft-only. Pass the ticket or
lookup hint, repository, base and evidence of completing/contributing scope. Use its verified identity,
permitted link form and event policy, or `not applicable`; preserve valid links on
Update. Draft-only grants no tracker writes.

For every title/body, read [review packet](references/review-packet.md). When
visuals clarify an interface, flow or structure, read
[visual evidence](references/visual-evidence.md). For visible UI changes, capture
and attach relevant app states when the app, capture tool and upload route are
available, reusing verified captures of that revision. Read
[attachments](references/attachments.md) for placement/upload; report inaccessible
prerequisites and retained evidence.

## Publish and verify

Before any Git/GitHub mutation, read [publication](references/publication.md) and
execute the applicable steps. Prepare reviewable copy and necessary validation
before seeking any remaining authorization. Apply its
[result check](references/publication.md#verify-the-result) also when accepting an
existing open PR without a write.

After verified publication for a **creation request**, including an existing open
PR that satisfies it, execute [continuation](references/continuation.md) before
returning: it continues into `pr-followup` Drive, which arms the host watch, unless
the user asked for the PR without follow-up. For Update with authorized follow-up, invoke `pr-followup` unless
create-only; reuse an existing loop. Draft-only starts none.
Publication never merges by itself.

## Return

Report `created`, `updated`, `draft-only` or `blocked`: URL when known, head/base,
draft state, body length against its budget with the reason for any overrun,
detail comment URL, validation, executed commands/results, remaining work and coordination omitted
from the body. Separate current execution from historical evidence. Draft-only
returns the copy and confirms no mutation; blockers name the prerequisite or
decision and completed work. Pass verified identity, revision and publication
state back to an authorized caller.
