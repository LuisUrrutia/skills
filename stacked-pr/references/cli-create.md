# Create or submit a native CLI stack

Use this branch only for the requested creation operation or for the adoption that a mutation on
this route requires. The CLI route's live-contract checks are
preconditions.

## Plan

Load [stack-design.md](stack-design.md). State the layers bottom-to-top, with one concern and one
owner for every incremental change; files may evolve across layers. For an oversized branch,
existing PRs, worktrees, or another branch manager, load
[troubleshooting.md](troubleshooting.md) before rewriting or adopting anything.

Planning is complete when every incremental change has one owner, every dependency points toward the
trunk, and the verification command for each layer is known.

## Build or adopt

Read live help for the current create/adopt and add-layer commands. Create the bottom layer from the
intended trunk, verify it, then create each upper layer from the one below. Stage explicit paths or
hunks so unrelated changes stay outside the stack. Multiple commits may share a layer when they
serve its single concern.

For adoption, preserve existing tips and verify ancestry before writing local stack metadata.

Build or adoption is complete when the CLI's JSON view shows the planned order, each adjacent parent
is an ancestor of its child, every incremental change and commit belongs to one concern,
layer checks pass, and no branch needs a rebase. Stop here when the request is local-only. A
prerequisite adoption ends at the criterion in [cli-workflow.md](cli-workflow.md); the requested
operation owns the rebase need.

## Submit

Read live help for the current non-interactive submit form and determine how it represents the
requested draft state. Submit only the built or adopted layers in scope.

Load the `pr` skill. Give every PR a repository-conformant title and body plus the same compact
bottom-to-top map, marking the current layer. Preserve the stage of existing PRs unless the request
changes it.

Submission is complete when a fresh GitHub read proves that every requested PR has the intended
head, base, title, body, stack map, and draft state. Report created and reused PR identifiers, then
stop.
