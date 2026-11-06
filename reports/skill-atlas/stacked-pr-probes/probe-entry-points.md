# Dry-run probe: stack entry points (2026-11-06)

Rendered once per arm: `__ROOT__` is the arm's skills root, and each `__*_DESC__` is the description from that arm's SKILL.md. The baseline arm held pr, pr-followup, stacked-pr and worktrunk at f2150614bb1fe44b37349f4134341973927ebcd8; the candidate arm held this change. Both arms held a copy of the aurora-payments/monorepo `stack-worktree` skill (sha256 c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2). Cases G and H were added after the first round; the baseline ran them from a prompt holding only the setup and those two cases.

```text
You are a coding agent following skills. This is a read-only dry run: read only the files named below and the files those skills tell you to load from the same folder, plus `shasum -a 256` on the files you read. Run no other command, edit nothing, and call no GitHub or network tool. Other skills named in these files (commit, review-code-changes, issue-workflow, comment-style, and so on) exist; describe invoking them without reading them.

Skills root: __ROOT__
Available skills (name: description). Load a skill by reading `<root>/<name>/SKILL.md`, then its references only as it directs.
- stack-worktree (project skill of the current repository): __SW_DESC__
- stacked-pr: __SP_DESC__
- pr: __PR_DESC__
- pr-followup: __PF_DESC__
- worktrunk: __WT_DESC__
- github-actions: Harden GitHub Actions and Dependabot: create or modify workflow YAML, reusable workflows, or .github/dependabot.yml; audit security, correctness, reliability, cost, or performance.
- commit: Git commits: use for preparation, creation, message guidance, or requested pushes.

Common setup (treat as verified command output): repository `acme/web` (GitHub org repo), remote `origin` = `git@github.com:acme/web.git`, default branch `main`, single remote, Git 2.50. You work in a WorkTrunk-managed linked worktree. `gh extension list` prints `gh stack  github/gh-stack  v0.3.0`, the newest release, published 2026-10-26; today is 2026-11-06. The authenticated actor is verified. Stacked PRs are enabled for the repository. Answer each case independently, as if it were its own session.

A. Branch `ci/carry-approval` has one commit on `origin/main`, not pushed, no PR. The user writes (Spanish): "eso me gusta, pero implementaría eso entonces como un stacked PR, donde en otro hagamos esto" — meaning: the existing CI change as PR 1 on `main`, and a new change (`storybook/anchored-clock`, not yet written) as PR 2 on top of it. Which skills do you load, in what order, and why? After reading them, give the exact commands that create each PR and how follow-up runs.

B. A caller that loaded `stack-worktree` earlier now invokes `pr` with: "Create mode. Branch ci/carry-approval (1 commit 0e5c9c4 on top of origin/main 2105bea), base main. Bottom of a 2-layer stack; layer 2 will be stacked on it." No PR exists. What does `pr` do, up to and including any PR-creating command or handoff?

C. `worktrunk` is invoked with: "Create a stacked worktree for new branch storybook/anchored-clock based on ci/carry-approval (PR #2488, already pushed, ordinary PR on main), then open its PR." What do you run for the worktree, and how is the PR for storybook/anchored-clock created?

D. Earlier in the session the user asked for a stacked PR; PRs #2488 (base main) and #2493 (base ci/carry-approval) were opened with plain `gh pr create` and form no native GitHub stack. `pr-followup` is now invoked directly: "Drive mode for a 2-PR stack, both drafts: #2488 bottom, #2493 top." No `stacked-pr` operation is running. What do you do first, and what must be true before the Drive passes continue?

E. The user says: "Create a PR for my branch fix/null-total." Base `main`, one commit, no PR, no other PR depends on it, the user never mentions stacks. A validated review report covers the exact range with no findings. Give the PR-creating command.

F. `stacked-pr`, on its manual route because the user explicitly asked for ordinary dependent PRs instead of a native stack, invokes `pr` in Create mode for branch `stack/02-api`, base `stack/01-schema` (open PR #40), already pushed; a validated review report covers the exact range with no findings. Give the PR-creating command and what `pr` returns.

G. A T3 Code watch wake resumes `pr-followup` Drive for draft PR #2501 (head `api/routes`, base `main`). Retained task state records that `stacked-pr` submitted it as the bottom layer of a planned stack and reported its native membership as pending until the second layer exists; `stacked-pr` owns the stack. The wake reports one new review comment. What do you do on this wake, in order?

H. The user says: "Create a PR for my branch hotfix/rounding against release/1.2." Open PR #50, authored by `release-manager` (a different user), has head `release/1.2` and base `main`. No PR exists for `hotfix/rounding`, one commit, and a validated review report covers the exact range with no findings. The user never mentions stacks. Give the PR-creating command or handoff.

For each case report: skills loaded (in order), the command that creates each PR (or the handoff instead), any `gh stack` commands, and what is reported or asked. Finally list each file you read with its sha256.
```

## Round 3

Run after the review gate's findings on efef7c4: the base-PR lookup in pr gained head-repository matching, and pr eval 30, the new pr eval 33 and worktrunk eval 2 had no recorded run. Only the candidate arm ran, with the same setup paragraph, the actor named `dev`, and these cases; F and H repeat as nearby regressions. The closing request also asks for `wt` commands.

```text
I. The user says: "Create a PR for my branch feature/api-routes against feature/data-model." `gh pr list --repo acme/web --state open --head feature/data-model` returns PR #12, authored by `dev` (you), head `feature/data-model` in `acme/web`, base `main`. No PR exists for `feature/api-routes`, one commit, all work committed. The user never mentions stacks. What does `pr` do, up to and including any PR-creating command or handoff?

J. The user says: "Create a PR for my branch hotfix/rounding against release/1.2." `gh pr list --repo acme/web --state open --head release/1.2` returns one PR, #61, authored by `dev` (you), whose head is `release/1.2` in the fork `dev/web` and whose base is `main`. The target `acme/web` has its own `release/1.2` branch. No PR exists for `hotfix/rounding`, one commit, and a validated review report covers the exact range with no findings. The user never mentions stacks. Give the PR-creating command or handoff.

K. The user says: "Create a worktree for a new branch docs/typo off main so I can fix a typo." No PR is requested and nothing depends on another branch. Which skills do you load, and what exact command do you run?
```

Case L ran afterwards from its own prompt: the same setup paragraph, this case, and a closing request for the skills loaded, any `gh stack` command or `stacked-pr` invocation, what is done first and the files read.

```text
L. A user invokes `pr-followup` directly: "Drive draft PR https://github.com/acme/web/pull/77 until approval." Its head is `fix/null-total` and its base is `main`. No other open PR builds on it, its base heads no other PR, and the user never mentioned stacks. CI has one failing lint job. No retained task state exists for it. What do you do first, in order, and which skills do you load?
```
