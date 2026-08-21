---
name: walkthrough
description: Explain current branch changes from a user perspective
---

## Context

Repository: !`git remote get-url origin 2>/dev/null | sed -E 's#(git@github.com:|https://github.com/)([^.]+)(\.git)?#https://github.com/\2#' || echo "No repository"`
Branch: !`git branch --show-current 2>/dev/null || echo "No branch"`

## Execution steps

1. Treat `$ARGUMENTS` as optional audience, base branch, or focus area. Examples: `for product`, `against main`, `focus auth flow`.
2. Confirm the current directory is inside a git repository. If not, stop and report that this command needs a git repo.
3. Determine the comparison base from `$ARGUMENTS`, the upstream branch, the default branch from `gh repo view`, then `main` or `master`.
4. Inspect commits and diffs with read-only git commands only. Do not edit files, checkout branches, stash, rebase, merge, or write output files unless explicitly asked.
5. Read the files needed to understand behavior, especially entry points, tests, docs, and user-facing flows touched by the diff.
6. Explain the changes as a walkthrough from the user's perspective. Organize by flows, states, and risks, not by file inventory.
7. Call out what appears unchanged when that helps the user trust the diff.
8. Include risks, edge cases, and suggested validation steps. Keep recommendations practical and scoped to the current branch.
9. Include safety notes for missing `gh` auth, missing upstream or base branch, no git repo, and empty diffs.

## Output format

# Branch Walkthrough

- Branch: [current branch]
- Base: [base branch]
- Audience: [resolved audience]

## What Users Experience

[Short narrative summary]

## Flows Changed

- [Flow name]: [what changed, expected behavior, visible impact]

## Risks And Edge Cases

- [Risk]: [why it matters and how to check it]

## Suggested Validation

- [Manual or automated checks a reviewer should run]

## Notes

[Missing auth, missing base, no repo, empty diff, or assumptions]
