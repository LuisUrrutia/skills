# User configuration

Read this reference only when changing personal Worktrunk preferences in `~/.config/worktrunk/config.toml`, such as worktree paths, command defaults, or personal hooks.

## Boundaries

User configuration is machine-specific and must not be committed. Read it before editing, preserve its structure and comments, and change only the requested keys. Ask before making a personal preference choice that the user has not specified.

Use this command to find the active configuration files and effective values:

```bash
wt config show
```

Create a fully commented user config only when the user wants one:

```bash
wt config create
```

## Worktree paths

`worktree-path` controls where new worktrees are placed. The default pattern creates sibling directories:

```toml
worktree-path = "{{ repo_path }}/../{{ repo }}.{{ branch | sanitize }}"
```

To place them inside the repository:

```toml
worktree-path = "{{ repo_path }}/.worktrees/{{ branch | sanitize }}"
```

For a centralized directory:

```toml
worktree-path = "~/worktrees/{{ repo }}/{{ branch | sanitize }}"
```

When worktrees live inside the repository, ensure the chosen parent directory is ignored before creating worktrees there.

## Personal hooks

User hooks use the same forms and template variables as project hooks, but they apply across repositories and run before project hooks.

Before adding one, confirm that broad scope is intended. Prefer `.config/wt.toml` when behavior belongs to one repository or should be shared with the team.

Validate changes with:

```bash
wt config show
wt hook show
```

Use `wt config --help` and https://worktrunk.dev/config/ for keys not covered here.
