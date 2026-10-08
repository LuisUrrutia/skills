# Native stack through `gh stack`

Use this workflow when SKILL.md selects the CLI route. On this route `gh-stack` owns local tracking
and GitHub stack state for every mutation. Branches that no tool tracks yet are adopted first, as
part of the requested mutation, through the adopt step in [cli-create.md](cli-create.md). That
adoption is complete when the stack view lists the existing branches in order with their tips
unchanged; the requested operation then handles any rebase they need. Branches that another tool
manages follow the interoperability section of [troubleshooting.md](troubleshooting.md). Perform
only the requested operation.

## Establish the live contract

Inspect the repository and extension before acting:

```bash
git status --short --branch
git remote -v
gh auth status
gh extension list
```

Install `github/gh-stack` only when the requested operation requires it and it is absent. For every
planned command, read `gh stack <command> --help` and derive its current flags and non-interactive
form. Preview behavior in live help and GitHub documentation outranks examples in this skill.

Setup is complete when the repository, trunk, push remote, authenticated principal, extension
availability, and non-interactive form of every planned command are recorded.

## Inspect

Use the current JSON view command from live help. For a remote stack without local tracking, inspect
it by PR or stack identifier through the supported read-only command or the API route. Treat a
missing local stack as observed state, then check remote state when the request requires it.

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

Load one matching branch at a time. Load another only when it is explicitly included in the request
and the current operation's completion criterion is satisfied:

- [cli-create.md](cli-create.md) — create, adopt, split, or submit layers.
- [cli-maintain.md](cli-maintain.md) — edit a layer, cascade a rebase, sync, or push.
- [cli-merge.md](cli-merge.md) — merge the approved native-stack scope.
- [troubleshooting.md](troubleshooting.md) — recover from conflicts, divergence, stale metadata,
  restructuring, worktrees, or another branch manager.
