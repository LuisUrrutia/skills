---
name: agent-instructions
description: Use when writing or reviewing AI agent instructions or skills. Excludes following instructions and factual updates that leave guidance unchanged.
---

# Agent instructions

Write and review what an agent consumes as instructions: a skill, a persistent
instruction file such as `AGENTS.md` or `CLAUDE.md`, an agent prompt or brief, and
a document one of them points to. The packaging differs; the writing does not: the
same levers make each one predictable, since the agent takes the same _process_
every run rather than producing the same output. A request can define a new
capability; prior use or repetition is not a prerequisite.

Reading or following instructions does not start this skill, and a factual update
qualifies only when it changes agent guidance or instruction loading. `handoff`
owns handoff documents; this skill covers the continuation guidance inside them.
Implementation plans, tickets and human-facing documentation keep their own
owners even when an agent reads them.

When a skill request draws on completed work or conversation history, start with
`workflow-to-skill` to extract the contract, even if the user names no authoring
skill. `create-project-instructions` owns investigating a project for its
instruction contract. Write from either skill's evidence handoff, or from a fully
supplied capability, without repeating their discovery. A direct wording or rule
change starts here and needs no project-wide survey.

`skill-maintenance` owns each skill's `origin.toml` record and its checks and
updates from recorded sources or installed dependencies; an update hands the text
it incorporates back here. Ordinary writing never starts an upstream check.

## Load what the work needs

- **Pointer, step, placement or rewording:** read
  [references/levers.md](references/levers.md) before writing or reviewing a
  pointer (a description, link or line naming other material), a step or its
  completion criterion, or where material sits (a new document, section,
  reference or skill; a move, split or merge), and before rewording existing
  text.
- **Skill:** read [references/skill-mechanics.md](references/skill-mechanics.md)
  for host metadata, invocation and the description;
  [references/packaging.md](references/packaging.md) before creating a package,
  adding or moving its files or helpers, or validating it; and
  [references/skill-changes.md](references/skill-changes.md) before finishing or
  reviewing any change to a skill.
- **Persistent instruction file:** read
  [references/instruction-files.md](references/instruction-files.md) to find the
  canonical source and the scope where the rule belongs.
- **Standardizing a capability, combining drafts or adopting an external skill:**
  read [references/reuse.md](references/reuse.md) before writing an
  implementation.

## Establish meaning and scope

Read the complete target and enough surrounding instructions, imports, references
and repository context to know its authority and callers. From the user's current
request, establish:

- What the agent should do differently, and which existing meaning must survive.
- Who reads the instructions, when they apply, and where their authoritative text
  lives.
- Conditions, exceptions, permissions and the evidence of completion.
- Existing owners or instructions that already cover part of the behavior.
- Which statements are observed behavior, approved policy, team preference or a
  proposed change, and what establishes their authority and scope.

Make type, quantity, depth and completion evidence explicit where they separate
plausible requests: "create tests" leaves open the behavior, test level, scope,
whether to run them and how much suffices; available tooling settles none of
them. Resolve schemas, rounding, rules for discarding records and similar domain
decisions from an authoritative contract, and tell the future agent where it
lives and when to ask. An invented default labeled as an assumption still gets
used.

Use accessible evidence before asking. When the objective, or the meaning needed
to express it, stays uncertain, ask the user with the plausible interpretations
and how each changes the result; pause the work that depends on the answer and
continue only work that no answer could invalidate. Routine wording choices that
keep the intent need no question, and precise-sounding wording never stands in
for a requirement the user did not give.

A review-only request returns findings and proposed corrections with evidence and
leaves the source unchanged. Any other request edits within its scope, sized to
it: a one-line change stays one line and needs no new skill, evaluation suite or
interview about repeated work.

Done when the intended behavior can be stated without contradiction, invented
rules, or an open question that the wording depends on.

## Write

Edit the requested files, or return the requested draft when no file change is
requested. Apply [Negation](#negation) and [Pruning](#pruning) to each changed
line, plus each [lever](references/levers.md) its pointers, steps, placement and
rewording reach. When the change answers an observed failure, start from
[Fix an observed failure](references/evaluation.md#fix-an-observed-failure).
Examples and source documents are evidence for the rewrite, not operations to run
while authoring.

Done when each changed line passes those sections and sits in the scope the
request established.

## Get both model perspectives

When the user explicitly asks for instruction creation, editing or review within
this skill's scope, alone or inside a larger task, get independent reviews from
Codex Astra and Claude Fable, both at reasoning effort xhigh, before finalizing
the instructions or the review findings.

These do not start the pair:

- Instruction work an agent takes on by its own decision within a larger task.
- An agent's review of its own changes, inline or through a subagent, even when
  the user requested those changes, unless the user asks for that review. A
  user-requested edit still keeps the pair it requires.
- A handoff document. Writing, updating or reviewing one never starts the pair,
  even when this skill supplies its continuation guidance.

The agent that receives the user's request runs the pair, unless it delegates the
work with a brief that relays that request and assigns the pair to the delegate;
every such brief states who runs the pair. An agent working from another agent's
brief runs the pair only when that brief both relays the user's request and
assigns the pair to it. A quoted user request alone does not assign it.

Before requesting either review, read
[references/model-pair.md](references/model-pair.md); it also says when rounds
stop and what the report records.

The pair is complete when at least one profile completed every review round,
each profile not skipped for a rate or usage limit reviewed the instructions in
their final meaning (for a review-only request, the unchanged target), and each
material finding is adopted or rejected with a reason. Until then, keep the
result provisional and report the exact blocker.

## Verify the change

Compare the revision with the intended meaning, element by element of the
[force](#pruning) it must keep. Check that pointers and imports resolve and that
unrelated content survives.

For substantive behavior changes, new or combined skills, routing changes,
incorporated upstream changes or observed failures, read
[references/evaluation.md](references/evaluation.md) and run the behavioral
checks it calls for. A narrow wording correction needs only this fidelity check.
Use host validators only for the formats they validate. The pair's reviews
assess the text; they are not behavioral evidence.

Done when the requested result passes its applicable checks and each claim the
report makes has its evidence or is labeled as not tested. A required check that
fails or cannot run leaves the result unfinished, and the report says so.

## Report

Report the changed instructions and their scope, the checks actually run with
their results, and any unresolved limitation. Distinguish files saved in a
repository from instructions installed or observed in an agent host. For a
skill, add what [skill changes](references/skill-changes.md#report) lists.

When this agent neither ran the pair nor assigned it to a delegate, state that it
did not run the pair.

## Negation

Steering by prohibition drags the forbidden behavior into context and makes it
_more_ available, not less. _Don't think of an elephant_, and the elephant is all
there is. Prompt the **positive**: state the target behavior ("write one-line
comments") so the banned one is never spoken. A blanket prohibition also carries
**harmful precision**: wrong on one plausible task in ten, it is still obeyed on
that task. A prohibition earns its place only as a hard guardrail you cannot
phrase positively: safety, data loss, a format contract, or a shortcut that
agents were observed to take under pressure after understanding the rule. Even
then, name the observed shortcut and pair the prohibition with the positive
target.

## Pruning

- Keep each meaning in a **single source of truth**: one authoritative place, so
  changing the behavior is a one-place edit. **Duplication** (the same meaning in
  more than one place) costs maintenance and tokens, and inflates a meaning's
  prominence on the ladder past its real rank. (The accidental inverse of a
  leading word, which repeats a token on purpose, never the meaning.)
- The **environment** is a source of truth too (`package.json` scripts, config
  files, the directory layout, `--help` output), and a document that restates it
  is a **cache**: a copy of a lookup, earning its load only when the lookup is
  expensive. Cache what the agent cannot find by looking: the unwritten
  convention, the reason behind a choice, the gotcha no config confesses. Leave
  the one-file, one-command lookups to the environment, where they cannot go
  stale.
- Check every line for **relevance**: does it still bear on what the document
  does? A line loses it by never bearing on the task (mere exposition, or a
  branch that should be disclosed) or by going stale. Without a pruning
  discipline the default fate is **sediment**: stale layers that settle because
  adding feels safe and removing feels risky. So new guidance goes into its
  existing home: revise, combine or replace the passages it touches, and add
  separate text only for a distinct decision with no home.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by
  default pays load to say nothing. The test (does it change behavior versus the
  default?) is model-relative, settled by running the document, not by debate.
  When a sentence fails, delete the whole sentence rather than trim words from
  it. A word too weak to beat the default (_be thorough_) is a no-op too; the fix
  is a stronger word (_relentless_).
- Grade a line by what it supplies before cutting it. Host behavior belongs in
  that host's adapter. Team policy and preferences stay, in one home, even when
  they differ from the model's default. An operational contract or an observed
  failure keeps the minimum that holds it. A volatile fact points to its current
  source.
- Pruning keeps **force**: actors, actions, scope, conditions, exceptions,
  obligation strength, quantity, authority and completion evidence. "Prefer"
  stays "prefer", a suggestion does not become a universal rule, a read does not
  become a write, and an attempted check does not become a successful one. Delete
  a rule as enforced elsewhere only after inspecting the actual configuration,
  execution path and coverage; brevity, a donor's score or a model's apparent
  knowledge cannot establish redundancy. Keep rare consequential constraints.
