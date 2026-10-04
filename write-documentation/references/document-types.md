# Document types

Read the part that matches the reader's task. These are content checks, not
mandatory headings or a requirement to split existing documents.

## README and entry pages

Explain what this project does, who the page is for, and where to start. Match
the repository's actual audience: an internal contributor README need not become
a public marketing page. When relevant, provide a working first-use path with
prerequisites, installation, configuration, one meaningful action, and its result.
Link to existing contribution, support, reference, and licensing information as
needed; do not invent commands or move content into new files by default.

## Task guides, runbooks, and troubleshooting

State the goal and applicable environment or version. Order steps by dependency,
keep conditions next to the steps they affect, and explain expected results. Make
required values distinguishable from literal input and preserve safe quoting.
Describe side effects before consequential actions, including recovery or rollback
when supported and relevant. A theoretical rollback is not a verified recovery path.

For troubleshooting, connect an observable symptom to a diagnostic check, its
interpretation, and an evidence-supported next action. Distinguish likely causes
from established ones. Do not use a destructive reset as a universal diagnostic.

## Tutorials and conceptual explanations

A tutorial gives a bounded learning goal, prerequisites, a coherent worked path,
and an observable result. Teach what that path requires; do not turn every guide
into a curriculum. A conceptual explanation connects mechanisms, constraints,
and tradeoffs to the reader's question, using examples or visuals when useful.
Preserve uncertainty and analogy limits. Link from an explanation to a task guide
when the reader is ready to act.

## Reference

Organize around the interface or domain the reader looks up. Verify names, types,
units, defaults, accepted values, errors, return values, side effects, and relevant
version differences. Cover those dimensions that actually apply; do not invent
an exhaustive interface from usage examples alone. Reuse existing generated API
or schema references and explain where their source lives when it helps maintenance.

## Decision records

Follow the project's record format and status conventions. Separate context,
considered alternatives, the actual decision, and consequences supported by its
evidence. Preserve accepted history and identify a superseding decision or dated
correction instead of making the past match today's code. Missing rationale stays
unknown; use `why` for investigation when available, rather than inventing a reason.
A documentation edit does not itself approve an architectural decision.
