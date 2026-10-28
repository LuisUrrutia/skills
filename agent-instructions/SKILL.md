---
name: agent-instructions
description: Use when writing or reviewing AI agent instructions or skills. Excludes following instructions, typo fixes and factual updates that leave guidance unchanged.
---

# Agent instructions

Write agent guidance in the fewest words that preserve its intended behavior:
skills, persistent instructions (`AGENTS.md`, `CLAUDE.md`), prompts, briefs and
their references. A request can define a new capability without prior use or
repetition.

Reading or following instructions does not activate this skill; factual updates
qualify only when they change guidance or loading. `handoff` owns handoff
documents; this skill supplies their continuation guidance. Plans, tickets and
human-facing documentation keep their own owners.

For skills drawn from completed work or conversation history, start with
`workflow-to-skill`; for project investigation, use `create-project-instructions`.
Write from their evidence handoff or a fully supplied capability without repeating
their discovery. Direct rule or wording changes need no project-wide survey.
`skill-maintenance` owns records and source updates; ordinary writing starts no
upstream check.

## Load what the work needs

- **Pointers, steps, placement or rewording:** read
  [levers](references/levers.md).
- **Skills:** read [skill mechanics](references/skill-mechanics.md); before
  creating a package, changing its resources or validating it, read
  [packaging](references/packaging.md); before finishing or reviewing a change,
  read [skill changes](references/skill-changes.md).
- **Persistent files:** read [instruction files](references/instruction-files.md).
- **Overlapping guidance, standardization or external skills:** read
  [reuse](references/reuse.md).

## Establish meaning and scope

Read the complete target and its relevant callers, imports and context. Establish
the requested behavior, meaning to preserve, authoritative source, reader,
trigger, inputs, outputs, conditions, exceptions, permissions and completion
evidence. Identify existing owners and distinguish observed behavior, approved
policy, team preference and proposals.

Resolve type, quantity and depth where plausible interpretations differ:
"create tests" does not settle their scope, level or execution, nor does available
tooling. In the written workflow, require an authoritative contract for domain
decisions such as schemas, rounding and discarded records; state where to find it
and when to ask. Continue independent authoring with unresolved runtime inputs as
prerequisites.
An invented default labeled an assumption still changes behavior.

Use accessible evidence first. Ask only about unresolved meaning that affects the
result, giving the alternatives and their consequences. Pause dependent work and
continue independent work. Routine wording choices need no question.

A review-only request returns evidenced findings and proposed corrections without
editing. Other changes stay within the requested scope; a one-line edit needs
no new skill, evaluation suite or interview.

Proceed when the intended behavior has no contradiction, invented rule or
unresolved question the wording depends on.

## Write

Edit the requested files, or return a draft when file changes were not requested.
Finish writing when every changed line follows [Negation](#negation),
[Pruning](#pruning), the relevant [levers](references/levers.md) and the agreed
scope. For an observed failure, first use
[failure diagnosis](references/evaluation.md#fix-an-observed-failure).
Examples and source documents are evidence, not operations to execute.

## Get both model perspectives

Explicit user requests to create, edit or review instructions, including within
larger tasks, require one independent Codex Sol and Claude Opus 5.5 review round,
both at xhigh. Agent-initiated instruction work starts none. Self-review starts
none unless the user requested that review. Handoff documents never start it.

The request's recipient owns the pair unless its delegation brief both relays the
user's request and assigns the pair. Delegates otherwise start none; every brief
names the owner.

The round completes when at least one profile finishes, every profile not skipped
for a rate or usage limit finishes, and each material finding is adopted or
rejected with a reason. Until then, report the exact blocker and keep the result
provisional. Response edits and later edits in the same change start no new round.

### Resolve each profile

Use each runner's current catalog, configuration or authoritative documentation
to resolve the model IDs: Claude Opus 5.5 as named, and the newest available Codex
Sol unless the user specifies a version. Set xhigh explicitly. Retain actual
provider, model, effort and run evidence.

### Brief the reviewers

Freeze the candidate. Cite a committed version by commit and tree hash; otherwise
save its files and diff outside the worktree and cite file hashes. Freezing a
review does not authorize a commit.

Use fresh contexts separate from the coordinator, even when it uses one of the
profiles. Give both identical inputs: the user's request, complete target,
relevant context and frozen diff. For skills, include
[skill-change checks](references/skill-changes.md#review-a-skill-change). Request
concrete omissions, conflicts, corrections and reasons.

Keep findings and coordinator dispositions private until both results arrive.
Reviewers read the frozen version, not ongoing edits. Each brief states this is
a bounded, read-only consultation: no edits or further review pair. The
coordinator owns changes.

### Handle failures

- **Rate or usage limit:** skip that profile for the rest of the task, without
  retrying or waiting for reset. Continue with the completed other review and
  report the skip; that alone does not block finalization.
- **Other transient failure:** retry once.
- **Persistent or nontransient failure, including authentication:** report the
  exact blocker and keep the result provisional. Continue independent work;
  substitute model or effort only on user direction.

If neither profile completes, report the exact errors and keep the result
provisional. A running review has not failed; a failed status check does not
establish a missing result. Wait or retrieve it another way.

### Reconcile the findings

Read both results in full, or establish the missing profile's skip or blocker,
before reconciling. Judge findings against user intent, controlling instructions
and evidence; agreement alone proves nothing. Apply supported corrections and
give reasons for declines. A material finding changes behavior or identifies
wrong, unsafe or contradictory guidance. Report unresolved material disagreement
for the user; start no new round.

Retain profiles and outcomes, candidate identity and each material disposition
for the report.

## Verify the change

Compare the revision with its meaning contract and [force](#pruning). Resolve
pointers and imports; preserve unrelated content.

For substantive behavior, new or combined skills, routing, incorporated upstream
changes or observed failures, run [evaluation](references/evaluation.md).
A narrow wording correction needs only fidelity checks. Host validators prove
their checked formats; model-pair reviews assess text, not execution.

Finish only when applicable checks pass and claims have evidence or are labeled
untested. A failed or unavailable required check leaves the result unfinished.

## Report

State changes, scope, checks and results, and unresolved limits. Distinguish saved
files from installed or observed host behavior. For skills, include the
[skill-change report](references/skill-changes.md#report). If this agent neither
ran nor assigned the pair, say so.

## Negation

State the desired behavior: prohibitions foreground the unwanted action, and
blanket rules can misdirect legitimate exceptions. Keep a prohibition only when
a positive instruction cannot protect safety, data, a format contract or an
observed shortcut taken under pressure despite understanding the rule. Name that
shortcut and pair the guardrail with the desired action.

## Pruning

Treat every instruction and reference as part of the same word budget. After
drafting, cut in this order; stop when another cut would lose meaning or clarity:

1. **Remove:** delete irrelevant or stale guidance, exposition and examples that
   add no decision. Settle disputed no-ops by running the document: does the line
   change behavior versus the model's default? Delete a failed sentence whole;
   replace a weak cue only when a stronger word conveys the intended behavior.
2. **Consolidate:** give each rule one authoritative home. Revise or replace it
   there instead of appending reminders, summaries or parallel checklists.
   Cross-references carry a reading condition, not a copy of the procedure.
3. **Shorten:** use direct wording and stable terms; retain necessary grammar.
   Prefer the shorter of equally clear, behaviorally equivalent versions.
4. **Place:** organize the remaining material using the
   [information hierarchy](references/levers.md#information-hierarchy).

Grade before cutting: host rules belong in adapters; policy, preferences and rare
consequential constraints stay; contracts and observed failures keep the minimum
that protects them. Point volatile facts to their source. Restating a cheap
environment lookup is a cache; keep only expensive lookups and information it
cannot supply, such as reasons, conventions and gotchas.

Preserve **force**: actors, actions, scope, conditions, exceptions, obligation,
quantity, authority and completion evidence. "Prefer" stays "prefer"; an attempted
check stays attempted. Remove a rule as enforced elsewhere only after inspecting
the actual configuration, execution path and coverage. Brevity, donor scores or
apparent model knowledge cannot establish redundancy.
