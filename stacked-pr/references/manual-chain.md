# Manual dependent-PR chain

Use this workflow when SKILL.md selects the manual route. Git ancestry and PR bases are the source
of chain state. Normally a manual chain has no native stack object on GitHub. Leave any retained one
unchanged; change its membership only through the API route, or dissolve it when the user
explicitly asked for ordinary dependent PRs or for dissolution. Perform only the requested
operation.

## Inspect

Inspect the local tree, remotes, authentication, relevant branch tips, and open PRs. Derive the chain
from Git ancestry and each PR's direct base. Compare every layer diff with its parent rather than
assuming the PR body map is current.

Inspection is complete when the report identifies the trunk, bottom-to-top branch and PR order,
every direct base, draft and merge state, ancestry or diff mismatches, and any missing fact with its
failed lookup. Stop after reporting those facts for a read-only request.

## Check out

Preserve dirty paths, resolve the requested PR to its exact head branch, and switch with plain Git.
Checkout is complete when the current branch is that head, its upstream is expected, dirty paths are
preserved, and its parent and child positions in the inspected chain are known. Stop unless another
operation was requested.

## Mutation branches

Load one matching branch at a time. Load another only when it is explicitly included in the request
and the current operation's completion criterion is satisfied:

- [manual-create.md](manual-create.md) — create or adopt an ordinary dependent-PR chain.
- [manual-maintain.md](manual-maintain.md) — edit, restack, retarget, or push the chain.
- [manual-merge.md](manual-merge.md) — merge one approved bottom layer and repair the remainder.
- [troubleshooting.md](troubleshooting.md) — recover or migrate the chain.

Keep the PR-body map accurate because it is operational orientation, not server-enforced state.
