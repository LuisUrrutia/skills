---
name: pr
description: Create or update GitHub pull requests. Use when user says "pr", "/pr", "create pr", "open pr", "pull request", or asks to submit changes for review. Requires gh CLI.
---

## Context
- Branch: !`git branch --show-current`
- Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"`
- Remote status: !`git status -sb`
- Existing PR: !`gh pr view --json url,state 2>/dev/null || echo "No PR exists"`
- Commits: !`git log origin/HEAD..HEAD --oneline 2>/dev/null || git log origin/main..HEAD --oneline`
- Diff: !`git diff origin/HEAD...HEAD -- . ':!*.svg' ':!*lock.json' ':!*lock.yaml' ':!*.lockb' ':!*.lock' ':!.opencode' ':!.claude' ':!.cursor' ':!*.png' ':!*.jpg' ':!*.jpeg' ':!*.gif' ':!*.ico' ':!*.webp' ':!*.avif' ':!*.bmp' ':!*.tiff' ':!*.psd' ':!*.ai' ':!*.eps' ':!*.raw' ':!*.woff' ':!*.woff2' ':!*.ttf' ':!*.eot' ':!*.otf' ':!*.mp3' ':!*.mp4' ':!*.wav' ':!*.ogg' ':!*.webm' ':!*.mov' ':!*.pdf' ':!*.doc' ':!*.docx' ':!*.xls' ':!*.xlsx' ':!*.ppt' ':!*.pptx' ':!*.zip' ':!*.tar.gz' ':!*.gz' ':!*.rar' ':!*.7z' ':!*.bin' ':!*.exe' ':!*.dll' ':!*.so' ':!*.dylib' ':!*.db' ':!*.sqlite' ':!*.sqlite3' ':!*.map' ':!*.js.map' ':!*.css.map' ':!*.min.js' ':!*.min.css' ':!*.bundle.js' ':!*.class' ':!*.jar' ':!*.war' ':!*.pyc' ':!*.pyo' ':!*.whl' ':!*.pem' ':!*.key' ':!*.crt' ':!*.p12' ':!*.parquet' ':!*.pickle' ':!*.npy' ':!*.sketch' ':!*.fig' ':!*.xd' 2>/dev/null || git diff origin/main...HEAD -- . ':!*.svg' ':!*lock.json' ':!*lock.yaml' ':!*.lockb' ':!*.lock' ':!.opencode' ':!.claude' ':!.cursor' ':!*.png' ':!*.jpg' ':!*.jpeg' ':!*.gif' ':!*.ico' ':!*.webp' ':!*.avif' ':!*.bmp' ':!*.tiff' ':!*.psd' ':!*.ai' ':!*.eps' ':!*.raw' ':!*.woff' ':!*.woff2' ':!*.ttf' ':!*.eot' ':!*.otf' ':!*.mp3' ':!*.mp4' ':!*.wav' ':!*.ogg' ':!*.webm' ':!*.mov' ':!*.pdf' ':!*.doc' ':!*.docx' ':!*.xls' ':!*.xlsx' ':!*.ppt' ':!*.pptx' ':!*.zip' ':!*.tar.gz' ':!*.gz' ':!*.rar' ':!*.7z' ':!*.bin' ':!*.exe' ':!*.dll' ':!*.so' ':!*.dylib' ':!*.db' ':!*.sqlite' ':!*.sqlite3' ':!*.map' ':!*.js.map' ':!*.css.map' ':!*.min.js' ':!*.min.css' ':!*.bundle.js' ':!*.class' ':!*.jar' ':!*.war' ':!*.pyc' ':!*.pyo' ':!*.whl' ':!*.pem' ':!*.key' ':!*.crt' ':!*.p12' ':!*.parquet' ':!*.pickle' ':!*.npy' ':!*.sketch' ':!*.fig' ':!*.xd'`

## Steps

1. **Check state**:
   - PR already exists? → Show URL and ask: update existing or create new?
   - On default branch (main/master)? → Warn and stop (PRs should be from feature branches)
   - Not pushed? → Will need to push first
   - Behind remote? → Will need to rebase first (warn: requires force-push after rebase)
2. **Analyze** - Review all commits and changes
3. **Generate** - PR title and description
   - Follow `.github/PULL_REQUEST_TEMPLATE.md` if exists
4. **Single confirmation** - Ask ALL relevant questions at once:
   - Need to push? → "Push branch to origin?"
   - Need to rebase? → "Rebase on [default branch] first?" (note: will require force-push)
   - Show PR title/description → "Approve?" / "Edit?"
   - "Create as draft?" → Yes/No
   - "Add reviewers/labels?" → Optional, list if requested
   - "Different base branch?" → Default is detected default branch
5. **Execute** - Push if needed, then `gh pr create` (add `--draft` if requested)
6. **Handle failures** - If push/PR creation fails:
   - `gh` not authenticated? → Run `gh auth login`
   - Push rejected? → Check permissions, branch protection rules
   - PR creation failed? → Report error, check for required fields

## Notes
- Follow PR template strictly if exists
- Complete all required sections
- Return the PR URL when done
