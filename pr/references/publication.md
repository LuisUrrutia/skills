# Publication and identity

Read before a Git or GitHub mutation. Apply request and standing authorization
first; a known authorized action does not need a second permission prompt.

## Before writing

Verify the exact target PR and head repository/ref, current local branch and HEAD,
push remote URL, base, and expected remote tip. Preserve unrelated work and index
state. If uncommitted in-scope work belongs in the PR, use `commit`; otherwise
describe only the published or selected committed head. A metadata-only edit does
not authorize shipping newer local commits.

Inspect the selected publication for credentials, private captures and unrelated
artifacts. Resolve any suspected exposure before publishing that content; do not
silently include it because it was already committed or appears in a template.

Resolve the intended GitHub actor from explicit user direction, otherwise the
path-effective `git config --get user.email` matched to an authenticated account.
The Git author name and SSH authentication do not prove the `gh` actor. Run
`gh api user --jq .login`; require an exact match before authenticated writes.
Switch to an already-authenticated intended account when necessary, then verify.
Ask if the mapping remains ambiguous. Never print tokens or secret configuration.

Use SSH for all Git network operations. Repair an SSH failure or report it; never
substitute HTTPS. Resolve missing or ambiguous destinations before pushing.

## Publish the selected branch

Use an explicit verified destination, such as
`git push -u <push-remote> HEAD:refs/heads/<branch>`, for a new tracking branch.
For an existing branch, verify the configured destination and push only that ref.
Do not publish unrelated refs or tags. Confirm the actual remote tip after success.

When an authorized base update is necessary, use rebase, not a merge commit.
`stacked-pr` owns cascading rewrites. Preserve a recovery ref and inspect conflicting
intent on both sides, then re-run the checks affected by the resulting code.

After an authorized rebase, publish only with a lease tied to the previously
recorded exact remote SHA, such as
`--force-with-lease=refs/heads/<branch>:<expected-sha>`. Immediately before the push,
recheck current branch, exact PR head, remote and remote tip. If the remote moved,
stop the push and reconcile the new work; do not refresh the lease blindly or
retry with plain force. A standing authorization for this operation remains valid.

After material publication to an open PR, rewrite its whole body from the verified
published diff in Update mode. Recheck head/base before writing; a concurrent
movement invalidates the prepared claims. Unless an explicit create-only instruction
applies, hand the new revision to `pr-followup` for a creation request or when
follow-up work is already authorized; return to an existing follow-up loop rather
than starting a nested one.

## Create or update metadata

Prepare multiline bodies in an ignored temporary file and use `--body-file`.
When including screenshots or recordings, read [attachments.md](attachments.md)
and add the verified files with `--attach` to this same create or edit operation.
Check the installed subcommand's help; do not infer support from a floating source.
Pass explicit repo, head, base and title. Creation defaults to:

```text
gh pr create --repo <target> --base <base> --head <head> --draft --title <title> --body-file <file>
```

Use `<branch>` for a same-repository head and `<owner>:<branch>` for a user-owned
fork. For the user's ready-by-default preference, omit `--draft`. Never use
interactive creation, `--web`, `--editor`, `--recover` or `--draft=false`.
Recheck exact open PR identity immediately before creating to avoid a duplicate.

Verify URL, head repository/ref/SHA, base, title, body and `isDraft` after writing.
For attached local references, expect `gh` to replace paths with uploaded URLs;
verify that transformation and surrounding content rather than byte equality with
the prepared body. Read back partial upload failures before any retry, as specified
in [attachments.md](attachments.md).
If a newly created PR has the wrong initial state, correct it once with
`gh pr ready <url>` or `gh pr ready --undo <url>` under the resolved initial-state
authorization, then verify. A continuing mismatch blocks further writes.

For Update, use the exact PR URL with `gh pr edit <url> --title <title> --body-file <file>`
and only authorized metadata flags. Leave base, reviewers, labels, milestone,
assignees and ready/draft state alone unless the request or standing scope covers
their change. Do not publish review replies, issue comments or approval reviews
as a side effect of writing a PR description.

If a write fails or times out, inspect remote state before retrying. Report the
actual partial outcome and failed prerequisite. Register the PR with the host and
verify any required thread links. PR readiness and merging are separate operations.
