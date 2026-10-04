# Behavior and timing experiments

Use this when a small executable experiment can settle a question about an
algorithm, API behavior, integration, resource use, or timing. A performance repair
or bug investigation remains with its normal workflow; this branch supplies a
bounded experiment when that work needs one.

Specify the observable result and the conditions that could change the decision.
Build the smallest script or harness that exercises those conditions. Reuse the
project's runtime when its behavior matters. Use representative fixtures and
record any simplification that could invalidate the inference.

Check that compared approaches produce the required behavior before comparing
their cost. Include meaningful setup costs; isolate or report them when they are
amortized over repeated operations. For performance claims, use `verify` by
registered name to assess the harness and results. Pass the question, alternatives,
workload, harness and rerun command, measurement boundary, relevant conditions,
authority and raw results.
It owns the shared measurement criteria; this skill still builds the experiment
and returns the bounded recommendation. If unavailable, run independently useful
checks and state which conclusions remain unverified; do not claim it ran. With
or without that assessment, keep inputs, workload, environment, warm-up, cache
state, and measurement boundary comparable; report repetitions, units, and a
range rather than one favorable sample.

Run the harness, inspect actual output, and preserve the parameters and observations
needed to reproduce the result. Assertions may check equivalence or an invariant;
they cannot turn a simulated service into evidence about a real one. Avoid new
dependencies unless the question requires them.

Before recommending a decision rule, check it against every observed condition.
Narrow or reject a rule contradicted by a result; keep the recommendation within
the measured conditions. If results are mixed, noisy, or dominated by the harness,
report that outcome and the next observation needed. Do not fabricate a winner or
expand into an open-ended tuning project to avoid an inconclusive result.
