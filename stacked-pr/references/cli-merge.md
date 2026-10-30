# Merge a native CLI stack

Use this branch for a merge request or the root `SKILL.md`'s standing landing authorization.
Its authorization gate is a precondition; under its personal-repository policy, select only
the current bottom PR and verify every `pr-followup` merge gate for its current head/base.

Immediately before the merge command:

1. Refetch the stack and resolve the authorized PR or stack identifier to the exact unmerged PR set.
2. Verify that the current set, head SHAs, draft states, checks, reviews, and merge method still
   match the explicit approval, or establish the standing policy's gates and method anew.
3. Read live merge help and select its non-interactive invocation for the repository-approved
   method. Pass the authorized target and method explicitly: without them, the non-interactive form
   merges the whole current stack with the last-used method.
4. Run one merge command for the authorized scope, then observe GitHub until it reports a terminal
   result or an explicit queued state.

A PR target may include lower unmerged layers; calculate and show that set, then verify its authorization.
Treat a queued result as queued rather than merged.

Merge is complete only when the exact authorized set is reported merged or queued, the remaining
stack's bases and order are verified, and the handoff distinguishes terminal success, queued work,
and failure. A queued result waits through the host watch. After verified merge under standing
authorization, continue with the next layer as the root skill directs; otherwise stop.
