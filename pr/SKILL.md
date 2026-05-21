---
name: pr
description: Create or update GitHub pull requests with safe git and gh CLI handling. Use when the user says "pr", "/pr", "create pr", "open pull request", "update pr", "draft pr", asks to push a branch for review, or wants reviewers, labels, title, body, or base branch changes on a PR.
---

# Pull Request

Create or update one GitHub pull request. Inspect the branch, commits, diff, template, and existing PR state; use safe defaults for low-risk actions; ask only before destructive, unusual, or ambiguous decisions.

Own push and PR work here. Use `/commit` before this skill when the branch still needs a clean commit.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo "No branch"`
- Status: !`git status -sb 2>/dev/null || echo "No git repo"`
- Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "No upstream"`
- Existing PR: !`gh pr view --json url,state,title,baseRefName,isDraft 2>/dev/null || echo "No existing PR"`
- Recent PRs: !`gh pr list --state merged --limit 5 --json number,title,url,body 2>/dev/null || echo "No recent PRs"`
- Recent commits: !`git log --oneline --decorate -10 2>/dev/null`
- Branch diff: !`git diff --stat @{u}...HEAD 2>/dev/null || git diff --stat origin/HEAD...HEAD 2>/dev/null || git diff --stat HEAD 2>/dev/null`
- PR template: !`ls .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md 2>/dev/null`

## Modes

- **Create mode**: No open PR exists for the branch. Create a draft PR by default.
- **Update mode**: An open PR exists. Show the PR URL and proposed edits; ask before changing title, body, or metadata.
- **Draft mode**: User asks to prepare copy, review PR state, or suggest metadata. Do not push, create, or edit.

## Safety Gates

Proceed without asking for low-risk defaults: pushing the current branch to origin when it has no upstream, creating a draft PR with the resolved default base, and filling title/body from commits, diff, and template.

Stop and ask before continuing when:

- The current directory is not a git repository, `gh` is missing, or `gh` is not authenticated.
- The branch is `main` or `master`, unless the user explicitly wants a PR from that branch.
- There is no commit or diff to review against the chosen base.
- The worktree has staged, unstaged, or untracked changes. PRs must be created from committed work only.
- Changed files include secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- The diff includes unrelated changes, generated noise, dependency changes, lockfiles, large binaries, or files outside the requested PR boundary.
- The branch is behind its upstream or has diverged.
- The operation needs rebase, force-push, non-default base branch, ready-for-review state, reviewers, labels, milestone, or assignees.

Never rebase, force-push, change base branch away from the resolved default, add reviewers, add labels, mark ready for review, or close/reopen a PR without explicit approval.

## Workflow

1. **Resolve repository state**
   - Confirm git repo, current branch, upstream, remote, and default branch.
   - Determine the base from `$ARGUMENTS`, existing PR base, upstream tracking branch, GitHub default branch, then `main` or `master`.
   - Detect an existing PR with `gh pr view`; if one exists, default to update mode.

2. **Inspect the PR boundary**
   - Review commits included in the PR, not just the latest commit.
   - Review the diff against the resolved base, excluding obvious binary/generated artifacts from summaries but still flagging risky files.
   - Check status for staged, unstaged, and untracked files. Stop if any are present.

3. **Prepare PR metadata**
   - Follow `.github/PULL_REQUEST_TEMPLATE.md` or `.github/pull_request_template.md` when present.
   - For template checklists, infer checked items from the diff when the evidence is strong. Leave unverifiable items unchecked.
   - If no template exists, inspect the previous five merged PRs and follow their title/body conventions when a clear pattern exists.
   - If no template or clear recent-PR convention exists, use: summary, changes, validation, risks.
   - If no tests or checks were run in the current session, write `Validation: not run` with the reason.
   - Title should be concise, imperative, and specific. Match recent PR or commit style when obvious.
   - Body should explain why the change exists, what changed, how it was validated, and any reviewer risks.

4. **Decide or ask once**
   - If only low-risk defaults are needed and no PR exists, proceed: push the current branch if needed, then create a draft PR.
   - If a PR already exists, show the existing PR URL and proposed title/body changes, then ask before editing.
   - If any risky decision is needed, present mode, branch, base, push/rebase needs, draft state, reviewers, labels, and the exact title/body.
   - Ask all required risky decisions in one turn. Do not proceed on partial approval when a risky operation remains undecided.

5. **Execute approved actions**
   - Push with `git push -u origin <branch>` when the branch has no upstream and the push is low-risk.
   - Create with `gh pr create --draft --base <base> --head <branch> --title <title> --body <body>` unless the user explicitly approved ready-for-review.
   - Update with `gh pr edit <url-or-branch> --title <title> --body <body>` and only the approved metadata flags.
   - If a command fails, report the exact command, concise failure, and next decision. Do not retry with broader permissions or destructive git actions.

## Output

For a completed PR, respond tersely:

```markdown
PR: <url>
Branch: <branch>
Base: <base>
Mode: created|updated
Draft: yes|no
Metadata: reviewers/labels/milestone/assignees changed, or none
Validation: commands reviewed or run, or not run with reason
Risk check: no unrelated or secret-looking changes found, or list flagged items
```

For blocked work, use `Status`, `Blocker`, `Decision Needed`, and `Draft PR Metadata`. Always return either the PR URL or the exact blocker preventing it.
