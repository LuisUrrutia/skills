---
name: arena
description: Use when comparing independent attempts at the same task and synthesizing a verified result.
---

# Arena

Run independent complete attempts at one task, compare them, choose a base,
incorporate useful parts, and verify the result. Use this when alternative
approaches or independent investigations justify the extra work. Splitting a
project into different subtasks is a separate coordination problem.

Arena owns the comparison. A selected specialist owns how each attempt does its
work. For specialist candidates, read
[references/specialists.md](references/specialists.md) before framing the task.
For requested source maintenance, use
[references/upstream-updates.md](references/upstream-updates.md).

## Frame

Establish the deliverable, scope, source revision or input snapshot, acceptance
requirements, and existing authority. Write a small task-specific rubric before
seeing candidates: correctness, coverage, maintainability, or other observable
criteria that distinguish a good result for this task. Give every candidate the
same requirements and grounding; keep comparison notes and emerging preferences
out of candidate prompts. A private rubric must not hide a requirement.
Derive hard constraints from the caller's requirements and applicable rules;
identify the source for each. Keep desirable implementation qualities as scored
preferences. Neither the rubric nor the judge may turn a preference into a new
reason for disqualification. Behavior outside the stated input domain can inform
a documented tradeoff, but is not a contract failure without a requirement.

Use the host's delegation mechanism and available model catalog. Honor requested
models, effort, candidate count, and budget. Otherwise start with two candidates;
different available model families can broaden the comparison, but two independent
contexts on one model remain useful. Report what actually ran. Do not guess model
identifiers or silently replace an explicitly requested model.

Choose an output location for each candidate and for the synthesis. Follow the
host's scratch, workspace, and ownership rules. Read-only candidates can share a
stable source snapshot. Code candidates need separate mutable targets: isolated
copies, patches against the snapshot, or workspaces provisioned through the
authorized lifecycle. Separate filenames do not isolate a shared checkout,
database, cache, or service. Arrange isolation before concurrent mutations; the
coordinator alone writes the integrated target.

If independent agents cannot be started, report the missing capability. Prepared
prompts or several answers written by the coordinator are not an executed arena.
When resuming from supplied candidates, label that starting point and verify their
scope and evidence without claiming to have generated them.

## Fan out

Give each candidate the same task, snapshot, requirements, selected specialist
contract, and tool authority, changing only its identity and isolated destination.
Ask for the complete artifact and a short rationale where the output contract
allows it. Do not seed candidates with another candidate's work or the intended
winner. Keep provenance and rationale outside a specialist's strict report format.

Tell each candidate and judge: "You are an arena participant. Do not invoke arena
or spawn further attempts." If already operating as such a participant, perform
the assigned single attempt instead of starting another arena.

Start candidates concurrently within the host's limits. If capacity requires
sequential execution, keep contexts independent and disclose the scheduling.
Track actual task IDs, models, status, and artifact paths. A finished turn with
live child work is not a completed attempt. Settle or cancel that work before
closing the run; do not leave writers active during comparison or integration.

Record failures and proceed with completed candidates. Retry a failed seat at
most once, only when its cause is recoverable within the existing budget. With
zero usable candidates, report the blocker. With one, verify it as a single
attempt: there is no comparative winner, cross-judge, or graft phase.

## Cross-judge and pick

After candidates stop writing, confirm their artifacts exist and use the agreed
snapshot. Freeze the compared versions. Start one independent judge with the
rubric and neutral candidate labels. Prefer a different available model family
from the coordinator when allowed; do not give it the coordinator's verdict.
The judge may inspect evidence and write its assessment, but must not edit the
candidates or integrated target. It scores each criterion and recommends a base.

Read every candidate end to end and assess it independently while the judge
works. Compare specific evidence and tradeoffs with its assessment. Agreement
does not confirm correctness; disagreement can reflect a defect, a missing fact,
or a legitimate tradeoff. Resolve material claims against sources or execution.
Check that the requirement behind a claimed defect actually applies; reproducing
a difference does not by itself establish which behavior is required.
Exclude artifacts that fail required constraints. Among suitable bases, prefer
coherent boundaries and the smaller sufficient API over gratuitous machinery.

If the judge is unavailable, disclose "no independent judge" and make a bounded
coordinator assessment. A request requiring that judge remains incomplete. Do
not invent a verdict or present a parent assessment as an independent one.

## Graft

Inspect useful ideas in the other candidates and incorporate only what improves
the chosen base under the same contract. Integrate deliberately; do not paste
incompatible architectures, contradictory claims, or duplicate findings together.
Record the source candidate for each graft and why significant alternatives were
rejected. No graft is needed when the base already contains the useful result.

For investigations, consider the union of substantive findings, then trace their
evidence. Keep a supported minority finding and reject a shared false positive.
Preserve unresolved premises and coverage gaps. Neither vote counts nor the
judge's confidence upgrade a claim's evidence level.

Divergence alone does not prove that the task was underspecified. Reframe only
when it exposes a material ambiguity, then reassess all candidates consistently.
Allow at most one new round within the authorized budget; surface a decision that
requires the user rather than running an unbounded contest.

## Verify and deliver

Check the integrated artifact itself against acceptance requirements and relevant
project checks. Candidate test results do not establish that grafts work together.
For an analysis, verify the decisive evidence and retain its actual limits. A
format validator checks structure, not whether a finding is true. Fix an observed
integration defect and repeat the affected checks; do not rerun the entire arena
without evidence that the framing failed.

Return the requested artifact plus a short synthesis note: input snapshot, actual
candidates and completion states, judge assessment or absence, chosen base,
grafts, meaningful rejections, verification evidence, and remaining limits. Keep
the note separate when the artifact has a strict grammar. Retain task IDs and
artifact paths so the execution can be checked. If the caller requires an exact
handoff line or machine-readable response, save the synthesis note beside the
artifact and return only that required response, without an appended explanation.
Record partial or unverified results in the permitted output. Comparison grants
no extra repair, publication, or deployment authority.
