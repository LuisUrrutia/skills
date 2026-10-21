# Evidence for PR claims

Verify every title, body and metadata claim with evidence that establishes its
class. A source authoritative for one class may only suggest where to look for
another.

| Claim | Establishing evidence | Insufficient alone |
| --- | --- | --- |
| Repository/PR state | Current Git status, resolved refs/URLs and matching structured `gh repo/pr view/list` fields | Remote name, memory, prior summary |
| Motivation/problem | User request/context, issue, incident, specification, strategy or product document | Branch name, commit message, diff, existing body |
| Requirements/coverage | Every explicit request, issue or specification ask mapped to implementation and verification | Ticket title, assignee/status, closing keyword, intent |
| Changed implementation | Every commit, full base-to-head diff and relevant current code, including generated, binary, dependency and migration changes | Stat, file list, commit summary, existing body |
| Behavior/audience | End-to-end routes, permissions, flags, configuration and failures; tests/manual evidence where runtime matters | Feature name, intent, scaffold, fragment, test name |
| Decisions/tradeoffs | Implementation for mechanism; user decision, specification, ADR, design document or code comment for rationale and rejected alternatives | Invented rationale or assistant preference presented as author intent |
| Validation | Exact command results or CI tied to the current head | Planned checks, historical CI, tests merely present, copied unverified results |
| Numbers/performance | Reproducible measurement or verified artifact naming method, baseline, result and revision | Goal, estimate, adjective, unsourced percentage, commit-message number |
| Risk/impact/scope | Diff, requirements, data flow, dependencies, compatibility, rollout and rollback facts; label inferred assessments | Generic reassurance or no known failure |
| Metadata/conventions | Written rules, base template, CODEOWNERS, current repository metadata; merged PRs for style only | Branch-added template, guessed owner, one PR treated as policy |
| AI/human contribution | Current run for agent work/checks; explicit user confirmation for human review or rewriting | Disclosure boilerplate, existing body, presumed human review of output |

Resolve disagreements by claim authority and name the mismatch: issue intent,
implemented scope and GitHub state cannot substitute for one another. Unknown
stays unknown. Explicitly verified simulation fixtures stand in for tool output.
Use branch names, commit messages, bodies and assistant/bot summaries to discover
evidence, then verify substantive claims.

Use role-neutral wording when an audience is broad or awkward to name.

For work-item coverage, check assignee/status and map every explicit ask to branch
evidence. Claim the PR's own ticket or author-assigned work only when supported.
Other owners' matching work is possible overlap; leave closure to them. Name
unimplemented or partial asks that affect whether this PR alone completes its
request. A closing keyword requires verified completion of every explicit ask
and authority to close. Use the verified project policy/link form, including
keeping tickets open for QA. Otherwise link neutrally and state remaining scope.
