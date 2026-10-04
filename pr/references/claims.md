# Evidence for PR claims

Everything the title, body, or reported metadata asserts is a **claim**, and every claim ships verified against evidence that can establish that class of claim. A source can prove one class and be only a discovery hint for another.

| Claim class | Evidence that can establish it | Insufficient on its own |
| --- | --- | --- |
| Repository and PR state | Current `git status`, resolved refs and remote URLs, and matching fields from `gh repo view --json`, `gh pr view --json`, or `gh pr list --json`. | A remote's name, user memory, or a prior summary. |
| Motivation and problem | The current user request or user-supplied context, a linked issue, incident, specification, strategy doc, or product doc. | The branch name, commit messages, the diff alone, or the existing PR body. |
| Requirements and work-item coverage | Each explicit ask in the current user request, issue, or specification mapped to the implementation and its verification evidence. Assignee and status establish ownership and workflow state only. | A ticket title, assignment by itself, a closing keyword, or intended scope with no branch evidence. |
| Changed surfaces and implementation | Every commit, the full `<base-ref>...HEAD` diff, and the relevant current code, including generated, binary, dependency, and migration changes. | A diff stat, file list, commit summary, or existing PR body. |
| Delivered behavior and audience | The implementation traced end to end through routes, gates, flags, configuration, and failure paths, with relevant tests or manual evidence when the claim depends on runtime behavior. | A feature name, issue intent, scaffold, isolated code fragment, or test name. |
| Design decisions and tradeoffs | The implementation establishes the mechanism; a user decision, specification, ADR, design doc, or code comment establishes its rationale and rejected alternatives. | An alternative invented from the diff, or an assistant preference presented as the author's decision. |
| Validation | Exact results from commands run for the current head, or a current CI result tied to that head commit. | Planned checks, historical CI, the presence of tests, or an unverified result copied from the PR body. |
| Numbers and performance | A reproducible measurement or verified artifact that names the method, baseline, result, and code revision. | A goal, estimate, adjective, unsourced percentage, or number from a commit message. |
| Risk, impact, and out-of-scope boundaries | Facts from the diff, requirements, data flow, dependencies, compatibility, rollout, and rollback behavior. Present an inference as an assessment, not as measured fact. | Generic reassurance such as `low risk`, or absence of a known failure. |
| Review metadata and conventions | Written repository rules, the template on the resolved base, `CODEOWNERS`, current repository metadata from `gh`, and recent merged PRs for house style only. | A template introduced by the branch, guessed ownership, or one prior PR treated as a rule. |
| AI assistance and human review | The current run establishes what the agent changed and verified. Only the user's explicit confirmation establishes what a human reviewed or rewrote. | Generic disclosure text, the existing PR body, or an assumption that tool output received human review. |

When sources disagree, use the source authoritative for that claim class and name the mismatch. The issue establishes intended scope, the branch establishes implemented scope, and GitHub metadata establishes PR state; none substitutes for another. Unknown remains unknown. In a simulation, a fixture explicitly supplied as verified tool output stands in for that tool output.

Branch names, commit messages, existing PR bodies, and prior assistant or bot summaries are discovery hints for substantive claims. Use them to find evidence, then verify the claim from the matrix above.

Verify before you write it:

- **What the PR delivers.** A scaffold behind a flag is not the shipped capability. Read what the code does end to end.
- **Who it affects.** Read the actual gate (permission check, flag reader, route guard) rather than inferring an audience from the feature's name. When the audience is broad or awkward to name, phrase it role-neutrally.
- **Numbers.** Cite a measurement allowed by the matrix. With no honest figure, carry the weight in the verb (`cut`, `unblock`, `start`, `stop`); a hand-waved figure is worse than none.
- **Work items.** Check each ticket's assignee and status before writing that the PR covers it. Claim coverage for the PR's own ticket and work assigned to the author only after mapping every explicit ask to branch evidence. Treat matching work owned by someone else as possible overlap and leave closure to its owner.
- **Closing the ticket.** List the issue's explicit asks, check each against the diff, and name the ones the branch leaves unimplemented or half-done. That gap is invisible in the diff and it decides whether the ticket can close on this PR alone.
- **The existing body, in update mode.** A body written mid-branch rots as commits land: a caveat that was true at the first push ("hidden for everyone", "no endpoint exists", "not wired yet") may have been implemented three commits later while the body still swears otherwise. Replace stale claims when rewriting the full body and report material corrections when useful.
