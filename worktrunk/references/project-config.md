# Project configuration

Read this reference before creating or editing `.config/wt.toml`, adding a project hook, or responding to a Worktrunk approval error.

## Scope

`.config/wt.toml` belongs to the repository and is normally committed. It can define lifecycle hooks, a per-worktree URL, and other team-wide behavior. Treat every command in it as repository-supplied shell code.

Keep personal path preferences in `~/.config/worktrunk/config.toml`; see [user-config.md](user-config.md).

## Create or update the file

1. Read the existing `.config/wt.toml` if present. Preserve unrelated settings and comments.
2. Inspect the repository for authoritative commands: package-manager scripts, lockfiles, build manifests, CI workflows, and project instructions.
3. Create a minimal `.config/wt.toml` containing only the requested behavior. For a fully commented starter instead, run:

   ```bash
   wt config create --project
   ```

4. Run each underlying command directly in the repository before wiring it into a hook.
5. Confirm Worktrunk parses the result:

   ```bash
   wt hook show
   wt hook show --expanded
   ```

6. Preview each changed hook with `wt hook <type> --dry-run`. Run the full lifecycle command only when its effects are safe and in scope.

The change is complete when the TOML parses, every configured command appears under the intended hook, template expansion is correct, and each blocking command succeeds directly.

## Choose the hook

Pre-hooks block the operation and abort on failure. Post-hooks run in the background.

| Hook | Use it for |
| --- | --- |
| `pre-switch` | Setup that must finish before resolving or entering the destination |
| `post-switch` | Terminal or editor updates after every switch |
| `pre-start` | Dependencies or generated files required before a new worktree is usable |
| `post-start` | Dev servers, watchers, long builds, and cache copying |
| `pre-commit` | Formatting, linting, and type checks |
| `post-commit` | Notifications or background checks |
| `pre-remove` | Saving artifacts or state before deletion |
| `post-remove` | Stopping services or deleting external resources |

Prefer `post-start` for work that may continue in the background. Use `pre-start` only when subsequent work depends on its result.

## Hook forms

A string defines one command:

```toml
pre-start = "pnpm install --frozen-lockfile"
```

A table runs independent commands concurrently:

```toml
[post-start]
dev = "pnpm dev"
storybook = "pnpm storybook"
```

An array of tables defines ordered stages. Keys within one stage still run concurrently:

```toml
[[pre-start]]
dependencies = "pnpm install --frozen-lockfile"

[[pre-start]]
database = "pnpm db:migrate"
assets = "pnpm build:assets"
```

Use a pipeline only when a later stage depends on an earlier one.

## Template variables

Common variables include:

| Variable | Meaning |
| --- | --- |
| `{{ branch }}` | Active branch |
| `{{ worktree_path }}` | Active worktree path |
| `{{ repo_path }}` | Repository root |
| `{{ default_branch }}` | Default branch |
| `{{ base }}` | Source/base during switching |
| `{{ target }}` | Destination during removal |

Useful filters include `sanitize`, `sanitize_db`, `sanitize_hash`, and `hash_port`.

Example of a distinct development port per worktree:

```toml
[post-start]
dev = "pnpm dev --port {{ branch | hash_port }}"

[list]
url = "http://localhost:{{ branch | hash_port }}"
```

Use `wt -v <command>` or `wt hook show --expanded` to inspect resolved variables. Consult `wt hook --help` and https://worktrunk.dev/hook/ before using less common variables or filters.

## Approval boundary

Worktrunk asks the user to approve project commands on first execution and whenever a command template changes. Approvals live outside the repository in `~/.config/worktrunk/approvals.toml`.

In an interactive user session, ask the user to review and approve with:

```bash
wt config approvals add
```

An automated coding session must stop at this trust decision. Do not bypass it with `--yes` or record blanket approvals. Those modes are for controlled CI jobs and containers whose project commands are already trusted.

## Reference

- Project config generator: `wt config create --project`
- Parsed hooks: `wt hook show [type] [--expanded]`
- Safe preview: `wt hook <type> --dry-run`
- Current documentation: https://worktrunk.dev/hook/
