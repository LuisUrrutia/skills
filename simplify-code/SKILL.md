---
name: simplify-code
description: Use when simplifying changed code and removing unnecessary complexity while preserving behavior.
---

# Simplify code

Make the requested change easier to read and maintain through focused edits that
preserve its behavior. Judge the code against its purpose and local conventions;
its appearance does not establish who wrote it or whether it is wrong.

An explicit review-only request returns recommendations without edits. A cleanup
request authorizes the cleanup, not new features or a repository-wide redesign.
Commit and publication follow the active task and repository rules.

## Fix the scope

Use the caller's files, diff, commit, or current task boundary. Read the relevant
repository instructions and record existing staged, unstaged, and untracked work
before editing. Inspect surrounding code and callers to understand the changed
unit without making neighboring debt part of the cleanup.

For a branch or PR, resolve its actual target base from the supplied context or
repository/PR metadata. A branch's tracking upstream may be its own remote head,
not its target base. Use the merge-base for the branch's introduced changes;
include working-tree changes only when they belong to the requested scope. Do
not assume `main`, compare base tips as though their independent changes were
yours, or include earlier layers of a stack. For a commit, inspect its own patch.

For uncommitted work, inspect both `git diff --cached` and `git diff`, plus
relevant untracked files from `git ls-files --others --exclude-standard`. Preserve
unrelated edits and existing staging. If no scope can be established and the
plausible choices would change what gets edited, ask before making those edits.

## Simplify from evidence

Read the complete changed unit, its relevant contracts, and representative callers
and tests. Identify the knowledge a reader must retain and the work that adds no
behavior or useful explanation. Make a simplification only when its benefit and
behavioral equivalence are supported:

- Remove comments that repeat the code. Preserve non-obvious reasons, invariants,
  public contracts, external constraints, legal notices, and meaningful tooling
  directives. Clear names or a small refactor can replace narration; they do not
  automatically replace a reason. Encode a constraint when that fits the current
  scope and preserves it, then remove only the prose made redundant.
- Check the actual producer, trust boundary, and lifetime before removing a
  validation or guard. Static types alone do not validate external data. A check
  before a callback or `await` may no longer establish mutable state afterward.
  Keep necessary checks at the point where their guarantee is used.
- Inspect error handling for recovery, translation, cleanup, logging, and async
  behavior. Remove a catch only when those effects and the caller's failure
  contract remain equivalent. In particular, a returned promise can reject after
  a surrounding `try` has exited; removing `await` can bypass its catch or run
  its finally before the operation settles.
- Replace type escapes with the real domain type, corrected API use, or `unknown`
  narrowed at an untyped boundary. Replacing `any` with an unchecked assertion,
  a suppression, or a fallback that hides invalid data does not fix the type gap.
- Reduce nesting, duplicate decisions, dead code, and unnecessary indirection when
  the local flow becomes clearer. Preserve evaluation order, side effects,
  resource lifetime, public shape, and valid falsy values. A shorter expression
  or an extra abstraction is not automatically simpler.
- Match established formatting and naming. Keep broad reformatting, dependency
  changes, and unrelated renames outside a focused cleanup.

When the reason for a consequential workaround remains unclear, use relevant
history or the available `why` skill by registered name. Check its present effect
as well as its original motivation. Missing evidence is a reason to retain the
uncertain part and explain the gap, not evidence that it is redundant.

A discovered bug is a separate behavioral decision. Repair it when the active
task already authorizes that fix and verify it explicitly; otherwise report it
and continue independent cleanup. Do not silently change failure behavior or
product rules under a claim of equivalence. Stop when the scoped opportunities
are resolved; no edit is a valid result when the code is already clear.

## Check and finish

Review the resulting diff against the recorded starting state, including unrelated
edits and staging. Confirm each edit has a concrete benefit and that no constraint
disappeared merely to reduce lines or warnings.

Run the relevant existing behavior checks and the repository's required type,
lint, build, and smoke checks against the final code. Exercise the specific
invariant that justified removing a guard or error path. Add a test only when it
covers a meaningful risk that existing checks cannot establish. Do not rewrite
expectations or disable checks to make a cleanup pass. Use `verify` by registered
name when the task needs application-level evidence or its local recipe.

Report what was simplified, the scope, exact checks and outcomes, and anything
retained because its necessity or verification remains unresolved. Keep the report
proportionate. A passing typecheck alone is not evidence of unchanged runtime
behavior; missing required checks keep the corresponding completion claim open.

For requested maintenance of this skill's sources, read
[references/upstream-updates.md](references/upstream-updates.md).
