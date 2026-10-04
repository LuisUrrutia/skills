---
name: analyze-change-effects
description: Use when tracing and testing what a change could break elsewhere.
---

# Analyze change effects

Find effects beyond the changed code and test the assumptions that would make
them safe. The result is a bounded account of breakage, cleared risks, and
unproven conditions, with evidence from the actual implementation.
Use this skill directly; no coordinator or upstream skill is required.

## Establish the change

Identify the requested change and its before/after behavior. For an existing
diff, establish the intended base and target rather than assuming the latest
commit or upstream contains the whole change. Read the surrounding implementation,
callers, configuration, and relevant contracts. Use history when it clarifies a
specific constraint; a complete historical investigation is not a prerequisite.

For a proposed change, state the behavior being considered and which details
remain undecided. Investigate current consumers and contracts without implementing
the proposal. A probe using a proposed value or format tests that scenario; it
does not establish the behavior of an implementation that does not yet exist.
Ask only when an unresolved choice would materially change the analysis.

## Follow effects beyond the diff

Trace how the changed behavior reaches a consumer or observable outcome. Symbol
searches find leads; read the actual path across calls, generated or serialized
data, persisted state, runtime configuration, and other processes or languages
when the change reaches those boundaries. Name what the recipient assumes and
how the change preserves or violates it.

Inspect the dependency version and local patches used by the project when its
semantics decide the outcome. Follow execution order, callbacks, task scheduling,
cleanup, shared state, or rollout versions when they affect the path. A compatible
type signature does not establish compatible timing or serialized behavior.

Identify the concrete assumptions each plausible risk depends on. Prioritize the
assumptions that decide the most consequential paths, while keeping independent
hazards separate. Proving one property clears only the risks that depend on it.
Avoid inventing callers, broad lists of hypothetical failures, or likelihood
percentages unsupported by evidence. Describe reachability and consequences.

Distinguish a path that exists in source from one known to be active in a deployed
configuration. A search with no matches establishes only that search's result;
it does not rule out dynamic dispatch, stored data, or external consumers. Mark
unavailable implementations and unknown deployment state as coverage limits.

## Test the deciding assumptions

For each material path, state a falsifiable claim and the smallest observation
that could refute it. Prefer an existing focused test or a disposable probe that
imports and exercises the actual code and resolved dependency. Observe the
failure path as well as a relevant normal case when needed to interpret the result.

A probe must check the behavior under question, not a reimplementation of it.
Use a fake only at a boundary outside the claim being tested and explain that
limit. For compatibility, exercise the relevant old/new producers and consumers
or data versions; a test of only the new producer does not test its old readers.
When timing matters, reach the lifecycle or scheduler boundary that decides it.

Record the command, input or scenario, observed output, and what that observation
supports. A setup failure is not a reproduction. A passing sample or aggregate
test suite supports only the paths and inputs it exercises; broader claims need
their own source trace or execution evidence. An assertion-free script that
exits successfully may not have checked the claimed property.

Keep product source, committed tests, dependency pins, configuration, and remote
state unchanged during investigation. Use permitted scratch storage for disposable
probes and generated output. Respect an explicit inspection-only request or an
execution restriction. Do not install, upgrade, repair, publish, or call a live
mutating service just to obtain proof. If execution or the real dependency is
unavailable, return the supported analysis, mark the affected claim unproven,
and name the smallest missing check. Do not quietly substitute another version.

Investigate directly. Independent exploration is optional when both the host and
task authorize it; reconcile any findings against source and execution evidence.
Agreement among agents is not proof and no model roster is required.

## Deliver the impact and evidence

Lead with the consequential effects and the scope examined. For each material
conclusion, connect the changed behavior, triggering condition, affected consumer,
and consequence to source locations and any observed check. Keep confirmed
breakage, risks cleared under stated conditions, and unproven paths distinct.
Distinguish source inspection, a traced unreachable path, a local execution, and
reproduction in the application rather than collapsing them into "verified".

Name the deciding assumptions, the evidence reached for each, and the remaining
test or integration prerequisite. Explain an unresolved risk's impact without
presenting it as an observed failure. Apply the same standard to alternative
dependency versions and suggested remedies: reproducing the current failure does
not verify an alternative. Leave untested alternatives conditional. Use a compact
table or causal path when it helps; respect the requested length and avoid a
general code-quality report.

Stop when the material paths have evidence or explicit limits and the next useful
check is clear. Do not turn an analysis request into repair or delivery. A caller
with a wider authorized task can use the result to choose its next action.

## Source maintenance

When asked to check or update this skill from its sources, read
[references/upstream-updates.md](references/upstream-updates.md). Ordinary impact
investigation does not fetch skill sources or require another skill.
