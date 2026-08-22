# Designing a stack

Read this reference before creating branches or splitting existing work. The output of this step is
a bottom-to-top layer plan, not branches.

## Find the dependency chain

A stack is useful only when the work forms one coherent story with ordered dependencies. Put
foundations near the trunk and consumers above them:

```text
main <- billing/schema <- billing/api <- billing/ui <- billing/integration
```

For each proposed layer, record:

| Check | Required answer |
| --- | --- |
| Concern | One sentence describing the change a reviewer accepts |
| Inputs | Only APIs, types, or behavior from the same or lower layers |
| Output | A coherent state that builds and can be reviewed against its base |
| Ownership | Every changed path and commit has exactly one layer |
| Verification | The smallest relevant tests or checks for that layer |

Move shared types, schemas, migrations, and utilities below their consumers. Put integration tests
above the implementation they exercise. A change that cannot be described in one sentence is a
signal to split again; a layer with no dependency on the story belongs in a separate stack.

Prefer a short stack—often two to four layers—because review and CI costs multiply per PR. Treat
that as a pressure, not a quota: preserve a real concern boundary even when it adds a layer.

The design is complete when every changed path has one owner, every dependency points toward the
trunk, and the bottom-to-top story can be read without explaining hidden coupling.

## Name branches by topic and concern

Follow the repository's branch convention first. Otherwise use a shared topic plus the layer's
concern, for example:

```text
billing/schema
billing/api
billing/ui
```

Explicit branch names keep the layer map stable across CLI, API, and manual routes.

## Stage deliberately

Create the stack before implementing new multi-part work. On each layer, stage only that layer's
paths or hunks:

```bash
git add src/billing/schema.ts db/migrations/20260822_billing.sql
git diff --cached --check
git diff --cached
git commit -m "Add billing schema"
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
