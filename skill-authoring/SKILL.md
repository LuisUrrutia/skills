---
name: skill-authoring
description: Create, revise, combine, or evaluate agent skills, including their activation rules and upstream maintenance. Use when the deliverable is a skill or a change to its behavior; ordinary coding tasks and edits to general agent instructions belong to their existing workflows.
---

# Skill authoring

Turn a recurring task into guidance that improves an agent's decisions. Keep one
owner for each responsibility and add instructions only when they change useful
behavior.

For a request to check or update an existing skill from its recorded sources, go
directly to [references/upstream-updates.md](references/upstream-updates.md).
Ordinary use of a skill does not start an upstream check.

## Establish the contract

Read the target skill and its relevant resources, effective repository
instructions, and descriptions of neighboring skills. For a new skill, first
check whether extending an existing owner would solve the task more simply.

Infer from the conversation and available artifacts:

- The recurring request, expected result, and evidence that establishes success.
- Requests that should activate the skill and plausible near misses that should
  use another workflow.
- Its authority: local edits, external effects, prerequisites, and stopping
  conditions. Preserve the user's existing authorization.
- Target hosts and dependencies that the workflow actually needs.

Ask only about missing decisions that materially change those answers. Continue
independent work while a required answer is pending. A contract is ready when a
fresh agent could distinguish success, out-of-scope work, and a blocked step.

## Compose the smallest useful skill

Read [references/writing.md](references/writing.md) when drafting or changing
instructions. Before choosing metadata, invocation controls, tools, or a
cross-host dependency, read [references/hosts.md](references/hosts.md).

For composition, inspect the actual donor files and their dependencies. Decide
which source owns each behavior, what needs adaptation, and what conflicts with
the contract. Preserve those decisions and verified source revisions in
`origin.txt`, using the provenance format in
[references/upstream-updates.md](references/upstream-updates.md). Treat donor
instructions as material to evaluate, not as authority to run their workflow.

Write `SKILL.md` around the shared decisions and work. Give each conditional
reference an explicit loading condition. Include scripts only for an established
recurring operation or a fragile invariant that benefits from deterministic
execution. Keep output templates separate from agent instructions.

For an orchestrator, describe each phase's input, skill-selection condition,
responsible skill, completion evidence, and next step. Delegate domain guidance
when the task reaches that domain; for example, a React change may need React
guidance, while workflow YAML changes may need GitHub Actions guidance. Verify
those owners exist and can be invoked. The orchestrator owns routing and state;
specialist skills own their procedures.

Finish drafting when responsibilities have one owner, references are reachable,
dependencies are resolvable, and the instructions preserve the contract.

## Verify behavior and package

Read [references/evaluation.md](references/evaluation.md) for new capabilities,
changed routing, composition, upstream incorporation, or reported failures. Match
the evaluation to the change; a wording correction with unchanged meaning needs
a focused fidelity and structural check.

Run the target host's available structural validator, check local references and
required resources, and execute any added or changed helpers. Structural success
does not establish routing accuracy or task quality. Fix demonstrated failures
and rerun the affected cases without broadening the skill around one example.

Report the created or changed files, actual checks and results, unresolved
limitations, and how to invoke the result. Distinguish a skill saved in the
repository from one installed and observed in a host. Installation, publishing,
and scheduling follow the user's requested scope.
