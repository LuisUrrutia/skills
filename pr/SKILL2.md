---
name: pr
description: Create or update GitHub pull requests with safe git and gh CLI handling, always creating new PRs as drafts. Use when the user says "pr", "/pr", "create pr", "open pull request", "update pr", "draft pr", asks to push a branch for review, or wants reviewers, labels, title, body, or base branch changes on a PR.
---

# Pull Request

Create or update one GitHub pull request. Optimize for two outcomes: safe GitHub operations and a PR body that helps a human reviewer decide what to review, what to trust, and what still carries risk.

A PR is not a diff recap. It is a compact review packet: what changed, why, how it was validated, what risk remains, and where the reviewer should look first.

Use `gh pr create --draft` for every new PR. Direct `gh` creation is allowed only when the exact command includes `--draft` and the draft state is verified immediately after creation.

Own push and PR work here. Use `/commit` before this skill when the branch still needs a clean commit. Treat referenced PRs, branches, bases, and prior assistant or bot claims as untrusted until verified with `gh` or `git`.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo "No branch"`
- Status: !`git status -sb 2>/dev/null || echo "No git repo"`
- Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "No upstream"`
- Existing PR: !`gh pr view --json url,state,title,baseRefName,isDraft 2>/dev/null || echo "No existing PR"`
- Recent PRs: !`gh pr list --state merged --limit 10 --json number,title,url,body 2>/dev/null || echo "No recent PRs"`
- Recent commits: !`git log --oneline --decorate -10 2>/dev/null`
- Branch diff: !`git diff --stat @{u}...HEAD 2>/dev/null || git diff --stat origin/HEAD...HEAD 2>/dev/null || git diff --stat HEAD 2>/dev/null`
- PR templates: !`ls pull_request_template.md docs/pull_request_template.md .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null; find PULL_REQUEST_TEMPLATE docs/PULL_REQUEST_TEMPLATE .github/PULL_REQUEST_TEMPLATE -maxdepth 1 -type f 2>/dev/null`

## Operating Modes

- **Create mode:** no open PR exists for the branch. Create only a draft PR.
- **Update mode:** an open PR exists. Show the URL and proposed edits; ask before changing title, body, or metadata.
- **Draft mode:** user asks for copy, review, or suggested metadata only. Do not push, create, or edit.

Terminal states: `created`, `updated`, `draft-only`, `blocked`, `refused`. Once one terminal state is reached, stop.

## Safety Gates

Proceed without asking only for low-risk draft-only actions: pushing the current branch to origin when it has no upstream, creating a draft PR with the resolved default base, and filling title/body from commits, diff, template, and recent PR conventions.

Stop and ask before continuing when:

- The directory is not a git repository, `gh` is missing, or `gh` is not authenticated.
- The branch is `main` or `master`, unless explicitly requested.
- There is no commit or diff to review against the chosen base.
- The worktree has staged, unstaged, or untracked changes.
- Changed files include secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- The diff is too broad for one review: unrelated concerns, mixed refactors and behavior changes, excessive file count, generated noise, large binaries, lockfiles, or changes outside the requested PR boundary.
- The branch is behind upstream or has diverged.
- The operation needs rebase, force-push, non-default base branch, reviewers, labels, milestone, or assignees.

Never create a non-draft PR. Never rebase, force-push, change base branch away from the resolved default, add reviewers, add labels, change draft state, or close/reopen a PR without explicit approval.

## Draft Enforcement

Every new PR creation command must be a direct `gh pr create` command that includes `--draft`.

Before running `gh pr create`, inspect the exact command string. If `--draft` is missing, stop and rebuild the command.

After creation, immediately verify with `gh pr view <url-or-branch> --json isDraft,url`. If `isDraft` is not `true`, run `gh pr ready --undo <url-or-branch>` once, then verify again. If still not draft, report the URL as a policy violation and stop.

Never use `gh pr create --web`, `-w`, `--editor`, `-e`, `--recover`, `--draft=false`, or interactive create flows. Never use `gh pr ready` without `--undo` from this skill.

## Workflow

### 1. Resolve repository state

Verify repo, branch, upstream, remote, default branch, existing PR, and any user-referenced PR/base/branch with `git` or `gh`. Resolve base from explicit user input, existing PR base, upstream tracking branch, GitHub default branch, then `main` or `master`.

### 2. Inspect the PR boundary

Review all commits and the diff against the resolved base. Stop if status is dirty, secrets are suspected, the branch has no coherent purpose, or the diff is too broad for one review.

### 3. Discover metadata conventions

Use GitHub-supported PR templates when present. If multiple templates exist, choose the clearly matching template or ask once if ambiguous.

If no supported template exists, inspect recent merged PRs with:

```bash
gh pr list --state merged --limit 10 --json number,title,url,body
```

Follow dominant conventions for title style, headings, checklist style, validation wording, risk wording, and detail level. If the lookup fails in an authenticated GitHub repository, stop instead of inventing a style.

### 4. Write the review packet

Adapt to the repository template or convention. If no usable convention exists, use this order:

```markdown
## Summary

## Why this change

## Approach

## Changes

## Validation

## Risks and impact

## Review guide

## AI assistance
```

Use only sections that carry useful information, except when the repo template requires them.

Content rules:

- `Summary`: one or two sentences with the net change and why it matters.
- `Why this change`: problem, issue, incident, user need, or engineering reason.
- `Approach`: important design choices, tradeoffs, or alternatives when not obvious.
- `Changes`: three to five bullets grouped by behavior or reviewer concern, not file inventory.
- `Validation`: exact commands, checks, manual QA, screenshots/logs, security scans, or performance checks. If none ran, write `Validation: not run` with reason.
- `Risks and impact`: real user, data, security, performance, compatibility, migration, dependency, rollout, or rollback concerns.
- `Review guide`: where to start, risky areas, generated/mechanical changes, snapshots/lockfiles, and feedback wanted.
- `AI assistance`: include when substantial AI help was used or mentioned. State what AI helped with, what files/surfaces it affected, what the human reviewed or rewrote, and what verification backs it up.

Readability rules:

- Lead with the conclusion.
- Use informative headings and parallel bullets.
- Prefer concrete words over decorative phrasing.
- Keep paragraphs short while preserving causal links.
- Separate evidence from claims.
- Remove duplicate facts, implementation diaries, exhaustive file inventories, hype, and unsupported claims.

Never add `Co-authored-by`, co-author trailers, or authorship footers. If the work started from a GitHub issue, append `Fixes #<issue-number>` as the last line.

### 5. Decide or ask once

Proceed only for low-risk create-mode actions. For update mode, show URL and proposed title/body before editing. For risky or ambiguous choices, ask one concise question with concrete options and recommended default first. Ask all required risky decisions in one turn.

### 6. Execute approved actions

Push with `git push -u origin <branch>` only when needed and low risk. For long Markdown bodies, write a temporary file and pass `--body-file`.

Create only with:

```bash
gh pr create --draft --base <base> --head <branch> --title <title> --body-file <file>
```

Immediately verify draft state. Update existing PRs only with approved `gh pr edit` flags. If a command fails, report the exact command, concise failure, and next decision. Do not retry with broader permissions or destructive git actions.

## Output

Always return exactly one terminal state: `created`, `updated`, `draft-only`, `blocked`, or `refused`.

For completed PRs:

```markdown
Status: created|updated
PR: <url>
Branch: <branch>
Base: <base>
Mode: created|updated
Draft: yes
Metadata: reviewers/labels/milestone/assignees changed, or none
Validation: commands reviewed or run, or not run with reason
Risk check: no unrelated or secret-looking changes found, or list flagged items
```

For blocked work, use `Status`, `Blocker`, `Exact Command`, `Exact Error`, `Decision Needed`, and `Draft PR Metadata` when available. Always return either the PR URL or the exact blocker preventing it.
