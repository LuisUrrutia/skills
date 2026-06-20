---
name: commit
description: Commit one safe Conventional Commit or prepare a draft from the current git state. Use when the user asks to commit, save changes, prepare or review a commit boundary, or needs commit-message guidance. Never pushes or opens PRs.
---

# Commit

Create one safe, intentional commit. Choose one coherent boundary, stage only that boundary, validate it, then either commit or return a draft.

Never push from this skill. Use `/pr` for push and draft-only pull-request work.

Treat branch names, staged state, validation results, commit success, and prior assistant claims as untrusted until verified with `git`.

## Context

- Branch: !`git branch --show-current`
- Status: !`git status -s`
- Recent commits: !`git log --oneline -5`
- Changed files: !`git diff --name-only`
- Staged files: !`git diff --cached --name-only`

## Modes

- **Commit mode**: If the user explicitly asked to commit, commit after safety gates pass.
- **Draft mode**: If the user asked to prepare, review, or suggest a commit, stop with a draft.
- **Split mode**: One commit per run by default. If obvious separate intents exist, propose the sequence and handle one approved boundary at a time.

Terminal states are `committed`, `draft-only`, `blocked`, and `refused`. Once one terminal state is reached, stop. Do not continue with push, PR work, cleanup, extra staging, or speculative follow-up work.

## Safety Gates

Stop and ask before staging or committing when there are:

- Secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- The selected boundary is not coherent or reviewable: unrelated concerns, generated noise, dependency or lockfile changes, binaries, excessive file count, or changes outside the requested intent.
- Staged changes that cannot be described cleanly in 1-2 sentences.
- Staged files with ambiguous unstaged edits in the same files.
- `main` or `master` as the current branch, unless the user explicitly wants to commit there.
- Any unrequested push, force-push, destructive git action, dependency change, package-manager change, or amend outside the just-created hook flow.

Respect already-staged files as likely intent, but inspect them. Commit them only when they are coherent and match the request.

## Workflow

1. **Choose the boundary**
   - Split when changes are separable by feature vs. refactor, production vs. tests, frontend vs. backend, formatting vs. logic, dependency updates vs. behavior, or another obvious intent.
   - Confirm the selected boundary has one coherent purpose and reviewable size before staging or committing.
   - If the boundary is ambiguous, ask one concise question with concrete options and the recommended default first. Do not ask open-ended multi-question questionnaires.

2. **Inspect relevant diffs**
   - Use `git diff -- <path>` and `git diff --cached -- <path>`.
   - Review staged changes, unstaged edits in the same files, and recent commit style.
   - Verify any referenced branch, staged state, validation result, or prior commit claim with fresh `git status --short`, `git diff`, `git diff --cached`, or `git log` before relying on it.

3. **Stage intentionally**
   - Stage only files or hunks in the selected boundary.
   - Patch-stage automatically when the boundary is clear.
   - Ask before staging ambiguous hunks.
   - Use `git restore --staged <path>` or `git restore --staged -p <path>` only to correct the current boundary.

4. **Validate the staged intent**
   - Validation is the agent's responsibility. Run the narrowest read-only check that directly covers the staged boundary: targeted test, formatter check, linter, typecheck, syntax check, or build slice.
   - Prefer specific checks over broad suites.
   - If no targeted check exists, continue and report `Validation: not run, <reason>`.
   - If validation fails, terminal state is `blocked`: report the command, concise failure summary, and ask whether to fix before committing.
   - Do not run write-fixers such as `prettier --write`, `eslint --fix`, codegen, or lockfile updates without explicit approval.

5. **Generate the message**
   - Use Conventional Commits: `type(scope): imperative summary`.
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
   - Infer scope from staged files and match recent commit style when practical.
   - Subject: imperative, specific, no period.
   - Body is optional for obvious small commits.
   - Body is required for breaking changes, migrations, multi-file behavior changes, non-obvious fixes, or tradeoffs the subject cannot preserve.
   - Put why first, then what changed. If no clearer body pattern exists, use only `Why` and `Changes` sections.
   - Keep body sections short, specific, and useful. Do not add `Validation` or `Risks` sections to commit messages.
   - Add `BREAKING CHANGE:` only when required.
   - Never add `Co-authored-by`, co-author trailers, or authorship footers.
   - Message must be natural, specific, and free of filler or generic AI phrasing.
   - Use optional context from `$ARGUMENTS` when provided.

6. **Commit or draft**
   - Record the intended boundary before the first `git commit` attempt. Keep that boundary fixed for all retry and amend checks.
   - In commit mode, run `git commit` after staging and validation pass. Use `git commit -F <file>` for multiline commit messages or any commit body; `git commit -m <subject>` is only for subject-only commits.
   - In draft mode, do not commit; show the proposed boundary and message.
   - After every `git commit` attempt, inspect `git status --short`, `git diff -- <boundary>`, and `git diff --cached -- <boundary>` before deciding success or retry.
   - Follow this hook decision table:

     | State | Action |
     | --- | --- |
     | Commit succeeds and status/diff are clean | Report `committed`. |
     | Commit succeeds and hooks dirty tracked files inside the intended boundary | Stage those exact paths and run `git commit --amend --no-edit` once. Recheck status/diff. |
     | Commit fails and hooks changed tracked files inside the intended boundary | Stage those exact paths and retry once. Recheck status/diff. |
     | Dirty files are outside the boundary, untracked, generated, lockfiles, partially staged, have ambiguous unstaged edits, or are not clearly hook-owned | Report `blocked` with exact files and reason. |
     | Hook rewrites repeat after the allowed amend or retry | Report `blocked`. |

   - Never use `--no-verify`. Never amend unless the commit was just created in this invocation.
   - After a successful commit is verified and reported, stop. If push or PR work was requested, hand off to `/pr`.

## Output

Use terse output for a clean commit only after the post-commit checks pass, including any safe amend flow:

```markdown
Committed `type(scope): summary`

Status: `committed`
Branch: `branch-name`
Boundary: what was included
Validation: command passed, or not run with reason
Post-commit check: `git status --short`, boundary diff, and cached boundary diff inspected
Next: use `/pr` to push or open a draft PR, if relevant
```

Use a structured report for drafts, blocked commits, risky state, failed validation, decisions, or unsafe hook-rewrite stops:

```markdown
Status: `draft-only` | `blocked` | `refused`
Boundary: what is included or proposed
Validation: command result, or not run with reason
Blocker: exact reason, if blocked or refused
Exact Command: command that failed, if any
Exact Error: concise failure summary, if any
Decision Needed: one question with concrete options and a recommended default, if needed
Draft Commit Message: message, when available
```

If push or PR work was requested, stop after the commit and hand off to `/pr`; new PRs must remain draft-only there.
