---
name: performance-optimization
description: Improve latency, throughput, resource use, or cost of a known operation when the winning change is unknown. Observed regressions start with debug.
---

# Performance optimization

Improve an operation that matters to the user through measured changes whose
benefit justifies their complexity. A valid outcome is a verified improvement,
evidence that the tried changes are not worthwhile, or the specific missing
evidence that prevents a decision. Do not promise an improvement before measuring.

Use this skill when the goal is known but the winning change is not. Preserve the
active task's scope: an audit produces findings; authorized implementation can
change code. Local experiments do not authorize production load, deployments,
new spending, publication or recurring monitoring.

## Define the operation and decision

Identify the user journey, request, job or repeated operation, its important
workloads, and the metric that captures the desired benefit. Specify units and
where the operation starts and finishes. Cost and throughput must count useful
completed work; a faster response that merely defers required work may move the
cost elsewhere. Keep relevant tail latency, memory, errors, freshness or cost as
guardrails so a primary-metric gain cannot hide an unacceptable regression.

Establish the required outputs and effects, including ordering, consistency,
tenant or authorization boundaries, cancellation and failure behavior where they
matter. Read existing correctness checks, performance budgets and tooling. Derive
the worthwhile improvement from the task and project, not a universal threshold.
When no target is given, state a reasonable decision criterion before tuning;
ask only when a missing choice would materially change the operation or tradeoff.

Bound the search by the available time, variants, compute, spend or data impact.
Use a proportionate local budget when none is supplied and state it. Stop when
the goal is met, the budget is exhausted, or the next experiment cannot resolve
a useful decision within it. A plateau does not authorize extending the budget.

## Establish evidence and find the limiting work

Reuse a suitable existing harness. If none exists and execution is authorized,
build the smallest reproducible local measurement and correctness check within the
task's budget, using its scratch location. Report a specific evidence blocker if
that cannot be done; a search harness need not become a permanent framework.
Capture the baseline state and workload, and check that the measurement completes
the required work correctly before optimizing it. A broken harness needs repair;
an observed baseline correctness failure goes to `debug` under the active scope.
Neither supports a performance win while unresolved.
Preserve fixed inputs, evaluation rules and original evidence
while exploring; correcting a misleading benchmark requires remeasuring every
candidate used in the decision, not changing the test to favor one variant.

Use `verify` by registered name to assess the baseline comparison method and the
evidence for retained claims, including the final combined result. Supply the
operation, target and guardrails, revisions, workload, harness, conditions, run
budget, execution authority and actual observations. It owns whether the comparison
supports the claim; this skill owns choosing and implementing the next experiment
and the keep/revert decision. Resume the authorized optimization after its verdict.
If `verify` is unavailable, inspect and retain the available evidence directly:
check completed correct work, comparable conditions and variation, and label any
unresolved claim inconclusive. Do not fabricate a skill invocation or measured gain.

Locate expensive or repeated work using existing traces, profiles, query plans,
allocation data or a smaller diagnostic measurement. Choose the cheapest evidence
that can change what to try or skip. Static patterns suggest hypotheses; they do
not establish a bottleneck or an achieved speedup. Keep diagnostic instrumentation
separate from scored measurements when its overhead changes the comparison.

Rank opportunities by the operation's measured limiting work, likely user benefit,
confidence, implementation cost and risk. Prefer removing unnecessary work or
avoiding repetition before adding scheduling or concurrency. A cheap local change
can be worthwhile; a large microbenchmark gain in an insignificant part of the
operation may not be. Use domain guidance for relevant mechanisms instead of
applying every frontend, database or infrastructure recipe.

## Run bounded experiments

State a hypothesis connecting the observed cost, proposed change and expected
effect. Change one coherent cause at a time so the result can be interpreted.
Use `prototype` when a disposable experiment can settle an uncertain mechanism
before application edits; give it the question, workload, constraints and budget,
then continue from its result under the existing authorization.

Keep the original baseline and best accepted variant reproducible through the
project's revision, patch or copy mechanism, including any uncommitted changes.
Check each
candidate's correctness before comparing performance under the agreed conditions.
Include costs introduced by the change, such as index construction, cache fills,
serialization, invalidation and work moved off the timed path. Choose cold, warm,
concurrent or sustained workloads when they matter to the actual operation.

For reuse or caching, preserve identity, authorization, freshness and bounded
resource use. For batching, deferred work or concurrency, preserve ordering,
completion, failure and cancellation semantics and account for contention or
backpressure. An optimization that drops work or weakens these requirements is
invalid even if its primary metric improves. Changing a required tradeoff needs
the user's decision unless the active task already authorizes it.

Keep a concise record with the hypothesis, revision plus any uncommitted diff or
content snapshot, workload and command,
correctness and guardrail results, measurements, and keep/revert reason for each
tried variant. Use existing project artifacts; a small task can keep this in its
result rather than introducing a permanent framework. Retain failed and neutral
attempts so later decisions do not repeat or conceal them.

## Keep only justified changes

Use the evidence assessment to decide, not the best single timing or effort
already spent. A retained performance claim needs a meaningful improvement beyond
normal variation, required behavior intact, acceptable guardrails and a benefit
worth the added complexity. A plausible causal explanation guides the next test;
it does not replace measurement. Compare with the best accepted variant as well
as the original when those answer different decisions.

Revert only this task's rejected performance edits, preserving unrelated work and
independently justified correctness or simplification changes within the approved
scope. A neutral simplification can remain for its own benefit, but is not a
performance win. If evidence is inconclusive, stop or choose a further discriminating
measurement within the remaining budget; do not retain complexity on speculation.

Recheck the final integrated change against the original operation and its
guardrails. Individually useful changes can interact; their isolated gains do not
add up to a measured combined result. Use project checks and `verify` for affected
behavior. Within the active scope, add or update a regression benchmark or budget
only when its workload and noise make it maintainable; avoid a flaky timing test.
Pipeline gates remain with `ci-cd-automation`.

Report the operation, workload, decision criterion and search budget, original
and final measured states, commands,
correctness, measured benefit and variation, resource tradeoffs, rejected attempts
and stopping reason. Separate local measurements from untested production effects.
When nothing qualifies, say that none of the tried variants earned retention;
do not claim that no further improvement is possible. Return to the active caller
for any remaining authorized implementation or delivery work.

## Keep neighboring responsibilities clear

- `debug` owns an observed regression or unexplained failure. Start there when
  restoring previously working behavior is the task; use this skill if a broader
  optimization search remains after diagnosis.
- `verify` owns assessing an existing performance claim. A request only to judge
  supplied measurements does not start a new tuning campaign.
- `observability` owns durable diagnostic signals when a missing measurement
  needs instrumentation that will outlive the experiment.
- `ci-cd-automation` owns pipeline speed, cost and delivery gates. A request to
  make the pipeline faster starts there; this skill can support a measured
  optimization of an operation within it.
- Existing domain skills own their mechanisms; their presence does not make
  every optimization task a framework, database or CI migration.

Resolve available owners through the host's skill catalog. Their absence does not
grant new authority or justify pretending their work ran; report the affected
limitation and continue independent work that remains possible.

For requested source maintenance, read
[references/upstream-updates.md](references/upstream-updates.md). For evaluation
of this skill, use [evals/cases.json](evals/cases.json), keeping expectations out
of executor inputs.
