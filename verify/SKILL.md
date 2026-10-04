---
name: verify
description: Use when verifying a software change or completion claim against current execution evidence.
---

# Verify

Establish what is being claimed, run the checks that can support it, and report
the observed result. Select the project's `verify-<app>` skill for application
behavior. That local skill owns launch, doctor, driving, evidence, and cleanup;
this entrypoint owns scope, selection, and whether the evidence supports the claim.

## Match scope to the claim

Identify the project root, target application, current change or input snapshot,
requirements, and applicable project checks. Distinguish the original symptom,
acceptance criteria, compilation/build, test coverage, and user-visible behavior.
If intended behavior or required scope remains unclear after reading the request
and project, ask before choosing what counts as passing.

For a change, select the affected mapped features and entry points, relevant
regressions and adjacent behavior, plus the project's required build, test,
lint, type, or smoke checks. A full-application request covers the full map.
Do not replace required coverage with a convenient passing sample or introduce
an arbitrary test quota. Keep expected results anchored in requirements and
contracts rather than deriving them solely from the implementation under test.
For browser behavior, read
[references/browser-evidence.md](references/browser-evidence.md) before choosing
routes, conditions, and probes. Other surfaces keep their applicable harness.
For latency, throughput, resource-use, speedup, or performance-regression claims, read
[references/performance-evidence.md](references/performance-evidence.md) before
selecting measurements or interpreting supplied results. Ordinary functional
verification does not require a benchmark.

Resolve the matching project-local `verify-<app>` by registered name from the
installed catalog or named skills supplied by the caller. Load and apply its
instructions using the host's supported mechanism. A supplied recipe can guide
execution without being globally installed; describe that as supplied context,
not proof of host installation, implicit selection, or a separate invocation.
Several targets require selection from the task or a question. Pass the project,
change/snapshot, features, acceptance criteria, execution authority, and evidence
destination. Read the map before driving. Domain guidance is conditional on the
task; it does not replace the local recipe.

If a local skill is unavailable, run independently useful existing checks within
scope and report exactly what they establish and which application paths remain
uncovered. Missing packaging alone does not invalidate observed behavior. Use
`verification-authoring` when creation or maintenance is authorized;
do not silently invent a persistent recipe or describe a supplied file as a
successfully invoked skill. A required missing dependency blocks that phase.

## Run against the actual state

Use the local launch and doctor contract to establish the application/build,
instance ownership, data/profile, and relevant access before driving. Run checks
against the final relevant change. A successful old log or another agent's
summary does not establish the current result. Associate evidence with its
revision or input identity, command/steps, environment, and outputs.

Read the actual command output and exit status, including failures, skips,
timeouts, and missing prerequisites. Exit 0 with no relevant assertions or no
discovered tests does not prove the requested behavior. Use the real build when
the project requires bundling; lint or typechecking is not that build. For a
reported bug, exercise its original reproduction. Do not claim a red/green cycle
from a test that only ran after the fix.

Drive the real user entry points, observe the action and resulting state, and
check relevant side effects independently. Internal setters, test-only endpoints,
or mocks of the behavior being claimed cannot substitute for that path. Respect
the local skill's safe fixtures and check what a dry-run actually does.

Doctor again after failures or unexpected behavior, and reset or relaunch when
process health cannot show that application state is usable. Do not reuse a
possibly corrupted instance merely to collect a green result. Clean up owned
resources on every failed attempt and after the final run. Keep proof separate
from disposable state and check that it survives teardown.

If a relevant edit, changed build, data reset, or environment change invalidates
evidence, rerun the affected checks. A still-running check against an earlier
snapshot cannot validate the new one; settle or cancel owned obsolete jobs.
Retain unaffected evidence when its inputs and conditions remain valid. A new
chat message alone does not require rerunning an unchanged expensive check.

## Resolve failures within authority

Distinguish a product failure, recipe/harness drift, and an unavailable prerequisite
using source and execution evidence. An unchanged retry needs a reason, such as
measuring a suspected intermittent failure or confirming an actual setup correction.
Keep the original failed result; do not hide it behind the successful retry.

A verification-only task reports failures without repairing product code or
weakening expectations. Route requested diagnosis or repair to `debug`; recipe
corrections belong to `verification-authoring`. A broader active implementation
task can already authorize those actions. After repair, repeat the affected
verification before claiming success. Missing execution access remains a blocker,
not permission to replace runtime proof with confident source inspection.

## Deliver evidence that matches the claim

Report the precise result and scope: project/revision or snapshot, requirements
and feature entry points checked, commands or actions, outcomes, retained evidence
paths, failures, skipped or blocked coverage, and the next missing check. Separate
observed failures from inaccessible checks and pre-existing failures from new
regressions only when there is evidence for that distinction.

Account for each required user path and criterion, including alternate entry
points that are in scope. Keep expected and observed results separate and attach
the supporting action or artifact. A blocked, skipped, inconclusive, or unrun
required check remains incomplete even if another check of that path passed.
Use the project's existing proof format when a tool consumes the results; its
overall success must agree with this coverage. A short task needs a short record,
not a new CLI, schema, feature map, or permanent report convention.

Claim completion only when the required checks and acceptance criteria have
supporting current evidence. Partial success is useful, but name the passing
subset and the failures; do not summarize an incomplete run as "tests pass" or
"done". A validator proves structure, not behavior; a passing suite does not
prove an unexercised user path. Inspection of a delegated artifact is useful,
but verify its decisive claims against actual artifacts and execution.

Verification grants no new publication authority. The caller and repository rules
own commits and PRs. For a requested check or update of this skill's sources,
read [references/upstream-updates.md](references/upstream-updates.md).
