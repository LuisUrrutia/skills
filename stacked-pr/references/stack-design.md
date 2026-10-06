# Designing a stack

Read this reference before creating branches or splitting existing work. The output of this step is
a bottom-to-top layer plan, not branches.

## Find the dependency chain

A stack is useful only when the work forms one coherent story with ordered dependencies.
Use the units from `task-breakdown` when supplied; otherwise establish coherent delivery
boundaries before choosing branches. Prefer a small complete behavior across necessary layers
over splitting by technical layer. Put genuine prerequisites below their consumers:

```text
main <- billing/monthly-total <- billing/monthly-comparison
```

For each proposed layer, record:

| Check | Required answer |
| --- | --- |
| Concern | One sentence describing the change a reviewer accepts |
| Inputs | Only APIs, types, or behavior from the same or lower layers |
| Output | A coherent state that builds and can be reviewed against its base |
| Ownership | Every change, hunk and commit belongs to one concern; a file may evolve across layers |
| Verification | The smallest relevant tests or checks for that layer and its integration limits |
| Review budget | Estimated additions plus deletions, applicable cap and actual measurement before publication |

Put shared prerequisites below their consumers only when they justify a separate unit.
Keep behavioral and integration tests in the first layer that can exercise the behavior;
do not reserve tests for a later PR merely because they cross layers.
A change that cannot be described in one sentence is a
signal to split again; a layer with no dependency on the story belongs in a separate stack.

Prefer a short stack—often two to four layers—because review and CI costs multiply per PR. Treat
that as a pressure, not a quota: preserve a real concern boundary even when it adds a layer.

The design is complete when every incremental change has one owner, every dependency points toward the
trunk, and the bottom-to-top story can be read without explaining hidden coupling.

## Name branches by topic and concern

Follow the repository's branch convention first. Otherwise use a shared topic plus the layer's
concern, for example:

```text
billing/monthly-total
billing/monthly-comparison
```

Explicit branch names keep the layer map stable across CLI, API, and manual routes.

## Stage deliberately

Create the stack before implementing new multi-part work. On each layer, stage only that layer's
paths or hunks:

```bash
git add server/billing/monthly-total.ts src/billing/monthly-total.tsx tests/billing/monthly-total.test.ts
git diff --cached --check
git diff --cached
git commit -m "feat(billing): show monthly total"
```

Use the repository's normal test commands after each layer. Multiple commits are acceptable when
they all serve the layer's concern. Keep unrelated dirty-tree changes unstaged and preserve them
across branch changes.

Finish or preserve the current concern before the selected route creates the next layer. Verify the
dirty tree again after every branch change.

## Split an existing change safely

For an oversized branch or PR, design the target layers before rewriting history. Record the source
branch and tip SHA, then preserve that ref until every rebuilt layer has the intended diff and all
tests pass. Use the adoption and rebuild paths in
[troubleshooting.md](troubleshooting.md); linking the oversized branch as one layer does not split
it.
