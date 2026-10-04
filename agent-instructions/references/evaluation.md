# Evaluation

Read this when changing instruction behavior, creating or combining skills,
changing routing, incorporating upstream changes, or correcting observed failures.

## Define the checks

Derive cases and expected outcomes from the contract before tuning. Cover ordinary
work, ambiguity, and relevant boundaries. Exercise techniques on changed inputs,
retrieve and apply reference information, and test both sides of conditional
rules. Routers need requests for different specialists and requests selecting none.

Observe artifacts, actions and resulting state. When a requirement competes with
a deadline, prior effort or pressure to skip it, use a realistic task that requires
the executor to act. Preserve authorization; use isolated fixtures or fakes for
external effects unless the evaluation is authorized against the real service.
Rule recitation cannot establish compliance.

Keep expectations with the grader and reserve unseen cases. A reserved failure
used to revise instructions becomes a regression case; use a new unseen case
before making another generalization claim. Read [../evals/cases.json](../evals/cases.json)
only when evaluating `agent-instructions` itself. Other targets need cases from
their own contracts.

For persistent instructions, test effective scope: global, repository and nested
rules can reach different work. Include imports or adapters that affect loading.
A focused edit need not acquire a permanent evaluation suite.

## Compare the right instructions

The required Codex and Claude consultations assess instructions; they do not
replace behavioral checks. Compare new instructions with the same task without
them, and revisions with the previous snapshot. Keep model, effort, tools,
fixtures, authorization and output format equal within each pair. Use independent
clean contexts with no access to another arm's instructions or answers.

For host-run claims, verify from durable run evidence which revision was actually
loaded; a requested path alone does not prove the runner used it. An unidentified
revision cannot support attribution.

To assess whether a rule earns its place, a no-instruction or rule-removal trial
can supplement the previous-version comparison. Exercise its protected
behavior, exceptions and any stated team preference; unrelated passes cannot
justify deletion. Keep editorial recommendations distinct from measured gains.

When independent executors are available and authorized, give them the request,
instructions and raw artifacts, withholding expectations, suspected defects and
proposed fixes. Otherwise use an available runner or report missing behavioral evidence.
Never substitute the author's simulated answer for an execution. Follow repository
scratch rules; add a permanent helper only for a recurring evaluation need.

## Judge the evidence

| Claim | Required evidence |
| --- | --- |
| Valid structure | Resolved pointers/imports; relevant metadata and host checks |
| Correct selection | Positive and near-miss requests with observed host selection |
| Useful behavior | Output artifacts, actions and required postconditions |
| Safe authority | Side effects remain within supplied authorization |
| Improvement | Matched baseline results, including regressions and failures |

Retain the case, revision, model, effort, supplied resources, output, action trace,
verdict and its evidence. Record costs only when measured. A read or dispatch can
prove phase entry without proving completion; check its required result. Use
omitted checks and stated justifications to distinguish missed, misunderstood and
bypassed instructions. Treat explanations as hypotheses, not established causes.

Use objective checks for formats and postconditions, and read substantive output
for scope, decisions, unnecessary questions and unjustified claims. Keywords and
confident self-reports are insufficient. A model choosing a description is a
selection probe, not observed host invocation; tool-free exercises cannot prove
tool execution, installation or network behavior. Mark unobservable outcomes as
not tested. If both versions pass, report that result without claiming improvement.

## Iterate proportionately

Fix failures at the responsible instruction or reference. Rerun the affected case
and a nearby regression case; broaden checks when routing, authority or termination
changes.

When a claim needs repeated trials, such as a nondeterministic failure, a model
migration or a performance comparison, define the metric, meaningful effect, run
budget and stopping rule before tuning. Use matched trials and report their
variation. Add identical-version controls when unexplained variation or runner
integrity needs investigation, and account for the controls' variation when
interpreting candidate differences. Interleave arms when changing conditions
could bias a comparison. A short streak or observed range cannot by itself
establish a gain.

Retain failed attempts and exclusions. Classify infrastructure failures from
cause evidence; a short answer, early stop or error exit alone does not justify
discarding a behavioral failure. State which paths were exercised and which
remain unmeasured. A small passing sample supports only its tested cases.

Stop when the contract is met and material failures are accounted for, reporting
remaining limits instead of adding speculative rules.
