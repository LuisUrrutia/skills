---
name: worktrunk
description: Use whenever a task involves Worktrunk (`wt`) or `.config/wt.toml`.
---

# Worktrunk

Use `wt` for every worktree lifecycle operation. Run it inside the repository.

## Core workflow

```bash
wt list
wt switch --create <branch>
wt switch <branch>
wt remove
```

- Use `--create` for a new branch. Without it, `wt switch` enters an existing worktree or creates one for an existing branch.
- `wt switch` opens the picker, `wt switch -` returns to the previous worktree, and `wt switch ^` enters the default branch worktree.
- Continue work in the directory reported by `wt`. When shell state does not persist between commands, set the next command's working directory explicitly.
- `wt merge` commits uncommitted changes, untracked files included, squashes and rebases the branch, fast-forwards the local target branch without fetching, then removes the worktree and branch. Run it only when the user asks for it, after confirming the worktree holds only the intended changes.
- Use `wt <command> --help` for version-specific flags. Use raw `git worktree` commands only when the user explicitly requests them. When `wt` is unavailable, report it as a blocker instead of substituting `git worktree`.

## References

Read only the reference that matches the task:

- Creating or editing `.config/wt.toml`, choosing hooks, or handling hook approvals: [references/project-config.md](references/project-config.md)
- Editing personal paths or defaults in `~/.config/worktrunk/config.toml`: [references/user-config.md](references/user-config.md)
- Using bases, shortcuts, remote branches, pull requests, or non-persistent shells with `wt switch`: [references/switch.md](references/switch.md)
- Filtering worktrees or consuming structured `wt list` output: [references/list.md](references/list.md)
- Removing worktrees or branches, including bulk cleanup and force flags: [references/remove.md](references/remove.md)
- Fixing setup, directory switching, hooks, or slow status collection: [references/troubleshooting.md](references/troubleshooting.md)
