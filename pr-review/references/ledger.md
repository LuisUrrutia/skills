# Candidate ledger

Read before the first completion and on later reviewer events. The parent alone
writes `candidate-ledger.md`; workers never receive it. Keep this source ledger
separate from the canonical synthesized `review.md` and from the comment plan.

## Source status and review basis

Record each engine, actual exposed model/effort (or unknown), snapshot, attempt,
terminal status, report path, elapsed time, validation and exact failure. Retain
requirement/standard sources and their outcomes, checks with commands and results,
coverage per changed path, and explicit gaps. For CodeRabbit, retain native
reviewedFiles when present without inventing canonical per-path coverage.
Terminal does not mean successful. Empty, failed and valid-zero results differ.

After the fresh pass, add earlier snapshot IDs, dispositions and rationale with
current evidence. A declined optional ask stays in Review basis unless new evidence
changes it. Deferring an unresolved defect does not resolve it, unless the
author confirmed a tracking ticket in its thread: record that disposition with the
ticket as an accepted deferral, which neither republishes nor blocks approval.
Mark missing prior artifacts as unavailable rather than inferring closure.

## Candidate entries

Keep one stable C identifier per root cause. Preserve these fields as a report is
reduced, including a vendor severity separately from synthesized severity:

```markdown
### C1 | verified | high | src/file.ts:48 | Retry duplicates a write

Sources: claude F2, coderabbit event 7 (vendor: major)
Class: correctness
Action: required
Affected: Requests retried after a timeout.
Diff cause: The new branch writes before its existing guard.
Impact: A retry repeats the operation.
Evidence:
- producer | `src/file.ts:48` | The branch persists before checking the request key.
- consumer | `src/worker.ts:91` | Timeouts enter this retry path.
Recommendation: Required: preserve the idempotency check before writing.
Unresolved premise: None.
Anchors: src/file.ts:48 RIGHT; src/other.ts:72 RIGHT.
Disposition: New comments at both verified sites.
Comment: Awaiting wording.
```

States are `pending`, `verified` and `dropped`. Match claims by substance and
causality, not just line or wording. Combine sources and distinct consequences;
keep every independently verified anchor. A repeated site receives its own comment
with a short back-reference. Duplicate source reports do not multiply comments at
the same site. `comment-style` owns wording, not this placement decision.

Read each completed report end to end, including Review basis, Checks, Open
questions and Coverage. Reduce candidates one at a time; inspect the decisive
source and strongest counterevidence. The protocol permits structural and
requirements evidence without an invented runtime trace. Preserve required/optional
Action even when an optional suggestion and a defect happen to share severity.

A dropped claim retains its sources and a concrete Drop reason. A supported minority
survives. A shared false positive is dropped. Calibration shapes and a vendor's
label cannot decide truth. Separate an unsupported diagnosis from a bad proposed
remedy; repair the remedy if the underlying finding still stands.

## Questions, seams and synthesis

Use stable Q identifiers with source IDs, exact missing premise, needed evidence
and status (`open`, `resolved`, `dropped`). A premise that decides whether an issue
exists remains a question. Name the boundary or access needed; do not turn absence
of access into a finding. Unresolved limits that affect only extent qualify an
otherwise supported finding.

Add seam gaps with both revision-specific locations through the same candidate
contract. Matching and unreadable seam verdicts are coverage, not automatic bugs.
Before external feedback is opened, every engine is terminal, every delivered
candidate has a disposition, every opened seam has a verdict, and every material
question has a resolution or an exact remaining premise.

Write canonical `review.md` using the resolved auditor's grammar, carrying the
combined Review basis, Class/Action/Recommendation, questions, checks and actual
coverage. Validate it against the frozen inventory. Separately reconcile its
finding IDs to ledger sources and each selected site to the final comment plan.
Retain unselected test/tooling findings internally with the selection reason.
Only then reconcile external feedback and prior dispositions, revalidate affected
conclusions and prepare the review comments.
