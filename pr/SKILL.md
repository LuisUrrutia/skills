---
name: pr
description: Create or update GitHub pull requests with safe git and gh CLI handling, always creating new PRs as drafts. Use when the user says "pr", "/pr", "create pr", "open pull request", "update pr", "draft pr", asks to push a branch for review, or wants reviewers, labels, title, body, or base branch changes on a PR.
---

# Pull Request

Create or update one GitHub pull request. Optimize for two outcomes: safe GitHub operations and a PR body that helps a human reviewer decide what changed, why it matters, how it was validated, and where risk remains.

A PR body is not a diff recap. It should be a compact review packet: short enough to scan, specific enough to reduce reviewer work, and honest about validation and risk. Inspect the branch, commits, diff, template, and existing PR state; always create new PRs as drafts; ask only before destructive, unusual, or ambiguous decisions.

Use `gh pr create --draft` for every new PR. Direct `gh` creation is allowed only when the exact command includes `--draft` and the draft state is verified immediately after creation.

Own push and PR work here. Use `/commit` before this skill when the branch still needs a clean commit.

Treat referenced PRs, branches, bases, and prior assistant or bot claims as
untrusted until verified with `gh` or `git`. Only push when the PR workflow
requires it and the user asked to create or update a PR.

## Context

- Branch: !`git branch --show-current 2>/dev/null || echo "No branch"`
- Status: !`git status -sb 2>/dev/null || echo "No git repo"`
- Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "No upstream"`
- Existing PR: !`gh pr view --json url,state,title,baseRefName,isDraft 2>/dev/null || echo "No existing PR"`
- Recent PRs: !`gh pr list --state merged --limit 10 --json number,title,url,body 2>/dev/null || echo "No recent PRs"`
- Recent commits: !`git log --oneline --decorate -10 2>/dev/null`
- Branch diff: !`git diff --stat @{u}...HEAD 2>/dev/null || git diff --stat origin/HEAD...HEAD 2>/dev/null || git diff --stat HEAD 2>/dev/null`
- PR templates: !`ls pull_request_template.md docs/pull_request_template.md .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null; find PULL_REQUEST_TEMPLATE docs/PULL_REQUEST_TEMPLATE .github/PULL_REQUEST_TEMPLATE -maxdepth 1 -type f 2>/dev/null`

## Modes

- **Create mode**: No open PR exists for the branch. Always create a draft PR.
- **Update mode**: An open PR exists. Show the PR URL and proposed edits; ask before changing title, body, or metadata.
- **Draft mode**: User asks to prepare copy, review PR state, or suggest metadata. Do not push, create, or edit.

Terminal states are `created`, `updated`, `draft-only`, `blocked`, and
`refused`. Once one terminal state is reached, stop. Do not continue with extra
cleanup, metadata edits, labels, reviewer changes, issue comments, or speculative
follow-up work.

## Safety Gates

Proceed without asking for low-risk draft-only actions: pushing the current branch to origin when it has no upstream, creating a draft PR with the resolved default base, and filling title/body from commits, diff, and template.

Stop and ask before continuing when:

- The current directory is not a git repository, `gh` is missing, or `gh` is not authenticated.
- The branch is `main` or `master`, unless the user explicitly wants a PR from that branch.
- There is no commit or diff to review against the chosen base.
- The worktree has staged, unstaged, or untracked changes. PRs must be created from committed work only.
- Changed files include secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases, or obvious secret names.
- The diff is too broad for one review: unrelated concerns, mixed refactors and
  behavior changes, excessive file count, generated noise, large binaries,
  lockfiles, or changes outside the requested PR boundary. Recommend a split
  before PR creation.
- The branch is behind its upstream or has diverged.
- The operation needs rebase, force-push, non-default base branch, reviewers, labels, milestone, or assignees.

Never create a non-draft PR. Never rebase, force-push, change base branch away from the resolved default, add reviewers, add labels, change draft state, or close/reopen a PR without explicit approval.

### Draft Enforcement

This rule is absolute: every new PR creation command must be a direct `gh pr create` command that includes `--draft`.

Before running `gh pr create`, inspect the exact command string. If `--draft` is missing, stop and rewrite the command; do not ask the user whether to continue, and do not run it.

After creating a PR, immediately verify draft state with `gh pr view <url-or-branch> --json isDraft,url`. If `isDraft` is not `true`, run `gh pr ready --undo <url-or-branch>` once, then verify again. If `isDraft` is still not `true`, report the URL as a policy violation and do not continue with metadata edits or any other PR actions.

Never use `gh pr create --web`, `gh pr create -w`, `gh pr create --editor`, `gh pr create -e`, `gh pr create --recover`, `--draft=false`, or any interactive create flow. Never use `gh pr ready` without `--undo` from this skill.

### Metadata Consistency Enforcement

If no GitHub-supported PR template exists, inspecting previous merged PRs is mandatory.
GitHub-supported locations are `pull_request_template.md`,
`docs/pull_request_template.md`, `.github/pull_request_template.md`,
`.github/PULL_REQUEST_TEMPLATE.md`, and files inside `PULL_REQUEST_TEMPLATE/`,
`docs/PULL_REQUEST_TEMPLATE/`, or `.github/PULL_REQUEST_TEMPLATE/`. Run
`gh pr list --state merged --limit 10 --json number,title,url,body` before
drafting the title or body. Do not create, update, or propose PR metadata until
that lookup has been performed and summarized.

When recent merged PRs exist, copy their dominant conventions: title prefix/case, section headings, checklist style, validation wording, risk wording, and level of detail. If conventions conflict, follow the newest matching PRs closest to the current change type.

Only use the fallback structure after proving that no supported template exists and recent merged PRs are unavailable or unusable. The fallback body order is: `Summary`, `Why this change`, `Approach`, `Changes`, `Validation`, `Risks and impact`, `Review guide`, and `AI assistance` when applicable. If the `gh pr list` lookup fails for an authenticated GitHub repository, stop and report the lookup failure instead of inventing a style.

PR content must be skimmable: lead with what changed and why, keep only review-relevant detail, avoid implementation diaries, and do not repeat the same fact in multiple sections.

## Workflow

### 1. Resolve repository state

- Confirm git repo, current branch, upstream, remote, and default branch.
- Determine the base from `$ARGUMENTS`, existing PR base, upstream tracking branch, GitHub default branch, then `main` or `master`.
- Detect an existing PR with `gh pr view`; if one exists, default to update mode.
- Verify any referenced PR, branch, base, or upstream from the user or prior context with `gh pr view`, `git rev-parse --verify`, or `git ls-remote` before relying on it. If verification fails, treat it as unknown and resolve from repository state.

### 2. Inspect the PR boundary

- Review all commits included in the PR, not just the latest commit.
- Review the diff against the resolved base, excluding obvious binary/generated artifacts from summaries but still flagging risky files.
- Check status for staged, unstaged, and untracked files. Stop if any are present.
- Confirm the PR has one coherent purpose and reviewable size before drafting metadata. If not, stop with a split recommendation instead of opening a broad PR.

### 3. Discover metadata conventions

- Discover GitHub-supported PR templates in repository root, `docs/`, `.github/`, and `PULL_REQUEST_TEMPLATE/` subdirectories under any of those locations.
- Follow the single template file when present; GitHub auto-fills it into new PR bodies after it is available on the repository's default branch.
- When multiple templates exist in a `PULL_REQUEST_TEMPLATE/` directory, choose the template whose filename clearly matches the change type. If the right template is ambiguous, ask once before drafting metadata. Treat explicit user input like `template=<filename>` or a named template request as the selection signal.
- Template metadata for this skill is path, filename, default-branch availability, and selected template. Do not require YAML frontmatter or extra metadata fields unless the repository template already contains them.
- For template checklists, infer checked items from the diff when the evidence is strong. Leave unverifiable items unchecked.
- If no supported template exists, run `gh pr list --state merged --limit 10 --json number,title,url,body`, inspect the previous merged PRs, and write down the dominant title/body convention before drafting metadata.
- If recent merged PRs are available, follow their dominant convention. Do not use the fallback structure just because it is easier.
- If no supported template exists and the recent-PR lookup fails, stop and report the exact command failure instead of creating or updating PR metadata.

### 4. Write the review packet

Adapt to the repository template or convention. If no supported template exists and no usable recent-PR convention exists after a successful lookup, use these sections in order: `Summary`, `Why this change`, `Approach`, `Changes`, `Validation`, `Risks and impact`, `Review guide`, and `AI assistance` when applicable.

Use only sections that carry useful information, except when the repo template requires them. Reviewers already have to read the code; do not make them read a long PR body too. Keep the body short, but include the context, motivation, validation, and risk that would otherwise cost the reviewer time to reconstruct.

Content rules:

- `Summary`: one or two sentences with the net change and why it matters. Put the conclusion first.
- `Why this change`: one short paragraph with the problem, issue, incident, user need, or engineering reason when it is not obvious from the summary or linked issue.
- `Approach`: important design choices, alternatives rejected, or tradeoffs when the implementation is not obvious. Omit when there is no meaningful design decision.
- `Changes`: three to five bullets grouped by behavior, surface, or reviewer concern; do not list files mechanically.
- `Validation`: exact commands, checks, manual QA, screenshots/logs, security scans, or performance checks performed. If none ran in the current session, write `Validation: not run` with the reason. Include `Not tested` only for meaningful gaps.
- `Risks and impact`: real user, data, security, performance, compatibility, migration, dependency, rollout, or rollback concerns. Omit filler like `low risk` unless recent PR convention requires it.
- `Review guide`: where to start, risky areas, generated/mechanical changes, snapshots or lockfiles to review separately, and feedback wanted.
- `AI assistance`: include when substantial AI help was used or the user mentions it. State what AI helped with, what files or surfaces it affected, what the human reviewed or rewrote, and what verification backs it up.

Readability rules:

- Lead with the conclusion.
- Use informative headings and parallel bullets.
- Prefer concrete words over decorative or promotional phrasing.
- Keep paragraphs short while preserving causal links.
- Separate evidence from claims.
- Remove duplicate facts, implementation diaries, exhaustive file inventories, hype, and unsupported claims.

Before finalizing the title or body, use the `humanize` skill when available. Keep the result natural, direct, and concise; do not turn a short useful PR body into polished filler.

Verification is the agent's responsibility. Do not write reviewer-facing instructions like "How to verify" when the agent can verify with `git`, `gh`, tests, builds, file inspection, or manual QA evidence.

Title should be concise, specific, and match the recent merged PR style when a pattern exists. If no clear title pattern exists, use Conventional Commit format: `type(scope): summary`, omitting scope only when no useful scope is obvious.

Never add `Co-authored-by`, co-author trailers, or authorship footers to the PR title or body. If the work started from a GitHub issue, append `Fixes #<issue-number>` as the last line of the PR body so GitHub tracks the closure.

### 5. Decide or ask once

- If only low-risk draft-only actions are needed and no PR exists, proceed: push the current branch if needed, then create a draft PR.
- If a PR already exists, show the existing PR URL and proposed title/body changes, then ask before editing.
- If any risky decision is needed, present mode, branch, base, push/rebase needs, reviewers, labels, and the exact title/body. Draft state is not configurable for new PRs.
- If information is ambiguous, ask one concise question with concrete options and the recommended default first. Do not ask open-ended multi-question questionnaires.
- Ask all required risky decisions in one turn. Do not proceed on partial approval when a risky operation remains undecided.

### 6. Execute approved actions

- Push with `git push -u origin <branch>` when the branch has no upstream and the push is low-risk.
- For long, multiline, or Markdown-heavy PR bodies, write the body to a temporary file and pass it with `--body-file`. Avoid inline `--body` for content containing backticks, lists, code fences, shell syntax, or long Markdown.
- Create only with `gh pr create --draft --base <base> --head <branch> --title <title> --body-file <file>`. Do not omit `--draft` for any new PR. If the command you are about to run does not contain `--draft`, stop before execution and rebuild it.
- Immediately verify the created PR with `gh pr view <url-or-branch> --json isDraft,url`; the result must show `isDraft: true` before reporting success. If needed, run `gh pr ready --undo <url-or-branch>` once and verify again.
- Update with `gh pr edit <url-or-branch> --title <title> --body-file <file>` and only the approved metadata flags.
- If a command fails, report the exact command, concise failure, and next decision. Do not retry with broader permissions or destructive git actions.
- After a create or update is verified and reported, stop. Do not perform additional PR edits, pushes, labels, reviewer changes, issue comments, or cleanup unless the user explicitly asks in a new instruction.

## Output

Always return exactly one terminal state: `created`, `updated`, `draft-only`,
`blocked`, or `refused`.

For a completed PR, respond tersely:

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

For blocked work, use `Status`, `Blocker`, `Exact Command`, `Exact Error`,
`Decision Needed`, and `Draft PR Metadata` when available. Always return either
the PR URL or the exact blocker preventing it.
