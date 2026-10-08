# Write for the reviewer

Apply the evidence rules in [claims.md](claims.md). The reader should understand
what problem the change addresses, what becomes true, and where to concentrate
attention before opening the diff.

The body serves the reviewer of this diff. Include a statement only when it helps
assess the change: its purpose, behavior, scope, decisions, risks, merge or deploy
prerequisites, or validation. Leave other project coordination to the tracker or
chat: when to enable a gate, release plans across tickets, and what other tickets
will deliver. Name another ticket only where it is a merge or deploy prerequisite
of this diff. Give the omitted notes to the user in the return rather than writing
them to a tracker. A question the user asked during the work does not earn its
answer a place in the body; apply the same test. Template guidance shapes how
content appears; it does not admit content that fails this test.

## Title and body

Use the repository's title convention. Name the concrete outcome at the scope
the branch actually delivers; avoid a file inventory, a generic editing verb, or
a promise derived only from an issue title. Never claim a measured improvement
without measurements.

Start the body with the problem and delivered behavior. A before/after example
helps when it makes a trigger or boundary concrete. Explain the mechanism only
as far as it helps evaluate correctness or a consequential tradeoff.

Reviewers can read the commit messages; do not restate them. When a commit's
message explains an effect beyond the PR's headline, such as a behavior change
outside its feature flag, point to it in one sentence that names the commit, what
it changes and for whom, and refer the reader to its message. Leave its
consequences and reasons there, give it no section or table, and add only what the
reviewer must check that the message leaves out.

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

- What changed for the caller or user, and which gates still limit it? Name each
  gate and its default state.
- Why this approach, where that reason is known? What material alternative or
  compatibility tradeoff must the reviewer assess?
- Where should review begin when the diff is nontrivial? Point to the owning
  module, invariant or critical path; do not repeat every changed filename.
- What ran, against which revision, and what did it prove? Include relevant
  commands, results and accessible artifacts. Name missing checks honestly.
- What requires care when merging or deploying this diff: migration, compatibility,
  deploy order, rollback, or an irreversible external effect? Assess concrete
  consequences, not generic risk labels.
- Which explicit asks of this PR's own ticket or request remain unimplemented or
  partial, when that could otherwise be mistaken for delivered scope? Name them
  even when another ticket will deliver them; work neither this ticket nor the
  request asked for is not a gap.

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
useful manual context, issue links and evidence only when still accurate; the
reviewer test above governs what you write, and it does not remove another
person's accurate notes.
Do not erase someone else's unresolved design question or turn their unchecked
item into a completed check without evidence. Repeated paragraphs describing each
repair belong in commit history, not the finished review explanation.

Use full issue URLs. A closing keyword requires verified coverage of every explicit
ask and authority to close that work item. Otherwise use a neutral reference and
state the remaining scope. Do not imply human approval, add promotional footers,
or invent author intent.

Before delivery, read it as a reviewer: can each claim be traced to evidence, can
the purpose, changes, consequential decisions and validation be found at a glance,
and does every paragraph help the reviewer assess this diff? Reorganize
dense blocks rather than merely adding headings above them. Remove repetition and
unsupported reassurance.
