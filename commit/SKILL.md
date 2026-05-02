---
name: commit
description: Create git commits with conventional commit messages. ALWAYS use this skill when committing code - whether user-requested or after completing a task. Triggers on "commit", "/commit", "make a commit", "git commit", "save changes", or any request to commit. Accepts optional context argument for commit message guidance.
---

# Commit

## Context

- Branch: !`git branch --show-current`
- Status: !`git status -s`
- Recent commits: !`git log --oneline -5`
- Changed files: !`git diff --name-only`
- Staged files: !`git diff --cached --name-only`

## Steps

1. **Run safety gates and choose the next boundary** - Stop before reading diffs
   or staging files when risk is present:
   - Secret-looking paths: `.env*`, private keys, certificates, token files,
     credential files, database files, or paths with obvious secret names
   - Binary, generated, or dependency noise unrelated to the user's requested work
   - Changed files that appear unrelated to the requested work
   - If unrelated files are present, ask which files to include. Do not stage or
     commit them by default.
   - Decide whether the work forms one clean commit before staging anything.
   - Split commits when changes differ by feature vs. refactor,
     backend vs. frontend, formatting vs. logic, tests vs. production code,
     dependency bumps vs. behavior changes, or any other separable intent.
   - If the staged change cannot be described cleanly in 1-2 sentences, the
     commit is probably too large or mixed. Return to the boundary decision.
2. **Analyze relevant diffs and stage intentionally** - Inspect only relevant
   diffs after the safety gates pass:
   - `git diff -- <path>` for unstaged changes
   - `git diff --cached -- <path>` for staged changes
   - Review staged changes, unstaged modifications in the same files, and
     current branch against the selected commit boundary.
   - Stage only files or hunks that belong in the next commit.
   - Prefer patch staging for mixed-purpose files: `git add -p <path>`.
   - To unstage a hunk or file, use `git restore --staged -p <path>` or
     `git restore --staged <path>`.
3. **Validate the staged intent** - Determine and run the narrowest useful
   validation before proposing a commit:
   - Prefer existing repo checks and file-specific syntax/type checks before
     broad test suites.
   - For production changes, run the closest existing test, type check,
     syntax check, or build slice that exercises the staged behavior.
   - For test-only commits, validate the test file or expected pass/fail
     behavior where practical.
   - If validation fails, stop and report the exact command plus a concise
     failure summary.
   - Do not propose or create a commit while relevant validation is failing.
4. **Describe and generate** - First describe the staged change in 1-2
   sentences, then create the commit message:
   - Description must answer: "What changed?" and "Why?"
   - If the description is awkward, broad, or needs multiple unrelated clauses,
     revisit Step 1 and split the commit.
   - Follow Conventional Commits exactly:

     ```text
     type(scope): short summary

     Body explaining why the change was needed, then what changed.

     BREAKING CHANGE: footer when needed.
     ```

   - Use context if provided: `context: $ARGUMENTS`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   - Infer scope from staged files (e.g., `feat(auth):` for changes in `auth/`)
   - Match recent commits style when possible
   - No co-authors
   - **Subject line**: imperative, specific, and no period. Use verbs like
     "add", "fix", "remove", or "refactor".
   - **Body**:
      - Explain why the change was needed first, then what changed. The why must
        be specific enough to justify the commit.
      - Use imperative mood and present tense, such as "allow users to filter by
        date" instead of "allowed" or "allows"
      - Include motivation for the change
      - Contrast with previous behavior when relevant
      - Be specific about user-facing impact. Avoid vague messages like
        "improved experience"; say exactly what changed.
   - **Footer**: include only required metadata such as `BREAKING CHANGE:` or
     issue references
   - **Breaking changes**: add **!** before the colon in the type prefix, such
     as `feat(api)!: remove v1 endpoints`, and/or use a `BREAKING CHANGE:`
     footer. The footer label MUST be uppercase.
   - Apply Humanizer rules: write naturally, avoid generic AI phrasing, remove
     filler, and keep the message specific to the change.
5. **Report draft** - Use this output format before any write action:

   ```markdown
   ## Status
   [Branch, changed-file count, staged-file count]

   ## Risk Check
   [Secrets/unrelated files/destructive action risks, or "None found"]

   ## Validation
   [Commands run and pass/fail results]

   ## Commit Boundary
   [What belongs in this commit and what, if anything, is intentionally left unstaged]

   ## Staged Change
   [1-2 sentences: what changed and why]

   ## Commit Draft
   [Suggested commit message]

   ## Actions Taken
   [Exactly what was staged, committed, or pushed. If none, say "No write
   actions taken"]

   ## Next Step
   [One clear next command or decision]
   ```

6. **Confirm** - Ask ALL relevant questions at once:
   - No staged files? → "Stage all changes?" / "Select files to stage?"
   - Unstaged mods in staged files? → "Include unstaged changes?"
   - On main/master? → "Create new branch?" with suggested name
   - Show commit message → "Approve?" / "Edit message?"
   - Commit requested? → Commit only after explicit approval
   - Push requested? → Push only after explicit approval
7. **Execute** - Apply only explicit user choices:
   - Stage only the next approved commit's files or hunks.
   - Commit only if the user explicitly requested or approved commit creation.
   - Push only if the user explicitly requested or approved pushing.
   - Never amend an existing commit unless the user explicitly requested amend.
8. **Handle failures** - If commit/push fails:
    - Report the error clearly
    - Never use `--no-verify` to bypass hooks
    - Suggest fixes (e.g., fix lint errors, resolve conflicts)
    - Retry after user addresses the issue
