# Switching and creating worktrees

Read this reference when `wt switch` needs a non-default base, a shortcut, a remote branch, a pull-request reference, or explicit handling for a shell that cannot retain directory changes.

## Branch behavior

```bash
wt switch feature
```

If `feature` already has a worktree, Worktrunk enters it. If the branch exists without a worktree, Worktrunk creates one. If only a remote tracking branch exists, Worktrunk creates its local tracking branch.

Create a new branch and worktree with:

```bash
wt switch --create feature
```

New branches use the default branch as their base. Choose another base explicitly:

```bash
wt switch --create hotfix --base production
wt switch --create follow-up --base=@
```

`@` is the current branch, `^` is the default branch, and `-` is the previous worktree. These shortcuts also work with `--base`.

## Picker and wider branch sets

`wt switch` without a branch opens the picker. Expand its candidates when needed:

```bash
wt switch --branches
wt switch --remotes
wt switch --prs
```

Pull-request and merge-request references can be addressed directly:

```bash
wt switch pr:123
wt switch mr:123
```

These remote operations require the appropriate forge CLI to be installed and authenticated.

## Shell behavior

An interactive shell needs Worktrunk's shell integration to change its own directory:

```bash
wt config shell install
```

Restart or reload the shell after installation. Use the bare `wt` command so the wrapper can intercept it; an absolute binary path and `git wt` bypass the wrapper.

In an execution environment where each command starts a fresh shell, do not rely on `cd` propagation. Read the destination from `wt list`, then set the next command's working directory explicitly. `wt switch --no-cd` is appropriate when navigation is managed by the caller.

## Lifecycle effects

Creating a worktree runs `pre-switch`, creates the worktree, runs blocking `pre-start`, then starts `post-start` and `post-switch` in the background. Switching to an existing worktree runs the switch hooks but not the start hooks.

Use `--no-hooks` only when skipping project hooks is intentional and authorized by the task.

## Failure guide

- Missing branch: use `--create` only if a new branch is intended, or inspect `wt list --branches`.
- Occupied target path: locate the existing worktree before changing anything.
- Stale non-worktree directory: inspect it before considering `--clobber`; that flag can remove the target path.
- No directory change: follow [troubleshooting.md](troubleshooting.md).

Run `wt switch --help` for the installed version's complete flags.
