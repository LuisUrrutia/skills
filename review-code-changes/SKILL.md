---
name: review-code-changes
description: Review a PR, branch, commit, or local changes for defects, unmet requirements, and code-quality regressions.
---

# Review code changes

Review one declared change and deliver findings supported by its actual code,
requirements, and contracts. Apply the project's language and runtime semantics.
This phase preserves product files, tests, the index, HEAD, and remote state.
Write reports and permitted probes in the caller's output or scratch location.
An enclosing implementation task can act on the findings after this review ends.

Read [references/protocol.md](references/protocol.md) before reviewing. It owns
the review criteria, evidence rules, severity, and canonical report grammar.
A caller that runs this audit in an engine unable to load skills may freeze that
protocol and `scripts/report.py` unchanged into its run packet, supplying its own
single-auditor role in place of this entrypoint's orchestration.

## Establish a reproducible scope

Honor the supplied comparison. Resolve refs to commit IDs and record the commands
and path inventory before reviewing:

- For a branch or PR, establish its actual target base from the caller or PR/repo
  metadata and use its merge-base with the head. An upstream tracking branch may
  be the PR's own head. Exclude earlier layers of a stack and unrelated base work.
- For a commit, inspect that commit's patch. Resolve the intended parent for a
  merge commit when different choices would change the review.
- For local changes, inspect staged and unstaged diffs and relevant untracked
  files. Record both intermediate and final states when staging changes behavior.
- For a supplied diff or file list, keep that exact boundary; surrounding code
  supplies evidence, not permission for a whole-repository audit.

For an unspecified scope, use current worktree changes when present; otherwise
resolve the current branch's target base from accessible context. Ask only when
the unresolved choice materially changes what is reviewed. An empty scope is a
valid result: report it instead of inventing work.

Save the unique changed-path inventory as a JSON array for report validation.
Record deleted paths and the new path of a rename, identifying the old path in
Coverage. Capture Git state so concurrent edits or accidental mutations are
detectable. If the input changes during review, refresh the affected analysis or
report that the result covers the earlier snapshot.

## Gather intent and review

Read effective repository instructions, the supplied request, relevant tests,
and accessible specifications. A PR body, ticket, author summary, and existing
test describe claims to check; they do not prove correctness. Mark a missing
specification as a limit while continuing the supported review. Do not invent
product requirements to fill it.

Review both intended behavior and applicable standards. Then apply the protocol
to every changed path and follow relevant callers, producers, consumers, schemas,
configuration, and dependencies beyond the diff. Use bounded discovery that
includes ignored or generated contract files where they govern the changed code.
Respect caller-owned boundaries and name the exact missing premise.

Review tests for what they actually establish. Run useful existing checks only
when their effects fit the review's permissions. Keep experimental mutations in
an authorized isolated copy; never alter the reviewed code to test a theory.
An unavailable check limits its claim, not independent inspection.

After forming the independent assessment, consider supplied or accessible PR
feedback when it adds relevant evidence. Validate each claim against the reviewed
revision, deduplicate shared causes, and attribute retained external findings.
Stale comments, agreement among reviewers, and author confidence are not proof.
Reading feedback does not authorize replies, resolution, repairs, or publication.

When reviewing a later revision of the same change, resolve the previous reviewed
snapshot and compare it with the current one. Keep the caller's declared scope;
the since-last-pass delta is context, not a replacement for that scope. After the
fresh assessment, reconcile earlier findings and skipped asks with current
evidence. Check factual skip reasons against the current snapshot. Record a
declined optional suggestion in Review basis rather than repeat it as a finding,
unless new evidence changes its basis. Deferring a supported defect does not
resolve it. Use the protocol's report placement for prior dispositions, surviving
in-scope findings and decisive unknowns. When the previous snapshot, report, or
rationale is unavailable, state that limit rather than infer closure.

## Use focused support

Resolve supporting skills by registered name only when a concrete review question
needs them. Pass the same scope, read-only boundary, evidence needed, and output
location. Read [references/specialists.md](references/specialists.md) when selecting
support. Missing optional help permits direct investigation with stated limits;
a missing requested specialist or essential source blocks only its affected claim.

For a straightforward change, perform the review directly. When the snapshot
exposes distinct consequential risks that benefit from separate investigation,
read [references/delegation.md](references/delegation.md) and coordinate focused
subagents automatically, within the caller's authority and host limits. Select
their questions from the change, not a fixed roster or file-size threshold.

An assigned facet worker or a `compare-solutions` participant performs its single
assigned review without delegation. `compare-solutions` remains the owner of
comparing independent complete audits; this skill's coordinator owns complementary
facets of one review. Neither mode recursively starts the other.

## Deliver the report

Locate this skill's installed directory separately from the reviewed project.
Write the canonical Markdown report at the caller's exact path, or in the
project's permitted scratch area. Run `python3 <skill-dir>/scripts/report.py
validate <report.md> --changed-paths <paths.json>` using actual absolute paths.
Repair format or coverage errors before delivery. The validator checks the
declared inventory and report structure, not the truth of a finding.

For a caller handoff, return `Wrote <count> findings to <absolute-report-path>`
after validation. For a standalone review, also run `python3
<skill-dir>/scripts/report.py render <report.md> <report.html> --changed-paths
<paths.json>` and return the HTML path followed by the Markdown path. Rendering
copies the stylesheet beside the HTML; keep both together. Edit Markdown first
when revising the result.

Finish when each changed path is accounted for, every retained finding has its
required evidence, and unresolved boundaries and checks remain explicit. No
findings means none supported in this scope; it is not an approval or a guarantee
that the change is ready to merge.

For requested source maintenance, read
[references/upstream-updates.md](references/upstream-updates.md).
