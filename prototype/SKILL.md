---
name: prototype
description: Use when prototyping a UI, state model, or uncertain behavior before implementation.
---

# Prototype

Build a disposable experiment to resolve one question. Return the artifact,
observations, and a recommendation with its limits. This skill works directly
from the user's request; it needs no work-mode state or upstream skill.

## Frame the experiment

Read the relevant project instructions, existing behavior, and supplied context.
Identify the question, constraints, and what observation would distinguish the
options. State these briefly in the artifact or result. Use the available context
before asking for a missing decision that would materially change the experiment.

If the request already specifies an implementation or a bug to fix, do that work
under its normal workflow. Use a prototype within it only when an unresolved
question warrants an experiment; do not invent alternatives for a settled choice.

Choose the cheapest artifact that can answer the question faithfully. Load only
the relevant reference; combine them only when the question needs both surfaces:

| Question | Reference |
| --- | --- |
| Can this model represent the required states and transitions? | [references/logic.md](references/logic.md) |
| Which layout, hierarchy, or interaction serves the task? | [references/ui.md](references/ui.md) |
| What does this approach actually do, or how does it behave under a workload? | [references/experiment.md](references/experiment.md) |

## Build and observe

Keep disposable work in the repository's permitted scratch location; here that
is ignored `.tmp/<task>/`. Preserve a requested deliverable at its requested or
established destination. Label the artifact as experimental and make it easy to
run with exact commands or an opening path, including required setup.

Use in-memory or fixture data unless persistence or integration is the question.
Stub mutations that are irrelevant to it. A necessary real side effect still
needs authority from the active task. Keep experiments separate from production
behavior; a prototype request does not authorize changing the live application.

Use existing components, frameworks, or domain skills when their behavior matters
to the decision. Load only relevant guidance. Avoid building production
infrastructure for an experiment, but retain checks and error handling needed to
trust the result and satisfy project rules. For plain HTML, use semantic markup
and external CSS unless the requested deliverable calls for another format.

Run the experiment and inspect the matching surface. Record observed results,
including failures and counterexamples. Separate measurements from assumptions
and simulated behavior from real integration evidence. If a required tool or
input is unavailable, report the missing observation and what remains unresolved;
do not replace it with a claimed successful run.

## Deliver and stop

Return:

- The question and the options actually explored.
- The artifact path and exact instructions to open or rerun it.
- Observed evidence, relevant conditions, and limitations.
- A recommendation and tradeoffs, or the specific uncertainty still unresolved.

Stop when the evidence supports a bounded decision, or when a missing input,
preference, or inconclusive result prevents one. Do not keep adding variants once
they no longer help answer the question. Preserve the artifact and evidence needed
for the handoff; remove only your obsolete scratch files and report anything
retained temporarily.

Production implementation, promotion of prototype code, archive branches, issue
updates, and PRs are separate work. This skill does not start them automatically.
Return to the caller if the wider task already authorizes the next phase; do not
add another approval gate. Reused code needs normal implementation and validation.
Applicable repository commit rules still govern this task's own deliverables.

For a requested source check or update of this skill, read
[references/upstream-updates.md](references/upstream-updates.md). For evaluation
of this skill itself, use [evals/cases.json](evals/cases.json); keep its expectations
out of executor inputs. Neither reference is needed to run a prototype.
