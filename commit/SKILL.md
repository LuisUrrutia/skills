---
name: commit
description: Create safe git commits with Conventional Commit messages. ALWAYS use this skill when committing code, whether user-requested or after completing a task. Use when the user says "commit", "/commit", "make a commit", "git commit", "save changes", or asks to prepare a commit. Accepts optional context for commit-message guidance.
---

# Commit

Create one safe, intentional commit. Inspect the work, choose a clean boundary, stage only what belongs, validate the staged intent, then commit when the user explicitly asked for it or approves the draft.

Never push from this skill. Use `/pr` for push and pull-request work.

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
   - In commit mode, run `git commit` after staging and validation pass.
   - In draft mode, do not commit; show the proposed boundary and message.
   - If hooks mutate files, inspect the new diff, re-stage only intended changes, and retry only when the boundary remains clear. Otherwise report what changed and ask.
   - Never use `--no-verify`. Never amend unless explicitly requested.

## Output

Use terse output for a clean commit:

```markdown
Committed `type(scope): summary`

Branch: `branch-name`
Boundary: what was included
Validation: command passed, or not run with reason
Risk check: no unrelated files or secret-looking paths found
Next: use `/pr` to push or open a PR, if relevant
```

Use a structured report only for drafts, blocked commits, risky state, failed validation, or decisions: `Status`, `Risk Check`, `Validation`, `Commit Boundary`, `Commit Draft`, and `Decision Needed`.

Ask all required questions in one turn. If commit, validation, or staging fails, report the exact problem and do not bypass hooks. If push or PR work is requested, stop after the commit and hand off to `/pr`.
