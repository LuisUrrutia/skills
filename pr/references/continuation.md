# Continue a creation request

Use after verified publication, including when an existing open PR satisfies
creation.

For a linked ticket, invoke `issue-workflow` with verified `pr-created` (drafts
included), ticket URL, exact PR/head/base, draft state and completing/contributing
relation. If its policy instead selects `pr-ready` and the PR is already non-draft,
reconcile that event now; otherwise retain it for the ready transition. Use current
state guards, not blind event replay.

Report synchronization separately. A blocked tracker transition does not undo
publication or stop independent follow-up. If the skill is missing, retain the
event and report the gap without guessing a tracker state.

Unless the user asked for the PR without follow-up (**create-only**), continue with
`pr-followup` in **Drive** before returning. Pass URL, exact head/base, draft state, validation, pending work and,
where relevant, ticket relation, transition result and merge-delivery owner or
uncovered event. It owns feedback/CI repair, readiness and post-ready observation
under this request. Pass **keep-draft** only for an explicit user instruction to
retain draft state. A current/default draft or metadata-only recovery supplies no
such instruction; otherwise leave readiness to Drive.
Return to an already authorized loop instead of nesting another.

If `pr-followup` is unavailable, report verified publication and the continuation
blocker. A creation summary alone does not finish this phase.
