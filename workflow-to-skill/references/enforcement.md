# Enforcement

Read this when a lesson could be enforced by code or the workflow proposes
automation: a bundled helper, a project check, or a rule that a type, lint or
test could enforce.

## Route the lesson

Route the lesson toward removing an invalid path or enforcing its invariant with
existing types, constraints, lint, or behavioral checks when the project supports
it, and name that enforcement's existing owner. Keep the judgment, reason, and
exceptions with their instruction owner. Remove a rule as redundant only after
verifying the actual enforcement and its coverage. If violations already exist,
distinguish preventing new ones from a separately scoped migration.

## Prove it

Hand over the existing execution owners, inputs, outputs, failure states, and
effects. Supply a minimized failing case and its expected rejection reason, plus a
valid nearby case and its expected acceptance. Use an observed failure when
available; otherwise reconstruct from the confirmed contract and label it as such.
Do not invent incident evidence.

Name the executor: the project's existing check owner implements project
enforcement under its own authorization; the writer implements a skill-bundled
helper. Either must run the check on both cases before claiming enforcement.

If a meaningful case or its expected outcome cannot be established, keep that
proof unresolved. An extraction-only result proposes the proof without making
unrequested repository changes.
