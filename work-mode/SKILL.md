---
name: work-mode
description: Use when coordinating or resuming a development task through its remaining phases to the authorized outcome.
---

# Work mode

Carry one selected task from its actual state to the requested result. Own route
selection, phase transitions, and continuation; existing specialists own their
procedures. A specialist can also be used directly without this coordinator.

## Establish the task and endpoint

Read the active request, project instructions, and the identified ticket, plan,
delivery unit, or handoff. Inspect existing work and evidence before choosing
the next action. Use the work the user selected; a nearby plan or backlog item
does not become another assignment.

For repository work, inspect the current checkout, branch, and uncommitted state
before editing. If the endpoint needs a different branch or checkout, follow
the host's ownership and handoff rules and `worktrunk` before the first edit.

Establish the outcome, scope, acceptance evidence, and current authority. Preserve
settled decisions and explicit limits such as diagnosis-only, read-only,
planning-only, local-only, create-only, or keep-draft. A generic implementation
request ends with the scoped change, required checks, and any commits required by
the task or standing rules; publication,
merge, deployment, and background scheduling require their own authority from
the request or standing rules.

Resolve accessible facts before asking. Ask immediately when an unanswered choice
materially changes scope, behavior, a contract, or execution authority and the
evidence cannot settle it. Pause dependent work and continue only work valid under
either answer. Already-authorized phases need no new approval; silence is not a
decision. Report the chosen route briefly, with the fact that determined it.

## Choose the next necessary phase

Route by the requested action and the remaining gap, not by the presence of a
ticket or plan path. Resolve skills by registered name through the host's catalog
or supplied named context, and use its supported invocation mechanism. Load only
the owners needed for the current work.

| Current need | Owner and input | Result needed before continuing |
| --- | --- | --- |
| Small, settled change or a ready unit | Implement directly with the supplied contract and applicable domain guidance. | The scoped behavior and its deciding checks; no direction map or separate decomposition ceremony. |
| Observed defect or regression | `debug`, with symptom, expected behavior, evidence, and diagnosis or repair scope. | Supported diagnosis or verified repair, including the original reproduction and any limits. A returned fix is already implementation. |
| Connected decisions prevent choosing a direction | `wayfinder`, with outcome, constraints, existing decisions, and exact unknowns. | A supported direction that permits planning, or the consequential unresolved choice. |
| Direction is clear but implementation approach is missing | `planning`, with the outcome, current code, constraints, and acceptance needs. | An executable approach and verification contract. Reuse a ready plan; revise only affected assumptions. |
| Work needs smaller delivery boundaries | `task-breakdown`, with the approach, acceptance criteria, dependencies, and review budget. | Coherent, testable units with readiness and integration checks. Continue selected ready scope, retaining blocked requirements. |
| Structure must change while behavior survives | Use `simplify-code` for focused cleanup, or `design-code-structure` for a substantive model or boundary decision. | The authorized structural result and evidence for the preserved behavioral contract. |
| A bounded experiment can resolve uncertainty | `prototype`, with the question, constraints, and deciding observation. | The experiment's observed result and limits. Promotion into production follows the enclosing scope. |
| Only a specialist result was requested | Use its owner, such as `planning`, `review-code-changes`, `verify`, `explain-code`, or `explain-decisions`. | That owner's requested artifact or answer; do not append implementation or delivery. |

The table is not a checklist. Resolve a single answerable question directly.
Use `tdd` when test-first implementation is selected, and domain skills when the
actual change reaches them. Focused impact analysis belongs to
`analyze-change-effects` when an indirect consequence needs investigation.
These supporting skills do not become extra phases for every edit.

A route-specific owner is needed when its phase is selected, not for every task.
If that owner, an explicitly requested specialist, or essential evidence is
unavailable, retain prepared inputs, name the missing capability, and block only
dependent work. Missing optional help permits useful direct work within authority;
never claim an absent invocation or required check succeeded.

## Run a phase and read its result

Give the owner the selected work, current constraints and authorization, relevant
artifact or revision, deciding evidence, and the result the caller needs. Include
the output destination and the next consumer when they matter. Use the owner's
existing scope or mode; do not invent a return protocol or grant a child the
rest of the workflow merely by invoking it.

When implementation actually starts from a ticket, use `issue-workflow` for
the configured `work-started` event, including work without a PR. Run it at the
first implementation boundary, before source or test edits. When `debug`, `tdd`,
or a delegated worker will implement, assign this event to that implementation
owner in its brief; retain the event receipt instead of waiting for a completed
repair to trigger it. Investigation, planning, and diagnosis alone do not
establish the event. Pass the verified ticket, project, and current event evidence.
A blocked tracker transition leaves independent authorized implementation
available. Creating new tickets is a separate publication operation.

Perform implementation directly unless delegation is requested or allowed by
the applicable task, host, or specialist policy and serves a concrete need.
Skill composition does not imply child agents. When delegating, give each worker
a bounded artifact and authority, account for shared writes and integration
order, and retain one mutation owner per checkout or external object.

Inspect the returned artifact, actual changes, execution evidence, and outstanding
findings against the phase's contract. An artifact's existence or a child's
"complete" label is insufficient. Reuse completed implementation and valid
evidence; recover missing evidence without dispatching the same fix again.
Partial, failed, and blocked results keep their unresolved scope visible.

When applying a specialist inline, continue its authorized workflow under this
routing. When a delegated child returns, the coordinator resumes from its actual
result. Keep one continuation owner; do not repeat a phase already run by the
specialist. Choose and run the next authorized phase while actionable work
remains. A child finishing does not finish the enclosing task. If changed
evidence affects direction, approach, or delivery boundaries, return that gap to
its owner and preserve settled, unaffected decisions. A larger discovered task
does not authorize silently widening or dropping the selected scope.

## Verify, review, and repair

For an implemented change, use `verify` with the current change, acceptance
criteria, project checks, execution authority, and evidence destination. It
selects the application recipe and judges what the
actual execution establishes. Carry relevant revision/input identity, commands,
results, and coverage gaps forward. Existing useful checks remain available
when a project recipe is missing; authoring a persistent recipe belongs to
`verification-authoring` only when authorized.

Review the actual final change proportionately under project requirements.
Use `review-code-changes` when a code-change audit is needed, with a declared
snapshot, requirements, and report destination. Independent review follows
applicable policy and the change's risks; this skill sets no model roster.
The audit stays read-only. After it returns, the implementation owner assesses
findings against the evidence and applies supported corrections within scope.
Preserve a reason for unapplied findings and ask about consequential unresolved
choices. A clean review is not execution evidence.

Rerun checks invalidated by a repair or changed input and refresh affected review
findings. Retain evidence whose inputs and conditions remain valid. If repeated
attempts add no evidence or progress, identify the missing premise or prerequisite
before another attempt; a round count cannot turn a surviving failure into success.

Use `commit` at completed atomic boundaries when standing rules or the task
authorize it, including during implementation. Keep the behavior, its necessary
tests, and required schema or generated output together. Read
[references/delivery.md](references/delivery.md) when the endpoint includes ticket
publication, PR work, or another external delivery phase.

## Retain the next action and finish honestly

Use the existing authoritative task or plan record and the host's progress surface.
A small task can use the conversation; it needs no separate ledger. Where work
spans phases or sessions, retain the selected unit, endpoint and authority, settled
decisions, current artifact/revision, observed checks, remaining work, exact blocker
or waiting event, next action, and active execution or watch owner. Keep relevant
external IDs when those phases exist. Do not impose a new schema on specialists.

On resumption, reconcile the record with current files, revisions, external state,
and active owners before acting. Refresh affected facts and reuse valid work.
Scratch state must follow the project's storage rules. If a local, ignored, or
host-private record is the only copy, state its retention limit and use `handoff`
when context must be transferred. A written handoff proves neither receipt nor
that another agent took ownership.

Completion means the requested endpoint has its required current evidence. Report
what was completed, exact checks and outcomes, and what remains, distinguishing
partial work, failure, an inaccessible prerequisite, a pending decision, and a
host-supported wait. Name the next actor or action for unfinished work. A host
watch can end this turn while the task remains waiting; it is not completion.
Stop with the requested result when its endpoint is met. Retrospectives, new
backlog work, skill rewrites, and recurring jobs are separate tasks.

For requested source maintenance, use `agent-instructions` with `origin.txt`.
