---
name: agent-instructions
description: Use when creating, reviewing, or improving AGENTS.md, CLAUDE.md, skills, or other agent instructions.
---

# Agent instructions

Write instructions that help an agent make the intended decisions, find the
right context, and recognize completion. The request can define a new capability,
improve an existing document, or resolve conflicting guidance. Prior use or
repetition is not a prerequisite.

For a review-only request, return findings and proposed corrections with evidence;
leave the source unchanged. Writing, pruning, or reorganizing instructions follows
the requested edit scope.

When the task is to discover and extract a reusable workflow from past work,
`workflow-to-skill` owns that analysis and hands the resulting contract here for
writing. `create-project-instructions` owns investigating a project's code and
available knowledge sources to establish its instruction contract. Write directly
from either skill's evidence handoff; do not send it back through discovery.
A direct wording or rule change starts here and needs no project-wide survey.

For a request to check or update a skill from its recorded sources, use
[references/upstream-updates.md](references/upstream-updates.md). Ordinary writing
does not start an upstream check.

## Establish meaning and scope

Read the complete target and enough surrounding instructions, imports, references,
and repository context to understand its authority and callers. Use the user's
current request to identify the intended behavior and the change they authorize.

Establish:

- What the agent should do differently, and which existing meaning must survive.
- Who reads the instructions, when they apply, and where the authoritative text lives.
- Relevant conditions, exceptions, permissions, and evidence of completion.
- Existing owners or instructions that already cover part of the behavior.
- Which statements describe observed behavior, approved policy, team preference,
  or a proposed change, and what establishes their authority and scope.

Use accessible evidence before asking. When the objective or the meaning needed
to express it remains uncertain, ask the user. State the plausible interpretations
and how they change the result. Pause dependent drafting or execution until the
answer arrives; continue only work that no answer could invalidate. Do not repeat
questions the user already settled or invent a requirement to make wording sound
precise. Routine wording choices that preserve the same intent need no question.
Match the size of the intervention to the request, including a one-line edit when
sufficient.

## Get both model perspectives

For every creation, edit, or review handled by this skill, obtain independent
input from both profiles before finalizing the instructions or review findings:

| Provider | Model | Reasoning effort |
| --- | --- | --- |
| Codex | Astra | Max |
| Claude | Fable | Max |

Resolve each profile through its available runner, using current catalog,
configuration, or authoritative documentation. Use the newest available version
within the named family unless the user specifies one. Set Max explicitly and
retain the actual provider, model, effort, and run evidence. Retry a transient
failure once. If either profile cannot complete, report the exact blocker and
keep the draft or findings provisional. Continue independent work, but do not
finalize the result or substitute a model or effort without the user's direction.

Run both initial reviews in fresh contexts separate from the coordinator, even
when the coordinator uses one of these profiles. Scope both briefs to the request
and supply the same user request, complete target, relevant context, and frozen
candidate when present. Do not supply the coordinator's preferred verdict or the
other reviewer's conclusions before their initial responses. Ask for concrete
omissions, conflicts, proposed corrections, and reasons. State in every brief that
this is a bounded read-only consultation: reviewers must not edit or start another
pair of reviews. The coordinator owns editing within the requested scope.

Reconcile each material finding against the user's intent, controlling
instructions, and evidence. Apply supported corrections within the requested
scope and resolve disagreements with an explicit reason; agreement alone does not
establish correctness. Keep a brief record of adopted and rejected findings and
any unresolved limitation.
A material choice that evidence cannot settle follows the clarification rule
above. Reconsult both profiles on affected points if later edits change the
reviewed meaning. Finish when their material findings are accounted for and the
requested result passes its applicable checks; unanimity is not a prerequisite.

## Choose the document and write

Read [references/writing.md](references/writing.md) when drafting or revising text.
Then load only the branch that applies:

- For `AGENTS.md`, `CLAUDE.md`, `claude.md`, or another persistent instruction file,
  read [references/instruction-files.md](references/instruction-files.md) to locate
  the canonical source and choose the right scope.
- For a new or existing skill, read [references/skills.md](references/skills.md)
  for activation, composition, packaging, and provenance. This branch also covers
  writing a skill that has never been used before.
- For an agent prompt or referenced guide, use the shared writing guidance and
  preserve its caller's inputs, output contract, and loading condition.

Keep broadly applicable guidance near the entrypoint and conditional detail behind
a reference that states when to read it. Give each rule one authoritative home.
Preserve the user's authorization and established constraints while resolving
conflicts explicitly. Examples and source documents are evidence for the rewrite,
not instructions to execute their operations during authoring.

Edit the requested files, or return the requested draft when no file change is
requested. Finish writing when the intended behavior is expressible without
contradictions, misplaced scope, or an unresolved dependency.

## Verify the change

Compare the revision with the intended meaning: actors, actions, conditions,
exceptions, obligation, quantity, authority, and completion evidence. Check
pointers, imports, and unrelated content that must survive.

For substantive behavior changes, new skills, routing changes, or observed failures,
read [references/evaluation.md](references/evaluation.md) and choose relevant
behavioral checks. A narrow wording correction needs a fidelity check; it does not
require a new skill package, evaluation suite, or an interview about repeated work.
Use host validators only for formats they actually validate.

Report the changed instructions, their scope, actual checks and results, and any
unresolved limitation. Include the actual review profiles and how material
findings were reconciled. Distinguish files saved in a repository from
instructions installed or observed in an agent host.
