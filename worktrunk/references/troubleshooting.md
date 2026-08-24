# Troubleshooting

Read this reference when `wt` cannot change directories, ignores configuration, blocks on approval, fails to run a hook, or stalls while collecting worktree status.

## Start with evidence

```bash
wt --version
wt config show
wt list
```

Then run the failing command with `-v`. Use `-vv` only when normal diagnostics are insufficient because it writes raw subprocess output under `.git/wt/logs/`.

## Directory does not change

Subprocesses cannot change a parent shell. Worktrunk installs a shell wrapper to propagate the destination.

1. Run `type wt`. In bash or zsh it should report a function, not only a binary path.
2. Run `wt config show` and inspect shell integration status.
3. Install or refresh integration:

   ```bash
   wt config shell install
   ```

4. Restart or reload the shell.
5. Invoke `wt` by its bare name. Absolute binary paths and `git wt` bypass the wrapper.

In environments that start a new shell for every command, set the next command's working directory explicitly instead of trying to repair shell integration.

## Configuration not loading

`wt config show` prints the active user, project, and system config locations. Confirm that `.config/wt.toml` is under the repository root and that the command runs inside the intended worktree.

Use these parsing checks:

```bash
wt hook show
```

## Hook not running or failing

1. Confirm its name and source with `wt hook show`.
2. Inspect expansion with `wt hook show --expanded`.
3. Preview it with `wt hook <type> --dry-run`.
4. Run the underlying shell command directly in the worktree.
5. For a post-hook, inspect paths reported by `wt config state logs`.

Move long, non-blocking work from a pre-hook to the corresponding post-hook. Keep a pre-hook when later work depends on its success.

## Approval error

Project hooks require user approval. Ask the user to inspect them with `wt hook show --expanded` and run:

```bash
wt config approvals add
```

Do not replace this review with `--yes` in an interactive development environment.

## `wt list` stalls

Run `git status --porcelain` inside the worktree named by the timeout. If it also hangs, inspect repository-specific Git integrations such as `core.fsmonitor` before changing Worktrunk settings. Do not terminate processes or remove sockets until the affected worktree and data-loss risk are identified.

For behavior not covered here, use the installed command's `--help` and current documentation at https://worktrunk.dev.
