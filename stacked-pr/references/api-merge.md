# Merge a native stack through REST

Use this branch for a merge request or the root `SKILL.md`'s standing landing authorization.
Its authorization gate is a precondition; under its personal-repository policy, select only
the current bottom PR and verify every `pr-followup` merge gate for its current head/base.

Immediately before the request:

1. Refetch the stack and resolve the authorized target to the exact unmerged PR set it will affect.
2. Verify that every selected PR is review-ready and that checks, reviews, merge method, and current
   head SHAs still match the explicit approval, or establish the standing policy's gates and method anew.
3. Read the live asynchronous-merge schema, including accepted states, conflict behavior, merge
   queue behavior, and the operation-status lookup.
4. Pin the request to the documented head SHA field and submit it once.

If GitHub reports an existing asynchronous operation, compare its target and options with the
authorized scope before observing it. Persist its operation identifier and use the host watch while
waiting for a documented terminal result or an explicit queued state. Refetch the stack and all
affected PRs afterward.

Merge is complete only when the exact authorized set is reported merged or queued. Report queued work
as queued, surface terminal failure with GitHub's reason, and verify the bases and order of any
remaining layers. After verified merge under standing authorization, continue with the next layer
as the root skill directs; otherwise stop.
