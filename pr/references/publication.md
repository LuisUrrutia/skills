# Publication and identity

Apply existing request/standing authority before seeking additional permission.

## Before writing

Recheck exact PR, head repository/ref/SHA, local branch/HEAD, push URL, base and
expected remote tip. Preserve unrelated work/index state. Use `commit` for
uncommitted work included in publication; metadata-only work ships no new commits.
Inspect selected content, the body and any detail comment for credentials, private
data, private captures and unrelated artifacts; resolve suspected exposure even
when already committed.

Resolve the intended GitHub actor from user direction, otherwise path-effective
`git config --get user.email` matched to an authenticated account. Neither author
name nor SSH authentication proves it. Require an exact
`gh api user --jq .login` match before authenticated writes; switch to the intended
already-authenticated account and recheck when needed. Ask if ambiguous; expose
no tokens or secret configuration.

Use SSH for every Git network operation. Repair failures or report the blocker;
never substitute HTTPS. Resolve ambiguous destinations before pushing.

## Publish the selected branch

Push only the verified branch to its explicit destination, for example
`git push -u <remote> HEAD:refs/heads/<branch>`; include no unrelated refs/tags.
Confirm the actual remote tip afterward.

For necessary authorized base updates, preserve a recovery ref and rebase;
`stacked-pr` owns cascading rewrites. Reconcile both sides' intent in conflicts and
rerun affected checks.

Publish a rebase only with an exact recorded lease:
`--force-with-lease=refs/heads/<branch>:<expected-sha>`. Immediately before pushing,
recheck branch, exact PR head, remote and tip. If the tip moved, reconcile the new
work before publishing; never blindly refresh the lease or use plain force.

After material publication to an open PR, perform Update from its verified
published diff. Recheck head/base before writing; movement invalidates prepared
claims. Continue according to the entrypoint's request/caller routing.

## Create or update metadata

Write multiline bodies to ignored temporary files and use `--body-file`. Check
installed subcommand help for flags. For captures, follow
[attachments](attachments.md) in the same operation.

Recheck exact open PR identity immediately before creating. Use explicit values:

```text
gh pr create --repo <target> --base <base> --head <head> --draft --title <title> --body-file <file>
```

The head is `<branch>` within one repository, `<owner>:<branch>` for a user-owned
fork. Omit `--draft` for ready preference. Creation is non-interactive: never use
`--web`, `--editor`, `--recover` or `--draft=false`.

For Update, use
`gh pr edit <exact-url> --title <title> --body-file <file>` with only authorized
metadata flags. Changing base, reviewers, labels, milestone, assignees or draft
state needs covering authority. Description work posts no replies or approvals.
Its only comment is one detail comment per PR, holding detail the
[length budget](review-packet.md#length-budget) moves out of the body; this skill
words it. Post it once the PR exists, link it from the body, and on later writes
edit it, for example with
`gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -F body=@<file>`,
instead of adding another. Feedback replies belong to `pr-followup`, their
wording to `comment-style`.

When GraphQL is exhausted as [exact PR](../SKILL.md#establish-identity-and-scope)
defines, recheck through its REST lookup, then create with
`gh api repos/<target>/pulls -f title=<title> -f head=<head> -f base=<base> -F draft=true -F body=@<file>`
(omit `draft` for ready preference; for a fork head add
`-F maintainer_can_modify=true`, and `-f head_repo=<head-repository-name>` when
both repositories share an organization owner), update with
`gh api -X PATCH repos/<target>/pulls/<number> -f title=<title> -F body=@<file>`,
post the detail comment with
`gh api repos/<target>/issues/<number>/comments -F body=@<file>`, and read back
with `gh api repos/<target>/pulls/<number>`. REST has no `--attach`; follow
attachments' unavailable route. Draft-state changes wait for the GraphQL reset.

## Verify the result

After every write, including failure/timeout, and before accepting an existing PR
without writing, verify remote URL, head repository/ref/SHA, base, title, body,
any detail comment, intended draft state and only requested metadata changes.
Resolve mismatches before declaring success or continuing; inspect uncertain
outcomes before retrying.
Report partial outcomes and failed prerequisites. Attachments require
URL transformation and surrounding-content checks, not local-body byte equality;
their reference owns recovery and rendering/access checks.

Correct a newly created PR's wrong initial state once with `gh pr ready <url>` or
`gh pr ready --undo <url>` under initial-state authority, then verify. A continuing
mismatch blocks further writes.

Register the PR with the host and verify required thread links.
