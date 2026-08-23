---
name: commit
description: "Git commits: use for preparation, creation, message guidance, or requested pushes."
---

# Commit

Create safe, intentional Conventional Commits one atomic boundary at a time. Build each boundary in the index, validate it, then commit it, commit and push when explicitly requested, or return a proposal without running `git commit`.

Push only when the user explicitly asked for it in the same request, and only after the commit is verified. Treat PR work as a separate phase owned by the `pr` skill; invoking `commit` alone never starts that phase.

Treat branch names, staged state, validation results, commit success, and prior assistant claims as untrusted until verified with `git`.

## Modes

- **Commit mode**: If the user explicitly asked to commit, commit after safety gates pass.
- **Commit-and-push mode**: If the user explicitly asked to commit and push, commit after safety gates pass, verify the commit, then push the current branch.
- **Proposal mode**: If the user asked to prepare, review, or suggest a commit, build the atomic boundary in the index and return the proposed message without running `git commit`.
- **Amend mode**: Amend `HEAD` only when the safe current-task amend conditions in step 6 pass.
- **Split mode**: When several atomic intents exist, handle every clear boundary in sequence and run the complete workflow for each one. Ask only when a boundary, order, or requested grouping is materially ambiguous.

Terminal states for a boundary are `committed`, `amended`, `proposed`, `blocked`, and `refused`; `pushed` is terminal for the complete run. Stop changing a boundary after it reaches a terminal state. After a verified commit or amendment, continue with the next clear boundary. Push only in commit-and-push mode. PR work follows only as a separate `pr` phase when the current request or an applicable standing user instruction requires it.

## Safety Gates

Stop and ask before staging or committing when there are:

- Secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- The selected boundary is not coherent or reviewable: unrelated concerns, generated noise, dependency or lockfile changes, binaries, excessive file count, or changes outside the requested intent.
- Staged changes that cannot be described cleanly in 1-2 sentences.
- Staged files with ambiguous unstaged edits in the same files.
- `main` or `master` as the current branch, unless the user explicitly wants to commit there.
- Any unrequested push, any force-push, destructive git action, dependency change, package-manager change, or amend outside the permitted flows in step 6.

Respect already-staged files as likely intent, but inspect them. Commit them only when they are coherent and match the request.

## Workflow

1. **Choose the boundary**
   - Run `git rev-parse HEAD`, `git branch --show-current`, `git status --short`, `git log --oneline -5`, `git diff --name-only`, and `git diff --cached --name-only` to establish the baseline commit, branch, worktree state, recent commit style, changed files, and staged files. Handle an unborn branch explicitly when `HEAD` does not exist.
   - Prefer atomic commits. Split when changes are separable by feature vs. refactor, production vs. tests, frontend vs. backend, formatting vs. logic, dependency updates vs. behavior, or another independent intent. Group separable intents only when the user explicitly accepts a broader commit.
   - Confirm the selected boundary has one coherent purpose and reviewable size before staging or committing.
   - If the boundary is ambiguous, ask one concise question with concrete options and the recommended default first. Do not ask open-ended multi-question questionnaires.
   - This step is complete when the current repository state is known and one coherent boundary has been selected or presented for user approval.

2. **Inspect relevant diffs**
   - Use `git diff -- <path>` and `git diff --cached -- <path>`.
   - Account for every changed file and every staged or unstaged hunk in the selected boundary. Classify all remaining changes as preserved work outside the boundary.
   - Review staged changes, unstaged edits in the same files, and recent commit style.
   - Verify any referenced branch, staged state, validation result, or prior commit claim with fresh `git status --short`, `git diff`, `git diff --cached`, or `git log` before relying on it.
   - This step is complete when every hunk in the boundary is understood, every pre-existing staged change is either included or deliberately removed from the index, and every excluded change is identified as preserved work.

3. **Stage intentionally**
   - Stage only files or hunks in the selected boundary.
   - Patch-stage automatically when the boundary is clear.
   - Ask before staging ambiguous hunks.
   - Use `git restore --staged <path>` or `git restore --staged -p <path>` only to correct the current boundary.
   - Staging and unstaging may reorganize the index, but must preserve every user change in the working tree.
   - This step is complete when `git diff --cached` contains the whole atomic boundary and nothing outside it, while every excluded user change remains preserved outside the index.

4. **Validate the staged intent**
   - Validation is the agent's responsibility. Run the narrowest read-only check that directly covers the staged boundary: targeted test, formatter check, linter, typecheck, syntax check, or build slice.
   - Prefer specific checks over broad suites.
   - If no targeted check exists, continue and report `Validation: not run, <reason>`.
   - If validation fails, terminal state is `blocked`: report the command, concise failure summary, and ask whether to fix before committing.
   - Do not run write-fixers such as `prettier --write`, `eslint --fix`, codegen, or lockfile updates without explicit approval.
   - This step is complete when a targeted command has passed, or the output records a specific reason no targeted validation exists.

5. **Generate the message**
   - Treat the message as a claim about the staged boundary. The diff proves what changed; the user's request, linked issue, and supplied project context establish why. Recent commits supply format and tone, not facts.
   - Conventional Commits is required for every proposal and created commit: `<type>[(<scope>)][!]: <imperative summary>`.
   - If the repository defines its own Conventional Commit type set, follow it. Otherwise use `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, or `test`.
   - Choose the type from the effect of the change, not the edited file's extension. Use `build` for build-system or dependency changes, `ci` for CI configuration and scripts, `perf` for performance improvements, and `revert` when reversing a previous commit.
   - Infer scope from the atomic boundary and match recent commit style when practical. Prefer a clear, stable scope; omit it when the repository convention avoids scopes or no honest useful scope exists.
   - Mark every breaking change with `!` before the colon and a `BREAKING CHANGE: <description>` footer. The footer states what breaks and what callers must change.

   **Subject**

   - Name the most important concrete result of the commit. A reader scanning the log should understand why the change matters without opening the diff.
   - State what becomes true: a capability added, a defect prevented, a rule enforced, a test case covered, or an architectural boundary made explicit. For docs and agent instructions, name the rule, decision, or behavior the text now establishes rather than the act of editing it.
   - Keep the promise no broader than the staged diff. A scaffold, partial migration, or first slice must read as one.
   - Use only audiences, measurements, and outcomes verified by the diff, tests, or supplied context.
   - Prefer plain, precise verbs. Replace abstract editorial verbs such as `improve`, `update`, `enhance`, `refine`, `sharpen`, or `clean up` with the behavior or rule that actually changed.
   - Keep the subject imperative and short, with no period.
   - Remove the Conventional Commit prefix and test the remaining words: if they could describe several unrelated diffs, rewrite the subject around the concrete result.
   - When two honest subjects make materially different promises and the evidence does not resolve the choice, show two or three options with their tradeoffs and ask once. Do not hide the ambiguity behind a vague compromise.

   ```text
   BAD   feat(pr): sharpen review packet workflow
   GOOD  feat(pr): verify PR claims against code and tickets

   BAD   fix(auth): handle session key collisions
   GOOD  fix(auth): keep desktop sessions after mobile sign-in

   BAD   docs(api): update authentication docs
   GOOD  docs(api): document token refresh failure modes
   ```

   **Body**

   - The body is optional for an obvious small commit.
   - Include one for breaking changes, migrations, non-obvious fixes, tradeoffs, or multi-file behavior whose relationship the subject cannot preserve.
   - Put the reason first, then the change. If no clearer pattern exists, use short `Why` and `Changes` sections.
   - Keep only details that help a future reader understand the decision. Leave validation and risk reporting in the assistant's output, not the commit message.
   - Keep the message natural and direct. Run it through the `humanize` skill when available without weakening technical precision.
   - Never add `Co-authored-by`, co-author trailers, or authorship footers.
   - This step is complete when every promise in the subject and body is supported, the subject identifies this boundary rather than a generic kind of work, and the body carries any context the subject cannot safely compress.

6. **Commit, amend, or propose**
   - Immediately before each `git commit` attempt, record the exact `HEAD`, `git status --short`, intended message, and staged diff. These are the verification baseline. Keep the atomic boundary fixed for all retry and hook-amend checks.
   - In commit mode, run `git commit` after staging and validation pass. Use `git commit -F <file>` for multiline commit messages or any commit body; `git commit -m <subject>` is only for subject-only commits.
   - In proposal mode, do not commit; show the staged atomic boundary and proposed message, and report how the index changed.
   - After every `git commit` attempt, inspect `git rev-parse HEAD`, `git rev-list --parents -n 1 HEAD`, `git log -1 --format=%B`, `git show --stat --oneline HEAD`, `git diff <baseline-head>..HEAD`, `git status --short`, and the staged and unstaged boundary diffs before deciding success or retry. For an unborn baseline, inspect the new root commit directly instead of using a revision range.
   - A successful commit must create exactly one new `HEAD` from the baseline, carry the intended message, contain the verified atomic boundary, and preserve pre-existing work outside that boundary. Pre-existing outside changes are expected residual state, not a blocker.
   - Follow this hook decision table:

     | State | Action |
     | --- | --- |
     | Commit succeeds; new `HEAD`, message, and committed diff match the intended boundary; no new hook changes remain | Report `committed`, including the short commit hash. |
     | Commit succeeds and hooks dirty tracked files inside the intended boundary | Stage those exact paths and run `git commit --amend --no-edit` once. Recheck status/diff. |
     | Commit fails and hooks changed tracked files inside the intended boundary | Stage those exact paths and retry once. Recheck status/diff. |
     | The attempt creates new changes relative to the baseline that are outside the boundary, untracked, generated, lockfiles, partially staged, ambiguous, or not clearly hook-owned | Report `blocked` with exact files and reason. Preserve them. |
     | `HEAD`, message, parent, or committed diff does not match the recorded baseline and intended boundary | Report `blocked` with the exact mismatch. |
     | Hook rewrites repeat after the allowed amend or retry | Report `blocked`. |

   - Amend an existing `HEAD` only when every safe current-task amend condition passes:
     - The current agent recorded the exact commit hash as successfully created earlier in the current task.
     - That hash is still `HEAD`; no later commit or external branch change has occurred.
     - The commit is local and unpublished. Verify its upstream state; if this cannot be proved, create a new commit.
     - The new staged changes complete or correct the same atomic purpose. A new requirement or independently reviewable behavior gets a new commit.
   - Before the amend, record the commit hash, parent, message, complete diff from its parent, worktree state, and staged addition. Validate the updated atomic boundary. Use `git commit --amend --no-edit` only when the existing message still describes the complete boundary; otherwise provide the corrected message explicitly.
   - After the amend, verify that `HEAD` changed exactly once, the parent stayed unchanged, the message describes the updated boundary, the complete diff from the parent is correct, and all outside work remains preserved. Report terminal state `amended`.
   - Never use `--no-verify`. Amend only through the safe current-task flow or the just-created hook flow above.
   - This step is complete only when the proposal is reported without a commit, or the commit or amendment passes every `HEAD`, message, boundary, and residual-state check. Then start again with a fresh baseline for the next clear boundary. Stop when no requested boundary remains; push only when the user explicitly requested it in this same request.

7. **Push only when explicitly requested**
   - Push only in commit-and-push mode, after every intended commit is verified.
   - Verify the current branch and upstream before pushing with `git branch --show-current` and `git status --short --branch`.
   - Use ordinary `git push` when an upstream is configured; otherwise use `git push -u origin <branch>` only if `origin` exists and the branch name is verified.
   - Never force-push. Never push tags unless the user explicitly requested tags.
   - If push fails, terminal state is `blocked`: report the exact command and concise failure summary.
   - After push, verify with `git status --short --branch`, `git rev-parse HEAD`, and `git rev-parse @{u}`. This step is complete when the intended upstream contains the verified commit and the branch's ahead/behind state is reported.

## Output

Use terse output for a clean commit, amendment, sequence, or explicit commit-and-push only after the post-commit checks pass. Repeat the commit line and boundary-specific fields for each boundary in a sequence:

```markdown
Result: `committed` | `amended`
Commit: `<short-hash> <message>`

Status: `committed` | `amended` | `pushed`
Branch: `branch-name`
Boundary: what was included
Validation: command passed, or not run with reason
Post-commit check: new `HEAD`, parent, message, committed boundary, index, and residual worktree verified
Remaining changes: preserved outside-boundary work, or none
Push: not requested, or command/result when explicitly requested
PR: not requested, or handed to the `pr` skill under the current request or an applicable user instruction
```

Use a structured report for proposals, blocked commits, risky state, failed validation, decisions, or unsafe hook-rewrite stops:

```markdown
Status: `proposed` | `blocked` | `refused`
Boundary: what is included or proposed
Index: what was staged or unstaged to build the atomic boundary
Validation: command result, or not run with reason
Blocker: exact reason, if blocked or refused
Exact Command: command that failed, if any
Exact Error: concise failure summary, if any
Decision Needed: one question with concrete options and a recommended default, if needed
Proposed Commit Message: message, when available
```

Invoking this skill alone ends with the commit result. When the current request or an applicable standing user instruction also requires a PR, hand the verified commit state to the `pr` skill as a separate phase; that skill owns PR creation, push requirements, and initial PR state.
