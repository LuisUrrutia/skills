---
name: debug
description: Use when diagnosing or fixing an observed software bug or performance regression.
---

# Debug

Explain an observed failure with evidence and, when requested, correct its cause.
Start with the user's report and the available project context; no work-mode or
earlier phase is required.

Infer the scope from the active request. Diagnosis alone leaves project source,
tests, configuration, and remote state unchanged. Use read-only inspection,
existing safe checks, and isolated experiments only within that scope. A request
to fix already authorizes normal investigation, regression tests, and repair.
Ask only when an unresolved choice materially changes the intended behavior or
requires authority the task does not provide.

## Establish the failure

Identify the observed behavior, the expected behavior and its source, the affected
path, and relevant input, version, or environment. Read the nearby implementation,
tests, and applicable project guidance. Treat the reporter's suspected cause as
a hypothesis; neither that guess nor the current implementation defines correctness.

Find the cheapest useful observation that reaches the reported failure: an existing
test, CLI invocation, HTTP request, browser interaction, trace replay, or isolated
harness. Match the user's symptom, not merely an exit code. Distinguish a product
failure from missing setup or a broken test. Run it and retain the command or
steps, relevant output, and conditions; redact secrets from captured evidence.

Reduce inputs or steps while retaining the same failure. Stop reducing when the
remaining scenario is useful for distinguishing causes; exhaustive minimization
is not a prerequisite. Keep the original scenario for final verification.

When reproduction is unavailable, the failure is intermittent or slow, or the
uncertainty crosses code, history, or consumer boundaries, read
[references/investigation.md](references/investigation.md). A missing reproduction
allows bounded investigation; it does not establish a verified cause or fix.

## Test the explanation

Trace the failing path and identify plausible causes supported by the evidence.
For each unresolved cause, state a prediction and choose a probe that can
distinguish it from alternatives. A simple failure need not acquire a fixed number
of hypotheses. Change one relevant condition at a time and use the result to
confirm, reject, or narrow the explanation.

Prefer existing inspection tools or targeted instrumentation at the deciding
boundary. Track temporary changes for cleanup. An unchanged retry adds no causal
evidence unless it measures intermittent behavior under stated conditions.
If a probe fails for an unrelated reason, repair the observation before treating
it as evidence about the bug.

Explain how the cause produces the original symptom, with the supporting
observation or code path and remaining uncertainty. For diagnosis-only work, this
is the result; do not continue into repair.

## Correct and verify when authorized

When a useful local test boundary exists, add a focused regression test before
changing production code and observe it fail for the reported reason. Derive
expected results from the contract or an independently worked example. Exercise
the real behavior through its public boundary, including interacting callers or
state transitions when those cause the bug.

If a permanent test would require disproportionate infrastructure or would miss
the actual failure, use the closest meaningful executable check and explain the
coverage gap. A user's explicit testing request and project requirements still
apply; this fallback does not silently waive them.

Fix the mechanism with the smallest coherent change that preserves nearby
contracts. Keep valid input checks, recovery behavior, and boundary guards; remove
one only when evidence shows it is wrong or redundant. Inspect related instances
when they share the mechanism, and change only those supported by evidence within
the authorized scope. Separate emergency mitigation from a root-cause correction.

Run the regression check again, then the original scenario and relevant adjacent
behavior. Complete the project's required checks. Remove disposable instrumentation
and inspect the final diff for accidental changes. A passing nearby test does not
prove an unexercised production symptom is fixed.

## Finish with evidence

Report the cause and confidence, changes if any, exact checks and outcomes,
remaining gaps, and the next observation needed for any unresolved hypothesis.
Distinguish a verified repair, a supported diagnosis, and work blocked on specific
evidence. Stop a stalled loop when the next useful probe needs inaccessible input
or new authority; report what is missing rather than repeating the same attempt.

This skill owns diagnosis and authorized repair. Repository instructions and the
active caller own commits, worktrees, PRs, and further delivery. A wider authorized
task can continue after this result. Load available domain guidance when the
investigation or fix reaches that domain; debug does not install dependencies or
start a general review or PR-monitoring workflow.

For a requested check or update of this skill's sources, read
[references/upstream-updates.md](references/upstream-updates.md).
