---
name: write-documentation
description: Use when creating, updating, or reviewing human-facing documentation, including guides, READMEs, API references, runbooks, and decision records.
---

# Write documentation

Create documentation that lets its intended reader understand or complete a task
from accurate, findable information. `communicate-clearly` owns prose and voice; load
it when available and not already active. This skill owns documentation
structure, source accuracy, examples, and validation. `agent-instructions` owns
instructions for agents.

## Find the reader, source, and destination

Establish the reader, their task and prior knowledge, the output language, and the
product version or state being described. Infer these from the request and existing
documentation; ask only about a material unresolved choice. A small correction does
not need a planning interview.

Read the complete target, relevant neighboring pages, navigation, and writing
conventions. Locate the canonical source before creating another page. Preserve
useful existing structure, generated-file ownership, and user edits. Make review
findings or a draft when requested; edit files only within the authorized scope.

Check behavior, defaults, commands, limits, and terminology against the relevant
code, configuration, tests, approved decisions, or current primary documentation.
Keep current behavior distinct from proposals, planned releases, historical
decisions, and unknowns. Code can establish behavior without proving why it was
chosen or whether it is approved policy. Surface consequential contradictions
instead of silently resolving them in favor of whichever source is newest.

## Organize for the task

Use reader needs to choose the structure: guided learning, completing a known task,
looking up a fact, or understanding an explanation. These Diataxis distinctions can
apply to sections. Keep a useful mixed README or existing page intact rather than
forcing a new file for every type.

Read [references/document-types.md](references/document-types.md) for the relevant
document's checks. Lead with what the page lets this reader do or understand. Place
prerequisites and consequential conditions before the actions they govern. Use
descriptive headings, ordered steps where order matters, and links to deeper
explanation when it would interrupt the task. Include enough context to understand
the step; a how-to guide need not be unexplained commands.

Follow the project's language and framework. Examples should demonstrate the
documented contract with the smallest sufficient setup. Distinguish runnable code
from illustrative fragments and name any omitted context. Preserve identifiers,
placeholders, required markup, units, and version-specific behavior.

Use screenshots, diagrams, or tables when they clarify a state, relationship, or
comparison. Verify that their labels and depicted behavior match the relevant
version; provide meaningful text alternatives. Assets are supporting evidence, not
proof that the instructions work.

## Verify what the reader will use

Follow the documented path your change affects, in order, using safe local fixtures
or an appropriate test environment within the active authorization. Check
prerequisites, commands, inputs, expected output, and how the reader recognizes
success. Run applicable documentation build, link, schema, and example checks from
the project. Use its established generator for generated documentation instead of
editing derived output.

A documentation request does not authorize a production migration, deployment,
message, or destructive operation just because a guide contains its command.
Validate such steps in an authorized disposable environment or report what remains
unverified. Distinguish static inspection, compilation, execution, and observed
application behavior; do not infer one from another or manufacture passing evidence.

Read the result without relying on private conversation context. Can a reader with
the stated prerequisites find the entry point, supply the required inputs, follow
the path, and recognize the outcome? For complex or high-consequence guides, an
independent reader check can expose hidden assumptions when available and
authorized. Treat model feedback as a check of this sample, not proof of universal
comprehension. Repair gaps and rerun the affected checks.

## Integrate and finish

Update affected navigation, local links, and examples within scope. When moving a
published page, account for existing links and the site's redirect mechanism; do not
move it merely to impose a preferred taxonomy. Keep requested language versions
aligned on meaning and behavior, adapting natural wording rather than translating
the source language's syntax mechanically. Report any unupdated versions and why.

Documentation maintenance does not by itself create a new docs platform, glossary,
CI workflow, policy file, or publication step. Use established owners and
conventions and propose a separate material change when one is actually needed.

Deliver the requested artifact or review. For file changes, report the paths,
material content changes, exact checks and outcomes, and unresolved gaps. Finish
when the content serves the reader's task, source claims are supported or explicitly
qualified, applicable checks pass, and any unavailable validation is stated.
