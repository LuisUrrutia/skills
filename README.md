# Agent Skills

A collection of skills for AI coding agents (Claude Code, OpenCode, and others) that enhance your development workflow.

## Skills

### agent-instructions

Write and improve instructions for agents in `AGENTS.md`, `CLAUDE.md`, skills,
referenced guides, and agent prompts. New skills do not require prior use or repetition.

**Triggers:** `update AGENTS.md`, `improve these agent instructions`, `create a skill`, `revise a skill`

**Features:**
- Edits the canonical instruction source at the intended scope
- Writes clear rules, conditional references, and completion criteria
- Preserves provenance pins and supports requested upstream reviews or updates
- Validates the changed behavior in proportion to the task

### workflow-to-skill

Extract a reusable workflow from task history or repeated work, then use
`agent-instructions` to write and validate the resulting skill. Install both when
using this extraction workflow.

**Triggers:** `turn this workflow into a skill`, `extract a skill from these sessions`

**Features:**
- Separates reusable decisions from variable inputs and incident-specific choices
- Preserves task-specific authorization boundaries
- Reuses an existing skill owner when appropriate and continues through the actual edit

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
- Always creates new PRs as drafts and refuses to report success unless draft state is verified
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

### Using npx (Recommended)

```bash
npx skills add LuisUrrutia/skills
```

### Manual Installation

Clone the repository and symlink to your agent's skills directory:

```bash
git clone https://github.com/LuisUrrutia/skills.git
cd skills

# For Claude Code
ln -s $(pwd)/commit ~/.config/claude/skills/commit
ln -s $(pwd)/pr ~/.config/claude/skills/pr
ln -s $(pwd)/github-actions ~/.config/claude/skills/github-actions

# For OpenCode
ln -s $(pwd)/commit ~/.config/opencode/skills/commit
ln -s $(pwd)/pr ~/.config/opencode/skills/pr
ln -s $(pwd)/github-actions ~/.config/opencode/skills/github-actions
```

## License

[MIT](LICENSE)
