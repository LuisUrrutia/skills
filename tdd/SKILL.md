---
name: tdd
description: Use when implementing features or fixes with test-driven development (TDD).
---

# Test-driven development

Build requested behavior through short red, green, and optional refactor cycles.
Use this method when the user or caller selects test-first development. Start
from the request and project context; no work-mode or earlier phase is required.

## Establish the behavior

Read the relevant implementation, tests, and project contracts. Identify the
observable behavior to add or change, its source of truth, and the existing test
command. Run the relevant existing checks to distinguish prior failures from
regressions introduced here.

Choose the public boundary callers use and the closest test layer that exercises
the behavior. Reuse established boundaries without asking for routine approval.
When accessible evidence leaves a material behavior or interface choice unresolved,
ask and pause its tests and implementation. Continue only work that remains valid
under any plausible answer. Do not turn the missing decision into an assumed
default, a new parameter, or a callback merely to keep coding; that also changes
the contract. The current implementation alone does not define correctness.

For a bug, take an established failure and intended correction as input. If they
are not evident from the request and code, diagnosis is separate work before the
TDD repair; do not expand this method into an open investigation. An existing
debug investigation can supply that evidence without becoming a dependency.

Keep a brief list of observable scenarios. Start with one useful behavior and
let later cycles cover remaining requirements and boundaries. A list of scenarios
is a plan, not a batch of speculative tests to write up front.

When choosing a test boundary, an independent expected result, or test doubles
requires judgment, read [references/test-design.md](references/test-design.md).

## Work one behavior at a time

1. **Write the check.** Add a focused test through the chosen boundary. Derive
   its expected result from the contract, a worked example, or another independent
   source. Assert the observable result and relevant state or effects; do not
   reproduce the production algorithm to compute the expectation. Name the test
   after its observable behavior using the project's terms.
2. **Observe red.** Run the test before implementing the behavior. Inspect why it
   fails. A broken runner, missing fixture, syntax error, or unrelated failure
   does not establish the intended red state. Add only minimal declarations or
   wiring when needed to make the test reach the missing behavior, then rerun it.
   That scaffolding must not satisfy the new assertion. Retain the command and
   relevant failure as evidence.
3. **Make it green.** Implement the smallest coherent change that satisfies this
   behavior and preserves existing contracts. Run the new test and relevant
   nearby tests. Resolve regressions introduced by the change before proceeding;
   do not weaken correct assertions to accommodate an incorrect implementation.
4. **Refactor when useful.** With the relevant tests passing, remove duplication
   or clarify the changed code without altering its contract. Rerun those tests.
   Refactoring is optional and stays within this change; a broader redesign is
   a separate decision.
5. **Choose the next scenario.** Use what the completed cycle established to
   select the next missing behavior. Repeat until the requested contract is
   covered and implemented, rather than anticipating unrelated future features.

A scenario may need several assertions to express one behavior, such as a
returned result and an unchanged balance. Group equivalent inputs when they
exercise the same rule; keep unrelated behaviors in separate cycles.

If a new test passes immediately, inspect its assertions and the existing path;
the behavior may already be supported. Keep useful coverage, report that no red
state occurred, and choose the next missing behavior. An optional mutation probe
belongs in a disposable copy and is separate from the TDD sequence. Do not damage
working code to manufacture red or describe tests added after implementation as
test-first development.

If the test cannot run, resolve in-scope setup problems with established tooling
first. New testing dependencies follow the project's choices and task authority.
When execution
still needs an inaccessible prerequisite or new authority, stop the affected
cycle and report the exact blocker. Continue independent work, but do not silently
switch the requested TDD task to unverified implementation-first work.

## Finish with evidence

Run the relevant suite and the project's required build, type, lint, and smoke
checks. Self-check the changed files and, when permitted, the diff for accidental
changes and tests tied to incidental structure. A broad code review remains a
separate caller-owned task. Separate pre-existing failures,
new regressions, and checks that could not run.

Report the behavior implemented, meaningful red and green observations, optional
refactoring, exact final commands and outcomes, and remaining gaps. A passing
final suite alone does not demonstrate test-first ordering.

This skill owns test-driven implementation. Diagnosis-only requests, running
existing checks, and adding coverage for already working code have different
completion criteria. Repository instructions and the caller own worktrees,
commits, PRs, and further delivery; this skill neither initiates those tasks nor
cancels an existing requirement to perform them.

For a requested check or update of this skill's sources, read
[references/upstream-updates.md](references/upstream-updates.md).
