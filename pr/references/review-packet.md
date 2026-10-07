# Write for the reviewer

Apply the evidence rules in [claims.md](claims.md). The reader should understand
what problem the change addresses, what becomes true, and where to concentrate
attention before opening the diff.

## Title and body

Use the repository's title convention. Name the concrete outcome at the scope
the branch actually delivers; avoid a file inventory, a generic editing verb, or
a promise derived only from an issue title. Never claim a measured improvement
without measurements.

Start the body with the problem and delivered behavior. A before/after example
helps when it makes a trigger or boundary concrete. Explain the mechanism only
as far as it helps evaluate correctness or a consequential tradeoff.

Use the selected template's meaningful sections and required checklists. Without
a template, use short named sections when the body covers distinct purposes such
as motivation, changes and validation. `Summary`, `Changes` and `Validation` are
a useful starting point; combine or omit sections that would be empty or repeat
the same point. An unsectioned body fits only when the explanation and verification
remain easy to scan in a few lines. A small diff alone does not justify dense
paragraphs.

Use bullets for parallel changes or checks so the reviewer can find each result
without unpacking a paragraph. Keep the opening brief and explanations cohesive;
do not turn every sentence into a separate bullet or repeat the summary in the
change list. State each command's outcome and any limit on what it proved next
to that command.

Cover these questions where they matter, without turning each into a mandatory
section:

- What changed for the caller or user, and which gates still limit it?
- Why this approach, where that reason is known? What material alternative or
  compatibility tradeoff must the reviewer assess?
- Where should review begin when the diff is nontrivial? Point to the owning
  module, invariant or critical path; do not repeat every changed filename.
- What ran, against which revision, and what did it prove? Include relevant
  commands, results and accessible artifacts. Name missing checks honestly.
- What requires care: migration, compatibility, rollout, rollback, or an
  irreversible external effect? Assess concrete consequences, not generic risk labels.
- Which requested work remains outside this PR, when that could otherwise be mistaken
  for delivered scope?

Keep necessary evidence inside an existing suitable section when possible. A
small additional section is useful when it substantially reduces review effort
and the repository does not require an exact format. Do not suppress meaningful
verification merely because old PRs omit it, or decorate a trivial change with a diagram.

## Evidence and continuity

Use [visual-evidence.md](visual-evidence.md) when visuals clarify a review decision.
Keep long traces and benchmark output in accessible artifacts; include only their
conclusion and the conditions needed to interpret it. Private local paths are not
reviewer-accessible attachments.

A long task may need a local decision record: phase, decision, reason, evidence,
result. Preserve consequential choices and corrections, not a transcript of tool
calls. Keep scratch evidence out of commits unless repository convention or the
user requests a maintained artifact. The PR should carry the resulting explanation.

On Update, rewrite the full description from the current published diff. Preserve
useful manual context, issue links and evidence only when still accurate. Do not
erase someone else's unresolved design question or turn their unchecked item into
a completed check without evidence. Repeated paragraphs describing each repair
belong in commit history, not the finished review explanation.

Use full issue URLs. A closing keyword requires verified coverage of every explicit
ask and authority to close that work item. Otherwise use a neutral reference and
state the remaining scope. Do not imply human approval, add promotional footers,
or invent author intent.

Before delivery, read it as a reviewer: can each claim be traced to evidence, can
the purpose, changes, consequential decisions and validation be found at a glance,
and does every paragraph change what the reader understands or checks? Reorganize
dense blocks rather than merely adding headings above them. Remove repetition and
unsupported reassurance.
