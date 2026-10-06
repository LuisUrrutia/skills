---
name: planning
description: Use when creating, reviewing, revising, or breaking down a software implementation plan.
---

# Planning

Turn a defined outcome into work another engineer or agent can execute and verify.
Preserve the reasoning, constraints, and dependencies that execution needs without
writing the implementation in advance.

Create a plan when none exists, revise the authoritative plan when asked to change
it, or split it into work units when separate delivery warrants them. A review-only
request returns findings and proposed corrections without editing the plan.
Planning alone authorizes the requested planning artifacts, not product changes,
tracker publication, or implementation status transitions. When planning and
implementation are both authorized, finish planning and continue within the
active host mode; do not add a second approval gate.

## Ground the work

Read the request, existing plan or specification, relevant project instructions,
and any Wayfinder direction or decision records supplied for this work. Preserve
settled choices and user corrections with their reasons and sources. A prior
Wayfinder map or formal spec is useful input, not a prerequisite.

Inspect the affected implementation, callers, tests, and configured commands.
Follow enough of the real path to identify where the change belongs and what
already provides part of it. Check consequential claims about interfaces,
dependencies, compatibility, and verification against accessible evidence. Keep
existing behavior distinct from intended behavior; contradictory code and docs
are a finding to resolve, not permission to redefine the requirement.

Answer repository questions through investigation. Make routine implementation
choices within delegated judgment. Ask when an unresolved choice materially
changes scope, behavior, a contract, or a hard-to-reverse action and neither
evidence nor existing authority settles it. State the consequence and a supported
recommendation. Keep the affected work blocked while progressing independent work;
labeling a consequential guess as an assumption does not make it executable.

If connected decisions still prevent choosing a direction, use `wayfinder` when
available with the outcome, evidence, and exact open questions. For an unsettled
data model, interface, or module boundary, use `design-code-structure` when useful,
in design-only scope. Resolve optional skills by registered name; otherwise do
the bounded analysis with available tools or report the missing evidence. Reuse
their decisions in the plan rather than duplicating their procedures.

## Choose the plan's size and home

Match detail to uncertainty, dependencies, and the executor's context. A small,
settled change may need only a short ordered plan with its deciding check. An
explicit planning request still gets that plan. Larger work needs enough detail
to expose integration risks and permit independent execution; file counts,
minute estimates, and a fixed number of tasks do not determine the right size.

Use the requested output and existing authoritative record. Keep a brief plan in
chat or the host's plan surface when sufficient. For a durable handoff, follow the
project's artifact convention; otherwise use `docs/plans/<topic>.md` relative to
the target project. Preserve another effort's plan and unrelated edits. Reuse the
current plan for the same work instead of creating competing progress records.

Name the authoritative location and check that the next executor can access it.
If the host's private plan or an ignored, temporary, or checkout-local file is the
only copy, state its retention or transfer limit and how to preserve it. A map or
spec keeps its own authority: link the relevant decisions and carry the constraints
needed for execution, without maintaining a second decision history.

## Describe executable work

Cover the following where they affect the change. Use the project's format; read
[assets/implementation-plan.md](assets/implementation-plan.md) when a new durable
plan needs a starting structure, and omit sections that add no useful information.

- **Outcome and scope:** the triggering problem, intended behavior, acceptance
  criteria, fixed constraints, and boundaries likely to be mistaken for scope.
- **Approach and evidence:** the existing capability to extend, affected components
  and relevant source paths, chosen contracts, and reasons for consequential
  choices. Distinguish verified locations from proposed files and untested claims.
- **Work units:** the result each unit delivers, changes needed, prerequisites,
  and evidence that proves it. Include consumed and produced interfaces where
  separate implementers must agree. State settled names or signatures precisely;
  leave ordinary implementation details to the executor.
- **Verification:** connect each material acceptance criterion to an observable
  scenario, expected result, and relevant command or interaction. Include failure
  behavior and compatibility that the requirement or affected path makes material.
  Locate existing check commands; distinguish checks to add from those available
  now. Name access or environment prerequisites and unverified command assumptions.
- **Risk and recovery:** order decisive feasibility checks early where dependencies
  permit. For migrations or irreversible changes, specify transition states,
  release prerequisites, and rollback or forward recovery within the agreed scope.

Prefer narrow, complete behavior changes that can be checked as they land. Keep
implementation and its behavioral tests together; setup and documentation belong
with the outcome they enable unless they are independently useful deliverables.
Read [references/work-units.md](references/work-units.md) when dividing a larger
change, planning a staged migration, or preparing tickets for separate executors.

Plan the checks that prove the outcome; do not replace acceptance with "tests
pass" or "run the suite". Existing project quality gates remain applicable.
Recorded inspections or authorized probes may ground a plan, but future tests,
proposed code, and another agent's confidence are not observed passing results.

## Check readiness and continue

Review the plan against the original request and authoritative decisions. Trace
each material requirement to its work and evidence; check dependency order,
interface consistency, meaningful failure cases, and the combined result. Remove
speculative scope and steps that decide nothing. Correct evidenced gaps in a plan
you are authoring; for review-only work, report them with their source and effect.
Repeat only after material changes or new evidence, not to attain a perfect score.

The plan is ready when its scoped work can proceed without inventing a
consequential decision and its completion can be checked. Report the plan or its
location, readiness, exact blockers or verification limits, and the next action.
A ready subset does not make blocked work ready or authorize dropping requirements.

For a handoff, make the briefing usable without this conversation: carry relevant
decisions, source pointers, prerequisites, and what evidence would require
replanning. When continuing an existing plan, reconcile actual work and changed
premises before updating remaining units; preserve completed work and other
contributors' changes. Reopen affected decisions rather than silently reversing
them. Keep genuine implementation progress distinct from planned checkboxes.

End a planning-only request with the plan or findings. If execution was already
requested and permitted, continue the ready work through the existing development
workflow, preserving required host approvals and real blockers. This skill does
not choose a worker topology or require another planning session.

For requested source maintenance, use `agent-instructions` with `origin.txt`.
