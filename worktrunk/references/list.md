# Listing worktrees

Read this reference when the task needs more than the default `wt list` table: hidden branches, remote branches, filtering, machine-readable output, or status collection diagnosis.

## Candidate sets

```bash
wt list
wt list --branches
wt list --remotes
wt list --full
```

- `--branches` includes local branches without worktrees.
- `--remotes` includes remote-only branches.
- `--full` includes additional forge and branch status. It may require network access and authentication.

Use the default local view for routine navigation. Add wider or remote data only when the task needs it.

## Structured output

Use JSON when another command or program will consume the result:

```bash
wt list --format=json
```

Inspect the installed schema instead of assuming fields from an older version:

```bash
wt list --help
```

When scripting, select entries by explicit branch or path fields and handle absent optional fields.

## Safety checks

Before removal or cleanup, inspect the target row's branch, path, working-tree status, and integration state. A dimmed or integrated row can still contain uncommitted files; `wt remove` performs its own final safety checks.

If collection hangs or times out, identify the named worktree and run `git status --porcelain` inside it. Continue with [troubleshooting.md](troubleshooting.md) if that command also hangs.

Run `wt list --help` for columns, filters, output schemas, and flags supported by the installed version.
