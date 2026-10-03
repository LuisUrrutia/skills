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
- Chooses between reusing, wrapping, deriving, or creating a skill before adding an implementation
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
- Separates missed activation from missing instructions, using traceable upstream extraction criteria

### prototype

Resolve a design, state-model, or behavior question with a disposable experiment.
Use it directly or as one phase of a larger task; it does not require work-mode.

**Triggers:** `prototype these layouts`, `explore this state model`, `try a small experiment before choosing an approach`

**Features:**
- Loads separate guidance for logic demos, interface alternatives, and empirical experiments
- Returns a runnable artifact, observed evidence, tradeoffs, and a bounded recommendation
- Keeps production implementation and delivery outside the prototype's scope
- Records Matt Pocock and Lauren Tan's pstack sources at exact commits
- Delegates requested source maintenance to `agent-instructions`; ordinary use has no skill dependency

### debug

Diagnose an observed bug or performance regression, and repair it when requested.
Use it directly, without work-mode or an installed upstream skill.

**Triggers:** `diagnose this failure`, `fix this bug`, `investigate this regression`

**Features:**
- Distinguishes diagnosis-only requests from authorized repairs
- Builds an observation that reaches the reported symptom and tests causal explanations
- Uses regression tests where they exercise the failure without disproportionate setup
- Loads conditional guidance for missing reproduction, intermittent failures, performance, and cross-boundary investigation
- Preserves exact source commits and delegates requested maintenance to `agent-instructions`

### tdd

Implement features or authorized fixes through test-first increments. Use it
directly when TDD is requested, without work-mode or an installed upstream skill.

**Triggers:** `implement this with TDD`, `fix this test-first`, `use red-green-refactor`

**Features:**
- Observes a meaningful failing test before implementing each behavior
- Tests caller-visible contracts using independent expected results
- Allows focused refactoring while tests remain green
- Distinguishes setup failures and already supported behavior from a valid red state
- Preserves Matt Pocock's exact source revision and delegates requested maintenance to `agent-instructions`

### how

Explain how existing code works and which component owns each responsibility.
Use it directly for a mechanism, subsystem, or ownership question.

**Triggers:** `how does this flow work`, `explain this subsystem`, `which module owns this state`

**Features:**
- Traces entry points, data, state transitions, and boundaries from actual source
- Answers at the requested depth with a concrete flow and relevant code locations
- Distinguishes inspected behavior, observed execution, documented reasons, and unknowns
- Keeps diagnosis, branch change reports, and guided teaching with their own owners
- Derives from pstack/how with limited presentation guidance from pstack/teach
- Records exact source commits and supports requested maintenance through `agent-instructions`

### why

Reconstruct the reasons behind existing code or design decisions from historical
evidence. Use it directly, without work-mode or an installed upstream skill.

**Triggers:** `why did we choose polling`, `what motivated this guard`, `where did this threshold come from`

**Features:**
- Follows relevant history and linked discussions, including earlier paths and revisions
- Separates recorded reasons, supported inferences, and unanswered questions
- Distinguishes original motivation from later decisions and current necessity
- Preserves contradictory evidence and reports missing sources without inventing intent
- Derives from Lauren Tan's pstack/why with exact provenance and requested source maintenance

### blast-radius

Trace what a change could break elsewhere and test the assumptions that decide
whether those paths are safe. Use it directly for implemented or proposed changes.

**Triggers:** `what could this change break`, `check the blast radius of this change`, `test whether old consumers still work`

**Features:**

- Follows effects across dependency behavior, lifecycle timing, data formats, and indirect consumers
- Uses focused execution against actual code to test deciding assumptions
- Distinguishes confirmed breakage, cleared risks, and unproven conditions
- Preserves product files and respects explicit inspection-only requests
- Records pstack provenance and supports requested maintenance through `agent-instructions`

### arena

Compare independent complete attempts at one task, select a base, incorporate
useful parts, and verify the integrated result. Use it directly when alternative
solutions or independent investigations justify the extra work.

**Triggers:** `compare independent solutions`, `run an arena on this design`, `reconcile independent audits of this diff`

**Features:**

- Uses actual host delegation and available models, with isolated mutable outputs
- Judges settled candidates and checks the final artifact instead of trusting consensus
- Supports conditional specialist workers, preserving review-audit and blast-radius contracts
- Records failed candidates, missing judges, graft decisions, and verification limits
- Preserves exact pstack sources and supports requested maintenance through `agent-instructions`

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
