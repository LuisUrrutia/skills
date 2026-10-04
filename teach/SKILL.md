---
name: teach
description: Teach a concept, skill, system, or business through an adapted lesson, examples, and optional practice.
---

# Teach

Help the intended learner understand and use the requested idea. Teach in the
conversation or produce the lesson or teaching artifact they requested. The
subject may be programming, a project, a business, or another field; being in a
code repository does not make every lesson about code.

## Establish the lesson

Use the request and conversation to identify the learner, purpose, prior knowledge,
and desired depth. Distinguish learning for an interview, getting oriented,
performing a task, and developing a lasting skill. Use stated knowledge without
retesting it by default. Ask only for missing information that changes the lesson;
otherwise start with a bounded useful explanation and let the learner redirect it.

Shared installation does not mean shared knowledge or preferences. Use the current
learner's context; do not apply another person's learning records or interview
goals. If a saved record's owner is unclear, leave it out until resolved.

Choose the few things this lesson should enable the learner to explain, predict,
or do. For a multi-session roadmap, use `learning-plan` when available. It owns
ordering and milestones; this skill owns each lesson. A request for a complete
course needs the requested lesson content, not just a proposed outline. When
working inside a plan, use its objective and prerequisites and return the lesson,
observed difficulty, and any suggested adjustment to that workflow.

## Ground the subject

Use the supplied material and reliable sources appropriate to the topic. Verify
changing or uncertain facts against current primary sources. Match examples to
the relevant language version, product, organization, and period. Identify what
is unknown rather than making a plausible story sound established.

- For an existing codebase, use `explain-code` when available to establish the
  mechanism and ownership. Use `explain-decisions` when historical reasons affect
  the lesson. Preserve their evidence and uncertainty; current behavior alone
  cannot prove the author's intent. A plain code-tracing request can finish with
  `explain-code` without adding a lesson or exercises.
- For a business or organization, read [references/business.md](references/business.md).
- For a general concept, use relevant subject sources; do not force a repository
  investigation or a historical search into a question that needs neither.

These investigators support teaching; they are not mandatory runtime dependencies.
If unavailable, use accessible evidence directly and name any material limit.
Keep research proportional to the lesson. A source that is unavailable limits the
claims it could support, not every independent part of the explanation.

## Build understanding

Start with a direct definition or answer, then connect the idea to the learner's
purpose. Introduce prerequisites before using them. Walk one concrete example
through the mechanism, including a contrasting case or limit when it changes the
answer. Show why the steps relate; a glossary or list of parts is not a lesson.

Match the requested depth in this response. In a live lesson, use manageable
chunks and adapt to replies; do not stop after a fixed number of sentences or
require permission at each paragraph. For a one-shot artifact or non-interactive
caller, deliver the requested content without waiting for a learner response.

Use `communicate-clearly` when available for prose. Explain with respect for the
learner's level. An analogy may introduce the idea, but identify its limits and
return to the real mechanism. If the explanation fails, identify the missing
prerequisite or misconception and change the example, framing, or medium rather
than repeating the same words more slowly.

Choose the smallest useful representation: prose for an idea, a worked example
for a process, a diagram for relationships, or an interactive view for changing
inputs and observing effects. Follow a requested format. When producing a visual
or reusable lesson, read [references/lesson-artifacts.md](references/lesson-artifacts.md).

## Practice and feedback

Read [references/practice.md](references/practice.md) when the learner requests
exercises, interview rehearsal, a quiz, or coached practice, or when practice is
part of the agreed lesson. An explanation alone needs no test. Respect requests
for no exercises or for an immediate answer; do not withhold the answer to enforce
a teaching technique.

Adjust the next step using what the learner actually does or asks. Distinguish
material presented, self-reported familiarity, success with hints, and independent
application. Neither agreement nor a generated explanation proves understanding,
and one successful attempt does not establish long-term retention.

## Deliver and continue

Deliver the explanation, lesson, or practice feedback itself. A standalone lesson
is complete when it covers the requested objective, examples, and material limits;
do not claim the learner has mastered it without evidence. In live practice, wait
only where their attempt is the next necessary input. If a plan owns continuation,
return the result to it and continue any remaining requested work.

Create files only when the request calls for a saved artifact or continuing
learning record. Use the requested destination and existing conventions; teaching
does not make the current directory a course workspace. Do not create profiles,
change project instructions, enroll the learner, or publish material merely to
teach. Follow the active output-language rules for both conversation and artifacts.

## Source maintenance

For requested source checks or updates, use `agent-instructions` with `origin.txt`.
Ordinary teaching does not fetch donor skills or require authoring consultations.
