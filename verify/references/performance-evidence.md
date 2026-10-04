# Performance evidence

Read this when checking a measured performance claim or a comparison used to
choose an implementation or configuration. Apply the checks relevant to that
claim. The caller owns the experiment or repair; the project harness owns how
measurements run. This reference owns what the evidence can establish.
A supplied harness, benchmark, or results packet can be assessed without a
project recipe. Application execution still follows the local recipe when one
is available; report missing application coverage separately.

## Define what the number must prove

State the operation, metric and unit, workload, compared revisions or inputs,
and the decision the result supports. Distinguish a requested rough observation,
a comparison of configurations as deployed, and choosing between alternatives.
For a comparison, define a meaningful difference, run budget and stopping rule
before running; for supplied results, check whether they were defined. Reuse the
project's benchmark and statistical conventions where they fit; do not invent a
universal repetition count or acceptance threshold.

Inspect what the harness times, counts, waits for and excludes. Confirm required
work completes inside the measurement boundary: asynchronous work is awaited,
lazy results are consumed, and the intended path actually runs. Check outputs or
independent side effects against the contract. Count successful work, errors,
timeouts and retries separately; faster rejection or skipped work is not a
successful speedup. Treat caching according to the claimed workload, not as an
automatic defect. Missing work or correctness evidence leaves the claim unproved.

## Make the comparison meaningful

Record relevant build mode, runtime, data, workload, concurrency, warm-up, cache
state and environment. Match conditions that the claim holds constant and name
intentional differences. A deployed-configuration comparison can establish its
observed difference without establishing which implementation is intrinsically
better. For an adoption decision, use representative supported configurations.
Resolve material configuration differences that could reverse the choice, or
justify them from the user's actual constraints. Merely identifying a handicap
does not settle its effect on the decision. Without that evidence or authority
to obtain it, leave the adoption choice unresolved. Verification does not
authorize tuning, installing tools, or applying production load.

Use repetitions appropriate to the decision and report sample counts and
variation. Interleave comparable runs when changing conditions could bias one
side. Retain failures and exclusions with reasons; do not select favorable runs
or infer statistical significance from a short streak or overlapping ranges.
A requested single-run estimate still needs completed-work and correctness
checks, and must be labeled as one observation. It cannot select a winner or
establish a durable regression.

## Check relevance and explanation

Use a separate diagnostic run for a profiler or intrusive tracing, then collect
scored timings without that instrumentation. Observe the load generator and
measurement overhead when they could limit the result. A saturated driver cannot
establish the target's maximum capacity. Keep a measured difference separate
from its cause; a claimed bottleneck needs runtime evidence linked to the path,
while an honest bounded observation may leave the mechanism unresolved.

Check the result against known workload, resource and time budgets. An apparent
gain beyond what the changed part or available resources can explain calls for
checking units, counters, boundaries, skipped work or changed conditions. For a
user-facing performance claim, measure the relevant end-to-end path. A micro
benchmark can establish a local result, but not an unmeasured application gain;
retain that distinction when broader execution is unavailable.

## Report and return

State whether the specific claim is supported, contradicted or inconclusive,
with measurements, units, counts, variation, correctness evidence and relevant
conditions. Link raw results using the project's existing evidence format.
Distinguish no resolved difference in this experiment from equivalence, and a
measured effect from an established cause. Name the next deciding observation
when evidence is missing; preserve valid narrower results.

Return the evidence verdict to the caller. When `debug` or `prototype` supplied
the claim, return to that active investigation or experiment without starting
another one. Any broader optimization follows its authorized task. Do not start
a tuning loop or turn every functional check into a benchmark.
