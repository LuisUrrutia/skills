---
name: wayfinder
description: Use when an ambiguous initiative needs connected decisions and a durable direction before execution can be planned.
---

# Wayfinder

Turn an ambiguous initiative into an evidence-backed direction that can be planned,
preserving decisions and context across sessions. A product, architecture, or
migration can emerge from this work; narrowing, deferring, or abandoning the
initiative can also be a sound outcome.

Own the uncertainty that prevents good planning. `planning` owns the implementation
approach and acceptance criteria; `task-breakdown` turns that plan into PR-sized
delivery units with their dependencies and checks. If the direction is
already clear enough to plan, carry its context into the authorized planning
workflow. Resolve a single answerable question directly; a map earns its place
when decisions connect or work must continue across sessions.

## Ground the destination

Locate any existing map in the requested or project-conventional location. On
resumption, read it first and its detail records as needed, then compare recorded
premises with the current request, evidence, and other contributors' updates
before choosing the next question. Otherwise start with the request, relevant
project evidence, and prior decisions.
Establish who needs what outcome, what happens today, the constraints and exclusions,
and what must be known to plan. Describe success in observable terms; distinguish
an agreed target from a proposed one.

Treat a suggested solution as a candidate unless the user already chose it.
Check whether it addresses the underlying problem, duplicates an existing
capability, or commits more scope than the outcome needs. Use evidence of current
behavior, workarounds, and pain; implementation feasibility alone does not establish
user value. Preserve settled choices unless new evidence or scope affects their
basis. Make facts, approved decisions, assumptions, and proposals distinguishable.

Investigate accessible facts before asking. Exercise judgment already delegated
within its bounds and record that authority. Ask only for a consequential choice
or missing input that neither evidence nor delegated judgment settles; explain
its effect and recommend when supported. If the user cannot assess an unfamiliar
area, first explain the relevant options and hazards from evidence. Keep both the
explanation and the question tied to decisions in this initiative.

## Chart the map

Map the consequential questions broadly enough to see their relationships before
going deep on one. A dependency means an answer required to resolve another
question; keep mere influences separate. Resolve mutually constraining choices
together instead of creating a cycle. Keep areas not yet sharp enough to question
visible, without inventing speculative tickets. A precise question can be recorded
even while blocked.

Persist the map in the requested or existing authoritative document or tracker.
Otherwise follow the project's durable artifact conventions. Check next-session
discovery and access, including whether cleanup would remove the only copy.
Provide its locator; if storage is temporary or checkout-local, state the retention
or transfer limit and the action needed to preserve continuity. For read-only work,
return the map in the response and say it was not saved. Tracker writes and
publication require the task's authority; a local artifact grants neither.

Read [assets/decision-map.md](assets/decision-map.md) when creating or restructuring
a map. Adapt its size to the initiative. Keep small maps in one file; split details
only when that helps resumption. Preserve IDs and links, with one authoritative
detail record per decision and compact summaries pointing to it.

## Resolve what matters next

Choose an unblocked question whose answer can change the direction or unlock
important decisions. Weigh the impact of being wrong against the cost of learning;
follow the user's focus where prerequisites permit. Scale the investigation to
that uncertainty and reversibility. Stop expanding it when further detail would
not change the choice or its readiness; inaccessible decisive evidence remains a
blocker, not a reason to assume success.

For a chosen question whose answer changes the direction, compare materially
different ways to meet the outcome. Consider retaining or extending what exists, a smaller
intervention, or doing nothing when credible. Honor settled constraints; do not
invent alternatives to fill a menu or reopen a settled choice to create one.

Judge options against the same outcome and constraints. Make the differences
concrete: who benefits, what changes, relevant costs and failure modes, and how hard
the choice is to reverse. Inspect or measure consequential claims where practical;
label estimates and unknowns. A sketch, example, or comparison table can make a
choice easier to assess; use only the design detail needed to evaluate it.

Identify the assumption or missing fact on which the recommendation turns, and
what evidence would change it. Prefer the least complexity that meets the whole
outcome, including its lasting operational cost. Cheap reversal can justify a
bounded experiment; it does not make an option that violates a hard constraint
acceptable. When only one viable path remains, state it and why.

Match the method to the missing answer:

- **Facts:** inspect relevant code, records, usage, user research, or current primary
  sources. Keep conflicting evidence and its limits visible.
- **Behavior or feasibility:** define the observation that would support or reject
  the option, then run the smallest authorized experiment that distinguishes it.
  Use `prototype` when available for UI, state, or behavioral prototypes, passing
  the question, constraints, and deciding observation.
- **Software structure:** use `design-code-structure` when available for a
  design-only investigation of the relevant model, interfaces, or boundaries.
  Bring alternatives, constraints, and the recommendation back to the map.
- **Human judgment or private context:** ask about the preference or fact that
  determines the choice, with evidence and consequences the user can assess.

Resolve optional specialists by registered name. If unavailable, investigate with
available tools or name the missing capability. Assess their results against the
original question: completion of a subtask alone does not answer it. Record actual
observations, inputs, and limits; distinguish supported, contradicted, and
inconclusive claims. A plausible design or proposed experiment is not a tested
result. Prototype code remains experimental unless integration is authorized.
Enabling work belongs here only when authorized and necessary to answer a decision;
implementation backlogs follow the planning handoff.

Pause only the branch that needs an unavailable prerequisite or user decision.
Continue independent useful work. Delegation follows the active task and host's
authority; parallel work needs independent questions. With multiple contributors,
record active ownership and reread canonical state before merging results.
Preserve their work; an owner field alone is not a lock.

## Keep the map current

After each answer, record the choice or pending recommendation, its authority,
rationale, evidence, material alternatives, remaining assumptions, and what would
change it. Update dependent questions and the next useful action in the same pass.
Record deferral or exclusion with its reason and authority, and deferral with a
condition for reconsideration. Closed, deferred, and out-of-scope records do not
establish that a question was answered.

When a premise changes, reopen affected decisions and block dependent planning
until resolved, preserving the superseded rationale. Promote uncertain areas as
their questions become precise; reintroduce exclusions only through an authorized
scope change.
Leave evidence pointers and a concrete next action so resumption does not depend
on private recollection or repeat settled discussions.

## Hand over a direction

The scoped initiative is ready when its outcome, boundaries, material choices,
and constraints permit executable work without guessing a consequential decision.
Check the direction against the original outcome, including relevant failure
behavior. Keep residual risks with the check or decision that will address them;
a blocking unknown cannot become a harmless assumption to declare readiness.

Deliver the direction, its reasons and evidence, boundaries, remaining uncertainty,
and the map's location when one exists. Continue the available planning workflow
when planning was already requested; no particular planning skill or extra approval
is required. If exploration alone was requested, finish with its result.

If blocked, name the exact question, its impact, and the action that can unblock
it. A smaller scope may be ready while the broader initiative remains blocked if
that scope change is authorized. Distinguish a recommendation to narrow, defer,
or abandon from an authorized decision, and record who or what authorized it.

For requested source maintenance, use `agent-instructions` with `origin.txt`.
