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

Do not restate commit messages. When one explains an effect beyond the headline,
such as unflagged behavior, point to it in **one sentence** naming the commit, change and audience.
Refer to its message for reasons and consequences; give it no section/table.
Add only review-critical information the message lacks.

Follow written repository rules and the base template's guidance, meaningful
sections and required checklists. Preserve exact enforced formats unless the user
explicitly overrides them. Otherwise use short sections for distinct purposes;
`Summary`, `Changes` and `Validation` are a fallback. Combine empty/repeated sections; a few
scannable lines can remain unsectioned. A small diff does not justify dense prose.
Place useful missing context in an existing section or add one when it materially
helps review; explain a material departure from convention.

Use bullets for parallel changes/checks, cohesive prose for explanations and a
brief opening. State each command's outcome and limits beside it; avoid repeating
the summary in the change list. Cover these questions where relevant:

- What changes for callers/users? Name gates and their default states.
- What evidenced reason, material alternative or compatibility tradeoff matters?
- Where should nontrivial review begin: owning module, invariant or critical path,
  not a filename inventory?
- What ran on which revision, with what results and accessible artifacts?
  Identify missing checks.
- What requires care at merge/deploy: migrations, compatibility, order, rollback
  or irreversible effects? State consequences, not generic risk labels.
- Which explicit asks of this PR's ticket/request remain partial or unimplemented?
  Name them even if another ticket will deliver them; unrelated work is no gap.

Use `communicate-clearly` when available, retaining technical meaning.

## Evidence and continuity

Use [visual evidence](visual-evidence.md) when it clarifies a review decision.
Keep long traces/benchmarks in accessible artifacts, with conclusions and
interpretive conditions in the body. Private local paths are not attachments.
Retain meaningful verification even when older PRs omit it.

For long work, an optional local record can retain phase, decision, reason,
evidence and result, not a tool transcript. Scratch stays out of commits unless
convention or the user requests a maintained artifact.

On Update, rewrite the **whole** description from the complete published diff.
Replace stale claims and report material corrections when useful. Revalidate
manual context, links, captures, evidence and completed checklist claims.
Preserve others' accurate notes and unresolved design questions: the reviewer
boundary governs your new prose, not deletion of their notes. Evidence is required
to complete an unchecked item. Repair history belongs in commits.

Use full issue URLs and the verified ticket policy. Include no promotional footer,
invented intent or implied human approval.

Before delivery, ensure every claim has evidence and every paragraph helps assess
the diff. Make purpose, changes, decisions and validation easy to find; reorganize
dense blocks, remove repetition and unsupported reassurance.
