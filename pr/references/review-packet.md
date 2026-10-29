# Write for the reviewer

Apply [claims](claims.md). Include only what helps assess this diff: purpose,
behavior, scope, decisions, risk, merge/deploy prerequisites and validation.
Gate-enablement timing, release plans across tickets and sibling-ticket scope go
to the user in the return, not the body or a tracker write. Name another ticket
only as a merge/deploy prerequisite of this diff. Neither a question asked during
the work nor a template's invitation to list follow-ups overrides this boundary.

## Title and body

Follow the repository's title convention; name the delivered outcome, not files,
generic editing or issue intent. Open with problem and resulting behavior; add a
before/after example when it clarifies a trigger or boundary. Explain mechanisms
only for correctness or consequential tradeoffs.

Point to repository documentation, such as a README's rules, steps or counts,
with at most a one-line summary instead of restating it. Do not restate commit
messages. When one explains an effect beyond the headline, such as unflagged
behavior, point to it in **one sentence** naming the commit, change and audience.
Refer to its message for reasons and consequences; give it no section/table.
Add only review-critical information the message lacks.

Follow written repository rules and the base template's guidance, meaningful
sections and required checklists. Preserve exact enforced formats unless the user
explicitly overrides them. Otherwise use short sections for distinct purposes;
`Summary`, `Changes` and `Validation` are a fallback. Combine empty/repeated
sections; a few scannable lines can remain unsectioned. A small diff does not
justify dense prose. Place useful missing context in an existing section or add
one when it materially helps review; explain a material departure from convention.

Use bullets for parallel changes/checks, cohesive prose for explanations and a
brief opening; avoid repeating the summary in the change list. Answer each
question below that the diff raises, in one line per item unless the reviewer
needs more to judge it:

- What changes for callers/users? Name gates and their default states.
- Which decisions would a reviewer question, unlike choices that follow a
  repository template or convention? Give the choice and its evidenced reason,
  material alternative or compatibility tradeoff.
- Where should review begin, if the reviewer would otherwise start in the wrong
  place? Name the owning module, invariant or critical path, not a file inventory.
- What ran on which revision, with what outcome, limits and accessible artifacts?
  Keep each check's key result, such as tests passed or rows changed. Identify
  missing checks.
- What requires care at merge/deploy: migrations, compatibility, order, rollback
  or irreversible effects? State consequences, not generic risk labels.
- Which explicit asks of this PR's ticket/request remain partial or unimplemented?
  Name them even if another ticket will deliver them; unrelated work is no gap.

Use `communicate-clearly` when available, retaining technical meaning.

## Length budget

Measure the body's characters with a tool, such as `wc -m` on the body file,
against its budget: the second-longest of the recent merged bodies measured for
this repository but at least 1,000 characters, or 2,500 characters when fewer
than three were measured or the lookup failed. The budget is a ceiling, not a
target. Exceed it only for content a reviewer needs to approve safely and cannot
open elsewhere, such as merge/deploy care, one-line validation results, required
captures, required template content or others' preserved notes. Merge/deploy care
stays in the body even when documentation or a commit message also states it.

Sub-results within a run, such as each access, SQL or validator check, per-item
counts, run logs and traces, stay out of the body, which keeps each run's outcome
and conditions. Put detail that still matters in an artifact at the PR's
visibility, such as an attachment or CI artifact but never a gist or external
host, or in the PR's one [detail comment](publication.md#create-or-update-metadata),
and link it. Draft-only returns it beside the body. Private local paths are not
artifacts.

## Evidence and continuity

Use [visual evidence](visual-evidence.md) when it clarifies a review decision.
Retain meaningful verification even when older PRs omit it.

For long work, an optional local record can retain phase, decision, reason,
evidence and result, not a tool transcript. Scratch stays out of commits unless
convention or the user requests a maintained artifact.

On Update, rewrite the **whole** description from the complete published diff,
re-measured against the length budget. Replace stale claims and report material
corrections when useful. A new run enters as one line and replaces the run it
supersedes, the same check or environment at an older revision; keep an older
run, in one line, only for evidence the newer one lacks. Revalidate manual
context, links, captures, evidence and completed checklist claims.
Preserve others' accurate notes and unresolved design questions: the reviewer
boundary governs your new prose, not deletion of their notes. Evidence is required
to complete an unchecked item. Repair history belongs in commits.

Use full issue URLs and the verified ticket policy. Include no promotional footer,
invented intent or implied human approval.

Before delivery, ensure every claim has evidence, cut each sentence whose removal
would not lower a reviewer's confidence, and check the budget. Make purpose,
changes, decisions and validation easy to find; reorganize dense blocks, remove
repetition and unsupported reassurance.
