---
name: observability
description: Assess and build project observability, from initial setup to instrumentation added during feature work.
---

# Observability

Equip the project with useful logs, metrics, traces and health signals. Analyze its
architecture and workflows, identify missing coverage, and build the observability
needed to understand its operation. Existing telemetry is input for deciding what
to reuse and extend. Work can start before any incident or monitoring stack exists.

`debug` owns investigating an observed failure using available evidence and targeted
probes. This skill owns lasting instrumentation and its collection, storage and
inspection setup. `error-handling` owns caller-visible errors, retries and recovery
policy. Preserve those contracts while adding observability.

## Choose the scope of the addition

Take the scope from the active request; the mode does not expand its authority.

- **Project assessment:** examine the relevant services, workflows or proposed
  telemetry changes, identify coverage gaps, and propose concrete additions in
  priority order. An assessment, review or design request produces recommendations
  without changing the project.
- **Initial setup or project improvement:** choose and implement the instrumentation
  and collection path needed for the requested coverage. If the project has none,
  establish a usable foundation instead of waiting for existing signals to inspect.
- **Feature work:** inspect the operations and boundaries the feature adds or
  changes. Add useful instrumentation as part of authorized implementation and
  extend the existing conventions. Keep unrelated project-wide improvements as
  separate recommendations; a small change need not acquire an entire stack.

## Find and prioritize instrumentation points

Read the project's architecture, runtime and deployment configuration, critical
workflows and existing telemetry conventions. Follow the relevant path through
entry points, queues, workers, storage and external dependencies. Locate meaningful
outcomes, decisions, delays and failures whose behavior is currently invisible.

For each proposed addition, identify the operation or boundary, the information
missing there, the signal to add and where someone will inspect it. Prioritize by
user impact, operational uncertainty and cost. Typical targets include failed or
slow requests, dependency calls, queue age, stalled jobs and incomplete workflows.
Include successful outcomes and recovery so failures have a meaningful denominator
or comparison. Define what an operator should be able to learn from each addition;
an observed incident is not required to justify useful coverage.

## Establish or extend the collection path

Reuse suitable project libraries, backends and deployment facilities. When they
are absent or insufficient, select the smallest setup that fits the language,
runtime, operational needs and budget. Configure the necessary producers,
collection/export, storage and a usable way to inspect the data. That can be a
documented log query, metrics endpoint or existing dashboard; choose traces,
dashboards and alerts where they serve the requested coverage.

Include environment-specific configuration and documented startup or inspection
steps so the setup is usable beyond the current session. Identify who can access
the data and its retention and operating costs. Keep exporter and backend credentials
in the project's secret mechanism, out of committed configuration, commands and
output. Resolve routine local choices within the task; a material backend, billing,
data-residency or external-service
decision needs the user's constraints or decision. Continue independent local
work and state any unavailable integration. A local collector proves only the
delivery path exercised, not production deployment.

## Instrument the deciding boundaries

Use or establish consistent event names, levels, units and semantic conventions.
Record meaningful outcomes and decisions in structured fields, including safe values
or classifications that explain them. Function entry/exit chatter rarely answers
an operational question. Give duplicate reports of one failure a clear owner.
Record otherwise silent failed operations with safe classification and operation
identity. Preserve results, exceptions, cancellation, effects and retry ownership
unless changing that behavior is also part of the task.

| Signal | Use it to answer | Preserve |
| --- | --- | --- |
| Structured log or event | What happened in this particular operation, and why? | Stable event name, time, operation/run identity, outcome and useful decision context |
| Metric | How much, how often, how slow, or how saturated? | Defined units, counted population, time window and bounded dimensions; distinguish attempts from logical operations |
| Trace | Where did an operation spend time across components? | The existing trace context, meaningful spans and links across synchronous and asynchronous boundaries |
| Health or status surface | Is a process alive, ready or making progress? | The specific state being measured, its scope and freshness; absence of errors alone is not evidence of health |

Create or validate correlation context at the trusted entry point and propagate it
through the affected calls, queues and workers. When several entry points share a
sink, record which entry point started the work alongside its run identity; a
correlation ID alone cannot establish that. Keep retries and child operations
associated without conflating separate executions. Treat incoming identifiers as
untrusted, bounded input. Reuse the project's propagation format; when none exists,
choose a standard supported by the tooling.

For metrics, use a bounded vocabulary such as operation, route template or outcome
class. Request IDs, user IDs, raw URLs and arbitrary error text do not belong in
metric dimensions. Histograms or an existing distribution measure support tail
latency questions; an average alone does not. Confirm what the instrument counts,
including retries, partial results and zero traffic, before deriving a rate.

Reuse existing tracing and auto-instrumentation; add manual spans where they answer
a missing question. Choose sampling and retention against diagnostic needs and
cost. Sampled traces cannot establish complete event counts or that an unrecorded
failure never happened. OpenTelemetry is an option, not a required migration.

## Keep diagnostic data safe and affordable

Allowlist fields before emission to logs, spans, metrics, persisted failures and
status responses. Raw exception messages, causes, stacks, URLs and payloads can
contain secrets or personal data even when the public error is generic. Preserve
useful classification and safe identifiers without copying unrestricted objects.
Apply the project's access and retention policy to every new diagnostic surface.

Bound payload size, label cardinality, event volume and buffer growth. Avoid
expensive serialization, blocking writes or per-iteration logging on hot paths;
aggregate, sample or use existing buffering when appropriate. Account for exporter
failure and backpressure so added telemetry does not unexpectedly fail or stall
the operation. Preserve an established mandatory audit contract, including its
failure policy, rather than silently making it best effort.

## Preserve evidence for unattended work

For background jobs, watchers or long-running processes, identify what remains
available after a crash or restart. Use the existing durable sink or state store;
add a failure record only where the diagnostic question needs one. Include safe
operation identity, phase, time, attempt and failure classification.

Scope state to the run or work item that produced it. Use the storage mechanism's
atomicity and concurrency controls so concurrent writers or a partial write do
not destroy evidence. Distinguish historical failure from current state: define
freshness and how success, recovery, restart or expiration updates it. An unrelated
successful job must not erase another job's failure.

Keep status reads cheap and free of business side effects. Distinguish liveness,
readiness and progress using the project's existing contract; a dependency outage
does not automatically justify declaring the process dead and restarting it.
Expose only the detail the intended reader is authorized to see.

## Add actionable alerts when needed

Use existing alert ownership, severity and delivery conventions. Choose conditions
that justify an action, usually user-visible errors, latency or delayed work; a
resource signal is useful when it predicts a concrete operational consequence.
Derive thresholds, duration and recovery conditions from service objectives,
observed behavior or an explicit project requirement. Identify the responder and
link the first useful query, mitigation or runbook. State how no traffic, stale
data and missing telemetry differ from recovery. Do not invent universal numbers
or delete existing alerts merely because they use another convention.
If ownership or the information needed to choose an actionable condition is
missing, propose the alert and the observations or decisions needed before enabling it.

## Verify the signals at their destination

For assessment, review or design, tie recommendations to the inspected project and
state how their result would be verified. During implementation, exercise the affected
success and representative failure paths in an isolated environment. Confirm that
the intended trigger occurred, then read the resulting events, metric series,
traces or status at the consumer. Check correlation across relevant entry points
and boundaries, safe fields, expected counts and units, and any new state lifecycle.
A configured exporter or successful
test command alone does not prove that a signal arrived. Confirm from the emitted
data alone that a reader without the original context learns what each addition
promised. If this requires reading the implementation or rerunning the operation
with extra instrumentation, record a coverage gap.

Use test collectors and notification sinks for failure injection and alert tests.
Production disruption, threshold changes or messages to real recipients need
authority from the active task; this skill grants none. Test delivery only through
the stages actually available and report unavailable destinations separately.
Missing or sampled-away data is unknown, not a zero error rate or verified health.

Verify that instrumentation preserves functional outcomes and relevant failure
behavior; exercise a telemetry outage when its new failure path can affect them.
Measure overhead under representative conditions when the changed path or budget
makes it material. Use available `verify` and project checks for execution evidence;
direct checks remain useful when that skill is unavailable. Remove only temporary
probes and fault controls owned by the task, preserving useful diagnostic evidence.

Deliver the prioritized additions for an assessment, or the implemented code,
configuration and inspection instructions for implementation. Report the coverage
proposed or added, where to read the signals, observed checks and remaining gaps. Keep
implementation, tested delivery and production operation distinct. Return to the
active feature or project task; `ci-cd-automation` owns rollout gates and deployment
recovery. Publication or ongoing monitoring follows the user's existing scope.

For a requested check or update of this skill's sources, read
[references/upstream-updates.md](references/upstream-updates.md).
