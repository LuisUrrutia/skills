# Merge a native stack through REST

Use this branch only for a merge request. The approval gate in the root `SKILL.md` is a
precondition.

Immediately before the request:

1. Refetch the stack and resolve the approved target to the exact unmerged PR set it will affect.
2. Verify that every selected PR is review-ready and that checks, reviews, merge method, and current
   head SHAs still match the approval.
3. Read the live asynchronous-merge schema, including accepted states, conflict behavior, merge
   queue behavior, and the operation-status lookup.
4. Pin the request to the documented head SHA field and submit it once.

If GitHub reports an existing asynchronous operation, compare its target and options with the
approval before observing it. Persist its operation identifier and poll with bounded backoff until
GitHub returns a documented terminal result or an explicit queued state. Refetch the stack and all
affected PRs afterward.

Merge is complete only when the exact approved set is reported merged or queued. Report queued work
as queued, surface terminal failure with GitHub's reason, and verify the bases and order of any
remaining layers before stopping.
