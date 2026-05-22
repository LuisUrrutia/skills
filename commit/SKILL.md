---
name: commit
description: Create safe git commits with Conventional Commit messages. ALWAYS use this skill when committing code, whether user-requested or after completing a task. Use when the user says "commit", "/commit", "make a commit", "git commit", "save changes", or asks to prepare a commit. Accepts optional context for commit-message guidance.
---

# Commit

Create one safe, intentional commit. Inspect the work, choose a clean boundary, stage only what belongs, validate the staged intent, then commit when the user explicitly asked for it or approves the draft.

Never push from this skill. Use `/pr` for push and draft-only pull-request work.

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

## Safety Gates

Stop and ask before staging or committing when there are:

- Secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- Unrelated changed files, generated noise, dependency changes, lockfiles, or binary files outside the chosen boundary.
- Staged changes that cannot be described cleanly in 1-2 sentences.
- Staged files with ambiguous unstaged edits in the same files.
- `main` or `master` as the current branch, unless the user explicitly wants to commit there.
- Push, force-push, amend, destructive git action, dependency change, or package-manager change not explicitly requested.

Respect already-staged files as likely intent, but inspect them. Commit them only when they are coherent and match the request.

## Workflow

1. **Choose the boundary**
   - Split when changes are separable by feature vs. refactor, production vs. tests, frontend vs. backend, formatting vs. logic, dependency updates vs. behavior, or another obvious intent.
   - Ask when splitting would require interpretation.

2. **Inspect relevant diffs**
   - Use `git diff -- <path>` and `git diff --cached -- <path>`.
   - Review staged changes, unstaged edits in the same files, and recent commit style.

3. **Stage intentionally**
   - Stage only files or hunks in the selected boundary.
   - Patch-stage automatically when the boundary is clear.
   - Ask before staging ambiguous hunks.
   - Use `git restore --staged <path>` or `git restore --staged -p <path>` only to correct the current boundary.

4. **Validate the staged intent**
   - Run the narrowest useful read-only check when relevant and available: targeted tests, formatter check, linter, typecheck, syntax check, or build slice.
   - Prefer specific checks over broad suites.
   - If no useful check exists, continue and report: `Validation: not run, no targeted check found`.
   - If validation fails, stop, report the command and concise failure summary, then ask whether to fix before committing.
   - Do not run write-fixers such as `prettier --write`, `eslint --fix`, codegen, or lockfile updates without explicit approval.

5. **Generate the message**
   - Use Conventional Commits: `type(scope): imperative summary`.
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
   - Infer scope from staged files and match recent commit style when practical.
   - Subject: imperative, specific, no period.
   - Body is optional for obvious small commits.
   - Body is required for breaking changes, migrations, multi-file behavior changes, non-obvious fixes, or tradeoffs the subject cannot preserve.
   - Put why first, then what changed. Add `BREAKING CHANGE:` only when required.
   - No co-authors unless explicitly requested.
   - Apply Humanizer rules: natural, specific, no filler, no generic AI phrasing.
   - Use optional context from `$ARGUMENTS` when provided.

6. **Commit or draft**
   - Record the intended boundary before the first `git commit` attempt. Keep that boundary fixed for all retry and amend checks.
   - In commit mode, run `git commit` after staging and validation pass.
   - In draft mode, do not commit; show the proposed boundary and message.
   - After every `git commit` attempt, inspect `git status --short`, `git diff -- <boundary>`, and `git diff --cached -- <boundary>` before deciding success or retry.
   - If the commit succeeds and hook rewrites leave dirty files:
     - Confirm every dirty path is already inside the intended boundary and clearly caused by hooks.
     - Stage those exact paths only.
     - If the dirty files belong to the just-created commit, run `git commit --amend --no-edit` once.
     - Inspect status and diff again before calling it done.
   - If the commit fails and hook rewrites changed files inside the intended boundary:
     - Stage the exact hook-touched paths only.
     - Retry once.
     - Inspect status and diff again after the retry.
   - If the dirty files are outside the boundary, untracked, generated, lockfiles, partially staged, have ambiguous unstaged edits, or the hook ownership is unclear, stop and report the exact files and reason.
   - If hook rewrites repeat after the allowed retry, stop and report.
   - Never use `--no-verify`. Never amend unless the commit was just created in this invocation.

## Output

Use terse output for a clean commit only after the post-commit status and diff checks pass cleanly, including any safe amend flow:

```markdown
Committed `type(scope): summary`

Branch: `branch-name`
Boundary: what was included
Validation: command passed, or not run with reason
Risk check: post-commit status/diff clean after any safe amend
Next: use `/pr` to push or open a draft PR, if relevant
```

Use a structured report only for drafts, blocked commits, risky state, failed validation, decisions, or unsafe hook-rewrite stops: `Status`, `Commit Result`, `Dirty Files`, `Reason`, and `Next`.

Unsafe hook-rewrite states stop here. Do not retry, amend, or broaden staging.

Ask all required questions in one turn. If commit, validation, or staging fails, report the exact problem and do not bypass hooks. If push or PR work is requested, stop after the commit and hand off to `/pr`; new PRs must remain draft-only there.
