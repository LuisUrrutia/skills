# Model pair

Read this before requesting either review of the pair that
[the entrypoint](../SKILL.md#get-both-model-perspectives) requires. The entrypoint
decides when the pair runs, who runs it and when it is complete.

## Resolve each profile

Resolve each profile through its available runner, using its current catalog,
configuration or authoritative documentation. Use the newest available version in
the named family unless the user names one. Set the reasoning effort to xhigh
explicitly, and keep the actual provider, model, effort and run evidence for the
report.

## Brief the reviewers

Freeze the candidate before each round and cite what was reviewed. A committed
candidate is cited by commit and tree hash (`git rev-parse <commit>^{tree}`): a
rebase or squash merge can move or drop the commit, while the tree hash still
identifies the content. Commit only when the request or repository rules
authorize it; otherwise freeze a copy of the candidate and its diff outside the
working tree, cited by file hashes.

Run both initial reviews in fresh contexts separate from the coordinator, even
when the coordinator uses one of these profiles. Give both the same brief, scoped
to the request: the user's request, the complete target, the relevant context,
and the frozen candidate with its diff when one exists. For a skill change, also
ask for the checks in [Review a skill change](skill-changes.md#review-a-skill-change).
Ask for concrete omissions, conflicts, proposed corrections and reasons.

Keep each round's inputs identical and private until both results are in:
neither reviewer sees the other's findings or the coordinator's dispositions or
preferred verdict. Point reviewers at the frozen candidate rather than a working
tree you keep editing, and write notes or dispositions nowhere they read.

State in every brief that this is a bounded read-only consultation: the reviewer
edits nothing and starts no further pair of reviews. The coordinator owns editing
within the requested scope.

## Handle failures

A rate or usage limit skips that profile for the rest of the task: send no retry
and do not wait for the limit to reset. Continue with the other profile's
completed review and report the skip; the skip is neither a blocker nor a reason
to call the result provisional. A round in which no profile completes, including
one where both are skipped, leaves the result provisional with the exact errors
reported.

Retry any other transient failure once. A profile that still fails, or fails for
another reason such as authentication, is not skipped: report the exact blocker
and keep the result provisional. Continue independent work, and substitute a model
or effort only on the user's direction.

A review still running has not failed. A status check that errs or is declined
does not make its result missing: wait for the result or retrieve it another way.

## Reconcile the findings

Reconcile a round only after reading both results in full, or after the missing
profile is skipped or blocked as above. Reconcile each material finding against
the user's intent, the controlling instructions and the evidence. Apply supported
corrections within the requested scope and resolve each disagreement with an
explicit reason; agreement alone does not establish correctness, and unanimity is
not required. A material choice that evidence cannot settle goes to the user under
the entrypoint's clarification rule.

A finding is material when it changes what the instructions make an agent do, or
shows them wrong, unsafe or contradictory. Apply or decline the rest with a reason,
without another round.

Reconsult only when your edits change the reviewed meaning, and only on the
affected points: consult both profiles, except any skipped for a rate or usage
limit, and give each the original brief, the prior findings, your dispositions
and any open objection. An edit that keeps the reviewed meaning needs no new
round, and a round that returns no material finding ends the loop.

Keep a record of each round for the report: each profile's actual provider,
model and effort, its run, rate-limit skip or blocker, the reviewed commit and
tree, and how each material finding was adopted or rejected, with any unresolved
limitation.
