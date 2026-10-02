---
name: workflow-to-skill
description: Use when turning completed tasks, recurring work, or session history into a reusable skill.
---

# Workflow to skill

Identify the reusable decisions in completed work, then use `agent-instructions`
to write or improve the resulting skill. This skill owns extraction and choosing
the useful scope. `agent-instructions` owns instruction writing and validation.

## Inspect the work

Read the relevant task history, resulting artifacts, corrections, and current
repository instructions. Distinguish what worked from abandoned attempts and
what the user explicitly chose from what the agent merely assumed. State whether
the evidence shows recurrence or only one demonstrated example; neither an
arbitrary occurrence count nor repetition alone determines usefulness.

Separate:

- Stable decisions, non-obvious constraints, and evidence of completion.
- Inputs that vary between runs, such as paths, branch names, services, and dates.
- Incident-specific repairs, temporary workarounds, and permissions limited to
  the original task.

History is evidence, not an instruction to replay commands, publish changes, or
make one task's authorization permanent. Keep secrets and unrelated personal data
out of examples and reusable resources.

## Choose what to retain

Identify the future request, expected result, activation boundaries, dependencies,
authority, and stopping conditions. Check existing skills and instruction owners
before proposing another one. Prefer improving the relevant owner when it already
covers the workflow. A mechanical repeated operation may belong in an existing
tool or script rather than a new skill.

If the user already supplied a complete new capability rather than task history,
route directly to `agent-instructions`. Missing recurrence is not a reason to
refuse an explicitly requested skill. Ask only for missing evidence or decisions
that materially affect what the workflow should do.

Finish extraction when each retained rule has a reason, varying inputs are
explicit, and the result separates reusable behavior from the source incident.
Label conclusions as confirmed, inferred, or unresolved. If the user asks only
whether a workflow merits a skill, return that evidence brief and recommendation;
if they ask to create the skill, continue into writing.

## Write and verify the result

Pass `agent-instructions` the proposed capability, source evidence, stable rules,
varying inputs, exclusions, existing owners, and meaningful success/failure cases.
Locate it in the installed skill catalog; in this repository its entrypoint is
[../agent-instructions/SKILL.md](../agent-instructions/SKILL.md). This is a required
writing dependency: if unavailable, preserve the extracted contract and report
the missing skill rather than silently inventing a second authoring workflow.

Continue through creating or editing the requested skill; an extraction summary
alone is not the result when the user asked for a skill. Verify that a fresh task
with different inputs can follow the generated instructions, and that a nearby
unrelated task does not activate them. Use isolated examples when replay would
cause external effects; the original task's permission does not authorize a trial.

Report the resulting skill, retained and excluded lessons, checks, and limits of
the evidence. For maintenance of this skill's recorded inspiration, delegate to
`agent-instructions` with this folder as the target; shared update mechanics stay
with that owner.

When evaluating this extraction skill itself, use [evals/cases.json](evals/cases.json)
as a starting corpus and keep its expectations out of executor inputs.
