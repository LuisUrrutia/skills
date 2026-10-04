---
name: explain-code
description: Use when explaining how existing code works or which component owns a behavior.
---

# Explain code

Explain an existing system from its source: what happens, which component owns
each responsibility, and where the behavior lives.
Use this skill directly; no coordinator or upstream skill is required.

## Establish the question

Use the question, conversation, and repository to identify the behavior and the
reader's purpose: getting oriented, understanding a mechanism, or finding an owner.
Use their question to choose the technical depth. State a useful scope when the
request is broad; ask only when an unresolved ambiguity would materially change
the answer.

Keep neighboring tasks distinct. Investigating an observed failure belongs to
debug; reconstructing a historical decision belongs to `explain-decisions`.
For a mechanism changed by a branch or commit, resolve the requested revision
and explain the relevant before and after behavior from the diff and source.
Do not turn that explanation into a review or a general activity report. Explain the
requested mechanism without silently starting repairs, a diff audit, or a course.
If the request combines tasks, preserve them and their existing owners.

## Trace the mechanism

Find the entry point and read the actual implementation. Follow the relevant
calls, data transformations, state changes, and boundaries until the requested
behavior is accounted for. Check the callers, configuration, and tests that decide
which path is active; names and an isolated function are insufficient evidence.

For a cross-component question, split the exploration into useful angles such as
request handling, state ownership, and background work. Investigate directly.
Parallel exploration is optional only when the host and task authorize it; it
must preserve the same scope and read-only authority. Reconcile findings against
the source before presenting them. Do not require particular models or tools.

Separate what the code establishes, what a test or execution actually demonstrates,
and what remains an inference. Read-only inspection does not establish production
configuration, external service guarantees, or runtime success. Identify missing
connections and conflicting documentation instead of filling them in. Use current
primary documentation when an external API's semantics are needed to explain the
path, matching the project's version.

Keep guarantees at the boundary the evidence covers: an internal status or a
provider's acknowledgement does not establish later delivery or user-visible
success. State the condition when a subsequent worker or external system must act.

Keep source, tests, configuration, and remote state unchanged. Observe execution
only when necessary and within the task's authority and safe local setup; reading
a test does not mean it passed. A requested explanatory artifact may be written
at its agreed destination. Do not create lesson files, learning records, or other
persistent infrastructure merely to answer a question.

## Make the explanation usable

Answer the question first, respecting the requested depth and length in this response.
Define necessary terms in place and follow a representative input or user action
through the actual components. Include a branch, failure path, or state transition
when it changes the answer. A list of functions is a navigation aid, not the
explanation of their relationship.

Use a diagram, small example, or excerpt when it clarifies that relationship.
Keep it consistent with the real path and distinguish illustrative inputs from
observed execution. Scale the format to the question; a narrow answer needs no
fixed sections. Guided teaching and exercises belong to `teach`; study plans belong to
`learning-plan`. Use them when requested, not for every explanation.

Put source locations beside the claims they support, with a short navigation map
only when it helps the reader continue. Distinguish a component's present function
from its authors' historical reasons. Include a documented reason when relevant,
but preserve its attribution and uncertainty. Code shape alone does not prove
why the design was chosen. A recommendation about where new behavior should live
must be labeled as advice grounded in observed ownership and conventions.

Finish when the requested path, ownership, and material limits are explained, or
when an inaccessible prerequisite limits the answer. State what remains unknown
and which evidence would resolve it. Deliver the explanation itself rather than
an activity report.

## Source maintenance

When asked to check or update this skill from its sources, read
[references/upstream-updates.md](references/upstream-updates.md). Ordinary
explanation does not fetch upstream or require another skill.
