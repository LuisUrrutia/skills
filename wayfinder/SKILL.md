---
name: wayfinder
description: Use when an ambiguous initiative needs connected decisions and a durable direction before execution can be planned.
---

# Wayfinder

Turn an ambiguous initiative into an evidence-backed direction that can be planned,
preserving decisions and context across sessions. The destination may be a product,
an architecture, a migration, or a reasoned decision to narrow, defer, or abandon
an initiative.

Own uncertainty that prevents good planning. Planning owns executable work units,
their order, dependencies, and acceptance criteria once the direction is clear.
When that direction already meets the readiness condition below, provide the
relevant context and continue the authorized planning workflow; do not manufacture
a discovery phase. A single answerable question can be resolved directly without
a separate map.

## Establish the destination

Read the request, existing decisions, and relevant project evidence. Establish the
desired outcome, who needs it, constraints, explicit exclusions, and what would
make the direction sufficiently clear to plan. Use what the user already settled;
revisit a decision only when new evidence or changed scope affects its basis.

Separate current facts, approved decisions, working assumptions, and proposals.
Investigate accessible facts before asking the user. Exercise judgment already
delegated within its agreed bounds and record that authority. Ask about a
consequential product preference, scope choice, or authority conflict only when
neither the evidence nor existing delegated authority settles it. Explain the
alternatives and their effect, with a recommendation when supported. Pause the
affected branch while continuing independent useful work.

## Keep one decision map

Use the requested or existing authoritative decision document or tracker record.
For connected decisions or work spanning sessions, persist a compact map there as
a continuity deliverable. Without an established location, use the project's
durable document or task-artifact conventions. Check that the intended next session
can find and access it and that required cleanup will not remove the only copy.
Include its locator in the response or requested handoff; update an existing index
only within the task's authority. If storage is temporary or local to this checkout,
state the retention or transfer limitation and the next action needed to preserve
continuity. Respect read-only requests: provide the map in the response and state
that it was not saved.

Read [assets/decision-map.md](assets/decision-map.md) when creating or restructuring
a map. Adapt its size to the initiative. A short initiative can keep the index and
decision details together; split substantial records only when that makes the map
easier to resume. Keep one authoritative detail record per decision and link to it
from summaries. Preserve existing IDs and links when updating a map.

Map the destination, settled decisions, explicit open questions, their decision
dependencies, uncertain areas not yet sharp enough to formulate, and exclusions.
Record the next useful step. Do not turn vague areas into speculative tickets or
mistake a deferred question for an exclusion agreed by the user.

Use a dependency only for an answer required before resolving another question;
record related topics and influences separately. When choices mutually constrain
each other, resolve them as a joint question instead of creating a dependency cycle.

An existing issue tracker can hold the map and decision records when the task
authorizes those writes. Use its native relationships and ownership where useful;
a tracker, label scheme, branch, or installed integration is not a prerequisite.
Without remote-write authority or access, keep local work and identify the missing
operation. Creating a local map does not authorize sending messages or publishing it.

## Resolve the next useful question

Choose a question whose prerequisites are satisfied and whose answer most affects
the destination or unlocks useful decisions. Follow the user's requested focus
when compatible with those dependencies. Match the method to the uncertainty:

- **An accessible fact:** inspect the relevant code, usage data, user research,
  records, or current primary sources. Record the evidence and its limits,
  including conflicting evidence.
- **Uncertain behavior or feasibility:** run the smallest authorized experiment
  that can distinguish the options. Use `prototype` when available for a UI, state,
  or behavioral prototype; pass it the question, constraints, and observation that
  would settle the question. Bring actual results and remaining uncertainty back.
- **A software boundary or model:** use `design-code-structure` when available for
  a design-only investigation of the affected data model, interface, or module
  boundaries. Bring its alternatives, recommendation, and relevant constraints
  back into the decision record. Implementation follows the planning handoff and
  the active task's authority.
- **A choice requiring the user's judgment:** present only the decision the user
  needs to make, its consequences, and the evidence already gathered. Keep a
  recommendation distinct from an accepted choice.

Resolve optional skills by registered name. If a specialist is unavailable,
perform the bounded investigation with available tools or state the exact missing
capability; do not invent results. Specialist completion alone does not establish
that the original question has been answered.

Define what evidence would resolve an investigation before expanding it. Record
what was actually observed, under which inputs or conditions, and which conclusion
it supports. A proposed experiment or a plausible design is not a tested result.
Prototype code remains an experiment unless the user authorized its integration.
Enabling tasks belong here only when authorized and needed to answer a decision;
implementation backlogs belong to planning.

Delegation and concurrent work follow the active host and task's authorization.
When multiple actors share the map, record who owns an active question and reread
the canonical state before merging results. Preserve other contributors' work;
ownership metadata alone is not a lock. Parallelize only independent questions.

## Update and resume

After an answer, record the decision, its authority, rationale, evidence, relevant
alternatives, and implications. Keep unresolved assumptions visible. Update the
dependent questions and the next useful step in the same pass. An issue marked
closed, deferred, or out of scope is not evidence that its question was answered.

When a premise changes, identify affected decisions, mark their conclusions as
needing reconsideration, and block dependent planning until the effect is resolved.
Preserve the previous rationale with a superseding link or note. Promote an
uncertain area into a specific question when it can be stated precisely, even if
a prerequisite answer is still pending.
Reintroducing an excluded area requires a scope change within the user's authority.

On resumption, read the map first and relevant detail records on demand. Compare
the recorded state with current evidence, agreements, and other actors' updates
before choosing the next question. Resume from unresolved dependencies rather than
repeating settled discussions. Leave the map with enough evidence pointers and a
concrete next action for another session to continue without private recollection.

## Finish with a direction

The scoped initiative is ready for planning when its outcome, boundaries, material
choices, and constraints are clear enough to choose executable work without
guessing a consequential decision. Keep residual risks explicit, with the check
or decision that will address them; a blocking unknown cannot become a harmless
assumption merely to declare readiness. A smaller scope can be ready while the
broader initiative remains blocked, provided the scope change is authorized.

Deliver the direction, reasons and evidence, boundaries, remaining uncertainty,
and the map's location. Hand this context to the available planning workflow and
continue when planning was already requested. No particular planning skill is
required. If exploration alone was requested, end with that result.

When a prerequisite or user decision remains unavailable, report the exact open
question, its impact, and the action that can unblock it; preserve the partial
result without calling it ready. If evidence favors narrowing, deferring, or
abandoning the initiative, explain why and distinguish the recommendation from an
authorized decision. Record who decided and the authority for the change of
direction, which can be a valid outcome.

For requested source maintenance, use `agent-instructions` with `origin.txt`.
It owns comparing the pinned upstream source and reconciling changes with this
skill's local contract.
