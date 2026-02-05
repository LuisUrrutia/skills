---
name: commit
description: Create git commits with conventional commit messages. ALWAYS use this skill when committing code - whether user-requested or after completing a task. Triggers on "commit", "/commit", "make a commit", "git commit", "save changes", or any request to commit. Accepts optional context argument for commit message guidance.
---

## Context

- Branch: !`git branch --show-current`
- Status: !`git status -s`
- Recent commits: !`git log --oneline -5`
- Staged diff: !`git diff --staged -- . ':!*.svg' ':!*lock.json' ':!*lock.yaml' ':!*.lockb' ':!*.lock' ':!.opencode' ':!.claude' ':!.cursor' ':!*.png' ':!*.jpg' ':!*.jpeg' ':!*.gif' ':!*.ico' ':!*.webp' ':!*.avif' ':!*.bmp' ':!*.tiff' ':!*.psd' ':!*.ai' ':!*.eps' ':!*.raw' ':!*.woff' ':!*.woff2' ':!*.ttf' ':!*.eot' ':!*.otf' ':!*.mp3' ':!*.mp4' ':!*.wav' ':!*.ogg' ':!*.webm' ':!*.mov' ':!*.pdf' ':!*.doc' ':!*.docx' ':!*.xls' ':!*.xlsx' ':!*.ppt' ':!*.pptx' ':!*.zip' ':!*.tar.gz' ':!*.gz' ':!*.rar' ':!*.7z' ':!*.bin' ':!*.exe' ':!*.dll' ':!*.so' ':!*.dylib' ':!*.db' ':!*.sqlite' ':!*.sqlite3' ':!*.map' ':!*.js.map' ':!*.css.map' ':!*.min.js' ':!*.min.css' ':!*.bundle.js' ':!*.class' ':!*.jar' ':!*.war' ':!*.pyc' ':!*.pyo' ':!*.whl' ':!*.pem' ':!*.key' ':!*.crt' ':!*.p12' ':!*.parquet' ':!*.pickle' ':!*.npy' ':!*.sketch' ':!*.fig' ':!*.xd'`
- Staged files: !`git diff --staged --name-only`

## Steps

1. **Analyze** — Review staged changes, unstaged modifications, and current branch
2. **Generate** — Create commit message following conventional commits: `type(scope): message`
   - Use context if provided: `context: $ARGUMENTS`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   - Infer scope from staged files (e.g., `feat(auth):` for changes in `auth/`)
   - Match recent commits style when possible
   - No co-authors
   - **Subject line**: imperative mood, present tense, lowercase, no period
   - **Body**:
     - Explain **why**, not **what** — the diff already shows what changed
     - Use imperative mood and present tense (e.g., "allow users to filter by date" not "allowed" or "allows")
     - Include motivation for the change
     - Contrast with previous behavior when relevant
     - Be specific about user-facing impact — avoid vague messages like "improved experience"; say exactly what changed
   - **Breaking changes**: indicate with `!` before `:` (e.g., `feat(api)!: remove v1 endpoints`) or a `BREAKING CHANGE:` footer — MUST be uppercase
3. **Confirm** — Ask ALL relevant questions at once:
   - No staged files? → "Stage all changes?" / "Select files to stage?"
   - Unstaged mods in staged files? → "Include unstaged changes?"
   - On main/master? → "Create new branch?" with suggested name
   - Show commit message → "Approve?" / "Edit message?"
   - "Push after commit?" → Yes/No
4. **Execute** — Apply user choices, commit, and push if requested
5. **Handle failures** — If commit/push fails:
   - Report the error clearly
   - Never use `--no-verify` to bypass hooks
   - Suggest fixes (e.g., fix lint errors, resolve conflicts)
   - Retry after user addresses the issue
