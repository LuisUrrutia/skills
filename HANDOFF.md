# Handoff: continue building the development skill collection

Context captured on 2026-10-04. This is continuation context, not a new source of
operating rules or authorization. Current user instructions, applicable project
rules, and freshly verified repository state govern the next session.

## Resume here

Continue selecting, creating, and refining focused skills before composing the
larger development workflow. The user has not selected the next skill after the
communication/documentation work. The future coordinator is called `work-mode`
in the atlas; it has **not been created**.

Start with [README.md](README.md) and the current
[atlas data](reports/skill-atlas/sources.json), especially `repositoryInventory`,
`sourceProgress`, and the current assessments. Then agree on the next focused
capability with the user. The original request still has uncovered React,
frontend-design, testing, and performance interests. A React specialist set is a
reasonable proposed next topic, not a user-approved implementation decision.
Planning is another recorded candidate, with Matthew Blode, Addy Osmani and
Compound Engineering sources already assessed in the atlas.

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
| Checkout | `/Users/luisurrutia/.t3/worktrees/skills/t3code-6f322d8f` |
| Branch | `t3code/curate-agent-workflow-skills` |
| Implementation baseline before this handoff | `0547c6db49b7934f8826dbdfaf4825d46471e3a3` |
| Git remote | `git@github.com:LuisUrrutia/skills.git` |
| Index before this export | Empty |
| Pre-existing worktree change | Deletion of `walkthrough/SKILL.md`; preserve it outside this handoff and unrelated commits |
| Shared editing window | All announced owners released README, atlas and staging after their verified commits; no active owner was reported at capture |

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

The atlas currently has **33 entries**, including the deprecated activity alias.
This is repository presence, not proof of installation, automatic selection or
production effectiveness. [README.md](README.md) describes the capabilities;
the entrypoint for a named package is `<name>/SKILL.md`.

| Area | Repository entries |
| --- | --- |
| Authoring and discovery | `agent-instructions`, `create-project-instructions`, `workflow-to-skill` |
| Understanding and design | `how`, `why`, `analyze-change-effects`, `compare-solutions`, `prototype`, `design-code-structure` |
| Implementation and domain rules | `debug`, `tdd`, `error-handling`, `accessibility`, `typescript-best-practices` |
| Verification and review | `verification-authoring`, `verify`, `simplify-code`, `review-code-changes` |
| Git and delivery | `worktrunk`, `commit`, `pr`, `pr-followup`, `stacked-pr`, `github-actions`, `ci-cd-automation` |
| Communication and continuity | `communicate-clearly`, `write-documentation`, `handoff`, `report-work-activity`, `daily-meeting-update` (deprecated alias) |
| Other retained personal capabilities | `article-processing`, `youtube-processing`, `people-memory` |

`work-mode` remains the future coordinator. `teach` is an optional future skill.
The personal capabilities do not all belong in a coding workflow.

## Decisions that must survive

- **Clear names.** `arena` became `compare-solutions`; `blast-radius` became
  `analyze-change-effects`; `architecture` became `design-code-structure`;
  `deslop` became `simplify-code`; `review-audit` became `review-code-changes`.
  The last name is the repository successor; a host may still expose the old
  installed skill.
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
- **Communication is not a teaching course.** `how` uses limited clarity guidance
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
progress is **128 ready, 44 pending, 48 optional, 43 not selected**. These are
source decisions, not counts of installed skills.

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

Use pinned URLs and provenance from the relevant package or report for claims
about what was actually reviewed. Current main-branch contents can differ.

## Recent completed work and evidence

These are existing results, not tests rerun while writing this handoff.

| Commit | Completed boundary | Evidence and limits |
| --- | --- | --- |
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

The next skill has not been chosen. The atlas retains source candidates for
React practices/composition/testing, frontend design, measured performance,
planning, security, observability and migrations. These are proposals of varying
priority, not authorization to build them all. `teach` remains optional.

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

The preview was used at http://localhost:8765/ and the recent section at
http://localhost:8765/#dyl-review-adoption. It is machine-local and may no longer
be running on pickup. If it is not running and port 8765 is available, start the
existing static atlas from the checkout root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory reports/skill-atlas
```

The command's options were checked with `python3 -m http.server --help`; no server
was started for this handoff. Preserve `.tmp/activity-preview`, an intentionally
retained synthetic demo used by the activity report's Quick command. Earlier
research scratch, including the dyl adoption fixtures, was removed after its
relevant inputs and outputs were retained in permanent reports. Do not rely on
old scratch paths still existing.

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

For this export, verification is limited to reading back the document, checking
its referenced local artifacts, comparing names/counts with the current atlas,
and preserving the pre-existing Git state outside `HANDOFF.md`. No skill
behavior, host activation, external service or historical test suite is rerun
merely to write continuation context.
