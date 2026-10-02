# Writing instructions

Use this reference when writing or revising a skill's behavior.

## Put decisions where they are needed

The description helps select the skill. Name the task and its distinct activation
conditions; add exclusions for likely collisions. Test discovery against nearby
skills instead of making every description more insistent.

Keep instructions needed on every path in `SKILL.md`. Move substantial guidance
used only on one path into a reference. A useful pointer states both the condition
and the file to read: "When changing workflow YAML, load the GitHub Actions skill."
Writing "see references" leaves the selection decision unspecified.

Keep each rule, its reason, and its exceptions together. Give each behavior one
authoritative home. Restating a specialist's procedure in an orchestrator creates
two versions to maintain; name its input and completion evidence instead.

## Make progress observable

Describe actions with enough freedom for the task. Use fixed sequences where
ordering protects an invariant, such as verifying an identity before a remote
write. Give open-ended work a result and decision criteria instead of a ritual.

End meaningful phases with evidence that distinguishes completion from an
attempt. "Understand the failure" is weak; "reproduce the failing behavior or
identify the inaccessible prerequisite" lets the next phase start honestly.
For loops, state what progress means, what ends the loop, and what happens when
the same blocker persists.

Use familiar terms and direct verbs. Explain a non-obvious constraint once.
Prefer the desired action over a list of prohibitions; retain explicit boundaries
when crossing one changes authority, scope, or correctness.

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

Select one rule or introduce an explicit condition. Record intentional deviations
from donors in `origin.txt`, especially defaults for invocation, approvals,
testing, tools, and external writes. Source popularity is not a reason to replace
a local rule that serves the contract.

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
