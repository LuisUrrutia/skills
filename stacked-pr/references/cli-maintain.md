# Maintain a native CLI stack

Use this branch for exactly one requested maintenance operation. Read live help for each planned
command before mutation.

## Edit one layer and cascade upward

Inspect the stack, check out the branch that owns the concern, and apply the change there. Run that
layer's checks, commit only its paths, then use the current cascading-rebase command for the affected
upper range. Resolve conflicts through [troubleshooting.md](troubleshooting.md). Push the affected
branches with the current safe non-interactive command.

This operation is complete when every affected layer contains its parent tip, layer checks pass,
GitHub has the expected heads and bases, and the JSON view reports no rebase need in the affected
range.

## Sync local and remote state

Fetch the push remote, inspect local and remote order, and read current sync help before running it.
When the two chains contain different work, stop mutation and use the divergence branch in
[troubleshooting.md](troubleshooting.md). Apply cleanup or pruning only when it is part of the
request.

Sync is complete when local and GitHub order, branch heads, PR bases, and trunk agree, while every
unrelated local ref and dirty path remains preserved.

## Push an already verified stack

Refetch remote heads immediately before pushing. Use the CLI's current safe push form and retain
lease protection for rewritten branches.

Push is complete when every intended remote ref equals its verified local tip, no unintended ref
changed, and a fresh stack read reports the expected order and bases.
