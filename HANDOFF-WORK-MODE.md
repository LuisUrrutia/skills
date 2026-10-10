# Work-mode: implementation handoff

Prepared on 2026-10-07 from the conversation and a fresh inspection of the skills
repository. The upstream comparison was performed on 2026-10-06 at the exact
revisions recorded below.

This document is continuation context. Current user instructions, applicable
project rules, host capabilities, and freshly verified state govern execution.
It does not grant new publication, installation, deployment, merge, messaging, or
background-scheduling authority. The exporting agent created this document only;
it did not implement work-mode, launch a receiving agent, or establish receipt.

## 1. Resume here

The next task is to design, implement, and validate a new local `work-mode` skill
that combines the two objectives the user selected:

1. Carry one authorized task through the work needed to reach its requested
   outcome: implementation, verification, review, and delivery when included.
2. Choose the appropriate route for the type and current state of the work:
   a bug, a feature, uncertain direction, an already-planned task, or a small
   settled change should not all receive the same process.

The user then requested a fresh comparison with other repositories, especially
pstack. That comparison is complete and summarized here. No candidate skill has
been drafted, installed, or behaviorally evaluated.

Start by reconciling the current repository with section 3, then read the local
owners in section 5. Use the supplied decisions and research to establish the
skill's contract; do not repeat the whole research survey as a prerequisite.
Reopen the pinned donor files that actually inform the implementation, including
their relevant dependencies and license notices. The proposed design in sections
6 and 7 is a reasoned starting point, not an additional set of user-approved rules.

Use `workflow-to-skill` to extract the reusable contract from this conversation
record, then `agent-instructions` for authoring and evaluation. The contract
extraction can be brief because the outcomes and ownership boundaries are already
substantial. Follow the receiving host's applicable skill-creation requirements.

The intended result is a portable coordinator integrated into this repository,
with evidence for its routing and continuation behavior. It should call the
existing skills by registered name and retain their responsibilities.

## 2. User decisions and conversation context

### Confirmed choices

- The name under discussion is `work-mode`.
- Asked to choose possible objectives, the user replied: "Vamos con 1, pero
  tambien 2". Those options were end-to-end work on one authorized task and
  adapting the route to the kind of work, respectively.
- The user specifically asked to inspect other repositories for inspiration,
  with particular interest in pstack. The research must examine the actual
  source instructions, not only an atlas summary or remembered descriptions.
- Comparisons were requested in chat, rather than inserted into the HTML atlas
  as a substitute for answering. Repository package integration is distinct from
  publishing another comparison page.
- The user values small, coherent, testable changes that a person can review.
  Their example was one dashboard statistics card with its actual data and
  required layers, rather than a PR for a button followed by a PR for a card shell.
  A justified backend prerequisite, frontend increment, and later integration
  can also be valid when a complete vertical slice is impractical.
- `wayfinder` chooses a direction; `planning` makes it executable;
  `task-breakdown` defines smaller delivery units. Work-mode should compose these
  owners when needed, preserving each as a separately usable capability.
- Starting implementation from a ticket must trigger the configured
  `issue-workflow` event even if no PR is involved. A previous description change
  narrowed this incorrectly, and the user explicitly called it a regression.
- The user objected to duplicating the PR size-check procedure in `pr` and
  `stacked-pr`. The implemented correction makes `pr` the shared check owner.
- The latest request to the exporting agent was to prepare a detailed handoff
  that can be passed verbatim to another agent. It was not a request to implement
  work-mode in the exporting turn.

### Important correction to the previous comparison

Earlier conversation and research used 5,000 changed lines as the PR budget in
the discussed example. The current repository subsequently changed its general
contract in `a427edf`: keep work reviewable, but enforce a numeric ceiling only
when the user, project rules, or authoritative task record explicitly sets it.
`task-breakdown/origin.txt` now describes the earlier figure as illustrative
guidance rather than a portable default.

Do not encode a universal 5,000-line ceiling in work-mode. Carry an actual
explicit cap, including 5,000 when one is established for the active task, to its
existing owners. The earlier research brief and assistant answer did not account
for this correction; the current files are the implementation baseline.

### Proposals, not separately confirmed choices

The previous assistant recommended combining pstack's task-specific routes with
Compound Engineering's caller/child return contract. It proposed explicit
endpoints, evidence-bearing phase returns, and recoverable state. The user has
requested continuation context, not approved every mechanism or field in that
proposal. The receiving agent should assess these mechanisms against the selected
objectives and current owners, resolve routine details autonomously, and ask only
about consequential choices that available evidence and authority cannot settle.

A long-running program manager that selects arbitrary backlog work, a recurring
scheduler, and a new autonomous-agent runtime were not selected as v1 objectives.

## 3. Repository snapshot and changes since research

Verified at export:

- Checkout: `/Users/luisurrutia/.t3/worktrees/skills/t3code-767d9f53`
- Branch: `luisurrutia/review-handoff-html-1`
- HEAD: `8df2b2888e313a179575a7f0f7d6625968a0825a`
- Configured upstream shown by Git:
  `origin/luisurrutia/review-handoff-html-1`
- Tracked worktree and index were clean before writing this ignored handoff.
- `work-mode/` and `work-mode/SKILL.md` do not exist.
- The atlas still records `work-mode` in `repositoryInventory.pending` as
  "Coordinator not created".
- `~/.agents/AGENTS_LOCAL.md` did not exist when checked. Recheck on pickup.

The source comparison started at `f87a7c1863ccb80fe090f5876bc9da475e900277`.
The branch has since advanced. These commits matter to continuation:

- `293d2d8`: task-breakdown carries risks and context into delivery units.
- `6191416`: issue-workflow again activates when ticket implementation starts.
- `f87a7c1`: `pr` owns the shared size-cap check; `stacked-pr` calls it.
- `7289b54`: `retro` was added as the owner for diagnosing session friction and
  routing proposed improvements.
- `a427edf`: enforce only explicitly established numeric PR caps.
- `4eb989b`: preserve authorization across QA and task-publication handoffs.
- `8df2b28`: reconcile the atlas inventory with the current packages.

Use `git show` for the relevant patch before changing a boundary it established.
Do not reset to the research commit or overwrite subsequent work.

`HANDOFF.md` is an older, broader collection handoff. It remains useful for the
atlas and authoring context, but its instruction to choose the next capability
predates the user's selection of work-mode. Its counts and historical source
assessments are not substitutes for current package state.

The user replaced the supplied global AGENTS instructions on 2026-10-07. Earlier
Orca-specific setup and ownership rules from the conversation are not part of
that replacement. Follow the current host and current effective instructions,
rather than reviving removed rules from old context.

## 4. What exists, what was checked, and what remains

Completed work relevant to this handoff:

- Existing local owners for direction, planning, decomposition, ticket events,
  verification, review, commits, PR publication, stack operations, and follow-up.
- A fresh comparison of seven upstream repositories at immutable revisions.
- Independent source consultations from Codex Astra Max and Claude Fable 5.1 Max,
  reconciled against the actual source files and local contracts.
- A later coordinator inspection of Compound's outer `lfg` skill, which clarified
  that `ce-work` is an executor inside a larger workflow.
- Fresh inspection during this export of the core local contracts and later
  commits that affect the design.

Not completed:

- Work-mode activation wording, entrypoint, references, or provenance package.
- A finalized rule for optional delegation, independent review, or work-mode
  state representation.
- Candidate instruction reviews, behavioral trials, host selection tests,
  portability checks, or installation of work-mode.
- Changes to README, registry, or atlas for a completed work-mode package.
- Any new PR, push, ticket mutation, host watch, or deployed workflow from this
  research/export task.

No prerequisite is currently known to block writing the candidate. Actual host
capabilities and required review-model access must be verified when needed.

## 5. Existing owners to preserve

All paths in this section are relative to the skills repository root. They are
source locations for authoring, not paths to hardcode into the installed skill.
At runtime, resolve collaborators through the receiving host's skill catalog.

- `wayfinder/SKILL.md`: connected uncertainty, alternatives, evidence, direction,
  and durable decision context. A single answerable question or an already-settled
  direction does not require a new map. Continues authorized planning.
- `planning/SKILL.md`: implementation approach, contracts, dependencies, acceptance
  evidence, readiness, and reasons to replan. It can produce a short plan for a
  small change. Planning-only scope ends at the artifact; already-authorized
  implementation continues without a second approval gate.
- `task-breakdown/SKILL.md`: functional delivery boundaries, real dependencies,
  readiness, acceptance checks, review budgets, and explicit caps. A formal plan
  is useful but not mandatory. The skill does not choose worker topology.
- `issue-workflow/SKILL.md`: Inspect, Synchronize, Publish, and Configure operations.
  The consuming project's canonical policy determines status destinations and
  event ownership. `work-started` fires when implementation actually starts,
  including without a PR. Reading, routing, planning, and triage do not establish
  that event. No linked ticket returns `not applicable`. A blocked transition
  leaves independent delivery work available.
- `debug/SKILL.md`: diagnosis and authorized repair of an observed bug or
  regression. It can be used directly. Do not implement a fix twice because
  work-mode assumes every specialist returns only a diagnosis.
- `prototype/SKILL.md`: resolve a question with a bounded experiment. Its artifact
  is experimental; integrating it into production is a separate scope decision.
- `tdd/SKILL.md`: test-first implementation when selected. Do not force TDD for
  every task merely because a donor does so.
- `design-code-structure/SKILL.md`: substantive model, interface, and module
  boundaries. Load it for a real structural question rather than every edit.
- `verify/SKILL.md`: decide whether current execution evidence establishes the
  requested behavior and completion claim. Project `verify-<app>` skills own
  concrete launch, doctor, driving, proof, and cleanup. Evidence must match the
  relevant input/revision and environment. Missing packaging does not erase useful
  existing checks, but those checks cannot prove unexercised application paths.
- `verification-authoring/SKILL.md`: author or repair an executable project
  verification recipe when that work is authorized. Missing a recipe does not
  silently authorize a new persistent setup.
- `review-code-changes/SKILL.md`: read-only review of a declared snapshot. The
  caller evaluates and applies findings after the review returns. Its report
  validator proves format and coverage declarations, not defect truth. Existing
  conditional delegation stays with that owner.
- `simplify-code/SKILL.md` and `analyze-change-effects/SKILL.md`: focused improvement
  and consequence analysis when the task merits them. Neither needs to become an
  unconditional extra phase for every tiny change.
- `commit/SKILL.md`: atomic commit preparation and creation under current branch
  and authorization rules. Do not postpone every commit until final delivery if
  the repository requires completed atomic boundaries to be committed.
- `pr/SKILL.md`: one PR's publication, title/body, evidence, identity, and shared
  `Check cap` operation. Creation defaults to draft and enters `pr-followup` Drive
  unless create-only scope limits continuation. Keep-draft constrains the ready
  transition, not all follow-up. An Update inside follow-up returns to that loop.
- `pr-followup/SKILL.md`: feedback, CI repair, conditional readiness, and Drive
  until verified current formal approval or actual merge. Green CI, an empty queue,
  and merge-ready are not interchangeable with those endpoints. Uses host-managed
  watches and yields while waiting; it does not create its own polling loop.
- `stacked-pr/SKILL.md`: one owner for stack topology and stack mutations. Calls
  `pr` Check cap per layer using its actual immediate base. Its own requested
  operation and merge boundaries remain authoritative.
- `worktrunk/SKILL.md`: worktree lifecycle through `wt` when needed. Do not make
  raw `git worktree` commands part of work-mode's portable procedure.
- `handoff/SKILL.md`: export continuation context. Writing a document does not
  mean another agent received it or took execution ownership.
- `retro/SKILL.md`: session-friction analysis and proposed improvements. Automatic
  skill rewriting or retrospective work is not an implicit end-of-task phase.

Domain skills such as `typescript-best-practices`, `accessibility`,
`github-actions`, `error-handling`, and `ci-cd-automation` remain conditional on
the actual change. `how` and `why` were renamed to `explain-code` and
`explain-decisions`; use the current registered names.

The QA case-authoring and tester-army installation effort is recorded separately
in `HANDOFF-QA.md`. The proposed `qa-test-authoring` name there is not an installed
dependency. Building that skill, installing `e2e`, and configuring Playwright MCP
are separate work, not prerequisites to authoring work-mode.

## 6. Proposed work-mode contract

This section turns the comparison into a candidate design. Validate it before
encoding it; keep the main entrypoint proportional and use conditional references
only when they carry meaningful separate detail.

### Entry and scope

Activate for coordinating execution or resuming an authorized piece of work.
Accept a direct request, ticket, selected delivery unit, implementation plan, or
existing in-progress state. Preserve the user's requested result and any explicit
limits such as read-only, diagnosis-only, local-only, create-only, or keep-draft.

The endpoint comes from the active request plus current standing rules. A generic
implementation request should not manufacture a PR, a deployment, or a merge.
Conversely, a request already covering delivery should not stop after writing a
plan or after a specialist finishes an intermediate phase.

Inspect existing decisions, work, and evidence before selecting a route. Do not
restart discovery for a settled ticket, choose an arbitrary backlog item, or
silently expand one bounded unit into a whole project.

### Route selection

Candidate routes, to be tested rather than copied mechanically:

1. **Small, settled change:** implement the scoped behavior with applicable domain
   guidance, verify, review proportionately, and complete the authorized endpoint.
   No formal direction map or decomposition is necessary merely to enter the mode.
2. **Bug or regression:** use `debug` with the observed symptom and scope. Carry
   its actual diagnosis/fix result forward. Verify the original reproduction and
   current change; review and deliver only as requested.
3. **Clear feature or ready task:** use the existing execution contract. Resolve
   missing implementation approach through `planning`; use `task-breakdown` only
   when the work needs smaller coherent delivery units or revised boundaries.
4. **Unsettled initiative:** use `wayfinder` for connected decisions, optionally
   supported by `prototype` or `design-code-structure`; continue planning and ready
   implementation when the enclosing request already authorizes them.
5. **Refactor:** preserve the existing behavioral contract, characterize what
   matters, change structure, and demonstrate equivalence within the actual scope.
6. **Research, planning, review, or prototype only:** return the requested result
   through its existing owner. The coordinator must recognize the endpoint rather
   than append implementation and publication automatically.

Do not treat these as a mandatory six-mode API or promise every route needs a
separate reference. A compact decision table or a few conditional paragraphs may
be enough. Actual input gaps and risks should drive the route.

### Phase composition and return

For each phase, establish its input, selection condition, responsible owner,
required result/evidence, and continuation. This is the coordinator's main value.

The child should receive the selected work, current constraints and authority,
relevant artifact/revision, requested scope, deciding evidence, and its output
destination when needed. After it returns, examine the actual result before
choosing the next phase. A returned implementation or fix should not be repeated.

The useful idea from Compound is: ending a child skill does not end the enclosing
task. Equally, calling a child does not grant it the rest of the delivery workflow.
Inspect existing modes before adding any new return mode. `pr` Check cap already
demonstrates a narrow operation that returns to its caller without publication.

Suggested information to preserve, without requiring a universal new JSON schema:

- Task/unit identity and authoritative plan or ticket.
- Requested outcome and explicit limits; source of consequential decisions.
- Current phase and next action; identity of the active mutation/watch owner.
- Artifact paths, relevant revision/input identity, and what actually changed.
- Observed checks, results, evidence locations, and which inputs they validate.
- Remaining findings, blockers, pending user decisions, or waiting events.
- Delivery state and exact external identifiers only when that phase exists.

Use each owner's actual return contract. Do not impose fields on every existing
skill simply to normalize the coordinator's bookkeeping.

### Review and repair

Keep auditing read-only. The implementation owner decides how to act on supported
findings under the current request, then reruns checks invalidated by the fixes.
Do not regard a clean report as execution evidence or a passing test as proof
that an untested requirement was delivered.

Choose review effort from the change and applicable policy. Mandatory independent
review for every future product task is not a confirmed work-mode requirement.
The separate mandatory Astra/Fable consultation for authoring this skill is an
existing `agent-instructions` requirement, not a work-mode runtime policy.

Avoid importing a numeric fix-round limit that silently converts an unresolved
defect into completion. If evidence indicates a loop is not progressing, identify
the real missing premise or decision and retain the unresolved result.

### Continuation, suspension, and completion

Continue authorized independent work when one prerequisite or decision is blocked.
Do not ask the user again for an already-authorized phase, and do not infer approval
from silence. Re-route when new evidence changes the task's needs; preserve settled
decisions and ask only for a consequential choice that existing authority cannot
resolve.

Keep `complete`, `waiting`, `blocked`, `failed`, and partial evidence distinct,
using the host and owner vocabulary rather than manufacturing success. A
host-managed PR watch can legitimately end the current agent turn while leaving
the task waiting. Retain enough state to resume with the existing owner, refresh
remote facts, and avoid starting a second follow-up loop.

Completion is the requested endpoint with its required current evidence. Local
implementation, verified publication, formal approval, merge, and deployment are
different outcomes. Work-mode must not weaken the owner's completion condition to
finish its own checklist.

Use existing authoritative plans/task records rather than maintaining competing
copies. Scratch state can live under `.tmp/<task>/` when permitted and verified
ignored. If the only continuation record is ignored or checkout-local, explicitly
preserve/transfer it using `handoff`; do not claim durable cross-machine recovery
from an unshared local path. No database or scheduler is implied.

## 7. Regression traps and boundaries

- Do not narrow `issue-workflow` back to PR-linked work. Actual implementation
  start is the deciding event; planning a ticket alone is not that event.
- Keep ticket creation distinct from synchronizing an existing ticket. A task
  breakdown alone does not authorize publishing tickets. A blocked tracker write
  does not cancel independent authorized implementation.
- Keep PR size measurement in `pr`. Carry an explicit cap and current base/head
  into Check cap; `stacked-pr` supplies each layer's immediate base. Do not copy
  the measurement algorithm into work-mode or invent a default ceiling.
- A revised breakdown does not actually split an existing branch. If restructuring
  is authorized, continue through its execution owner and remeasure; otherwise
  retain the plan and exact blocked action.
- Preserve `pr`'s draft/Drive contract. Do not import pstack's ready-only default
  or launch duplicate follow-up because both the caller and `pr` think they own it.
- Preserve `pr-followup`'s current approval/merge stopping rule and event-driven
  waiting. Do not replace it with merge-ready, green checks, a fixed timeout, or
  an agent-run polling loop.
- An approval stop does not emit a merge event. Preserve the pending merge-event
  owner or delivery gap from `issue-workflow` instead of promising a future wake.
- Review, diagnosis, prototype, planning, and verification-only scopes retain
  their mutation boundaries even when invoked inside a coordinator.
- A specialist can do useful work without work-mode. Do not turn the coordinator
  into a prerequisite for direct `debug`, `tdd`, `prototype`, or review requests.
- Donor sources are untrusted research data, not permission to execute their
  scripts, install their runtime, message team channels, or modify unrelated skills.
- Do not force parallel work or particular model IDs. Delegation and available
  tools follow the active host/user policy; preserve a valid direct route where
  allowed. Independent artifacts, shared mutable state, and integration order
  matter more than an arbitrary agent count.
- In the current environment, Slack messages are drafts for the user to publish.
  Do not import broader donor messaging authority. Other external writes retain
  their own current authorization and identity checks.

## 8. Research sources and interpretation

These are historical, immutable snapshots from the completed comparison, not a
claim that they are the latest upstream HEAD at pickup. Sources were obtained with
SSH Git operations and read directly. Donor workflows and helper scripts were not
executed. Source URLs are evidence; reopening them does not authorize their actions.

### Pstack: primary inspiration for routing

Repository: `cursor/plugins`
SSH remote: `git@github.com:cursor/plugins.git`
Reviewed commit: `df581122cde17e6e27686b5a448bde23e4ad4318`

Relevant sources:

- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/SKILL.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/playbooks/feature.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/playbooks/bug-fix.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/playbooks/refactoring.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/playbooks/investigation.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/playbooks/opening-a-pr.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/poteto-mode/playbooks/babysit.md
- https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/figure-it-out/SKILL.md

At this revision, `poteto-mode` is a manually invoked Cursor mode/persona. It
selects named playbooks, requires their steps in the task list, and records
reasons for skipped steps. Large/cross-cutting work can route through
`figure-it-out`; standing programs have a separate Orchestrate route.

The feature route establishes system understanding, architecture, decomposition,
implementation, verification, reviewable commits, and PR opening. It requires
delegated implementation, while the coordinator keeps design, review, and
verification. Its throughput checkpoint distinguishes blocking work, independent
streams, shared mutable state, and the smallest safe decomposition.

Bug work reproduces the symptom, tests causal hypotheses, repairs it, and verifies
the original surface. Refactoring establishes prior behavior and checks
equivalence. Investigation is explicitly read-only and can end with a supported
answer. Do not read the generic claim that PR opening ends every other playbook
as overriding that explicit investigation boundary.

`figure-it-out` contributes a checkable done condition, proportionate rigor,
early investigation of risky unknowns, a baseline, small measured changes, and
honest verified/not-verified/inconclusive outcomes. Many of those procedures
already belong to our specialists; work-mode should coordinate them.

Its normal PR route opens ready PRs and does not automatically begin babysitting;
documented autopilot routes have exceptions. Babysitting distinguishes check,
threads-only, background, and drive; drive stops at merge-ready, with shipping
separate. These endpoints differ from the local PR contracts.

Adaptation decision proposed by the research: derive the routing/composition
ideas rather than wrap poteto-mode wholesale. Its mandatory feature delegation,
Cursor-specific primitives, model configuration, external actions, Git recovery
practices, and delivery defaults require changes across the procedure.

### Compound Engineering: strongest composition reference

Repository: `EveryInc/compound-engineering-plugin`
SSH remote: `git@github.com:EveryInc/compound-engineering-plugin.git`
Reviewed commit: `efcb657d9a5733ccc154c36cc7d3d78b4136eb23`

- https://github.com/EveryInc/compound-engineering-plugin/blob/efcb657d9a5733ccc154c36cc7d3d78b4136eb23/skills/lfg/SKILL.md
- https://github.com/EveryInc/compound-engineering-plugin/blob/efcb657d9a5733ccc154c36cc7d3d78b4136eb23/skills/lfg/references/intake.md
- https://github.com/EveryInc/compound-engineering-plugin/blob/efcb657d9a5733ccc154c36cc7d3d78b4136eb23/skills/lfg/references/work-return.md
- https://github.com/EveryInc/compound-engineering-plugin/blob/efcb657d9a5733ccc154c36cc7d3d78b4136eb23/skills/ce-work/SKILL.md
- https://github.com/EveryInc/compound-engineering-plugin/blob/efcb657d9a5733ccc154c36cc7d3d78b4136eb23/skills/ce-work/references/return-to-caller.md

`lfg` is the outer coordinator for an explicit autonomous end-to-end request.
It routes an existing plan, a concrete bug, an unsettled judgment, ambiguous
product shape, and a non-code outcome differently. A fixed return from `ce-debug`
already constitutes implementation; it does not run the feature executor again.
Code delivery normally ends at an open PR with CI decided, not a merge or the
local `pr-followup` endpoint. Non-code routes can finish with their owner's result.

`ce-work` implements a plan/spec or clear request. Its return-to-caller mode
performs implementation and local verification, including canonical unit commits,
then returns structured evidence. It leaves final review/publication/CI to the
caller. The documented return ends the child skill, not the enclosing turn.
Resume logic checks existing work and fills evidence gaps without reimplementing.

Useful transfer: explicit input/return contracts, one continuation owner, and
recognition of completed work. Adapt its broad autonomy, fallback/model carriers,
fixed code-delivery tail, and host-specific mechanisms to the local owners.

### Matt Pocock: concise execution and dependency-ready tickets

Repository: `mattpocock/skills`
SSH remote: `git@github.com:mattpocock/skills.git`
Reviewed commit: `7a030a8b0dcaa601bb0dda9aaf174affb3d61145`

- https://github.com/mattpocock/skills/blob/7a030a8b0dcaa601bb0dda9aaf174affb3d61145/skills/engineering/implement/SKILL.md
- https://github.com/mattpocock/skills/blob/7a030a8b0dcaa601bb0dda9aaf174affb3d61145/skills/engineering/implement-spec/SKILL.md

`implement` is a short recipe: implement the supplied scope, use TDD where
appropriate, run targeted checks and the full suite at the end, review, and
commit. It does not itself require PR publication.

`implement-spec` coordinates ready tickets according to dependencies. Implementers
use separate worktrees/branches, and a merger integrates them into one integration
branch. PR creation is conditional on the tracker/user workflow; it can create a
draft after the first merge and ready it after the complete scope lands.

Useful transfer: a direct route for well-defined work and explicit readiness.
Preserve our task-breakdown and per-PR review boundaries; importing one large
integration PR indiscriminately could undo them. `wizard` builds human-only
manual procedure scripts; it is not this repository's general task router.

### Superpowers: execution variants and resumption records

Repository: `obra/superpowers`
SSH remote: `git@github.com:obra/superpowers.git`
Reviewed commit: `8ca22dba9a94f28898bbce59f2537ff4d87c747d`

- https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/using-superpowers/SKILL.md
- https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/executing-plans/SKILL.md
- https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/subagent-driven-development/SKILL.md
- https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/finishing-a-development-branch/SKILL.md

It offers inline execution and subagent-driven execution. The latter uses fresh
implementers and task review; both maintain a task ledger and end with a fresh
whole-change review. At this revision the subagent path does not permit
concurrent implementers; do not equate it with unrestricted parallel execution.

Useful transfer: explicit task state, decisions, resumption, and review against
the actual change. Its broad skill-activation policy, approval gates, mandatory
integration menu, and capped review loops need independent assessment rather
than direct adoption. A round limit does not prove a surviving defect resolved.

### Gstack: plan-review orchestration and evidence freshness

Repository: `garrytan/gstack`
SSH remote: `git@github.com:garrytan/gstack.git`
Reviewed commit: `c285d88b90d39116ccfa2b901f80ea0fce0b26eb`

- https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/autoplan/SKILL.md
- https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/autoplan/sections/phase-close.md

`autoplan` coordinates plan reviews: product/scope, conditional design and developer
experience, then engineering last. It closes phases only after required review
results and accepted changes are reconciled, and retains a final approval gate.
It does not implement the software itself.

Useful transfer: evidence must correspond to the amended input; skipped,
unavailable, and completed phases differ. Hashes or saved reports alone do not
prove that a reviewer consumed the final changes. Keep actual verification rules
with `verify`; do not import a fixed executive-review lineup for every task.

### GSD 2: runtime-backed state, not just a skill

Repository: `gsd-build/gsd-2`
SSH remote: `git@github.com:gsd-build/gsd-2.git`
Reviewed commit: `33c00aaffa56e5d394bccce1c8df59fb842e84c5`

- https://github.com/gsd-build/gsd-2/blob/33c00aaffa56e5d394bccce1c8df59fb842e84c5/docs/user-docs/auto-mode.md
- https://github.com/gsd-build/gsd-2/blob/33c00aaffa56e5d394bccce1c8df59fb842e84c5/src/resources/GSD-WORKFLOW.md

Auto mode describes a runtime with SQLite authority, fresh execution contexts,
dispatch guards, and verification before closeout. Its portable/manual workflow
document describes a different layer with file-based records. Do not conflate
their storage authority or claim those runtime guarantees for a Markdown skill.

Useful transfer: preserve current state, evidence, decisions, and the next action;
refine later work when it is ready. Building an equivalent runtime is outside v1.

### Matthew Blode: a specialized delivery endpoint

Repository: `mblode/agent-skills`
SSH remote: `git@github.com:mblode/agent-skills.git`
Reviewed commit: `cef4cfa837ca41b50d19f54551a3939ed7460434`

- https://github.com/mblode/agent-skills/blob/cef4cfa837ca41b50d19f54551a3939ed7460434/skills/autoship/SKILL.md

`autoship` is a changesets/npm release workflow, with intent-specific routes and
an endpoint checked against the published registry result. It is not a general
feature coordinator. Its transferable idea is checking the requested final
artifact rather than stopping at an intermediate green CI result.

## 9. Independent consultations and their reconciliation

The source comparison used separate initial contexts, the same common brief,
and a frozen set of upstream files. Reviewers were asked for concrete gaps,
conflicts, transferable ideas, and limitations without a supplied preferred
verdict. Neither was asked to implement work-mode or execute donor workflows.

- Codex profile: `gpt-6-astra`, reasoning effort `max`.
  Native consultation name: `/root/work_mode_astra_sources`.
- Claude profile: provider `claudeAgent`, model `claude-fable-5-1`, effort `max`.
  T3 task ID:
  `node:delegated-task:command%3Amcp%3A09faa9e0-a759-4aec-af4a-c75e3176cb7e%3Adelegate-task%3Awork-mode-source-fable-v1-20261006`.

Both completed. These identifiers are historical evidence pointers, not a
promise that another thread or host can retrieve their private run records.

Material findings adopted in the comparison:

1. Own route selection, continuation, and task state in work-mode; keep specialist
   procedures with their existing owners.
2. Carry the requested endpoint through nested callers, especially publication
   and follow-up, to avoid early stops or duplicate loops.
3. Carry evidence and artifact identity across phases and invalidate only the
   evidence affected by changed inputs.
4. Preserve a useful next action and decision record for resumption without
   building a GSD-like runtime.
5. Retain a direct path for settled small work and the ticket-start event without
   a PR.

Behavior to exclude from wholesale adoption or avoid during local composition,
including the later explicit-cap correction:

- Mandatory feature subagents, fixed model rosters, and Cursor-only commands.
- Blanket external-write authority or additional universal approval ceremonies.
- Ready-only PR creation and merge-ready as the local Drive stopping point.
- A new default PR line ceiling, duplicated cap checks, or combining all tickets
  into a large integration PR regardless of the review boundary.
- Runtime guarantees, universal watchers, or autonomous background scheduling
  represented as if skill prose alone implemented them.
- Turning a review-round limit or an old completion trail into current proof.

One reviewer highlighted the tension between pstack's broad PR-ending statement
and its read-only investigation route. The comparison follows the explicit route
boundary and carries this as a reason to define endpoints clearly locally.

Scope limit: the shared primary set covered `ce-work`; the outer `lfg` package
was discovered afterward and inspected by the coordinator. Do not claim both
independent reviewers assessed the later LFG material. No work-mode candidate
existed for those consultations, so they do not satisfy the candidate review
required before finalizing the new skill.

The original frozen set contained 96 Markdown files; 11 later LFG files were
captured separately. Their 107 hashes were checked successfully against the two
manifests before cleanup. The scratch clones, extracted sources, manifests, and
common review brief under `.tmp/work-mode-research/` were removed after the
comparison. They are not pickup dependencies. Recover source content from the
immutable links/SSH remotes above. No permanent work-mode comparison report was
committed; the essential conclusions are preserved in this document.

## 10. Decisions to resolve while authoring

These are implementation choices, not reasons to reopen the user's two objectives
or ask for permission before every phase.

1. **Activation and endpoint:** make the description distinguish coordination from
   direct specialist requests. Determine the endpoint from the active request and
   standing rules; ask only if an unresolved distinction materially changes scope.
2. **Review policy:** reuse the existing review owner and project requirements.
   Decide when independent review adds value without importing an unconditional
   multi-agent requirement or suppressing required review.
3. **Return contract:** determine whether existing specialist modes suffice. Add
   only a narrow, tested change to a collaborator if composition genuinely needs
   it; preserve standalone behavior and existing descriptions.
4. **State:** use the existing task/plan record and a small continuation record
   where needed. Resolve its lifetime and transfer explicitly. Avoid inventing a
   schema or permanent script unless there is a concrete recurring need.
5. **Unavailable dependencies:** distinguish optional help from a required phase.
   Run useful supported work and report the exact missing capability. Never claim
   an absent specialist was invoked or bypass its required result silently.
6. **Scope growth:** pass oversized or newly dependent work back to the responsible
   planning/decomposition owner. Keep already-authorized ready work moving without
   becoming a program scheduler or silently dropping blocked requirements.

## 11. Suggested implementation sequence and artifacts

1. Recheck branch, HEAD, dirty state, effective instructions, and installed skill
   identities. Preserve other agents' work. No new worktree is required merely
   because this is a handoff; use the current host and `worktrunk` if a change is
   needed.
2. Read the authoring owners and relevant local contracts. Extract a compact
   confirmed/proposed/unresolved contract from this document. Identify positive
   activation, near misses, endpoints, and semantic regression cases before drafting.
3. Reopen the selected pinned donor instructions and licenses. Record why a small
   derivation is preferable to an unchanged installation or thin wrapper. Research
   candidates that contribute nothing need not become active provenance feeds.
4. Create `work-mode/SKILL.md`, with a short activation description and a body
   centered on inputs, routing, phase completion, continuation, and recovery.
   Keep substantial route-specific detail in conditional references only if it
   earns that split. Do not embed machine-local paths or host-specific model IDs.
5. Add `work-mode/origin.txt` using the repository's current provenance format.
   Separate actual external inspiration from local runtime dependencies. Retain
   applicable license notices in the package; inspect the source license rather
   than assuming all donor files have identical terms.
6. Review a frozen candidate independently with the current Codex Astra Max and
   Claude Fable Max profiles required by `agent-instructions`. Resolve current
   IDs and effort from the live catalog, keep first contexts independent, retain
   actual run evidence, and reconcile material findings. Reconsult affected
   meaning after material revisions. Do not treat the old source reviews as this
   candidate review.
7. Run proportionate behavioral and packaging checks from section 12. Fix observed
   failures at their actual owner and rerun affected and nearby regression cases.
8. Integrate the finished package into `README.md` and the Engineering grouping in
   `skills.sh.json`, following their existing conventions. Update the atlas's
   targeted package inventory and source-adoption records if needed for consistent
   repository integration; preserve unrelated historical assessments and overlays.
9. Run applicable checks, report exact commands and limits, and use `commit` for
   completed atomic boundaries on the work branch under current instructions.
   Source files saved in the repo are distinct from globally installed skills.

Expected deliverables are the skill package, accurate provenance/notices,
appropriate discovery/registry updates, and retained evidence for the tested
behavior. A source-comparison report and a validation record can follow existing
`reports/skill-atlas/` conventions if useful; their exact names are not fixed.
Do not generate a large report merely to match another report's size.

The atlas consists of `reports/skill-atlas/sources.json`, its exact JavaScript
mirror `reports/skill-atlas/catalog.js`, `app.js`, `index.html`, and the existing
stylesheet. If changed, preserve the mirror relationship and relevant asset
cache key, and test the affected UI paths. The current inventory has a pending
work-mode entry; mark only actually completed incorporation. An inspected source
is not automatically an adopted source. Do not turn the user's chat comparison
request into another HTML comparison deliverable.

Installation into global catalogs, changes to dotfiles, PR publication, remote
pushes, unrelated skill upgrades, and live workflow trials retain their separate
authorization. A work-mode implementation does not require any of them by default.

## 12. Validation contract for the future implementation

Read `agent-instructions/references/evaluation.md`, `skills.md`, `reuse.md`, and
`hosts.md` before deciding which claims the tests can establish. The following
cases are proposed from the contract; they have not been executed.

### Behavioral cases

Cover the material branches and failure boundaries, combining cases where that
keeps the evaluation small without hiding a distinction:

1. **Small ready change:** finish a concrete bounded task without manufacturing
   a direction map, elaborate plan, or unrelated specialists. Observe artifacts,
   checks, and continuation rather than a narrated list of skill names.
2. **Ticket without PR:** with a supplied valid tracker policy, implementation
   start reaches the configured work-started handler. A paired planning-only
   request performs no transition. Use an isolated adapter/fixture for writes.
3. **Ready vertical slice:** implement one statistics card with required real
   data behavior and tests; retain its acceptance contract and small review
   boundary instead of selecting the entire dashboard.
4. **Bug repair:** observe the original failure, a supported correction, and the
   original reproduction after repair. A diagnosis-only near miss preserves
   product files. A fixed child return does not trigger duplicate implementation.
5. **Uncertain direction:** route the connected question to its owner; preserve
   a consequential unresolved choice as blocked rather than inventing a contract.
   Continue unrelated authorized work when available.
6. **Explicit numeric cap:** an over-cap or unavailable diff blocks capped
   publication and routes revision to its owner. A changed base/head invalidates
   the prior measurement. A nearby case with no explicit cap does not acquire an
   invented 5,000-line prohibition.
7. **Child return and continuation:** after a successful implementation/verification
   return, complete the remaining requested phases. A failed or incomplete return
   must not pass solely because an output file exists.
8. **Read-only boundaries:** review-only, planning-only, research-only, and
   verification-only requests reach their actual endpoint without unauthorized
   product edits, new tickets, commits, PRs, or deployment.
9. **Review repair:** a supported finding returns to the implementation owner,
   is addressed within authority, and invalidated checks run again. A remaining
   supported failure stays visible rather than becoming success after a round cap.
10. **Evidence freshness:** a later relevant edit or changed input prevents reuse
    of an earlier passing result. Unaffected evidence can remain valid; do not
    require unrelated reruns merely because a new message arrived.
11. **Missing dependency:** report a genuinely required unavailable owner/tool and
    preserve useful completed preparation. Optional support absence does not become
    a blanket stop, and a required missing check never becomes a pass.
12. **PR composition:** default draft creation continues into the existing Drive
    owner exactly once. Explicit create-only ends after verified publication;
    keep-draft preserves the draft while allowing the authorized Drive work.
13. **Watch and resume:** yield to a supported host watch with retained state,
    resume on an event, refresh the revision, and avoid duplicate publication,
    tracker transitions, or follow-up loops. A missing watch is an explicit
    coverage limit, not a promise of background monitoring.
14. **Scope and integration:** a large request goes through appropriate delivery
    decomposition; independent units are not forced into a stack. A staged
    prerequisite reports honest intermediate verification limits and the combined
    capability has a specified integration check.
15. **Resumption:** existing completed work is inspected and reused, remaining
    evidence is gathered, and changed premises reopen only affected decisions.
    A stale record cannot substitute for the current artifact or remote state.
16. **Near-miss activation and portability:** a direct question or explicitly
    invoked specialist works without a mandatory work-mode wrapper; the packaged
    skill can be read from another working directory and account layout.

Use matched baseline/candidate runs with the same model, effort, tools, fixtures,
authority, and outputs. Keep expectations with the evaluator, reserve a fresh
case, and record real actions/results. A candidate rerun after fixing a reserved
failure makes that case a regression case, not still-unseen evidence.

Use isolated fixtures or fakes for external effects unless the user explicitly
authorizes live execution. Tool-free reasoning trials can assess supplied-context
decisions but cannot prove tool execution, network behavior, installation, or
implicit host selection. Report the distinction. If both arms pass, report that
result without claiming a measured improvement.

### Structure and integration checks

- Frontmatter/name/description validity and positive versus near-miss selection.
- All package-relative links and symlink targets remain inside the portable
  package; local collaborator names resolve as declared.
- Copy only the package to a neutral location with symlinks preserved and read
  required resources from another working directory with the original package
  unavailable. State the platforms/account layouts actually tested.
- `origin.txt` parses under its actual format, uses exact verified commits, and
  distinguishes external sources, local dependencies, and rejected candidates.
- README and registry agree with the actual package name and capability.
- If the atlas changes: JSON validity, `catalog.js` mirror equality, relevant
  inventory hashes/counts, source links, filters/search, and nearby unchanged UI.
- Behavioral verification, any applicable build/compile step, and a broader
  smoke path follow the effective repository rules. Do not substitute unrelated
  passing checks for work-mode execution evidence or claim a build that did not run.

Existing commands/examples for relevant files and helpers are:

```sh
node --check reports/skill-atlas/app.js
node --check reports/skill-atlas/catalog.js
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s review-code-changes/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s verification-authoring/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s report-work-activity/tests -v
```

These are existing syntax/helper checks, not a work-mode test suite or a claim
they are all required for a Markdown-only change. Select applicable checks and
the meaningful smoke path from the actual diff. Fish supplies the user's tool
PATH; check it before concluding a runtime is unavailable. An older default
Python in earlier sessions lacked `tomllib`, while Fish resolved a newer Python.

Retain case inputs, candidate identity/hashes, actual model/effort, artifacts,
action traces, failures, dispositions, and verification limits in the chosen
evidence record. A successful consultation or parser check does not prove the
coordinator works in an agent host.

## 13. Local evidence and reading map

The following artifacts exist in the exporting checkout. Read the relevant
record before extending a historical claim; the export did not rerun its tests.

- `README.md`: current user-facing package responsibilities and standalone use.
- `skills.sh.json`: current grouping/discovery registry.
- `HANDOFF.md`: earlier collection, atlas, and authoring context; chronology caveats
  in section 3 apply.
- `HANDOFF-QA.md`: separate pending QA and e2e installation stream.
- `agent-instructions/SKILL.md`: current instruction authoring and dual-review owner.
- `agent-instructions/references/writing.md`: instruction wording.
- `agent-instructions/references/skills.md`: activation, composition, and packaging.
- `agent-instructions/references/reuse.md`: install/wrap/derive/create decision.
- `agent-instructions/references/hosts.md`: actual host metadata and invocation.
- `agent-instructions/references/evaluation.md`: behavioral evidence requirements.
- `agent-instructions/references/upstream-updates.md`: provenance and maintenance.
- `reports/skill-atlas/planning-validation.json`: historical planning validation.
- `reports/skill-atlas/wayfinder-rewrite-validation.json`: historical direction work.
- `reports/skill-atlas/task-breakdown-validation.json`: initial decomposition checks.
- `reports/skill-atlas/task-breakdown-refinements-validation.json`: later context,
  risk, and progressive-detail checks.
- `reports/skill-atlas/task-breakdown-review-budget-validation.json`: explicit-cap
  correction; important when old evidence assumes a default number.
- `reports/skill-atlas/issue-workflow-start-validation.json`: implementation-start
  activation regression and its correction.
- `reports/skill-atlas/pr-size-owner-validation.json`: shared cap-check ownership.
- `reports/skill-atlas/pr-feedback-validation.json`: later workflow/inventory work.
- `reports/pr-workflows-validation.json`: historical PR ownership checks.
- `reports/verification-validation.json`: historical verification checks.
- `reports/review-code-changes-delegation-validation.json`: scoped review delegation.

No old atlas server or Tailscale URL is required for this task. If visual atlas
verification becomes necessary, establish current service state rather than
assuming the historical preview is still running. In this T3 environment, use its
collaborative preview tools when available. Remote fleet operations retain the
`fleet` skill's current requirements.

## 14. Export verification, access, and next result

The export checked `git status --short --branch`,
`git rev-parse --show-toplevel HEAD`, `git log -8 --oneline`, and the relevant
`git show --stat` output. It read the local contracts described above, confirmed
the pending atlas entry and absent work-mode package, and checked that the chosen
handoff destination is ignored with:

```sh
git check-ignore .tmp/work-mode-handoff/HANDOFF-WORK-MODE.md
```

The saved document was read back in full. A one-off Python reference check
confirmed 47 unique local files exist, resolving short filenames in their stated
directory context. The proposed work-mode package files and the explicitly absent
optional machine-local instructions were kept separate from existing artifacts.
The 24 upstream links use full immutable commit IDs; their network availability
was not rechecked for this export. No behavioral tests or historical suites were
rerun merely to write the handoff. A final Git status check retained the clean
tracked worktree and index.

The file is retained at:

`/Users/luisurrutia/.t3/worktrees/skills/t3code-767d9f53/.tmp/work-mode-handoff/HANDOFF-WORK-MODE.md`

It is local and ignored by Git. Transfer this file's content together with access
to the relevant checkout when handing off to another machine/thread. Do not delete
it before pickup; a new clone will not contain it. The immutable source URLs
remain usable without the deleted research scratch, subject to the recipient's
actual network access.

The expected next substantive result is an implemented and validated work-mode
package with current-source ownership preserved, or an exact blocker with useful
independent work retained. This document preserves the context needed to start;
it does not assert that the future skill, host integration, or any live delivery
workflow has already been tested.
