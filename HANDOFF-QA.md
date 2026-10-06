# QA test authoring: continuation

## Next task

Develop a workflow that turns a ticket or an existing feature into useful QA
cases and, when requested, executable tests. Use that contract to create a
dedicated local skill based on `verify` and the project's verification recipe.
Add installation of tester-army's upstream `e2e` skill to dotfiles unchanged.
The current task prepares this handoff; QA skill creation and the dotfiles
installation change remain pending.

Case design and local skill drafting can proceed independently. Complete the
dotfiles installation before validating execution through the installed e2e skill.

Read the target repository's current instructions and state before implementation.
This document carries context, not new authority beyond the user's request.

## Confirmed user choices

- Accept a ticket or a feature as input, including existing functionality with
  no useful tests. Test generation must not depend on having a recent code diff.
- Build a dedicated QA test-authoring skill using `verify` as the foundation.
- Support https://tester.army/e2e and https://e2e.tester.army/docs.
- Install https://github.com/tester-army/e2e/tree/main/skills/e2e through dotfiles
  without modifying the upstream skill or its bundled references.
- Otherwise follow the target repository's testing convention, generally
  Playwright. Installing the global skill does not migrate existing test suites.
- Playwright MCP configuration is a later task. Do not bundle it into this
  installation or assume it is already available.
- Write repository artifacts in English. Discuss the work with Luis in Spanish.

## Proposed responsibility split

The final local skill name and packaging have not been chosen. `qa-test-authoring`
is a candidate name, not a registered dependency.

| Owner | Responsibility |
| --- | --- |
| Future QA authoring skill | Turn requirements and coverage gaps into cases; create or extend tests in the selected project framework when authorized. |
| Upstream `e2e` skill | Own e2e-specific setup, test APIs, execution, reports, and debugging. Keep this package unchanged. |
| `verify` | Judge completion from current execution evidence, real entry points and resulting effects; retain failed, blocked, skipped and unrun checks honestly. Verification alone does not authorize writing tests or product repairs. |
| Project `verify-<app>` | Own concrete launch, doctor, drive, evidence and cleanup procedures. |
| `verification-authoring` | Create or maintain a missing or stale project verification recipe when that work is requested. Its absence need not prevent drafting useful cases. |
| `tdd` | Own the red/green implementation workflow when implementing behavior with TDD. QA authoring must also work for already implemented features. |
| `planning` | Preserve acceptance scenarios and their relationship to executable work. |

The user approved a small `planning` improvement in this task: each proposed
test identifies a regression and a gap in existing coverage; extend an existing
test of that contract when this avoids a near-duplicate. Carry that decision
into the QA workflow without copying another skill's whole procedure.

## Candidate workflow to validate

1. Read the ticket, acceptance criteria, supplied plan and relevant product
   contract. For a feature without a ticket, inspect its real entry points,
   callers, documentation and existing tests. Distinguish observed behavior from
   the intended contract; do not bless a defect merely because it exists today.
2. Inventory relevant coverage and the project's commands, fixtures and test
   conventions. Identify missing behavior, not a target number of tests.
3. Derive cases with a requirement/source, preconditions and data, action,
   independently justified expected result, and relevant final state or effect.
   Include failure, permission, boundary, persistence, retry or concurrency cases
   when the contract makes them material. Record consequential unknowns instead
   of inventing expected behavior. Ask only for choices that evidence cannot settle.
4. Show which existing case to reuse or extend and what regression each new
   case catches. Keep enough traceability to carry every material acceptance
   criterion into implementation and verification, using project conventions.
5. Select the supported execution route. Use e2e for the requested e2e route;
   otherwise retain the repository's framework, commonly Playwright. A global
   skill's presence alone does not choose a project's framework. Do not introduce
   e2e or convert tests just because a feature lacks coverage.
6. For test-writing scope, create or extend maintainable tests and use the
   existing setup and cleanup boundaries. Use real behavior and an independent
   expectation; do not mock the behavior being claimed or expose production
   internals solely to satisfy the test.
7. Run within the requested scope, inspect results and artifacts, and use
   `verify` for the completion claim. Preserve product failures as findings;
   changing product behavior or weakening an assertion needs its own authority.

A request for cases alone ends with cases and open questions. A request to write
and run tests continues through those authorized steps without another routine
approval. Keep planned cases, committed tests and observed passes distinct.

## Upstream e2e findings

Inspected on 2026-10-06 at commit
`fd3a0c766b4d40c74fabdbc578e3832d80553bf9`:
https://github.com/tester-army/e2e/tree/fd3a0c766b4d40c74fabdbc578e3832d80553bf9/skills/e2e

This is an inspected candidate revision, not an installed or approved runtime pin.
Recheck the selected version and its compatibility before adoption.

- The package contains `SKILL.md` and eight references: setup, writing-tests,
  agent, running, explore, debugging, mcp and bug-bash. Install the whole package.
- e2e combines exact assertions and interactions with optional agent-driven
  goals. Web targets use its Playwright engine; mobile uses agent-device.
  Deterministic tests need no model; agent steps need configured model access.
- Its CLI runs tests and writes reports such as `.e2e/report.json`. MCP supplies
  live inspection; an MCP session is not a replacement for an executed test.
- The upstream description also triggers on broad end-to-end requests, and its
  workflow routes missing e2e config to setup. Exercise the local routing with
  a repository that uses plain Playwright so installation does not force a migration.
- `e2e init` can change project dependencies and MCP configuration. Installing
  only the global upstream skill is a separate operation; do not run init in
  dotfiles as a substitute for skill installation.
- The entrypoint also instructs agents to send `e2e feedback` upstream when the
  tool causes a problem. External reports remain subject to active user and host
  authorization; retain existing authority without adding a redundant gate.
  This instruction was read, not executed or verified as CLI behavior.

Primary documentation read:

- https://tester.army/e2e.md — the landing page's linked Markdown representation.
- https://e2e.tester.army/docs — framework and execution surfaces.
- https://e2e.tester.army/docs/quickstart — project setup and prerequisites.
- https://e2e.tester.army/docs/coding-agents — skill installation, MCP versus CLI,
  and report consumption.
- https://github.com/tester-army/e2e/blob/fd3a0c766b4d40c74fabdbc578e3832d80553bf9/skills/e2e/SKILL.md

No e2e runtime, model calls, MCP sessions or tests were executed in this task.
Only the entrypoint and selected reference material were inspected; execution
compatibility and the full upstream package still need validation.

## Dotfiles installation continuation

Local repository: `/Users/luisurrutia/.dotfiles`.
At inspection: branch `main`, revision
`bf778323b7287853e56e54383a4b03b6067b121e`, 13 commits behind its recorded
`origin/main`, with pre-existing edits in AI, bat, Claude, Fish, mise, SSH and
Vim configuration. Refresh this state before work; preserve those edits.

Read `AGENTS.md` there. The existing owner is `tools/skills/install.sh`:

- `GLOBAL_SKILL_GROUPS` declares source and selected skill names.
- It invokes the mise-managed skills installer non-interactively with `-g -y`.
- Current explicit agent targets are `opencode` and `claude-code`; inspect shared
  skill discovery and links before claiming availability in any other host.
- It separately installs Playwright CLI skills. Preserve that behavior.

The minimal expected addition is a source-group entry:

```text
git@github.com:tester-army/e2e.git|e2e
```

Use the existing installation mechanism and SSH Git transport. Preserve upstream
files byte-for-byte, including references; keep local policy in the local QA
skill or the appropriate project instructions. Inspect existing lock/update
behavior and record the actual installed revision and host discovery evidence.
Skill installation does not install a test framework into an application.

Extend `tools/skills/tests/install.sh` to cover the selected source, `--skill e2e`,
existing agent flags, noninteractive installation and preserved Playwright setup.
Run its behavioral checks and the applicable syntax/static/smoke gates required
by dotfiles. Those checks have not been run here because dotfiles was only read.
Resolve `agent-instructions` and `commit` by name where the receiving host makes
them available; installation mechanics remain owned by dotfiles.

## Choices to settle during continuation

- Select the local skill name and approved upstream revision using the existing
  package and update conventions; both are currently proposals, not installed state.
- The QA workflow owns framework selection. Decide whether project instructions
  or host selection configuration must also constrain direct requests that could
  activate upstream e2e automatically. Its broad description stays unchanged;
  test the chosen routing with a plain Playwright project before claiming it works.
- For a repository with no framework, use an explicitly requested compatible
  framework first. Otherwise investigate the project constraints and recommend
  a suitable choice. Ask only if an unresolved choice materially changes scope,
  runtime or dependencies and the request does not settle it. Missing coverage
  alone does not select or authorize a framework installation.

## Acceptance cases for the future skill

- A ticket with clear criteria and no tests yields grounded cases. When writing
  and running tests is authorized, also produce a test in the selected framework
  and run it, or state the exact execution prerequisite blocking the run.
- Existing tests already cover the contract: extend only a missing case and
  avoid adding duplicate tests merely to produce new files.
- A feature with no ticket: distinguish established behavior from an unresolved
  product decision; finish independent cases while the material question is open.
- For an authorized request to write and run tests in an e2e project: load the
  unchanged installed skill, write and execute a relevant test, and inspect
  current reports rather than accepting an agent's assurance.
- A plain Playwright project: preserve its fixtures, runner and conventions;
  do not require e2e or the future Playwright MCP to author and run existing tests.
- A requirement present in the ticket/plan but absent from the diff remains in
  the final verification scope. A changed contract invalidates affected old evidence.
- An observed failure or unavailable environment remains failed or blocked;
  no fabricated pass, arbitrary sleep, weakened expectation or silent product fix.

Use matched baseline/candidate trials and the independent model reviews required
by `agent-instructions` when creating the skill. No representative application,
ticket or runtime was supplied for this handoff; use isolated fixtures or a
subsequently provided project before claiming the workflow works.

## Local context and delivery

This document belongs to the skills checkout:
`/Users/luisurrutia/.t3/worktrees/skills/t3code-767d9f53`, branch
`luisurrutia/review-handoff-html-1`. The task started at
`aa5827cfad450c573b27cb913e0a6150a36903a3` with a clean index and worktree.
This task changes `planning` and adds this document; it does not implement the
QA skill, alter dotfiles, install e2e or configure MCPs.

Relevant existing artifacts, relative to this checkout:

- `planning/SKILL.md` and `planning/origin.txt`: accepted coverage rule and source.
- `verify/SKILL.md`: verification contract and routing.
- `verification-authoring/SKILL.md` and `verification-authoring/references/feature-map.md`:
  project verification recipes and requirement-to-proof mapping.
- `tdd/SKILL.md` and `tdd/references/test-design.md`: test boundaries and oracles.
- `error-handling/references/recovery.md`: partial effects, replay and recovery.
- `HANDOFF.md`: earlier skills/atlas context; this QA handoff preserves it.

The handoff is a repository file. No receiving session was launched and no
delivery outside this checkout was verified. Another machine needs this file
and the relevant repository revision; no temporary research clone is required.
