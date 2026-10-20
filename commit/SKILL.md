---
name: commit
description: "Git commits: use for preparation, creation, message guidance, or requested pushes."
---

# Commit

Create verified Conventional Commits, one atomic boundary at a time, using the
existing checkout and branch. Ground state and completion claims in fresh Git
evidence, including claims from earlier assistant messages.

## Modes

Resolve authority from the active request, standing user instructions and
authorized caller. A commit request alone authorizes neither pushing nor PR work.

| Mode | Action |
| --- | --- |
| Commit | Commit after applicable checks pass |
| Commit-and-push | Verify all intended commits, then publish within existing authority |
| Proposal | Stage the boundary and propose its message without committing |
| Amend | Apply the [current-task conditions](references/hooks-and-amend.md#amend-an-existing-commit) before amending |
| Split | Repeat the complete workflow for every clear atomic intent |

Preparing, reviewing or suggesting a commit selects Proposal mode. For material
ambiguity in boundaries, order, grouping or authority, ask one concise question
with concrete options and a recommended default.

Each boundary ends `committed`, `amended`, `proposed`, `blocked` or `refused`.
Stop changing that boundary; after a verified commit or amendment, continue the
next clear boundary from a fresh baseline. `pushed` ends a published run.

## Resolve boundaries before writing

Inspect these conditions before staging; use existing authority and repository
evidence, asking only when they leave a material decision unresolved:

- Secret-looking paths/content: `.env*`, keys, certificates, tokens, credentials,
  databases and obvious secret names.
- Independent or out-of-scope concerns, including changes that cannot be
  described in one or two sentences.
- Ambiguous staged and unstaged edits in the same file.
- `main` or `master`, unless the user explicitly wants to commit there.
- Unrequested publication, destructive Git actions, out-of-scope dependency or
  package-manager changes, or an amendment outside the linked conditions.

Inspect generated files, dependencies, lockfiles and binaries; their presence or
size alone requires no approval. Treat existing staged entries as likely intent,
including them only when coherent with the request. Branch-history rewrites
belong to their authorized workflow.

## Workflow

### 1. Choose the boundary

Establish `HEAD` (or an unborn branch), branch, worktree/index state, recent message
style and changed paths:

```sh
git rev-parse HEAD
git branch --show-current
git status --short
git log --oneline -5
git diff --name-only
git diff --cached --name-only
```

Split by independently understandable intent and reversibility. Keep behavior,
regression tests and required schema/generated output together. Separate mechanical
cleanup when each part stays coherent. Order dependencies into working revisions,
explaining necessary dependencies in commit bodies. File types and arbitrary
line quotas do not define boundaries.

Continue when the repository state is known and one coherent, reviewable boundary
is selected; present an ambiguous boundary for the user's decision.

### 2. Inspect its diffs

Read `git diff -- <path>` and `git diff --cached -- <path>`. Account for every
hunk, including unstaged edits in staged files. Identify all excluded changes as
preserved work. Continue when every selected hunk is understood and every
pre-existing index entry has an explicit inclusion or preservation decision.

### 3. Stage intentionally

Stage only selected files or hunks; patch-stage clear boundaries automatically.
Ask before staging ambiguous hunks. Use `git restore --staged <path>` or its patch mode
only to correct this boundary.

Preserve unrelated work in the worktree and index. Before excluding index entries,
save their exact blobs, modes and deletions; restore them after the commit without
staging their unstaged hunks. An isolated index is an option.

Inspect the final index. Commit that index without a trailing path list:
`git commit -- <paths>` can capture unstaged content after hunk staging.
Continue when the index contains the complete boundary alone and excluded work
remains recoverable in its original state.

### 4. Validate the index

Run the narrowest read-only check covering the staged boundary: a targeted test,
formatter check, lint, typecheck, syntax check or build slice. When none exists,
report `Validation: not run, <reason>`.

Diagnose failures; repair and recheck within the enclosing task's authority.
Otherwise report the exact failure and needed decision. A failed check does not
satisfy the prerequisite. Run formatters, generation or lockfile updates only
when required by the authorized change and repository workflow; inspect their
full output before staging.

Continue only after a covering check passes or a specific reason no check exists
is recorded.

### 5. Generate the message

The staged diff proves what changed; the request, linked issue and supplied
context establish why. Recent commits supply style, not facts.

Use Conventional Commits for proposals and commits:
`<type>[(<scope>)][!]: <imperative summary>`. Follow the repository's type set;
otherwise use `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`,
`revert`, `style` or `test`. Choose by effect, not file extension: build/dependencies,
CI, performance and reversals use their corresponding types. Use a stable,
boundary-specific scope consistent with local style, or omit it when unhelpful.
Every breaking change needs both `!` and a `BREAKING CHANGE:` footer stating what
breaks and what callers must change.

**Subject:** name the concrete result, including the rule or behavior established
by documentation or instructions. Keep it short, imperative and without a period.
Its promise must fit the diff, including partial work; verify any claimed audience,
measurement or outcome. Replace vague editorial verbs with the actual effect:
`feat(pr): verify PR claims against code and tickets`, not `sharpen review workflow`.
Remove the prefix mentally: if the remainder fits unrelated diffs, rewrite it.
If evidence leaves materially different promises plausible, offer two or three
options with tradeoffs and ask once.

**Body:** optional for obvious small commits; include it for breaking changes,
migrations, non-obvious fixes, tradeoffs or multi-file relationships the subject
cannot preserve. Put the reason before the change; short `Why` and `Changes`
sections are a fallback. Keep decision-relevant details; validation and risk
belong in the report. Apply `communicate-clearly` when available, preserving
technical precision. Include no `Co-authored-by` or other authorship footers.

Continue when every promise is supported, the subject identifies this boundary
and the body preserves necessary context.

### 6. Commit, amend or propose

For a proposal, report the staged boundary, message and index changes; create no
commit. For an amendment, first read
[hooks and amend](references/hooks-and-amend.md).

Immediately before each commit attempt, record exact `HEAD`, short status, intended
message and staged diff. Keep the boundary fixed through retries. Commit after
staging and validation, using `git commit -F <file>` for any body or multiline
message; `-m <subject>` is only for a subject alone. Run hooks; never bypass them
with `--no-verify`.

After every attempt inspect `HEAD`, its parents, full message, stat, diff from the
baseline, short status, and staged/unstaged boundary diffs. For an unborn baseline,
inspect the new root directly. A new commit must have exactly one new `HEAD`,
with the baseline as its sole parent, or no parents for an unborn baseline.
Its message and boundary must match, and outside work must be preserved.
Expected pre-existing residual changes are not a blocker.

When hooks change files, an attempt fails, or those checks disagree, read
[hooks and amend](references/hooks-and-amend.md) before staging, retrying or
declaring success. Continue only after every parent, message, boundary and residual
state check passes, or report the precise blocked/refused state.

### 7. Publish when authorized

In Commit-and-push mode, after verifying every intended commit, read and execute
[publication](references/publication.md). Otherwise report the boundary results.
When the request or standing instructions also require PR work, continue with
`pr`, passing the verified commit state and existing authority.

## Output

Report only verified states. For each boundary include:

- **Status:** `committed`, `amended`, `proposed`, `blocked` or `refused`.
- **Commit:** short hash and message when created; proposed message when available.
- **Boundary:** what was included or proposed; when step 4 fails, identify the
  staged behavior or paths.
- **Validation:** exact command/result, or not run with reason.

For completed commits, also give the branch, post-commit verification of `HEAD`,
parent, message, committed diff, index and residual worktree; remaining changes;
push status/command/result; and PR handoff or not requested. A published run adds
overall status `pushed`.

For proposals, blockers, failed validation or risky state, also report index
changes, exact blocker, failed command, concise error and needed decision when
applicable.
