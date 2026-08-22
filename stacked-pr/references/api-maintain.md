# Maintain a native stack through REST and Git

Use exactly one operation below. Establish the API route's live contract and inspect the current
stack first.

## Edit or restack branches

Apply a change on the branch that owns it. Use plain Git to replay only the affected upper range,
with recorded conflict resolution enabled when available. Branches checked out in another worktree
require explicit handling. Push rewritten refs atomically with leases, then refetch remote state.

This operation is complete when every affected branch contains its parent tip, the intended remote
accepted every leased update, layer checks pass, and the stack read still reports the planned order
and bases.

## Change review stage

Use the current documented PR transition for each affected PR. Preserve all unrequested PR stages.

This operation is complete when fresh PR reads report the requested stage for every affected PR and
unchanged stages for all other stack members.

## Restructure or dissolve

Preserve every branch tip and record the combined top diff. Read the current documentation to
determine whether the requested membership change is supported in place. When it is not, use the
documented dissolve operation, rewrite ancestry, patch PR bases, and recreate the stack in the new
bottom-to-top order. A partial or locked response is state to resolve before recreation.

Restructuring is complete when fresh stack and PR reads prove the requested order and bases, the
combined top diff changed only as requested, and the preserved tips keep the previous state
recoverable. Dissolution is complete when no eligible PR remains grouped and branch and PR state is
reported explicitly.
