# Writing instructions

Use this reference when writing or revising any instruction an agent consumes.

## Put decisions where they are needed

An entrypoint or pointer determines when an agent reaches detailed guidance. Name
the task and its distinct conditions. In a skill, the description does this work;
in a persistent instruction file, a scoped rule or reference does. Use exclusions
for likely collisions rather than making every instruction more insistent.

Keep instructions needed on every path in the entrypoint. Move substantial guidance
used only on one path into a reference. A useful pointer states both the condition
and the file to read: "When changing workflow YAML, load the GitHub Actions skill."
Writing "see references" leaves the selection decision unspecified.

Keep each rule, its reason, and its exceptions together. Give each behavior one
authoritative home. Restating a specialist's procedure in an orchestrator creates
two versions to maintain; name its input and completion evidence instead.

## Choose words for their intended effect

Use familiar terms and direct verbs. Check literal meaning and connotations:
words can imply an obligation, breadth, effort, certainty, or permission that the
user did not intend. "Prefer" and "require", "create" and "run", or "one" and
"all" produce different behavior; they are not interchangeable in a rewrite.
Explain a non-obvious constraint once. Prefer the desired action over a list of
prohibitions; retain boundaries that protect authority, scope, or correctness.

Make type, scope, quantity, depth, and completion evidence explicit where they
distinguish plausible interpretations. For "create tests", establish what behavior
or risk the tests must check, the relevant level (unit, integration, end-to-end,
or smoke), whether to write or run them, and sufficient coverage or quantity.
Use the user's objective and established context; an installed framework alone
does not settle these choices. Ask the user about intent that remains unclear
before encoding a test level, quota, or depth. Preserve room for judgment within
the confirmed objective.

## Choose the form from the observed failure

When correcting a failure, inspect the output and action trace before adding a
rule. Check loading evidence before attributing the failure to an unread or
unclear instruction. An unread rule needs a selection or placement fix. If
loading is unobserved, report that limit while correcting defects visible in
the text.

| Observed failure | Useful correction |
| --- | --- |
| The result has the wrong structure or order | Describe the required parts in the order the reader needs them. |
| A required element is missing | Give it a named field or slot in the existing output structure. |
| A rule is applied in the wrong circumstances | State an observable condition and the action for each relevant branch. |
| An understood requirement is bypassed | State the boundary and address the observed shortcut; test it under the relevant pressure. |

Preserve material exceptions when making conditions explicit. Add counters for
observed workarounds only; a growing prohibition list is not a substitute for a
clear output contract.

## Make progress observable

Describe actions with enough freedom for the task. Use fixed sequences where
ordering protects an invariant, such as verifying an identity before a remote
write. Give open-ended work a result and decision criteria instead of a ritual.

End meaningful phases with evidence that distinguishes completion from an
attempt. "Understand the failure" is weak; "reproduce the failing behavior or
identify the inaccessible prerequisite" lets the next phase start honestly.
For loops, state what progress means, what ends the loop, and what happens when
the same blocker persists.

Separate the reusable workflow from domain decisions that the sources do not
establish. A missing schema, rounding policy, or rule for dropping records is a
contract to resolve, not a default to invent. Tell the future agent where to find
that contract and when an unresolved choice requires a question. Labeling an
invented default as an assumption in the completion report does not prevent the
generated skill from applying it later.

## Resolve conflicts before combining

For each overlapping instruction, compare trigger, responsible owner, action,
completion evidence, and authority. Similar wording can hide incompatible
behavior: a read-only review and a repair workflow need different mutation scope.

Resolve conflicts from established authority, scope, or an explicit user decision.
If those do not establish the intended behavior, ask the user before combining the
affected rules. Once intent is clear, keep the governing rule or state distinct
conditions. Record intentional deviations from donors in the existing provenance
record when maintaining a derived skill.
For other documents, preserve their established attribution conventions rather
than adding skill-specific files. Source popularity is not a reason to replace
a local rule that serves the contract. Pay particular attention to changes in
invocation, approvals, testing, tools, and external writes.

Keep common procedures in the existing owner. Split a new skill only when it has
a distinct task or needs independent invocation. Use a conditional reference for
detail that belongs to the same task.

## Prune without weakening the contract

Remove repeated meanings, generic encouragement, and instructions already
supplied by an authoritative local owner. Read configuration and CLI help for
facts the environment can supply; document the reason or gotcha it cannot.

Check the revision against the original actors, actions, conditions, scope,
exceptions, and evidence. Shortening must not turn a suggestion into a universal
rule, a read into a write, or an attempted check into a successful one.
