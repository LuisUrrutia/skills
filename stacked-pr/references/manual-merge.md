# Merge a manual dependent-PR chain

Use this branch only to merge the current bottom PR. The approval gate in the root `SKILL.md` is a
precondition. Manual chains merge one layer at a time; a higher PR still targets a feature branch.

Immediately before the command, refetch the chain and verify that the approved PR is the current
bottom, its head SHA and diff match the approval, checks and reviews pass, and the merge method is
allowed by the repository. Merge only that PR.

After GitHub confirms the merge, fetch the trunk. Replay the remaining chain onto it so commits
already represented by the merged layer are removed, push rewritten refs with leases, and retarget
the next PR explicitly to the trunk. Verify its diff and update every remaining PR map.

Merge is complete when GitHub reports the approved bottom PR merged, the next PR targets the trunk
with only its own layer diff, remaining branch ancestry and maps agree, and every preserved dirty
path is intact. Stop; another layer requires another approval and operation.
