---
name: pr
description: "Pull requests: create, update, or inspect a PR; draft titles, bodies, and metadata; push a branch for review"
---

# Pull request

Create or update one GitHub pull request: safe `gh` operations, and a body a reviewer can act on.

This skill owns the push, the PR, its title, body, template conventions, and initial state. Land the commits with the `commit` skill first. When the branch is stacked (`gh stack view --json` succeeds, the resolved base is another feature branch, or the user asks for a stack), `stacked-pr` owns branch order, base resolution, submit, rebase, and merge sequence.

## Modes

- **Create**: no exact PR exists for this target repository and head repository/branch. Open one in the user's preferred initial state, defaulting to draft.
- **Update**: one exact open PR exists for this target repository and head repository/branch. Audit its body against the diff, then show the URL and the proposed edits and ask before changing title, body, or metadata.
- **Draft-only**: the user wants copy, a state read, or metadata suggestions. Deliver them and stop, with no push, create, or edit.

A closed or merged PR is historical state, not Update mode. Report its URL and state, then ask whether the user wants a new PR when commits remain against the target base. Edit, reopen, or replace it only when the user explicitly chooses that operation.

Terminal states are `created`, `updated`, `draft-only`, and `blocked`. Reaching one ends the turn. Further edits, labels, reviewers, issue comments, or cleanup wait for a new instruction.

## Claims

Everything the title, body, or reported metadata asserts is a **claim**, and every claim ships verified against evidence that can establish that class of claim. A source can prove one class and be only a discovery hint for another.

| Claim class | Evidence that can establish it | Insufficient on its own |
| --- | --- | --- |
| Repository and PR state | Current `git status`, resolved refs and remote URLs, and matching fields from `gh repo view --json`, `gh pr view --json`, or `gh pr list --json`. | A remote's name, user memory, or a prior summary. |
| Motivation and problem | The current user request or user-supplied context, a linked issue, incident, specification, strategy doc, or product doc. | The branch name, commit messages, the diff alone, or the existing PR body. |
| Requirements and work-item coverage | Each explicit ask in the current user request, issue, or specification mapped to the implementation and its verification evidence. Assignee and status establish ownership and workflow state only. | A ticket title, assignment by itself, a closing keyword, or intended scope with no branch evidence. |
| Changed surfaces and implementation | Every commit, the full `<base-ref>...HEAD` diff, and the relevant current code, including generated, binary, dependency, and migration changes. | A diff stat, file list, commit summary, or existing PR body. |
| Delivered behavior and audience | The implementation traced end to end through routes, gates, flags, configuration, and failure paths, with relevant tests or manual evidence when the claim depends on runtime behavior. | A feature name, issue intent, scaffold, isolated code fragment, or test name. |
| Design decisions and tradeoffs | The implementation establishes the mechanism; a user decision, specification, ADR, design doc, or code comment establishes its rationale and rejected alternatives. | An alternative invented from the diff, or an assistant preference presented as the author's decision. |
| Validation | Exact results from commands run for the current head, or a current CI result tied to that head commit. | Planned checks, historical CI, the presence of tests, or an unverified result copied from the PR body. |
| Numbers and performance | A reproducible measurement or verified artifact that names the method, baseline, result, and code revision. | A goal, estimate, adjective, unsourced percentage, or number from a commit message. |
| Risk, impact, and out-of-scope boundaries | Facts from the diff, requirements, data flow, dependencies, compatibility, rollout, and rollback behavior. Present an inference as an assessment, not as measured fact. | Generic reassurance such as `low risk`, or absence of a known failure. |
| Review metadata and conventions | Written repository rules, the template on the resolved base, `CODEOWNERS`, current repository metadata from `gh`, and recent merged PRs for house style only. | A template introduced by the branch, guessed ownership, or one prior PR treated as a rule. |
| AI assistance and human review | The current run establishes what the agent changed and verified. Only the user's explicit confirmation establishes what a human reviewed or rewrote. | Generic disclosure text, the existing PR body, or an assumption that tool output received human review. |

When sources disagree, use the source authoritative for that claim class and name the mismatch. The issue establishes intended scope, the branch establishes implemented scope, and GitHub metadata establishes PR state; none substitutes for another. Unknown remains unknown. In a simulation, a fixture explicitly supplied as verified tool output stands in for that tool output.

Branch names, commit messages, existing PR bodies, and prior assistant or bot summaries are discovery hints for substantive claims. Use them to find evidence, then verify the claim from the matrix above.

Verify before you write it:

- **What the PR delivers.** A scaffold behind a flag is not the shipped capability. Read what the code does end to end.
- **Who it affects.** Read the actual gate (permission check, flag reader, route guard) rather than inferring an audience from the feature's name. When the audience is broad or awkward to name, phrase it role-neutrally.
- **Numbers.** Cite a measurement allowed by the matrix. With no honest figure, carry the weight in the verb (`cut`, `unblock`, `start`, `stop`); a hand-waved figure is worse than none.
- **Work items.** Check each ticket's assignee and status before writing that the PR covers it. Claim coverage for the PR's own ticket and work assigned to the author only after mapping every explicit ask to branch evidence. Treat matching work owned by someone else as possible overlap and leave closure to its owner.
- **Closing the ticket.** List the issue's explicit asks, check each against the diff, and name the ones the branch leaves unimplemented or half-done. That gap is invisible in the diff and it decides whether the ticket can close on this PR alone.
- **The existing body, in update mode.** A body written mid-branch rots as commits land: a caveat that was true at the first push ("hidden for everyone", "no endpoint exists", "not wired yet") may have been implemented three commits later while the body still swears otherwise. Name every stale claim when you present the proposed edits.

## Guardrails

### Initial state

A new PR opens as a draft by default. A user preference for ready PRs overrides that default. Accept the preference from the current request or user-specific instructions available in context; repository conventions, existing PRs, and prior assistant or bot summaries do not establish it. The preference chooses only a new PR's initial state; changing an existing PR's state still requires explicit approval.

For one PR, use the command matching the resolved state:

- Draft default: `gh pr create --repo <target-repo> --draft --base <base> --head <head-ref> --title <title> --body-file <file>`
- Ready preference: `gh pr create --repo <target-repo> --base <base> --head <head-ref> --title <title> --body-file <file>`

Use `<branch>` for `<head-ref>` when the head and target repositories are the same. For a user-owned fork, use `<head-owner>:<branch>` so `gh` never has to guess which repository supplies the head.

Inspect the command string before running it: `--draft` is present for the draft default and absent for a ready preference. Rebuild a mismatched command before execution. For a stack, pass the resolved state to `stacked-pr`, which owns the submit command.

Verify right after creation with `gh pr view <url> --json isDraft,url`. The result must match the resolved state. Correct one mismatch with `gh pr ready --undo <url>` for the draft default or `gh pr ready <url>` for a ready preference, then verify again. Still mismatched: report the URL and stop, with no metadata edits or other PR actions.

Forbidden creation paths are `--web`, `-w`, `--editor`, `-e`, `--recover`, `--draft=false`, and any interactive flow. Omit `--draft` for a ready PR.

### Stop and ask

Proceed unasked on low-risk creation work: pushing a branch that has no upstream, creating a PR in the resolved initial state on the default base, and filling title and body from commits, diff, and template.

Everything else waits for the user:

- Not a git repository, `gh` missing, or `gh` not authenticated.
- The branch is the resolved target repository's default branch, unless the user wants a PR from it.
- No commit or diff against the chosen base.
- Staged, unstaged, or untracked changes in the worktree. PRs ship committed work.
- Secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases.
- A diff too broad for one review: unrelated concerns, mixed refactor and behavior change, generated noise, large binaries, lockfiles, or anything outside the requested boundary. Recommend a split instead.
- The branch is behind its upstream or has diverged.
- The target repository, target remote, push repository, or push remote is ambiguous.
- An exact PR for this target and head is closed or merged. Show its URL and ask whether the remaining diff should become a new PR.
- The operation needs a rebase, force-push, non-default base, reviewers, labels, milestone, or assignees.

Approval is per-operation and explicit: rebase, force-push, base change, reviewers, labels, changing an existing PR's state, and close or reopen each need their own.

## Workflow

### 1. Resolve repository state

- `git status --short --branch`, `git branch --show-current`, `git remote -v`.
- `git rev-parse --abbrev-ref --symbolic-full-name @{u}` for the upstream; failure means there is none. The upstream identifies the default push destination for this branch. It never identifies the PR base.
- Map each candidate remote to its GitHub repository with `git remote get-url <remote>` and `gh repo view <url> --json nameWithOwner,isFork,parent,defaultBranchRef` rather than inferring repository identity from a name such as `origin` or `upstream`.
- Resolve the **push repository and push remote** from the current branch's upstream when it exists. Without an upstream, select a named remote only when its mapped GitHub repository is the intended head repository; ask when zero or several remotes match.
- Resolve the **target repository** in this order: a repository named by the user or encoded in a supplied PR URL, the push repository when it is not a fork, or the parent when the push repository is a fork and the user is contributing upstream. When a fork task does not distinguish its fork from its parent, ask once. A typical fork contribution has target remote `upstream`, push remote `origin`, and two different repositories.
- Resolve the **target remote** as the named remote whose GitHub repository equals the target repository. A missing or ambiguous target remote is a blocker because a fork's local `main` may not represent the target repository's `main`.
- Resolve the **head owner** from the push repository. Set `<head-ref>` to `<branch>` when the push and target repositories are the same, otherwise to `<head-owner>:<branch>`.
- Read `gh repo view <target-repo> --json defaultBranchRef` for the target's default branch. In Create mode, use a user-requested base after verifying it; otherwise use this default. In Update mode, keep the existing PR's `baseRefName`; treat a requested change as a separate, approval-gated operation. The upstream tracking branch never participates in base selection. Fetch the chosen base from `<target-remote>` and verify `<base-ref>` resolves to that target-remote branch before inspecting the boundary.
- Discover prior PRs with `gh pr list --repo <target-repo> --state all --head <branch> --json number,url,state,title,body,baseRefName,isDraft,headRefName,headRepositoryOwner`. Because `gh pr list --head` cannot qualify an owner, filter the result to both `headRefName == <branch>` and `headRepositoryOwner.login == <head-owner>`.
- Classify one exact open match as Update and no exact PR history as Create. Multiple exact open matches are ambiguous. When there is no open match but an exact closed or merged match exists, report the historical PR and ask before creating, reopening, or editing anything.
- In Create mode, resolve the new PR's initial state under [Initial state](#initial-state). In Update mode, record the existing PR's `isDraft` value and leave it unchanged unless the user explicitly approves changing it. In Draft-only mode, resolve only the repository state and metadata needed for the requested deliverable.
- Verify every PR, repository, branch, base, remote, and upstream that came from the user or earlier context with `gh pr view`, `gh repo view`, `git rev-parse --verify`, or `git ls-remote`. Unverifiable means unknown: resolve from repository state instead.

For Create and Update, done when target repository and remote, push repository and remote, branch upstream, head owner and ref, exact PR history, mode, default branch, and base and local base ref are all known. Create also requires the new PR's initial state; Update requires the existing PR's current `isDraft` value. Draft-only is done when every repository-state or metadata input needed for the requested deliverable is resolved.

### 2. Inspect the PR boundary

- `git log --oneline --decorate <base-ref>..HEAD`: read every commit, not just the last one.
- `git diff --stat <base-ref>...HEAD`, then `git diff <base-ref>...HEAD`: read the whole diff. `<base-ref>` is the fetched target-remote branch, not a same-named local branch or the head's upstream. Summaries skip binary and generated artifacts; risky files still get flagged.
- Confirm one coherent purpose and a reviewable size. When that fails, stop with a split recommendation.
- Run the [Claims](#claims) checks that read the branch: what it delivers, who it affects, the issue's asks, and in update mode the existing body.

Done when every commit and changed file is accounted for, the boundary is coherent and committed, and no claim in an existing body contradicts the diff.

### 3. Discover metadata conventions

Check all three sources before drafting a word.

**The written rules.** Read the repo's own pull-request section first: `CONTRIBUTING.md`, and the PR or workflow section of `AGENTS.md` / `CLAUDE.md`. Requirements no template carries live here — a ticket link in the description, a title format, a merge strategy, a review bar — and they outrank this skill's defaults wherever the two disagree. `grep -in "pull request" CONTRIBUTING.md AGENTS.md CLAUDE.md` finds the section when no heading names it.

**The template.** Search the resolved base and current tree in the repository root, `docs/`, `.github/`, and any `PULL_REQUEST_TEMPLATE/` directory under them for `pull_request_template.md` or `PULL_REQUEST_TEMPLATE.md`. A single template file on the base is the established shape to follow. A template added or changed by the current branch is part of the change, not evidence of repository convention. With several in a `PULL_REQUEST_TEMPLATE/` directory, pick the base template whose filename matches the change type, and ask once when that is ambiguous; a user saying `template=<filename>` has already picked.

**Recent merged PRs.** Run `gh pr list --repo <target-repo> --state merged --limit 10 --json number,title,url,body` and read at least three bodies. When fewer than three merged PRs exist, read every available body. The template gives the skeleton; merged PRs show how the target repo fills it: how deep each section runs, whether bullets are bold-led, which optional sections real authors keep, the house tone, and the title convention. With at least three, copy the dominant pattern; when patterns conflict, follow the newest PRs closest to this change type. Treat one or two bodies as supporting evidence, with the written rules and template still authoritative. When no merged PRs exist, skip this source and use the written rules, the selected template, and the fallback structure.

A lookup failure in an authenticated GitHub repo stops the run: report the exact command failure rather than inventing a style.

Done when the written rules, the selected template and whether it exists on the resolved base (or its proven absence), and the merged-PR evidence are established: at least three bodies, every available body when fewer exist, or a confirmed zero-result fallback. Every requirement the written rules impose is on a list you check before finalizing.

### 4. Write the review packet

The body is a **review packet**: what changed, why it matters, and where the risk sits, in the fewest lines a reviewer can act on. The reviewer already has the diff.

Read [references/review-packet.md](references/review-packet.md) completely before drafting a title or body. Apply the repository conventions from step 3 and verify every substantive statement under [Claims](#claims). Run the final copy through the `humanize` skill.

Done when the requested title and/or body satisfy the written rules and selected template, every claim is verified, and the `humanize` reader and fidelity passes leave copy that a reviewer can understand on the first read. When a body is requested, every affected surface is named once at review altitude, and the problem, shipped scope, validation, and real risk are clear without opening the diff.

### 5. Decide or ask once

- No PR yet and only low-risk work needed: proceed. Push the branch if it needs it, then create the PR in the resolved initial state.
- A PR already exists: show its URL, the stale claims found in step 2, and the proposed title and body, then ask before editing.
- A closed or merged exact match exists: show its URL and state, whether commits remain against the target base, and the proposed metadata for a new PR when applicable; ask what to do next.
- A risky decision is needed: present mode, target repository and remote, push repository and remote, head ref, branch, base, initial state, push or rebase needs, reviewers, labels, and the exact title and body.
- Ambiguous input: ask one concise question with concrete options, recommended default first.

Put every risky decision in that single turn, and hold execution until each one is answered.

Any branch that asks the user for approval or disambiguation ends the current turn as `blocked`, with the known PR URL and `Decision Needed`. Resume the workflow from that decision on the next turn.

### 6. Execute approved actions

- Push with `git push -u <push-remote> HEAD:<branch>` when the branch has no upstream and the resolved push is low-risk. An existing upstream keeps its verified remote and branch.
- Write the body to a temporary file and pass `--body-file`. Inline `--body` mangles backticks, lists, code fences, and shell syntax.
- Grep the final title and body file for `—`, `–`, curly quotes (`“ ” ‘ ’`), and a sentence opening on `This PR` or `This change`, and fix every hit. Drafting slips past these, and one command catches them.
- Create with the sanctioned command from [Initial state](#initial-state), then verify `isDraft` matches the resolved state.
- Update with `gh pr edit <url> --title <title> --body-file <file>` plus only the approved metadata flags. Use the exact URL found in step 1 so a same-named branch from another fork cannot be edited.
- On a failed command, report the exact command, the concise failure, and the next decision. Retrying with broader permissions or destructive git actions is off the table.
- Once the create or update is verified and reported, stop.

## Output

Return exactly one terminal state. For a completed PR:

```markdown
Status: created|updated
PR: <url>
Target repo: <owner/repo>
Target remote: <remote>
Push remote: <remote> (<owner/repo>)
Head: <branch-or-owner:branch>
Branch: <branch>
Base: <base>
Draft: yes|no
Metadata: reviewers/labels/milestone/assignees changed, or none
Validation: commands run and their results, or not run with reason
Risk check: no unrelated or secret-looking changes found, or the flagged items
```

For a draft-only result:

```markdown
Status: draft-only
PR: <url or not created>
Mutation: none
Validation: evidence used, or not run with reason
```

Follow the block with only the requested state, title and body copy, or metadata suggestions. Preserve repository template headings in proposed body copy.

For blocked work:

```markdown
Status: blocked
Blocker: <exact reason>
Decision Needed: <user decision or external change required>
```

Include `PR` when its URL is known, `Exact Command` and `Exact Error` when a command failed, and `Proposed PR Metadata` when it exists. Every run ends with the completed PR URL, the requested draft-only deliverable, or the exact blocker.
