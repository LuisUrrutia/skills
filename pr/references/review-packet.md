# Write for the reviewer

Apply [claims](claims.md). Include only what helps assess this diff: purpose,
behavior, scope, decisions, risk, merge/deploy prerequisites and validation.
Gate-enablement timing, release plans across tickets and sibling-ticket scope go
to the user in the return, not the body or a tracker write. Name another ticket
only as a merge/deploy prerequisite of this diff. Neither a question asked during
the work nor a template's invitation to list follow-ups overrides this boundary.

## Title and body

Follow the repository's title convention; titles often become squash commit
messages. Lead with the delivered outcome and why it matters, not the mechanism
alone, files, generic editing or issue intent; state a figure only when measured:

- Weak: `perf(server): negotiate permessage-deflate on the websocket`
- Strong: `perf(server): cut websocket frame size by 70%+ with compression`

Follow written repository rules and the base template's guidance, meaningful
sections and required checklists. Preserve exact enforced formats unless the user
explicitly overrides them, and fit the [default structure](#default-structure)'s
content into the template's sections. Without a template, use that structure.

Write in plain words, with `communicate-clearly` when available: one line per fact
and bullets, not dense prose. Link tickets named in prose and give gates their
default states. Describe what users and callers see; class names, design tokens,
CSS and internal function names belong only in review-note links. Point to
repository documentation or a commit message in one line instead of restating it.
Leave out:

- Commit hashes and revisions, including those of captures and runs; reviewers
  read the PR as a whole, so say "before this change" or "an earlier version of
  this branch".
- Who did what, closing summaries, and reassurance such as "no auth code changes".
- Statistics or counts offered to justify the change.
- Test commands and their totals, even when repository instructions ask for them
  in the description; report those in the return.
- Tables of checks, lines saying CI or Chromatic ran, and steps the team does on
  every PR, such as accepting Chromatic changes or merging a stack in order.

Size every section to the diff: what a reviewer reads quickly in the diff gets a
line or nothing, and a diff of a few lines never gets more text about what changed
than the diff itself: one What changes bullet, with no mechanism.

## Default structure

Use these sections in order, leaving out any that has nothing to say.

1. **Ticket line:** `Completes [KEY-1](<ticket URL>)` or `Part of [KEY-1](<ticket URL>)`,
   followed on the same line by ` · [Design](<design URL>)` when a design exists.
   A tracker policy's permitted link form sets the keyword, not the format: the
   link keeps the ticket key as its text. No stack or "Stacked on" line.
2. **Why:** what goes wrong for users or the business without the change, from
   the ticket and its epic, said as you would tell a colleague: who does what,
   what stops them today, in terms of what they see. Measurements, widths and
   mechanism belong in What changes. Do not restate what the ticket asks. Keep
   each part, Goal and Constraint included, to one short, direct sentence.
   - A goal and a constraint: label them **Goal:** and **Constraint:**; the
     constraint is what the change must never do and what that would cost.
   - A single reason: one plain sentence with no label. A purely technical or
     ticketless change says the problem or what the team gains.
   - Product and code reasons that clearly differ: put them under **Product** and
     **Code** headings, the code reason in one line.
   - Name a cause by linking its upstream report or failing run, not with counts.
     Make no argument that the fix is safe.
3. **What changes:** the delivered behavior as a user would sum it up, in a few
   bullets. Leave UI detail that the captures or the diff show, such as row
   wording, empty, loading and error states, or layout at each width, to them.
   - Several behaviors of one kind, each with a before and an after, even in a
     tiny fix: a small Before | After table. A one-to-one mapping, such as
     statuses to stages: a two-column table.
   - Do not describe in words intended visual changes reviewers see in Storybook
     or Chromatic anyway; captures still show them, and an unexpected visible
     difference still goes in the body.
   - Add [screenshots and diagrams](visual-evidence.md) beside the change they
     show.
   - End with a short `Not in this PR:` line for explicit asks of the ticket left
     out.
4. **Before turning it on** or **Depends on:** steps outside this PR, such as
   config in another repository or another service's deploy, in at most two
   bullets. Link the companion PR that carries the exact values when it exists.
5. **How it was tested:** results, not steps, on the closest real environment,
   with links to the runs or events they produced. Results from CI, including
   which specs or stories it ran, stay out: the PR's checks show them. Several cases from a real
   end-to-end run go in a small Request | Before | After table; logic that unit
   tests cover gets no table. Name a layer only CI can run, or a step meant to run
   after merge, and why; any other untested layer
   [blocks publication](../SKILL.md#publish-and-verify). Leave the section out
   when nothing runs, such as a Markdown-only change.
6. **Risk:** consequences, not generic labels; unknowns go here, not in a separate
   section.
   - No real risk: one line, `Low.`, plus the only difference users notice or a
     single non-obvious point, such as a parameter the API does not check.
   - Otherwise, and for a shared component that reaches every place it is used:
     **Impact:**, **Rollback:** with its real cost, and **Error detection:**,
     saying plainly when only a person would notice.
   - Money movement or wider data access: also who is and is not affected, who
     notices first or who could see what they should not, what happens to
     records made before a rollback, and how anyone can check the result.
7. **Review notes:** only what the diff does not explain, one idea per note, each
   saying why it matters: where to begin and why, a decision a reviewer would
   question, a consequential trade-off, in plain words rather than token or
   attribute names. Leave out implementation mechanics that the code or its
   comments explain, notes about tests, such as which states lack one or where a
   test lives, and what the PR page already shows, such as the base branch.
   Keep at most three notes, the concrete points a reviewer should check; details
   such as generated code, flag reads or matching time boundaries stay out. Link
   code to its line in the PR diff,
   `https://github.com/<owner>/<repo>/pull/<number>/files#diff-<sha256 of the path>R<line>`.
   Leave the section out when the diff explains itself.
8. **How to verify:** numbered steps on the closest real environment for every
   changed layer, such as the processor's test environment for a payment change,
   naming the screen to open and what to see. A test command is not a step. Every
   PR has one.

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
and conditions. Put detail that still matters in a folded `<details>` block in the
body, or in an artifact at the PR's visibility, such as an attachment or CI
artifact but never a gist or external host, and link it. Private local paths are
not artifacts.

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

Use full issue URLs and the verified ticket policy. Include no promotional footer
or unrequested model/harness attribution; satisfy a repository-required AI
disclosure from its claims evidence. Include no invented intent or implied human
approval.

Before delivery, ensure every claim has evidence, cut each sentence whose removal
would not lower a reviewer's confidence, and check the budget. Make purpose,
changes, decisions and validation easy to find; reorganize dense blocks, remove
repetition and unsupported reassurance.
