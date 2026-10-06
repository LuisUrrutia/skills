# Create a manual dependent-PR chain

Use this branch only to create or adopt an ordinary chain.

## Plan and build

Load [stack-design.md](stack-design.md). State the bottom-to-top plan, then create each branch from
the one below it and commit one concern per layer. For adoption or an oversized source branch,
preserve every original tip and load [troubleshooting.md](troubleshooting.md) before rewriting.

Build is complete when each branch contains its parent, every incremental change has one owner layer,
layer checks pass, and the combined top diff matches the intended feature.

## Open or adopt PRs

Push the named branches. Query by exact head before creating a PR, reuse an existing open match, and
set every direct base to the branch immediately below. Load the `pr` skill for repository title,
template, and review-packet conventions. Put the same bottom-to-top map in every body and mark the
current PR.

Creation is complete when every requested layer has exactly one PR, its direct base and diff contain
only that layer, titles and bodies follow repository conventions, and the requested draft state is
verified from fresh GitHub reads. Stop after reporting the chain.
