---
name: observability
description: Design, add, or review the telemetry, health status, and alerts that make running systems diagnosable in operation.
---

# Observability

Make the affected behavior understandable from signals available to a person or
agent arriving without the original context. Preserve the requested scope: design
and review produce recommendations; authorized implementation adds and verifies
the instrumentation. Work with the project's existing language and telemetry tools.

## Establish the diagnostic questions

Read the affected operations, entry points, asynchronous boundaries, failure paths,
and existing logs, metrics, traces, status surfaces and alerts. Identify who uses
the signals, where they can read them, and the relevant access, retention and cost
constraints. Reuse useful coverage before adding another producer or backend.

Choose concrete questions from the task and plausible failure modes: which run
failed, why a branch was taken, whether work is progressing, how often a dependency
fails, or where time is spent. Map each question to the smallest useful signal and
an observation that would answer it. Include success or recovery when needed to
distinguish failure from expected operation. A simple change need not acquire every
signal type, a dashboard, an alert or a new service.

`debug` owns investigating an observed failure; this skill owns durable diagnostic
coverage. `error-handling` owns caller-visible errors, retries and recovery policy.
An instrumentation change preserves results, exceptions, cancellation, effects and
retry ownership unless a behavior change is also authorized. During authorized
instrumentation, record a caught failure that would otherwise be silent with safe
classification and operation identity. Preserve what the caller receives; route
changes to that contract to `error-handling`.

## Instrument the deciding boundaries

Use established event names, levels, units and semantic conventions. Record
meaningful outcomes and decisions in structured fields, including the safe values
or classifications that explain them. Function entry/exit chatter rarely answers
an operational question. Give duplicate reports of one failure a clear owner rather than paging
at every layer.

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
untrusted, bounded input and use the existing propagation format.

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

## Verify the signals at their destination

For design or review, inspect available evidence and state which checks remain
unrun. When execution is authorized, exercise the affected success and representative
failure paths in an isolated environment. Confirm that the intended trigger occurred, then
read the resulting events, metric series, traces or status at the consumer. Check
correlation across relevant entry points and boundaries, safe fields, expected
counts and units, and any new state lifecycle. A configured exporter or successful
test command alone does not prove that a signal arrived. Answer each diagnostic
question from the observed signals as a reader without the original context would.
If answering requires inspecting the implementation or rerunning the operation,
record the missing diagnostic evidence as a blind spot.

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

Report the questions covered, changes or findings, where and how to inspect each
signal, observed checks and remaining blind spots. Keep implementation, tested
delivery and production operation distinct. Return to the active caller for
remaining work; `ci-cd-automation` owns rollout gates and deployment recovery.
Publication or ongoing monitoring follows the user's existing scope.

For a requested check or update of this skill's sources, read
[references/upstream-updates.md](references/upstream-updates.md).
