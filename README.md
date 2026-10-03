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
- Reuses or adds regression tests that exercise the failure without disproportionate setup
- Compares effective environments and component boundaries, and revisits stalled explanations
- Handles observation-sensitive failures with controlled schedules and explicit evidence limits
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

### analyze-change-effects

Trace what a change could break elsewhere and test the assumptions that decide
whether those paths are safe. Use it directly for implemented or proposed changes.

**Triggers:** `what could this change break`, `analyze the effects of this change`, `test whether old consumers still work`

**Features:**

- Follows effects across dependency behavior, lifecycle timing, data formats, and indirect consumers
- Uses focused execution against actual code to test deciding assumptions
- Distinguishes confirmed breakage, cleared risks, and unproven conditions
- Preserves product files and respects explicit inspection-only requests
- Records pstack provenance and supports requested maintenance through `agent-instructions`

### compare-solutions

Compare independent complete attempts at one task, select a base, incorporate
useful parts, and verify the integrated result. Use it directly when alternative
solutions or independent investigations justify the extra work.

**Triggers:** `compare independent solutions`, `compare solutions to this design`, `reconcile independent audits of this diff`

**Features:**

- Uses actual host delegation and available models, with isolated mutable outputs
- Judges settled candidates and checks the final artifact instead of trusting consensus
- Supports conditional specialist workers, preserving review-code-changes and analyze-change-effects contracts
- Records failed candidates, missing judges, graft decisions, and verification limits
- Preserves exact pstack sources and supports requested maintenance through `agent-instructions`

### design-code-structure

Design or compare data models, public interfaces, and module boundaries for a
concrete software change. Use it directly for a decision or during authorized implementation.

**Triggers:** `design this module`, `compare these interface designs`, `model the state and ownership for this change`

**Features:**

- Derives types and operations from real caller usage and established constraints
- Compares meaningful alternatives by correctness, caller effort, locality, state, and cost
- Uses how, why, analyze-change-effects, prototype, and compare-solutions when the decision needs them
- Handles shared invariants, retries, cancellation, external contracts, and migration when relevant
- Revisits a design when repeated implementation friction exposes a wrong assumption
- Records pstack and Matt Pocock sources with conditional upstream maintenance

### simplify-code

Simplify changed code through focused edits that preserve behavior. Use it
directly for cleanup or as a bounded step in an implementation task. Its criteria
adapt to the project's language and runtime without language-specific examples.

**Triggers:** `simplify this change`, `clean up this diff`, `remove unnecessary complexity`

**Features:**

- Resolves the actual change scope and base, preserving unrelated work and staging
- Removes redundant comments, type escapes, nesting, and indirection when evidence supports it
- Preserves necessary guards, error handling, resource lifetime, contracts, and explanations
- Retains useful abstractions and checks material cost changes on sensitive paths
- Respects review-only requests and separates cleanup from behavior-changing bug fixes
- Uses why and verify conditionally, with pinned Cursor, pstack, and Addy Osmani provenance

### review-code-changes

Review a PR, branch, commit, or local changes for defects, unmet requirements,
and code-quality regressions. This is the repository's successor to the installed
review-audit skill; it preserves a read-only review phase and local reports.

**Triggers:** `review this diff`, `review this branch`, `check this change against the spec`

**Features:**

- Pins the actual comparison and accounts for every declared changed path
- Traces causal evidence, requirements, standards, structure, security, and verification
- Distinguishes required changes, optional improvements, and unresolved questions
- Uses relevant specialists within the review's scope and permissions
- Delegates independent risk areas automatically when useful, with one coordinator validating evidence and complete coverage
- Validates Markdown coverage against a path inventory and renders HTML with an external stylesheet
- Records local snapshots and pinned review sources, including Compound Engineering, OpenClaw, and Alireza Rezvani

### verification-authoring

Create and maintain project-local `verify-<app>` skills that another agent can
execute from a cold start. Install `agent-instructions` alongside this authoring skill.

**Triggers:** `create a verification skill for this app`, `maintain verify-memo`, `update the verification recipe`

**Features:**

- Discovers real launch commands, driving tools, observation points, and isolation
- Preserves pstack's Launch, Doctor, Drive, Evidence, Cleanup, and Helpers contract
- Creates a feature map and proves one feature; maintenance reviews and drives every feature
- Distinguishes recipe drift from product defects and preserves evidence after cleanup
- Includes a read-only map checker and pinned pstack sources with requested upstream maintenance

### verify

Verify a change or completion claim using current execution evidence. Select the
project's local `verify-<app>` recipe for application behavior.

**Triggers:** `verify this change`, `check this bug is fixed`, `verify before calling this complete`

**Features:**

- Matches requirements and affected entry points to the checks that can prove them
- Runs project checks and the relevant local application recipe within the active scope
- Checks real user paths, side effects, build identity, and retained evidence
- Separates failures, blocked checks, and partial success; a verification-only request does not authorize repair
- Adds conditional browser evidence guidance and records pstack, Superpowers, GSD, and Addy Osmani sources

### commit

Create atomic Conventional Commits that a human can understand and review.

**Triggers:** `commit`, `/commit`, `make a commit`

**Features:**

- Keeps one coherent behavior with its regression tests and required generated output
- Preserves unrelated staged and unstaged work, including partial-file boundaries
- Grounds the message in the verified index and supplied motivation
- Verifies the actual commit, parent, message and residual work after hooks run
- Publishes only within existing authorization and hands PR presentation to `pr`

### pr

Create or update a GitHub PR with a concise explanation and useful review evidence.

**Triggers:** `create a PR`, `update the PR description`, `draft a PR body`

**Features:**

- Resolves the exact target, fork, head and actual base
- Checks claims against implementation, requirements and current verification
- Follows repository conventions while allowing useful additions where the format permits
- Uses diagrams, genuine screenshots and measured comparisons when they aid review
- Preserves draft preference, verifies the GitHub actor and publishes over SSH
- Refreshes the whole description after material publication under existing authorization

### pr-followup

Evaluate feedback on an existing PR and resolve authorized code, CI and base problems.

**Triggers:** `resolve this PR's feedback`, `check PR readiness`, `babysit this PR`

**Features:**

- Separates read-only checks, feedback repairs and bounded active observation
- Collects threads, reviews, conversation, check annotations and reviewer logs
- Reevaluates edited comments and new replies in resolved or outdated threads
- Tests claims against current code and keeps independent repairs progressing
- Uses `commit` and `pr` for their phases; requires those local owners when those phases are reached
- Distinguishes fixed, verified, published, replied and resolved states
- Rechecks new heads and reports pending checks or decisions without automatic merge or scheduling

All three record pinned sources and local decisions in `origin.txt`, with requested
source maintenance through `agent-instructions`. Repository files are distinct from
installed copies.

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
