# Claude Code Skills

A collection of skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that enhance your development workflow.

## Skills

### commit

Create git commits with conventional commit messages.

**Triggers:** `commit`, `/commit`, `make a commit`

**Features:**
- Analyzes staged changes and generates conventional commit messages
- Follows `type(scope): message` format (feat, fix, docs, style, refactor, test, chore)
- Matches your repository's existing commit style
- Handles staging, branch protection warnings, and push in one flow

### pr

Create or update GitHub pull requests.

**Triggers:** `pr`, `/pr`, `create pr`, `open pr`, `pull request`

**Features:**
- Analyzes all commits since branching from main
- Generates PR title and description
- Respects `.github/PULL_REQUEST_TEMPLATE.md` if present
- Handles push, draft PRs, reviewers, and labels
- Requires `gh` CLI

### github-actions

Guidelines for writing secure and maintainable GitHub Actions workflows.

**Triggers:** `workflow`, `github actions`, `CI/CD`, `actions yaml`

**Features:**
- Security best practices (pinned actions, least-privilege permissions)
- Performance patterns (caching, parallel execution, fail-fast)
- Shell scripting guidelines
- Reference docs for API calls, matrix builds, and reusable workflows
- Integrates with `actionlint` for validation

## Installation

Copy the skill folders to your Claude Code skills directory:

```bash
# macOS/Linux
cp -r commit pr github-actions ~/.config/claude/skills/

# Or clone and symlink
git clone https://github.com/LuisUrrutia/skills.git
ln -s $(pwd)/skills/commit ~/.config/claude/skills/commit
ln -s $(pwd)/skills/pr ~/.config/claude/skills/pr
ln -s $(pwd)/skills/github-actions ~/.config/claude/skills/github-actions
```

## License

[MIT](LICENSE)
