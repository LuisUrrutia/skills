# Maintain a project verification skill

Keep the existing recipe honest as the application changes. The feature is the
unit of coverage: read every feature against source and exercise every feature
live. A clean source review alone cannot establish a clean maintenance pass.

## Locate and read

Resolve the target project-local verification skill by registered name and read
its launch/doctor/drive contract and feature index. Ask when several targets fit.
When none exists, report that creation is needed rather than inventing a target.
Establish intended behavior from requirements and history where necessary.

Run this skill's map checker for index hygiene. Reconcile missing, duplicate,
or dead entries with the actual feature files; no separate generated inventory
needs to become a project artifact.

## Source wave

Use one read-only worker per feature through available, authorized delegation,
concurrently within host capacity. Give each the feature file and relevant raw
source, asking for: user-visible behavior, source entry points, suspected drift
with citations or none, and one concise live recipe. Workers do not drive the
application, edit files, or spawn further workers. Track and settle their actual
tasks before integrating the pass. If independent readers cannot run, disclose
that limit and perform the source coverage directly when the caller permits;
do not claim an independent review occurred.

Require a returned source assessment for every feature. Reconcile overlapping
recipes into as few application states as practical. Spot-check drift citations;
do not spend the pass re-proving every clean sentence. Inspect recent changes
for user-facing features missing from the map and identify a concrete source
path before calling one missing.

## Drive every feature

The coordinator alone drives the mutable application state. Follow the target's
launch model: a serially driven long-lived instance, or fresh isolated sessions
for short-lived commands. Exercise every feature at least once and record which
entry points and sub-features the evidence actually covers. A proof through one
entry point does not mark another as verified. Preserve these invariants through
every failure and repair:

1. Doctor before the first drive, on each fresh session where sessions are the
   unit, and after any failed or surprising drive. If process health cannot
   establish a usable UI state, reset to a known state or relaunch.
2. Evidence captured so far survives each cleanup. Check its named location.
3. Processes, sessions, and fixtures do not outlive their useful drive. Clean
   failed-iteration residue too; for a shared instance, remove owned residue
   without terminating the shared application.

If doctor fails because the recipe drifted, correct the in-scope cause and retry
once, restarting only what the correction invalidates. A still-unavailable
prerequisite blocks that coverage. Record an unreachable path only with the
attempted route and concrete missing auth, entitlement, OS, or external state.
This verifies the inability to reach it, not that its behavior works; missing
prerequisites in the map are documentation drift.

## Correct the right layer

| Observation | Action |
| --- | --- |
| Intended behavior works, description is wrong or missing | Correct the map and verify the revised description against the live path. |
| Intended behavior works, harness cannot drive it | Correct the owned harness or instructions; exercise the corrected path live. |
| The application violates its intended behavior | Report a product regression and evidence; do not change the map to endorse it. |
| Intent is unresolved | Ask about that contract; continue only independent features. |
| Runtime or access prerequisite is unavailable | Record the attempted check and blocked coverage; do not report it as passed. |

Maintenance edits stay inside the target verification skill and its owned
helpers. Product repair, dependency installation, or external operations require
the active task's authority. Each corrected harness must run before delivery;
rerun affected checks after the final relevant edit. Teardown follows the last
re-proof, and retained evidence must remain readable.

## Report the outcome

These outcomes describe recipe maintenance, not whether the product passed.
Report the product's observed failures separately even when no recipe change
is needed.

- **clean:** every feature received source and live coverage, with no correction
  needed and no required coverage left blocked.
- **changed:** proven recipe, harness, or map corrections are ready, and required
  coverage is complete. Name any product failure found rather than hiding it.
- **blocked:** coverage or proof of a correction could not finish. Preserve useful
  corrections but identify them as partial; list the missing prerequisites.

Name tested features and entry points, untested paths, product gaps, corrections,
commands, evidence, and the outcome. Keep concise run notes in the permitted
evidence/scratch location. Publication follows the caller and the `commit` and
`pr` owners when applicable; a maintenance pass does not itself require a PR.
