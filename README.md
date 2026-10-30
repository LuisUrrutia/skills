# Agent Skills

A collection of skills for AI coding agents (Claude Code, OpenCode, and others) that enhance your development workflow.

## Skills

The code investigators have clearer names: `how` is now `explain-code`, and
`why` is now `explain-decisions`. Update explicit invocations and installed copies
to these names; the old names are not alias packages in this repository.

`learning-plan` is retired: `teach` now covers study plans, courses and continued
study. Update explicit invocations and remove installed copies of
`learning-plan`; the old name is not an alias package.

### teach

Teach any subject at the learner's level, from one lesson in the conversation to
study that continues across sessions in a learning workspace.

**Triggers:** `teach me Go channels`, `make me a study plan for SQL`, `next lesson`, `practice this interview topic`

A concrete question gets a direct lesson in the conversation. Continued study gets
a workspace under `~/learning/<topic>/` with the learner's mission, a roadmap of
ordered objectives and checkpoints, checked resources, evidence-based learning
records and short HTML lessons. Workspace files follow the learner's language.
Explicit requests about files, questions or practice win, and shared
installations do not share learner records. Built on Matt Pocock's `teach`.

### wayfinder

Turn an ambiguous initiative into an evidence-backed direction before execution
planning, preserving connected decisions and context across sessions.

**Triggers:** `work out the direction for this initiative`, `resume our decision map`, `resolve what prevents planning this migration`

Grounds the problem, compares real options, and investigates the uncertainty that
could change the direction. A compact decision map keeps reasons, evidence,
authority, dependencies, and the next useful step across sessions. Changed
premises reopen affected decisions. Once the direction is clear, continue the
authorized workflow with `planning`.

### planning

Turn a defined outcome into an implementation plan that another engineer or agent
can execute and verify. Create, review or revise plans according to the
requested scope.

**Triggers:** `plan this implementation`, `review this migration plan`, `revise the implementation approach`

Grounds the work in current code and settled decisions, then defines observable
results, genuine dependencies, interface agreements, and acceptance checks. Small
changes get short plans; larger work passes its approach and constraints to
`task-breakdown` for PR-sized delivery units. A durable plan preserves enough context
for another session. Planning-only work ends with its artifact; already-authorized
implementation continues without a new approval gate.

Uses Wayfinder when connected direction decisions remain unresolved. Selected
ideas from Matthew Blode, Matt Pocock, Sentimony, and Superpowers are recorded in
`planning/origin.toml`; reviewed alternatives are in the atlas source review.

### task-breakdown

Divide a feature or implementation plan into small, testable units for human review,
normally one task and one PR per unit. Keep an already-small change together.

**Triggers:** `break this plan into PR-sized tasks`, `split this feature for review`, `revise an oversized delivery unit`

Prefer complete behaviors across the necessary layers, such as one statistics card
with its real data and tests. Use backend, frontend and integration stages when a
concrete dependency warrants them, with honest intermediate verification limits.
Size each PR for coherent human review. Numeric examples are guidance; an explicit
user or project cap is enforced against the full additions-plus-deletions diff,
including tests and generated text. The breakdown carries acceptance checks,
dependencies, context and the applicable review budget to each executor.
`issue-workflow` publishes the tasks only when requested.

The flow is `wayfinder` → `planning` → `task-breakdown` → authorized ticket publication
and implementation. `stacked-pr` handles branch dependencies when a stack is useful.

### work-mode

Coordinate one development task from its current state through the remaining
authorized work. Reuse completed work and choose the next phase from the actual
gap: a defect, unresolved direction, missing approach, or ready implementation.

**Triggers:** `carry this task through to completion`, `resume this implementation`, `coordinate this feature through delivery`

Uses the existing planning, implementation, verification, review, and delivery
owners. Small settled changes keep a direct route. Specialist-only requests keep
their own endpoint, and PR publication follows the task's actual authority.
Ticket implementation triggers its configured workflow even without a PR;
follow-up retains one owner and the host's resumable watch. The package records
selected pstack and Compound Engineering sources in `work-mode/origin.toml`.

This is a repository package, not a global installation or a background runtime.

### agent-instructions

Write and improve instructions for agents in `AGENTS.md`, `CLAUDE.md`, skills,
referenced guides, and agent prompts. New skills do not require prior use or repetition. Typo fixes that leave the guidance unchanged do not use it.

**Triggers:** `update AGENTS.md`, `improve these agent instructions`, `create a skill`, `revise a skill`

**Features:**
- Requests one round of Codex Sol and Claude Opus reviews at xhigh per change for instruction work the user explicitly requests, then reconciles them; if one reaches a rate or usage limit, continues with the other without retrying the limited profile or blocking progress. Instruction work or self-review the agent starts on its own, and any handoff document, skips them
- Edits the canonical instruction source at the intended scope
- Writes on Matt Pocock's writing-for-agents levers: context pointers, the two loads, information hierarchy, completion criteria, guarded leading words, and pruning
- Chooses between reusing, wrapping, deriving, or creating a skill before adding an implementation
- Hands each skill decision to `skill-maintenance` for the skill's `origin.toml` record in a repository that keeps records
- Prunes the entrypoint and references together: removes repetition, keeps each rule in one home, and compares file and package word counts without treating relocation as a reduction
- Reviews every skill change for justified growth, evaluation evidence, record hand-overs, and stale callers or README entries that name the skill
- Validates the changed behavior in proportion to the task; behavioral trials stage only runtime files and run on Claude Code and Codex. After an edit, only the cases it can affect rerun, and other results carry over with a diff-based reason that reviews check. Reports name the revision each result ran on and every unrun case
- Keeps the round's two reviews independent until both results are in, cites the reviewed candidate by commit and tree (or by file hashes when nothing is committed), and starts no new round for edits made in response; a disagreement left after it goes to the user
- Preserves business constraints and preferences when pruning, and distinguishes file size from actual loaded context

### skill-maintenance

Record each skill's goal, decisions, and sources in its `origin.toml`, and check or
update a skill from its recorded sources or installed dependencies. Install it with
`agent-instructions`, which writes the skill text.

**Triggers:** `record why we changed this skill`, `check this skill for upstream changes`, `update this skill from its sources`

**Features:**
- Records the goal, invariants, base deviations, adopted ideas, and declines in words a model without the original conversation can follow
- Keeps a record for every skill in a repository that keeps records, including skills built without outside sources
- Credits each reason to its actual source and cites evidence that survives a rebase or squash merge
- Asks before changing a skill's approach when its base no longer fits
- Lists the skills whose records depend on a skill, so a contract change can reach its callers
- Checks a skill against its sources without changing it, or incorporates compatible changes and records the review
- Advances a source's review cursor only after its full range is resolved and validated
- Includes a checker for the record format, its locations, field length, commits cited from unmerged branches, and review ranges checked against a source clone

### create-project-instructions

Investigate a project's implementation and available knowledge sources, then use
`agent-instructions` to create or update its `AGENTS.md` or `CLAUDE.md`. Install
both skills for this workflow.

**Triggers:** `create project instructions`, `research this project and write AGENTS.md`, `update CLAUDE.md from our project decisions`

**Features:**
- Uses repository evidence and relevant available docs, tickets, PRs, and discussions
- Distinguishes current behavior, approved business decisions, proposals, and unknowns
- Preserves canonical instruction owners, host adapters, and scoped exceptions
- Checks real commands and keeps private context appropriate for the destination
- Reports source coverage, unresolved conflicts, and checks actually performed

### retro

Review a coding session to identify friction and propose concrete improvements to
the agent's working environment. Each finding includes evidence, a responsible
owner and a way to check the proposed improvement.

**Triggers:** `review this session`, `what slowed us down`, `suggest improvements from this session`

**Features:**

- Inspects navigation, check wiring, instruction activation and tool use when the session warrants it
- Distinguishes missing instructions from instructions the agent never loaded
- Routes code, checks, documentation and instruction changes to their existing owners
- Returns proposals by default and continues improvements already authorized by the caller
- Accepts no useful finding and reports evidence gaps without inventing causes
- Records pinned Matt Pocock and pstack sources

### workflow-to-skill

Turn completed work, or what the user corrected in a session, into a new skill or
a change to an existing one, then use `agent-instructions` to write and validate
it. Install both when using this extraction workflow, plus `skill-maintenance` to
record the skill's decisions in a repository that keeps records, such as this one.
`retro` is optional: it diagnoses the corrections that only restate or point at
existing guidance, or at a mistake the environment allowed; without it they are
listed in the report.

**Triggers:** `turn this workflow into a skill`, `extract a skill from these sessions`, `make my corrections from this session stick in that skill`

**Features:**
- Separates reusable decisions from variable inputs and incident-specific choices
- Preserves task-specific authorization boundaries; a directive inside session history is evidence and never a reason to open, list or run what it names
- Improves the skill the session used instead of adding another, through a change request with the user's stated reasons and what its record needs, and continues through the actual edit; a reason the user never gave is never credited to them
- Sends corrections that only restate or point at existing guidance, or at a mistake the environment allowed, to `retro` instead of adding a rule; a correction stating behavior the skill does not clearly define stays here
- Follows deciding context and routes lessons to skills, project instructions, personal preferences, or existing checks
- Gives automation owners a failing case, its rejection cause, and a valid acceptance case; extraction alone does not implement enforcement

### communicate-clearly

Write clear, natural prose for the reader, language and channel. Replaces
`humanize`, preserving its claim-by-claim fidelity, author voice and pattern catalog.

**Triggers:** applies by default to prose, including answers, explanations, drafts, rewrites and reviews

**Features:**

- Explains necessary concepts at the reader's level without turning each answer into a lesson
- Adapts clarity principles to the target language while preserving exact tokens and qualifications
- Removes generic wording and mechanical structures without inferring authorship
- Keeps summaries, faithful rewrites and authorized additions distinct
- Prepares channel-appropriate content; external sending remains a separate authorized action
- Records selected pinned sources, independent Astra/Fable Max reviews and bounded multilingual trials

### comment-style

Word brief PR replies, review comments, chat messages and social replies with
the point first. Keep fitting enthusiasm, humor and useful curiosity alongside
the facts that matter.

**Triggers:** `reply to this PR comment`, `shorten this Slack message`, `draft a WhatsApp reply`

Starts from the former private `comment-style` package. A short sentence is the
default; facts, conditions and the user's intended tone survive shortening.
Wording and authorized sending remain separate. Review workflows retain code
repairs, comment placement and thread resolution.

### write-documentation

Create, update or review human-facing documentation using current evidence and a
path the intended reader can follow. Uses `communicate-clearly` when available;
`agent-instructions` retains agent-consumed instruction authoring.

**Triggers:** `write a guide`, `update this README`, `review the API reference`, `document this runbook`

**Features:**

- Organizes content by reader need while preserving useful existing structure
- Verifies commands, examples, prerequisites, expected results and version-specific claims
- Distinguishes current behavior, approved decisions, proposals and unknown rationale
- Checks the document without relying on private author context
- Maintains relevant links and requested language versions within scope
- Reports actual validation and its limits without authorizing production operations or publication

These are repository packages, not a global installation. Replace installed
`humanize` references with `communicate-clearly` when migrating a host; do not keep
both as competing automatic prose owners. Host selection still depends on the
installation and supported activation mechanism.

### report-work-activity

Explain activity over a chosen period and current outstanding work in a private
HTML report with retained evidence. Replaces the deprecated `daily-meeting-update`;
the old name remains an explicit migration alias, and its legacy digest is retired.

**Triggers:** `what did I do yesterday`, `summarize last month's work`, `what commitments are still open`

**Features:**

- Uses one Codex Luna extractor per available source/workstream and primary verification
- Covers engineering, collaboration, sent email, calendars, meeting notes, incidents and agent history when connected
- Separates work and open source, with work totals and per-repository counts
- Distinguishes historical events from current commitments, assignments and unanswered requests
- Resolves calendar periods and renders escaped offline HTML with deterministic Python helpers
- Retains detail pages, excerpts, source locators and ledgers for follow-up without recollection
- Records seven selected donor feeds and the 19-repository source review

### handoff

Create a focused Markdown document so another agent or session can continue a
task, including a parallel side task while the original session continues.

**Triggers:** `prepare a handoff`, `save context for another agent`, `export this task for a new session`

**Features:**

- Front-loads the next action and preserves relevant decisions, partial work, evidence, and blockers
- Distinguishes confirmed choices from proposals and checks that passed from checks not run
- Uses the user-named destination or OS temporary storage, reporting any pickup limits
- Checks saved content and local references, and reports access or retention limits
- Keeps document creation separate from receipt, session launch, and execution ownership
- Records four source feeds at exact revisions; uses `agent-instructions` when available

### prototype

Resolve a design, state-model, or behavior question with a disposable experiment.
Use it directly or as one phase of a larger task; it does not require work-mode.

**Triggers:** `prototype these layouts`, `explore this state model`, `try a small experiment before choosing an approach`

**Features:**
- Loads separate guidance for logic demos, interface alternatives, and empirical experiments
- Returns a runnable artifact, observed evidence, tradeoffs, and a bounded recommendation
- Keeps production implementation and delivery outside the prototype's scope
- Records Matt Pocock and Lauren Tan's pstack sources at exact commits
- Uses `verify` for performance-evidence assessment while retaining the experiment and a useful fallback when the specialist is unavailable

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
- Uses `verify` for performance claims, including memory regressions, then continues the active diagnosis or repair
- Records exact source commits

### tdd

Implement features or authorized fixes through test-first increments. Use it
directly when TDD is requested, without work-mode or an installed upstream skill.

**Triggers:** `implement this with TDD`, `fix this test-first`, `use red-green-refactor`

**Features:**
- Observes a meaningful failing test before implementing each behavior
- Tests caller-visible contracts using independent expected results
- Allows focused refactoring while tests remain green
- Distinguishes setup failures and already supported behavior from a valid red state
- Records Matt Pocock's exact source revision

### explain-code

Explain how existing code works and which component owns each responsibility.
Use it directly for a mechanism, subsystem, or ownership question.

**Triggers:** `how does this flow work`, `explain this subsystem`, `which module owns this state`

**Features:**
- Traces entry points, data, state transitions, and boundaries from actual source
- Answers at the requested depth with a concrete flow and relevant code locations
- Distinguishes inspected behavior, observed execution, documented reasons, and unknowns
- Explains requested before/after mechanisms; keeps diagnosis, diff audits, activity reports, and guided teaching with their owners
- Derives from pstack/how with limited presentation guidance from pstack/teach
- Records exact source commits

### explain-decisions

Reconstruct the reasons behind existing code or design decisions from historical
evidence. Use it directly, without work-mode or an installed upstream skill.

**Triggers:** `why did we choose polling`, `what motivated this guard`, `where did this threshold come from`

**Features:**
- Follows relevant history and linked discussions, including earlier paths and revisions
- Separates recorded reasons, supported inferences, and unanswered questions
- Distinguishes original motivation from later decisions and current necessity
- Preserves contradictory evidence and reports missing sources without inventing intent
- Derives from Lauren Tan's pstack/why with exact provenance

### analyze-change-effects

Trace what a change could break elsewhere and test the assumptions that decide
whether those paths are safe. Use it directly for implemented or proposed changes.

**Triggers:** `what could this change break`, `analyze the effects of this change`, `test whether old consumers still work`

**Features:**

- Follows effects across dependency behavior, lifecycle timing, data formats, and indirect consumers
- Uses focused execution against actual code to test deciding assumptions
- Distinguishes confirmed breakage, cleared risks, and unproven conditions
- Preserves product files and respects explicit inspection-only requests
- Records pstack provenance

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
- Preserves exact pstack sources

### design-code-structure

Design, compare, or improve data models, public interfaces, and module boundaries
for a concrete software change. Connect the chosen design to demonstrated structural
checks during authorized implementation; design-only requests stop at the plan.

**Triggers:** `design this module`, `compare these interface designs`, `model the state and ownership for this change`

**Features:**

- Derives types and operations from real caller usage and established constraints
- Compares meaningful alternatives by correctness, caller effort, locality, state, and cost
- Selects improvements using scoped semantic history, requirements, correctness risk, locality, and migration cost
- Checks whether edits from partial context preserve boundaries and authoritative registry relationships
- Proves selected structural checks with valid, violating, and restored inputs through the real verification command
- Uses explain-code, explain-decisions, analyze-change-effects, prototype, and compare-solutions when the decision needs them
- Handles shared invariants, retries, cancellation, external contracts, and migration when relevant
- Revisits a design when repeated implementation friction exposes a wrong assumption
- Records pstack, Matt Pocock, and Matthew Blode sources

### error-handling

Design, implement, or review error contracts and recovery across software
boundaries. Adapt to the project's language and existing public interfaces.

**Triggers:** `review this operation's error handling`, `design safe recovery`, `implement retries for this boundary`

**Features:**

- Preserves established error representations, useful causes, cancellation, and resource ownership
- Separates known failure from an unknown or partially completed operation
- Bases retries on real replay guarantees, transient classification, deadlines, and one retry owner
- Keeps public messages accurate and filters sensitive diagnostic content before recording it
- Tests observable results and effects, including recovery and effects that must not repeat
- Uses debug and verify conditionally, with pinned ECC and pstack provenance

### observability

Assess and build a project's observability, from initial setup to instrumentation
added during feature work. Identify useful additions from the architecture and
workflows, then implement and verify the requested coverage.

**Triggers:** `set up observability and metrics for this project`, `find where we should add instrumentation`, `add observability while building this feature`

**Features:**

- Prioritizes concrete instrumentation points by impact, visibility gaps and cost
- Builds a usable collection and inspection path when telemetry is absent
- Extends existing conventions within a feature's affected operations and boundaries
- Adds safe logs, bounded metrics, traces, health signals and alerts where useful
- Delivers code, configuration, inspection instructions and verified emitted data
- Keeps assessment-only work read-only and incident investigation with debug

### performance-optimization

Improve a user-relevant operation through measured changes that preserve required
behavior and earn their complexity. Use it when the goal is known but the winning
change is not.

**Triggers:** `reduce this job's memory use`, `improve API throughput`, `make this operation faster without changing its results`

**Features:**

- Defines the operation, worthwhile benefit, correctness and resource limits before tuning
- Prioritizes measured bottlenecks and runs bounded, interpretable experiments
- Keeps supported gains, rejects unsafe or unjustified changes and records unsuccessful attempts
- Uses `verify` for evidence, `debug` for regressions, `prototype` for disposable experiments and `observability` for durable signals
- Adapts pinned Addy Osmani, pstack, ECC and Compound Engineering sources with original notices
- Accepts a supported no-improvement result or a specific evidence gap; never promises a speedup

### accessibility

Design, implement, or audit accessible user interfaces across complete tasks,
including errors, recovery, and the resulting state. Use it directly or as a
specialist within an implementation or code review.

**Triggers:** `audit this dialog's accessibility`, `fix keyboard navigation`, `check this flow with a screen reader`, `review WCAG requirements`

**Features:**

- Selects platform criteria and preserves audit-only or implementation authority
- Uses conditional web, native, and terminal guidance without language-specific code recipes
- Checks semantics, keyboard and focus, visual conditions, content alternatives, and recovery
- Distinguishes automated findings, observed interaction, and missing assistive-technology evidence
- Uses verify and local recipes for execution; keeps required third-party steps in coverage
- Records six selected source feeds, primary references, and corrections

### typescript-best-practices

Implement or review TypeScript contracts without confusing static compatibility
with runtime guarantees. Use it directly or as a language specialist during a change.

**Triggers:** `implement this TypeScript contract`, `review these types`, `diagnose this TypeScript module configuration`

**Features:**

- Strengthens types where an operation needs a guarantee, preserving legitimate states and callers
- Checks boundary parsing, predicate claims, mutable aliases, missing values, and async callback ownership
- Loads compiler and package-consumer guidance only for relevant configuration or module work
- Keeps style in existing tooling and broader design, review, and recovery with their owners
- Records five selected source feeds after reviewing nineteen repositories and all twenty-four pstack principles
- Includes technical compiler/runtime evidence; independent agent improvement and host activation remain untested

### deprecate-and-remove

Retire a dependency, API, or feature the project no longer wants to maintain.
Replace it when needed and complete cleanup while preserving required behavior.

**Triggers:** `replace MUI with shadcn`, `replace Moment with date-fns`, `retire this feature progressively`

Supports a coordinated internal replacement or a staged sunset with no successor.
Tracks consumers, notices, access closure and removal conditions; preserves shared
code, supported clients and required records. Distinguishes local cleanup from
deployed retirement and composes the existing design, delivery and verification
skills. Records three pinned donors and bounded synthetic execution evidence.

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
- Uses explain-decisions and verify conditionally, with pinned Cursor, pstack, and Addy Osmani provenance

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

### pr-review

Review another author's GitHub PR with independent Codex and Claude attempts
over the same frozen scope, then publish one review: Comment with the
verified findings, or Approve when the review is complete and nothing blocking
remains.

**Triggers:** `$pr-review <url>` or a request to review and publish on a PR you were asked to review; an unpublished review belongs to `review-code-changes`.

Uses `review-code-changes` for the audit protocol, `compare-solutions` for independent
attempts and `comment-style` for wording. The parent verifies findings, checks
cross-repository seams and reconciles existing feedback, continuing a same-topic
point in its existing thread. It never requests changes, never submits a review
the user started, and approves only when no required finding or required
reviewer thread remains open; open suggestions and nits never block approval.
Read-only review controls, bounded retries and exact actor/head
binding remain part of the workflow. Where the host can rename a conversation
dedicated to one review, as in T3 Code, it titles it
`[REVIEW] #<number> <ticket> <author>`, with `NO_TICKET` when no subject ticket
is found in any tracker. After a published Comment review it starts
`pr-review-followup` unless you ask for the review without follow-up.

This replaces `pr-review-draft`, which left a pending review for the user to
submit. Update installed links and explicit invocations to `pr-review`; no alias
package is included. Private profiles stay outside the package, in
`$XDG_CONFIG_HOME/pr-review/profiles` (or `~/.config/pr-review/profiles`), with the
legacy `pr-review-draft/profiles` used when the new directory is absent, or a
directory passed with `--profiles-dir`. Generic reviews need no profile.

### pr-review-followup

Follow a PR you reviewed until your required threads are settled and it is
approved.

**Triggers:** starts after `pr-review` publishes a Comment review unless you ask for the review without follow-up, or when you ask to follow up a PR you reviewed. A status question gets only the current state.

In T3 Code it runs when T3's PR watch reports a change; elsewhere it runs every
30 minutes by default. Each run re-reviews a new head with `pr-review`, replies
in your own threads, resolves what the current head or a confirmed ticket settles,
reopens a thread whose finding still stands, and approves only through a gate its
helper enforces: a complete review of the current head, no standing required
finding and every required reviewer thread resolved and verified. Open
suggestions and nits do not block it, and stay with the author after approval.
Your own PRs belong to `pr-followup`.

### verification-authoring

Create and maintain project-local `verify-<app>` skills that another agent can
execute from a cold start. Install `agent-instructions` alongside this authoring skill.

**Triggers:** `create a verification skill for this app`, `maintain verify-memo`, `update the verification recipe`

**Features:**

- Discovers real launch commands, driving tools, observation points, and isolation
- Preserves pstack's Launch, Doctor, Drive, Evidence, Cleanup, and Helpers contract
- Creates a feature map and proves one feature; maintenance reviews and drives every feature
- Distinguishes recipe drift from product defects and preserves evidence after cleanup
- Includes a read-only map checker and records pinned pstack sources

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
- Assesses performance claims through completed correct work, comparable conditions, variation, and realistic resource budgets
- Returns measurement verdicts to `debug` or `prototype` without starting another investigation or requiring benchmarks for functional checks

### commit

Create atomic Conventional Commits that a human can understand and review.

**Triggers:** `commit`, `/commit`, `make a commit`

**Features:**

- Keeps one coherent behavior with its regression tests and required generated output
- Preserves unrelated staged and unstaged work, including partial-file boundaries
- Grounds the message in the verified index and supplied motivation
- Verifies the actual commit, parent, message and residual work after hooks run
- Publishes only within existing authorization and hands PR presentation to `pr`

### issue-workflow

Publish prepared tasks and keep source tickets aligned with implementation start,
PR creation and merge. `task-breakdown` owns the delivery boundaries; Publish mode
preserves those contracts, reconciles existing tickets and verifies relationships.
Drafting tasks alone makes no tracker writes or implementation-state transitions.
Each consuming project owns its rules in `docs/agents/issue-tracker.md`, or a
user's own instructions designate a policy for the repositories they choose; the
package includes an unconfigured template and Linear, Jira and GitHub guidance.

**Triggers:** `create tickets from this breakdown`, `start implementing this ticket`, `synchronize this merged PR's ticket`, `configure ticket transitions`

Starting work maps to In Progress, PR creation to In Review (including drafts),
and verified merge to the project's chosen state, such as Ready for QA or Done.
For each workflow scope, selected from the ticket's own fields, the policy
chooses real states, source guards, branches, completion conditions and one
transition owner. Partial work, manual progress and native automation are
preserved; uncertain writes are reconciled before retrying.

Install alongside `pr` and `pr-followup` for their event hooks. Approval alone is
not merge. Other publishers need an explicit invocation or their own integration;
unattended events require a configured durable handler. Repository files alone do
not install the skill or enable tracker automation.

### pr

Create or update a GitHub PR with a concise explanation and useful review evidence.

**Triggers:** `create a PR`, `update the PR description`, `draft a PR body`

**Features:**

- Resolves the exact target, fork, head and actual base
- Checks claims against implementation, requirements and current verification
- Checks a task's review-size cap against the actual PR diff before publishing code or creating the PR
- Follows repository conventions while allowing useful additions where the format permits
- Keeps the body to what helps review the diff and returns project coordination, such as flag timing or other tickets' scope, to the user
- Sizes the body against the repository's recent merged PRs, gives each decision and check one line, replaces superseded runs on updates, and moves run detail to a linked artifact or one detail comment
- Captures visible UI changes and attaches real images through supported `gh --attach` operations
- Continues into `pr-followup` after creating a PR unless you ask for it without follow-up
- Preserves uploaded URLs on rewrites and recovers partial uploads without duplicate PRs
- Uses diagrams and measured comparisons when they aid review
- Preserves draft preference, verifies the GitHub actor and publishes over SSH
- Refreshes the whole description after material publication under existing authorization
- Resolves ticket hints through `issue-workflow` and applies the project-selected review event after creation

### pr-followup

Evaluate feedback on an existing PR and resolve authorized code, CI and base problems.

**Triggers:** `resolve this PR's feedback`, `check PR readiness`, `babysit this PR`

**Features:**

- Separates read-only checks, feedback repairs and host-managed babysitting under the applicable stopping policy
- Ends watch wakes that change nothing without a message; in T3 Code, waits on its PR watch and unwatches before handing a turn back to you
- Collects threads, reviews, conversation, check annotations and reviewer logs
- Reevaluates edited comments and new replies in resolved or outdated threads
- Tests claims against current code and keeps independent repairs progressing
- Uses `commit` and `pr` for their phases; requires those local owners when those phases are reached
- Distinguishes fixed, verified, published, replied and resolved states
- Merges settled PRs in LuisUrrutia's personal repositories without waiting for approvals, after all feedback is resolved and CI/CD passes
- Elsewhere, follows PRs until merge or formal approval; rechecks new heads and reports pending work without automatic scheduling
- Reconciles observed ready/merge events through `issue-workflow`, preserving Check scope and existing authority

These Git and ticket workflow skills record pinned sources and local decisions in
`origin.toml`. Repository files are distinct from
installed copies.

### ci-cd-automation

Design or improve CI/CD stages, required checks, artifact promotion, and release
or deployment criteria. Keep provider mechanics in their specialist skills.

**Triggers:** `design our CI/CD`, `what should our pipeline contain`, `review artifact promotion`, `improve pipeline structure`, `reduce pipeline wait and cost`

**Features:**
- Selects checks from product risks and existing project commands
- Connects stages through exact candidate identity, evidence and trust boundaries
- Defines rollout acceptance, interrupted-run recovery and shared-target ownership
- Loads stateful delivery and measured efficiency guidance only when relevant
- Uses `github-actions` for GitHub implementation, `verify` for execution evidence, and `pr-followup` for existing PR checks
- Records five selected source feeds after research across 19 repositories

### github-actions

Guidelines for writing secure and maintainable GitHub Actions workflows.

**Triggers:** `GitHub workflow`, `github actions`, `Dependabot`, `actions yaml`

**Features:**
- Security best practices (pinned actions, least-privilege permissions)
- Performance patterns (caching, parallel execution, fail-fast)
- Shell scripting guidelines
- Reference docs for API calls, matrix builds, and reusable workflows
- Integrates with `actionlint` for validation

### domain-search

Check whether domain names are available to register and what they cost.

**Triggers:** `is acme.io available?`, `check these names on .com and .ai`, `search acme in every TLD`

**Features:**
- Checks several names in one run, by default on .com, .ai, .app, .io and .dev
- Counts a DNS-delegated domain as taken and asks the TLD's registry over RDAP or WHOIS about the rest; a failed or throttled check is never reported available
- Searches every TLD that Porkbun prices, plus .cl and .es, by TLD popularity in the Tranco top-1M list; the registry checks the 30 most popular open TLDs per name, and the rest are listed with DNS evidence only
- Reports each domain as a bullet with Porkbun's public first-year and renewal prices, fetched without an API key
- Paces queries per registry server and keeps a throttling server in cooldown across runs, because one registry blocks bursts for 24 hours

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
