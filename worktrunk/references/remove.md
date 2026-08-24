# Removing worktrees and branches

Read this reference before removing a non-current worktree, retaining or deleting its branch, or using `--force`, `-D`, `--reap`, or bulk cleanup.

## Safe removal

```bash
wt remove
wt remove feature
wt remove --no-delete-branch feature
```

With no argument, `wt remove` targets the current worktree. By default, Worktrunk deletes the branch only when its changes are already integrated. Use `--no-delete-branch` when the branch must remain.

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

## Completion

After removal, run `wt list` and verify that only the intended worktree disappeared. If the branch was meant to remain, verify it with `git branch --list <branch>`.
