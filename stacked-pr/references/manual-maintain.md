# Maintain a manual dependent-PR chain

Use exactly one operation below. Inspect the chain and preserve relevant tips before mutation.

## Edit one layer

Apply feedback on the branch that owns the concern, run its checks, and commit only its paths. Replay
each affected upper layer onto its updated parent and push rewritten refs atomically with leases.
Update PR-body maps when identifiers or order change.

This operation is complete when every affected branch contains its parent tip, each PR still shows
only its layer, checks pass, remote refs match verified local tips, and all maps agree.

## Restack onto a moved trunk

Fetch the intended remote and replay the entire chain from the top so intermediate refs move with
their commits. Handle branches checked out in other worktrees explicitly. Push the affected refs
atomically with leases, then verify PR bases and diffs.

Restacking is complete when every branch contains the new trunk, every direct PR base remains the
intended parent, each layer diff is unchanged except for conflict resolutions, and all remote refs
match their verified local tips.

## Retarget or restructure

Preserve the previous tips and combined top diff. Rewrite ancestry bottom-up, set every PR base to
its new direct parent, and update all maps.

Restructuring is complete when ancestry and GitHub bases prove the requested order, every layer owns
one concern, the combined top diff changed only as requested, and the previous state remains
recoverable.
