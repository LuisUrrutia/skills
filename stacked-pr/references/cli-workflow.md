# Native stack through `gh stack`

Use this workflow when SKILL.md selects the CLI route. On this route `gh-stack` owns local tracking
and GitHub stack state for every mutation. Branches that no tool tracks yet are adopted first, as
part of the requested mutation, through the adopt step in [cli-create.md](cli-create.md). That
adoption is complete when the stack view lists the existing branches in order with their tips
unchanged; the requested operation then handles any rebase they need. When their open PRs form no
native stack yet, a request to create or submit a stack ends with the submit step in cli-create.md.
For any other operation, report the missing stack and ask before adoption whether to convert it,
because sync links two or more open PRs into a native stack. A declined conversion is the user's
choice of ordinary dependent PRs, and the manual route takes the operation. Branches that another
tool manages follow the interoperability section of [troubleshooting.md](troubleshooting.md).
Perform the requested operation and the root skill's authorized follow-up and landing continuation.

## Establish the live contract

Inspect the repository and extension before acting:

```bash
git status --short --branch
git remote -v
git --version
gh auth status
gh extension list
gh release list -R github/gh-stack --exclude-pre-releases --json tagName,publishedAt
```

The eligible release is the newest one older than the repository's release cooldown, or three days
when it sets none. When the listing lacks `github/gh-stack`, install that tag with
`gh extension install github/gh-stack --pin <tag>`. Before a mutation, when the installed version
is older and no rebase or modify recovery is pending, record it and copy its directory under the
`gh` extensions directory (by default `~/.local/share/gh/extensions/gh-stack`) to task scratch, then
run `gh extension remove gh-stack` and install the eligible tag with the same command; `--force`
would ignore the pin and take the latest release. If that install fails, restore the copy, or
reinstall the recorded version with `--pin` when no copy exists, and confirm `gh stack --version`
before continuing. A read-only request only reports the newer release. Record the version actually
installed with `gh stack --version`. Git older than 2.36 is a blocker for this route.

Retry a transient install failure once, then report it with its stderr; SKILL.md decides the next
step, and it never leads to layers opened with `gh pr create` on this route. After a failed upgrade,
report it and continue with the installed version. A stack that spans worktrees needs v0.2.0 or
later, where shared worktree tracking starts; with an older installed version, report a blocker.

For every planned command, read `gh stack <command> --help` and derive its current flags and
non-interactive form. Pass the recorded push remote with `--remote` to every command that accepts
it; with several remotes and no `remote.pushDefault`, non-interactive commands fail, and writing
that setting needs the user's approval. Preview behavior in live help and GitHub documentation
outranks examples in this skill.

Setup is complete when the repository, trunk, push remote, authenticated principal, Git and
installed extension versions, and non-interactive form of every planned command are recorded.

## Inspect

Use the current JSON view command from live help. It takes no target and reads only the current
local stack, and checkout writes local tracking, so inspect a remote stack without local tracking
through the API route's read endpoints. `gh pr view` reports each PR's head, base, and state, but
not stack membership. Treat a missing local stack as observed state, then check remote state when
the request requires it.

Inspection is complete when the report identifies:

- the trunk and push remote;
- every layer bottom-to-top, with branch and PR identifiers;
- each PR's base, draft or review-ready state, and merge state;
- local divergence or rebase needs;
- any fact that could not be established and the exact lookup that failed.

Stop after reporting those facts for a status, explanation, or review request.

## Check out

First run the inspection step and record dirty paths. Resolve the target to one exact branch, PR, or
stack before using the current non-interactive checkout form from live help. Preserve unrelated
changes across the switch.

Checkout is complete when the current branch is the resolved target, `git status --short --branch`
shows the expected upstream and preserved dirty paths, and a fresh stack view places that branch at
the expected layer. Stop after checkout unless the user requested another operation.

## Mutation branches

Load one matching branch at a time. After its completion criterion is satisfied, load another
when the request or the root skill's standing follow-up and landing authorization includes it:

- [cli-create.md](cli-create.md) — create, adopt, split, or submit layers.
- [cli-maintain.md](cli-maintain.md) — edit a layer, cascade a rebase, sync, or push.
- [cli-merge.md](cli-merge.md) — merge the authorized native-stack scope.
- [troubleshooting.md](troubleshooting.md) — recover from conflicts, divergence, stale metadata,
  restructuring, worktrees, or another branch manager.
