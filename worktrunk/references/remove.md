# Removing worktrees and branches

Read this reference before removing a non-current worktree, retaining or deleting its branch, or using `--force`, `-D`, `--reap`, or bulk cleanup.

## Safe removal

```bash
wt remove
wt remove feature
wt remove --no-delete-branch feature
```

With no argument, `wt remove` targets the current worktree. By default, Worktrunk deletes the branch only when its changes are already integrated. Use `--no-delete-branch` when the branch must remain. Removal continues in the background after the command returns unless `--foreground` is passed; add `--format=json` for a result to verify under [Completion](#completion).

Before removal, inspect the exact target:

```bash
wt list
git -C /path/to/worktree status --short
```

Resolve the path from `wt list`; do not guess it.

## Force flags

The force flags protect different data:

| Flag | Overrides |
| --- | --- |
| `--force` / `-f` | Dirty-worktree protection; uncommitted files can be lost |
| `--force-delete` / `-D` | Unintegrated-branch protection; commits can become unreachable |

Use either flag only when the user explicitly authorized the corresponding data loss and the exact target was verified immediately beforehand.

```bash
wt remove --force feature
wt remove -D feature
wt remove --force -D feature
```

`--reap` terminates non-interactive processes whose working directory is under the worktree. Use it only when stopping those processes is part of the request.

## Bulk cleanup

`wt step prune` removes every worktree and branch integrated into the default branch, using the same criteria as `wt remove`. It skips the main worktree, locked or dirty worktrees, candidates younger than `--min-age` (one day by default), and candidates whose hooks include an unapproved project command; read the approval state first as described in [project-config.md](project-config.md#approval-boundary). Use it only when the request covers all integrated candidates, and preview them first:

```bash
wt step prune --dry-run
```

For a subset, remove each verified target with `wt remove`. Lower `--min-age` only when the user wants recent candidates included.

## Completion

Check each `branch_outcome` that `wt remove` or `wt step prune` reported with `--foreground --format=json`: `deleted` means the branch is gone, a `retained_*` value names why Worktrunk kept it, and `not_attempted` is expected with `--no-delete-branch`. `deferred` means the run lacked `--foreground`: removal is still running in the background, so `wt list` can still show the target; check again after it finishes.

Then run `wt list` and verify that only the intended worktrees disappeared. If the branch was meant to remain, verify it with `git branch --list <branch>`.
