# Focused review support

Read this when a specific uncertainty needs another available skill. Keep its
work inside the current review's scope and permissions; using a specialist does
not authorize editing, installing dependencies, contacting people, or publishing.
Use the returned evidence with its limits and reconcile it with the protocol.

| Review question | Support and requested result |
| --- | --- |
| How does this path work, and who owns its state? | `how`: a bounded mechanism and ownership trace. |
| Why does this consequential guard or constraint exist? | `why`: historical evidence, distinguished from inference and current necessity. |
| Could this changed contract break an indirect consumer? | `analyze-change-effects`: the deciding assumption, trace, and permitted probe. Preserve caller-owned seams and inspection-only limits. |
| Is there a concretely better model or boundary? | `design-code-structure`: a design-only comparison grounded in current callers; no implementation or repository-wide redesign. |
| Is a proposed cleanup useful and behavior-preserving? | `simplify-code`: explicitly review-only recommendations and equivalence constraints. |
| Does application behavior support the author's claim? | `verify`: only the permitted checks from the relevant local recipe; report required mutations or missing prerequisites instead of performing them during review. |
| Does the diff reach domain-specific rules? | Select the installed specialist for that domain, such as `github-actions`, `agent-instructions`, or applicable React guidance. Request a review of the relevant contracts, not its edit workflow. |

Do not load every skill for every diff. Domain advice must match the actual
framework/version and project conventions. A specialist's checklist does not
turn an irrelevant recommendation into a defect.

For independent audits, the caller can use `compare-solutions` with the same
scope snapshot, intent, standards, caller-owned seams, this skill version, and
separate report destinations. Candidates remain independent reviewers; the
coordinator rechecks disputed evidence and validates the combined report. Votes
do not establish correctness or severity.
