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

Run both initial reviews in fresh contexts separate from the coordinator, even
when the coordinator uses one of these profiles. Give both the same brief, scoped
to the request: the user's request, the complete target, the relevant context,
and the frozen candidate when one exists. Withhold the coordinator's preferred
verdict and the other reviewer's conclusions until both initial responses
arrive. Ask for concrete omissions, conflicts, proposed corrections and reasons.

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

## Reconcile the findings

Reconcile each material finding against the user's intent, the controlling
instructions and the evidence. Apply supported corrections within the requested
scope and resolve each disagreement with an explicit reason; agreement alone does
not establish correctness, and unanimity is not required. A material choice that
evidence cannot settle goes to the user under the entrypoint's clarification
rule.

When later edits change the reviewed meaning, reconsult both profiles, except any
skipped for a rate or usage limit, on the affected points. Give each the original
brief, the prior findings, your dispositions and any open objection. Keep a short
record of adopted and rejected findings and any unresolved limitation for the
report.
