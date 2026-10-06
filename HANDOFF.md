# Handoff: continue building the development skill collection

Context refreshed on 2026-10-06. This is continuation context, not a new source of
operating rules or authorization. Current user instructions, applicable project
rules, and freshly verified repository state govern the next session.

## Resume here

`wayfinder` and `planning` now exist. Wayfinder resolves connected uncertainties
into a supported direction; planning turns a defined outcome into executable,
verifiable work. The latest request was to review the missing gstack repository
and add the findings here. That scoped review is recorded below; it did not change
either skill, install gstack, or add it to the atlas as an incorporated source.

The future coordinator is called `work-mode` in the atlas; it has **not been
created**. Continue selecting and refining focused capabilities before composing
that workflow. The gstack comparison is input to a later decision, not an approved
implementation backlog.

Start with [README.md](README.md) and the current
[atlas data](reports/skill-atlas/sources.json), especially `repositoryInventory`,
`sourceProgress`, and the current assessments. Then agree on the next focused
capability with the user. React practices/composition/testing and frontend design
remain candidate topics. Performance, observability, teaching and planning now
have local packages; assess any remaining source against those owners instead of
recreating them.

For the chosen capability, use the repository's
[agent-instructions](agent-instructions/SKILL.md). Read the actual source skill
and its relevant linked instructions, compare them with existing local owners,
and decide whether to retain, install, wrap, derive, combine, or create. Do not
assume every pending source needs a new package.

## What the user wants to achieve

The end goal is a workflow inspired primarily by pstack's `poteto-mode`: the user
can request work, and the agent selects the appropriate investigation, design,
implementation, verification, review, Git and PR steps. Worktree isolation should
be used when needed. The workflow should load domain guidance when the work
reaches that domain, such as React performance/composition or GitHub Actions.

The workflow should produce code and artifacts a human can review easily, then
support PR follow-up: inspect CI and every relevant feedback channel, evaluate
human and AI comments against the current code before acting, address justified
feedback, and handle base updates or conflicts within the authorized scope.
CodeRabbit and Greptile were examples, not exclusive integrations. Current Git,
publication, review and session-ownership rules remain authoritative.

The user values pstack highly and wants careful adaptation of its reasoning, not
an unexamined copy of its tools, model choices or mandatory steps. The original
priority was to establish a strong skill-authoring capability before building
the rest. That foundation now exists. The HTML atlas must explain each skill's
purpose, overlap, adaptation rationale, sources and actual incorporation status.

## Repository and collaboration state

| Item | Captured state |
| --- | --- |
| Checkout | `/Users/luisurrutia/.t3/worktrees/skills/t3code-767d9f53` |
| Branch | `luisurrutia/review-handoff-html-1` |
| Implementation baseline before this handoff refresh | `b4e780a5505807e5a181cf59671bc71b8af185f4` |
| Git remote | `git@github.com:LuisUrrutia/skills.git` |
| Index and tracked worktree before this refresh | Clean |
| Current edit boundary | `HANDOFF.md` only; preserve unrelated work if the state changes |

This document is a later, separate context artifact. Use `git log -1` and
`git status --short` for the receiving session's exact revision and residual
state; do not mistake the baseline above for a claim that HEAD never moved.

Previous agents serialized edits to `README.md`, `skills.sh.json`,
`reports/skill-atlas/index.html`, `sources.json`, `catalog.js`, `app.js`, and the
shared Git index. Keep that coordination if parallel work resumes. Package-only
changes and uniquely named research reports can proceed independently when their
boundaries do not overlap. The most recent owners committed and released their
work; do not resurrect the old handoff -> activity -> dyl -> retune queue.

The user's standing instructions require English repository artifacts and
commits, conversation in the user's current language (Spanish for the main
requests), SSH Git transport, intentional atomic commits on this work branch,
and preservation of other work. Fish carries
some tool configuration unavailable through the default shell. Read active
machine/project instructions on resume instead of copying this summary into a
new global policy. `~/.agents/AGENTS_LOCAL.md` was absent at capture. Session and
Orca ownership must be resolved from the receiving environment when applicable.

## Current capability inventory

The atlas currently has **42 entries**, including the deprecated activity alias.
This is repository presence, not proof of installation, automatic selection or
production effectiveness. [README.md](README.md) describes the capabilities;
the entrypoint for a named package is `<name>/SKILL.md`.

| Area | Repository entries |
| --- | --- |
| Authoring and discovery | `agent-instructions`, `create-project-instructions`, `workflow-to-skill` |
| Understanding, direction and design | `explain-code`, `explain-decisions`, `analyze-change-effects`, `compare-solutions`, `prototype`, `design-code-structure`, `wayfinder`, `planning` |
| Implementation and domain rules | `debug`, `tdd`, `error-handling`, `observability`, `performance-optimization`, `accessibility`, `typescript-best-practices`, `deprecate-and-remove` |
| Verification and review | `verification-authoring`, `verify`, `simplify-code`, `review-code-changes` |
| Git and delivery | `worktrunk`, `commit`, `pr`, `pr-followup`, `stacked-pr`, `github-actions`, `ci-cd-automation`, `issue-workflow` |
| Communication and continuity | `communicate-clearly`, `write-documentation`, `handoff`, `report-work-activity`, `comment-style`, `daily-meeting-update` (deprecated alias) |
| Teaching and learning | `teach`, `learning-plan` |
| Other retained personal capabilities | `article-processing`, `youtube-processing`, `people-memory` |

`work-mode` remains the future coordinator. Repository presence does not mean
every capability belongs in every coding workflow.

## Decisions that must survive

- **Clear names.** `arena` became `compare-solutions`; `blast-radius` became
  `analyze-change-effects`; `architecture` became `design-code-structure`;
  `deslop` became `simplify-code`; `review-audit` became `review-code-changes`.
  `how` and `why` are now `explain-code` and `explain-decisions`. A host may still
  expose an old installed name; resolve the repository and host separately.
- **Keep review and impact investigation distinct.** `review-code-changes`
  audits an implementation, another person's PR, a branch, commit, or local
  changes. `analyze-change-effects` investigates indirect consequences and the
  assumptions that determine whether other consumers break. They can support
  each other without becoming the same skill. Review itself remains read-only;
  feedback repairs belong to the authorized follow-up workflow.
- **Verification has two levels.** The user explicitly chose a common `verify`
  entrypoint plus project-local `verify-<app>` recipes. `verification-authoring`
  creates and maintains them using pstack's Launch, Doctor, Drive, Evidence,
  Cleanup and Helpers structure. Preserve actual execution evidence and
  unavailable checks; a screenshot or successful command alone is not a complete
  user-journey result.
- **Readable delivery.** `commit` and `pr` should help human reviewers. PRs should
  include real screenshots for visible changes when feasible and diagrams when
  they explain the change. Preserve repository conventions while allowing useful
  improvements. Attachment handling was explicitly researched and implemented;
  consult `pr` before replacing it with an improvised upload process.
- **Evidence before acting on feedback.** `pr-followup` covers human and bot
  review feedback, conversation comments and relevant CI output. It must assess
  claims before fixing them and distinguish fixed, checked, published, replied
  and resolved states. The active host's monitoring and authorization rules still
  apply.
- **Language-neutral simplification.** `simplify-code` is generic and should not
  accumulate language-specific code examples. Preserve necessary guards,
  comments explaining non-obvious constraints, error behavior and valid
  abstractions.
- **Communication is not a teaching course.** `explain-code` uses limited clarity guidance
  from teaching sources; the user did not want it dominated by `teach`.
  `communicate-clearly` now replaces `humanize`, preserving prose-pattern repair,
  fidelity and voice. `write-documentation` owns human-facing documentation;
  `agent-instructions` owns agent instruction authoring. Do not maintain two
  competing automatic prose owners during a future host migration.
- **Repeat reviews retain context and coverage.** The recent dyl-review adoption
  reconciles previous findings and skipped asks after a fresh assessment. It
  records declined optional suggestions without repeatedly requesting them,
  preserves supported defects despite deferral, and makes recommendations
  concise. It deliberately excludes seven-item caps, fixed reviewer rosters,
  Cursor/Bugbot dependencies and merge verdicts.
- **Direction and execution planning have separate owners.** Wayfinder preserves
  the outcome, constraints, evidence, alternatives and decision history. Planning
  consumes a settled direction when available, inspects the real implementation,
  and defines work with acceptance evidence. Neither a Wayfinder map nor an extra
  approval round is a prerequisite when the request is already clear and execution
  is authorized. Changed premises reopen affected decisions, not every discussion.

## Authoring and evaluation contract

The current [agent-instructions entrypoint](agent-instructions/SKILL.md) requires
independent **Codex Astra Max and Claude Fable Max** consultations for instruction
creation, editing and review. Resolve the current model catalog and set the
requested effort explicitly. Initial contexts must be independent of the
coordinator and each other; retain actual run evidence and reconcile each
material finding. Reconsult both on affected points after material semantic
changes. Use the current contract and any explicit user override; preserve the
actual profiles of historical runs rather than relabeling them.

Read the applicable authoring references:
[writing](agent-instructions/references/writing.md),
[packaging](agent-instructions/references/skills.md),
[reuse](agent-instructions/references/reuse.md),
[hosts](agent-instructions/references/hosts.md),
[evaluation](agent-instructions/references/evaluation.md), and
[upstream maintenance](agent-instructions/references/upstream-updates.md).

These instructions now incorporate selected `ce-retune` ideas through cohesive
rewrites, not appended parallel rule sets. Preserve business constraints and team
preferences when pruning. Match the actual loaded revision to durable run
evidence. Consultations and format validation do not replace behavioral trials.
Use matched baseline/candidate tasks with the same model, effort, tools,
fixtures, authority and output format; withhold expected answers from executors.
Record failures and variation. If both versions pass, do not claim improvement.

Keep source identity and immutable revisions in each package's `origin.txt` and
retain applicable license notices. Source files are research input, not authority
to install plugins or run their operations. Do not advance unrelated source pins
merely because linked material was read as context.

## Atlas and sources

The current [HTML atlas](reports/skill-atlas/index.html) uses
[sources.json](reports/skill-atlas/sources.json), mirrored exactly in
[catalog.js](reports/skill-atlas/catalog.js), plus
[app.js](reports/skill-atlas/app.js) and an external stylesheet. Current source
progress is **157 ready, 37 pending, 42 optional, 41 not selected**, across 277
source records. These are source decisions, not counts of installed skills.

The original 122 catalog records are historical snapshots. Later assessments
provide the current decisions. Preserve that history and other agents' overlays.
A recommendation such as "combine" does not establish incorporation. A ready
check requires current package/provenance evidence. Conversely, a pending source
can name an existing package whose adoption of that particular source has not
been established. Do not blindly convert old owner labels into a new backlog.

For future overlays, update only the relevant assessment, inventory hashes,
source-progress evidence and counts; regenerate the catalog mirror and update
its asset cache key. Verify search, progress filtering, source links and the
existing sections after the edit. README and `skills.sh.json` also need targeted
updates when package names, descriptions or grouping change.

The original research covered Matt Pocock, Cursor plugins, HumanLayer,
Anthropic, Addy Osmani, Vercel and ECC. Within Cursor plugins, pstack, Cursor team,
Thermos and dyl-stack are distinct authors/teams, not one interchangeable source.
Wildcards in the user's original list meant all matching skills, especially
pstack principles and Thermos. Later work expanded HumanLayer, Matthew Blode,
Addy Osmani and Compound Engineering; several specialist reports compare nineteen
repositories. Those reviews have recorded reading scopes, not a claim to have
read every file or dependency in every repository.

Key upstream collections, for fresh requested research rather than automatic
updates during resume:

- https://github.com/cursor/plugins
- https://github.com/mattpocock/skills
- https://github.com/humanlayer/skills
- https://github.com/mblode/agent-skills
- https://github.com/addyosmani/agent-skills
- https://github.com/EveryInc/compound-engineering-plugin
- https://github.com/anthropics/skills
- https://github.com/vercel-labs/agent-skills
- https://github.com/affaan-m/ECC
- https://github.com/obra/superpowers
- https://github.com/gsd-build/gsd-2
- https://github.com/garrytan/gstack

Use pinned URLs and provenance from the relevant package or report for claims
about what was actually reviewed. Current main-branch contents can differ.

## gstack review: findings and possible use

Reviewed on 2026-10-06 from Garry Tan's repository, cloned over SSH from
`git@github.com:garrytan/gstack.git`. The inspected `origin/main` revision was
`c285d88b90d39116ccfa2b901f80ea0fce0b26eb`. Its root license is MIT, copyright
2026 Garry Tan. This is an additional scoped review; it does not retroactively
expand the earlier nineteen-repository studies or establish incorporation.

The documented workflow runs through discovery, planning, implementation,
review, testing, delivery and reflection. Its useful connective mechanism is
explicit artifacts: discovery produces a design document for plan review;
engineering review produces a test plan for QA. `autoplan` orchestrates plan
reviews, not the entire development lifecycle. It orders CEO, applicable design
and developer-experience reviews, then engineering review against their amended
plan. These are documented contracts, not behavior verified by running gstack.

| Component | Useful mechanism | Local owner and assessment |
| --- | --- | --- |
| `office-hours` | Examine the actual problem and current workaround; adapt discovery to a startup or another kind of project; preserve the chosen direction, rejected approaches and document lineage. | `wayfinder` already covers outcome, evidence, alternatives, authority and changed premises. Keep discovery proportionate to the user's goal; commercial demand is not the test for every internal, learning or hobby project. |
| `plan-ceo-review` | Distinguish expanding, holding or reducing scope; reuse settled decisions and challenge them when premises change. | `wayfinder` already preserves scope and decision history. The four named modes are an upstream interface choice, not a missing local capability. |
| `plan-eng-review` | Connect realistic failures to handling, user-visible behavior and test coverage; pass the resulting test plan downstream. | `planning` and `verify` are the existing owners. Planning already links acceptance to observable scenarios and material failure behavior. A useful future test would check that verification actually consumes that contract. |
| `spec` | Read code before technical questions; make acceptance, dependencies, exclusions and recovery concrete enough for another implementer. | `planning` already covers these planning obligations; `issue-workflow` owns tracker delivery. Its issue-filing and optional worker-launch path is not a reason to add those actions to Wayfinder. |
| `autoplan` | Review the amended plan in dependency order; repeat affected reviews after changes; keep skipped, unavailable and completed reviews distinct. | A reference for future `work-mode`. The transferable concern is freshness of inputs and evidence, not a mandatory roster or identical phase sequence for every task. |

**Recommendation:** no immediate Wayfinder rewrite is justified by this reading.
Most relevant discovery mechanisms are already present. Before adopting anything,
use a concrete case to expose a gap in the planning-to-verification handoff or in
how a future coordinator invalidates reviews after the plan changes. Adapt the
smallest coherent mechanism that closes that gap; do not append a second discovery
checklist or create a package solely because gstack has a named role.

Do not carry over compulsory interview rounds, a minimum number of alternatives,
reopening settled work to satisfy a template, repeated approval gates, fixed score
thresholds, file-count or time-based scope heuristics, or mandatory review rosters.
The private gstack store, dual document writes, helper binaries and host-specific
launch commands support its own runtime; they are not dependencies of our skills.
Any later incorporation needs its own source attribution and applicable license
notice. No package origin or atlas adoption status changed in this review.

### Reading scope and immutable sources

The review read the complete `office-hours` entrypoint, its startup and builder
discovery sections, the `plan-eng-review` entrypoint, `autoplan`'s phase-close
section and the root license. It read selected portions of the other templates
and overview documentation. Primary references, with the relevant read ranges:

- Workflow overview, README lines 239–282:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/README.md#L239-L282
- Discovery entrypoint and its two mode sections, read in full:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/office-hours/SKILL.md.tmpl
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/office-hours/sections/phase-2a-startup-diagnostic.md.tmpl
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/office-hours/sections/phase-2b-builder-brainstorm.md.tmpl
- Design record and handoff, lines 1–180:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/office-hours/sections/design-and-handoff.md.tmpl#L1-L180
- Product/scope review, lines 58–100, 247–290 and 389–460:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/plan-ceo-review/SKILL.md.tmpl
- Engineering entrypoint in full; review sections lines 384–554:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/plan-eng-review/SKILL.md.tmpl
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/plan-eng-review/sections/review-sections.md.tmpl#L384-L554
- Specification, lines 81–195, 198–300 and 437–493:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/spec/SKILL.md.tmpl
- Review orchestration, lines 1–148 and 290–465; phase-close section in full:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/autoplan/SKILL.md.tmpl
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/autoplan/sections/phase-close.md.tmpl
- License:
  https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/LICENSE

This is a comparison of selected authoring templates, not a complete audit of
generated skills, shared preambles, helper implementations or linked review
phases. No gstack setup, skill execution, behavioral comparison, test suite or
independent model review ran for this research-only update. The immutable sources
above remain the recovery path after the temporary clone is removed.

## Recent completed work and evidence

These are existing results, not tests rerun while writing this handoff.

| Commit | Completed boundary | Evidence and limits |
| --- | --- | --- |
| `b4e780a` | Create `planning` for executable work, durable plans and work-unit boundaries; integrate the package into the atlas | [Planning source review](reports/skill-atlas/planning-source-review.json) and [final validation](reports/skill-atlas/planning-validation.json). Four bounded matched cases and recorded checks support the reported outcomes; global installation, implicit activation and network issue publication were not tested. |
| `b9e6f04` | Rewrite Wayfinder around evidence, real alternatives, a maintained decision map and planning readiness | [Wayfinder source review](reports/skill-atlas/wayfinder-source-review.json) and [rewrite validation](reports/skill-atlas/wayfinder-rewrite-validation.json). Nineteen repositories screened, fifty selected reading records, four incorporated sources, independent Astra Max/Fable Max review and four bounded matched cases. Final criteria passed; no general quality gain, interrupted-checkpoint durability or host activation claimed. |
| `5cc6610` | Create the original Wayfinder package | [Original validation](reports/skill-atlas/wayfinder-validation.json). Historical failures and corrections remain evidence; the later rewrite record owns the current assessment. |
| `0547c6d` | Replace `humanize` with `communicate-clearly`; add `write-documentation`; migrate named callers and registry; update README/atlas | [Communication validation](reports/skill-atlas/communication-validation.json) and [source review](reports/skill-atlas/communication-source-review.html). Both Max consultations closed. Six matched cases per arm and a final reserved rewrite pair passed; no measured quality gain or host activation claimed. |
| `63dbdf9` | Activity reports cover every configured `gh` profile | [Profile validation](reports/skill-atlas/report-work-activity-gh-profiles-validation.json). Four synthetic Luna executions and actual review profiles are retained; the default-host probe and live-auth behavior have stated limits. |
| `7f7a837` | Integrate retune ideas into authoring/evaluation guidance | [Retune validation](reports/skill-atlas/agent-instructions-retune-validation.json). Matched artifact checks, focused regressions, independent consultation and attribution/variation requirements. |
| `6d2d744` | Incorporate selected dyl-review guidance | [Dyl adoption](reports/skill-atlas/dyl-review-adoption.json). Four executor trials; baseline and candidate found the same two defects. The final boundary retained eight findings and handled declined optional feedback. Twelve helper tests, eleven smoke tests, compilation and format checks passed. Browser DOM checks passed; snapshots failed. |
| `5efcc19` | Replace the activity workflow; retain the deprecated alias and retire its old digest | [Activity research](reports/skill-atlas/report-work-activity-research.html) and [validation](reports/skill-atlas/report-work-activity-validation.json). Current contract covers multiple workstreams, current obligations and private evidence-backed HTML. |
| `ea8ccb3` | Create the portable handoff skill used for this export | [Handoff validation](reports/skill-atlas/handoff-implementation-validation.json). Document creation is separate from transfer, receipt or launching a receiving session. |

Earlier relevant records include [verification](reports/verification-validation.json),
[browser verification](reports/skill-atlas/verify-browser-validation.json),
[review delegation](reports/review-code-changes-delegation-validation.json),
[PR workflows](reports/pr-workflows-validation.json),
[PR attachments](reports/pr-attachments-validation.json),
[accessibility](reports/skill-atlas/accessibility-validation.json),
[TypeScript](reports/skill-atlas/typescript-best-practices-validation.json), and
[CI/CD](reports/skill-atlas/ci-cd-automation-validation.json). Read the relevant
record before extending a claimed capability; do not copy aggregate success
claims across unrelated skills.

## Remaining work and acceptance for the eventual coordinator

The next implementation after Wayfinder and planning has not been selected in
this request. React practices/composition/testing, frontend design and security
remain candidate topics. Other pending sources may improve existing owners rather
than justify new skills. The gstack opportunities above are proposals to evaluate,
not authorization to implement its pipeline or build every candidate.

Once the selected specialists and ownership boundaries are settled, design the
coordinator around phase inputs, selection conditions, responsible skills,
completion evidence and continuation. It should route differently for a simple
change, a bug, design uncertainty, React work and GitHub Actions work, and select
no specialist when none is needed. It should preserve caller authorization and
return from specialists to finish the remaining requested workflow. Specialists
own their procedures; the coordinator should not duplicate them.

An eventual workflow evaluation should observe real selection, handoffs and
continuation, including blocked or failed verification, changing PR heads and
unavailable dependencies where relevant. A list of skill names or a successful
instruction consultation is not proof that the workflow executes correctly.

## Local access, preview and verification on pickup

The handoff and linked reports are repository files. Transfer the checkout or
these artifacts together if moving to another machine; an absolute local path
does not make them remotely accessible. Installed skill catalogs can be stale:
this host still advertised legacy names during the work. Recent commits did not
perform global installation. PR/remote publication state was not rechecked for
this export, and exporting context does not request a push or PR.

The most recent Wayfinder preview was verified through Tailscale at
https://noir.tail3e9a72.ts.net:8765/#wayfinder, with the static server on
http://127.0.0.1:8765/. Availability was not rechecked for this documentation
update. Preserve `.tmp/atlas-tailnet-recovery`, which retains server recovery
state. The earlier foreground Tailscale serve command ended with `unexpected EOF`
when T3 restarted; do not treat that cancelled process as a live server.

If the local server is unavailable and port 8765 is free, its command from the
checkout root is:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory reports/skill-atlas
```

This command serves locally; it does not establish the Tailscale proxy. Verify
both before promising tailnet access. No server was started for this refresh.
The older `.tmp/activity-preview` demo is absent in this checkout. Earlier
research scratch, including the Wayfinder fixtures, was removed after its relevant
inputs and outputs were retained in permanent reports. Do not rely on old scratch
paths still existing.

For future changed-helper checks, existing commands include:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s review-code-changes/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s verification-authoring/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s report-work-activity/tests -v
node --check reports/skill-atlas/app.js
node --check reports/skill-atlas/catalog.js
```

Choose checks for the actual change and follow the current verification rules;
these examples are not a complete suite for every skill. Fish resolves the
configured Python, Node and uv commands. During earlier checks, the default
shell's Python lacked `tomllib` while the Fish-configured Python supported it.

For this refresh, verification is limited to reading back the document, checking
its referenced local artifacts, comparing names/counts with the current atlas,
and preserving the pre-existing Git state outside `HANDOFF.md`. No skill
behavior, host activation, external service or historical test suite is rerun
merely to write continuation context.
