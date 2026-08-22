# Merge a native CLI stack

Use this branch only for a merge request. The approval gate in the root `SKILL.md` is a
precondition.

Immediately before the merge command:

1. Refetch the stack and resolve the approved PR or stack identifier to the exact unmerged PR set.
2. Verify that the current set, head SHAs, draft states, checks, reviews, and merge method still
   match the approval.
3. Read live merge help and select its non-interactive invocation for the repository-approved
   method.
4. Run one merge command for the approved scope, then observe GitHub until it reports a terminal
   result or an explicit queued state.

A PR target may include lower unmerged layers; calculate and show that set before consuming the
approval. Treat a queued result as queued rather than merged.

Merge is complete only when the exact approved set is reported merged or queued, the remaining
stack's bases and order are verified, and the handoff distinguishes terminal success, queued work,
and failure. Stop after reporting that result.
