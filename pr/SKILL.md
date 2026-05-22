---
name: pr
description: Create or update GitHub pull requests with safe git and gh CLI handling, always creating new PRs as drafts. Use when the user says "pr", "/pr", "create pr", "open pull request", "update pr", "draft pr", asks to push a branch for review, or wants reviewers, labels, title, body, or base branch changes on a PR.
---

# Pull Request

Create or update one GitHub pull request. Inspect the branch, commits, diff, template, and existing PR state; always create new PRs as drafts; ask only before destructive, unusual, or ambiguous decisions.

Use `scripts/create-draft-pr.sh` for every new PR. Treat raw `gh pr create` as forbidden unless the wrapper is unavailable; if raw creation is unavoidable, it must use the exact draft enforcement sequence below.

Own push and PR work here. Use `/commit` before this skill when the branch still needs a clean commit.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo "No branch"`
- Status: !`git status -sb 2>/dev/null || echo "No git repo"`
- Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "No upstream"`
- Existing PR: !`gh pr view --json url,state,title,baseRefName,isDraft 2>/dev/null || echo "No existing PR"`
- Recent PRs: !`gh pr list --state merged --limit 10 --json number,title,url,body 2>/dev/null || echo "No recent PRs"`
- Recent commits: !`git log --oneline --decorate -10 2>/dev/null`
- Branch diff: !`git diff --stat @{u}...HEAD 2>/dev/null || git diff --stat origin/HEAD...HEAD 2>/dev/null || git diff --stat HEAD 2>/dev/null`
- PR template: !`ls .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md 2>/dev/null`

## Modes

- **Create mode**: No open PR exists for the branch. Always create a draft PR.
- **Update mode**: An open PR exists. Show the PR URL and proposed edits; ask before changing title, body, or metadata.
- **Draft mode**: User asks to prepare copy, review PR state, or suggest metadata. Do not push, create, or edit.

## Safety Gates

Proceed without asking for low-risk draft-only actions: pushing the current branch to origin when it has no upstream, creating a draft PR with the resolved default base, and filling title/body from commits, diff, and template.

Stop and ask before continuing when:

- The current directory is not a git repository, `gh` is missing, or `gh` is not authenticated.
- The branch is `main` or `master`, unless the user explicitly wants a PR from that branch.
- There is no commit or diff to review against the chosen base.
- The worktree has staged, unstaged, or untracked changes. PRs must be created from committed work only.
- Changed files include secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- The diff includes unrelated changes, generated noise, dependency changes, lockfiles, large binaries, or files outside the requested PR boundary.
- The branch is behind its upstream or has diverged.
- The operation needs rebase, force-push, non-default base branch, reviewers, labels, milestone, or assignees.

Never create a non-draft PR. Never rebase, force-push, change base branch away from the resolved default, add reviewers, add labels, change draft state, or close/reopen a PR without explicit approval.

### Draft Enforcement

This rule is absolute: every new PR creation command must include `--draft`. Prefer the bundled wrapper because it inserts `--draft`, blocks interactive/non-deterministic flags, verifies the result, attempts one conversion back to draft, and fails closed if draft state cannot be proven.

Before running any raw `gh pr create` command, inspect the exact command string. If `--draft` is missing, stop and rewrite the command; do not ask the user whether to continue, and do not run it.

After creating a PR, immediately verify draft state with `gh pr view <url-or-branch> --json isDraft,url`. If `isDraft` is not `true`, run `gh pr ready --undo <url-or-branch>` once, then verify again. If `isDraft` is still not `true`, report the URL as a policy violation and do not continue with metadata edits or any other PR actions.

Never use `gh pr create --web`, `gh pr create -w`, `gh pr create --editor`, `gh pr create -e`, `gh pr create --recover`, `--draft=false`, or any interactive create flow. Never use `gh pr ready` without `--undo` from this skill.

### Metadata Consistency Enforcement

If no PR template exists, inspecting previous merged PRs is mandatory. Run `gh pr list --state merged --limit 10 --json number,title,url,body` before drafting the title or body. Do not create, update, or propose PR metadata until that lookup has been performed and summarized.

When recent merged PRs exist, copy their dominant conventions: title prefix/case, section headings, checklist style, validation wording, risk wording, and level of detail. If conventions conflict, follow the newest matching PRs that are closest to the current change type.

Only use the fallback `summary, changes, validation, risks` structure after proving that no template exists and recent merged PRs are unavailable or unusable. If the `gh pr list` lookup fails for an authenticated GitHub repository, stop and report the lookup failure instead of inventing a style.

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
   - If no template exists, run `gh pr list --state merged --limit 10 --json number,title,url,body`, inspect the previous merged PRs, and write down the dominant title/body convention before drafting metadata.
   - If recent merged PRs are available, follow their dominant convention. Do not use the fallback structure just because it is easier.
   - If no template exists and the recent-PR lookup fails, stop and report the exact command failure instead of creating or updating PR metadata.
   - If no template exists and no usable recent-PR convention exists after a successful lookup, use: summary, changes, validation, risks.
   - If no tests or checks were run in the current session, write `Validation: not run` with the reason.
   - Title should be concise, imperative, and specific. Match the recent merged PR style when a pattern exists; otherwise use commit style only as a last resort.
   - Body should explain why the change exists, what changed, how it was validated, and any reviewer risks.
   - If the work started from a GitHub issue, append `Fixes #<issue-number>` as the last line of the PR body so GitHub tracks the closure.

4. **Decide or ask once**
   - If only low-risk draft-only actions are needed and no PR exists, proceed: push the current branch if needed, then create a draft PR.
   - If a PR already exists, show the existing PR URL and proposed title/body changes, then ask before editing.
   - If any risky decision is needed, present mode, branch, base, push/rebase needs, reviewers, labels, and the exact title/body. Draft state is not configurable for new PRs.
   - Ask all required risky decisions in one turn. Do not proceed on partial approval when a risky operation remains undecided.

5. **Execute approved actions**
   - Push with `git push -u origin <branch>` when the branch has no upstream and the push is low-risk.
   - Create only with `scripts/create-draft-pr.sh --base <base> --head <branch> --title <title> --body <body>`. The wrapper must print the PR URL only after proving `isDraft: true`.
   - If the wrapper is unavailable, create only with `gh pr create --draft --base <base> --head <branch> --title <title> --body <body>`. Do not omit `--draft` for any new PR. If the command you are about to run does not contain `--draft`, stop before execution and rebuild it.
   - Immediately verify the created PR with `gh pr view <url-or-branch> --json isDraft,url`; the result must show `isDraft: true` before reporting success. If needed, run `gh pr ready --undo <url-or-branch>` once and verify again.
   - Update with `gh pr edit <url-or-branch> --title <title> --body <body>` and only the approved metadata flags.
   - If a command fails, report the exact command, concise failure, and next decision. Do not retry with broader permissions or destructive git actions.

## Output

For a completed PR, respond tersely:

```markdown
PR: <url>
Branch: <branch>
Base: <base>
Mode: created|updated
Draft: yes
Metadata: reviewers/labels/milestone/assignees changed, or none
Validation: commands reviewed or run, or not run with reason
Risk check: no unrelated or secret-looking changes found, or list flagged items
```

For blocked work, use `Status`, `Blocker`, `Decision Needed`, and `Draft PR Metadata`. Always return either the PR URL or the exact blocker preventing it.
