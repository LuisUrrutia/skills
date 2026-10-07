---
name: stacked-pr
description: Manage GitHub stacked pull requests and dependent PR chains. Use for designing or operating a stack, splitting work into reviewable layers, recovering divergent stacks, or changing CI workflows, bots, or webhook integrations whose behavior depends on stack state.
---

# Stacked pull requests

A **stack** is a linear chain of pull requests in one repository. The **bottom** targets the
**trunk**; every layer above targets the branch below it, so each PR shows only its own concern.

```text
main <- data-model <- api-routes <- ui
          bottom                  top
```

Dependencies point toward the trunk, changes to a lower layer cascade upward, and merges proceed
bottom-up.

## Scope and safety

Bound the work to the requested operation. Explanations, reviews, and status checks are read-only.
Creation and maintenance may change only the local branches and linked PRs needed for that
operation. A later lifecycle stage must be explicitly included in the request.

Merging requires the user's explicit approval for the exact PR set and merge method immediately
before the merge command. Preserve unrelated dirty-tree work. Before rewriting ancestry, record the
current branch and relevant tips so every original commit remains reachable until verification.

When a request, project rule or task record sets a review-size cap, carry it through
the selected route. Before pushing or creating PRs, invoke `pr` in
Check cap mode for each layer, passing its actual immediate PR base, selected
head and cap. An upper layer is never checked cumulatively against trunk. Require
a current `within-cap` result; if `pr` is unavailable, report the missing check
and keep capped publication pending. The selected stack route retains mutation
and remediation ownership under the shared contract defined by `pr`.
Read-only inspection may use the same check and report its verdict without publishing.

## Route the request

Choose one primary route. Load its file, select the requested operation there, and stop when that
operation's completion criterion is satisfied. For a request that explicitly includes several
operations, complete them in dependency order and satisfy each criterion before loading the next.

Resolve the routes in this order. Select the automation route when the fix is an automation
artifact, and the API route when REST owns the state. Otherwise run `gh extension list`, record the
result, and take manual when one of its conditions holds, CLI otherwise:

- **Stack-aware CI and integrations** — the fix changes a workflow, bot, GraphQL client, or webhook
  because of stack state; product-code and test failures use another route. Load
  [references/automation.md](references/automation.md).
- **API** — a bot, integration, stateless job, or explicit REST request performs a concrete
  native-stack operation. Load [references/api-workflow.md](references/api-workflow.md).
- **Manual** — the user explicitly asks for ordinary dependent PRs instead of a native stack, GitHub
  reports native stacks unavailable for the repository, or installing the absent extension is
  prohibited or fails. Load [references/manual-chain.md](references/manual-chain.md).
- **CLI** — `github/gh-stack` is installed, or it is absent and may be installed; the route file
  installs it only when the requested operation requires it. Load
  [references/cli-workflow.md](references/cli-workflow.md).

When conditions overlap, the user's explicit choice outranks GitHub's availability report, which
outranks the extension listing. GitHub's report comes from a failed native-stack read, link, or
submit; routing adds no probe. When it appears during a mutation on the CLI route, record it as
the selecting observation and move ownership to manual through the migration branch in
troubleshooting.md; if the user explicitly asked for a native stack, report the failure instead.
A read-only request reports it and continues inspecting through Git and PR reads, leaving tracking
and ownership unchanged.

Existing branches and PRs that no tool tracks yet do not select the route. For a mutation on the
CLI route, adopting them is a prerequisite step of the requested operation, not a separately
requested operation: use the adopt step in cli-create.md and the adoption branch in
troubleshooting.md, preserving existing tips. Branches another manager owns follow the
interoperability branch there instead. Read-only requests inspect them without writing tracking.

Keep one mutation owner throughout an operation. Read-only inspection through another interface is
safe; switching writers during a mutation can desynchronize local tracking and GitHub state. Once
the stack view shows that `gh-stack` tracks a chain, a plain `git rebase` or push on its branches
switches the writer; a user's explicit move to manual migrates ownership through the migration
branch in troubleshooting.md first.

Routing is complete when the requested operation, the primary route, and the observation that
selected it are recorded, such as the extension listing, GitHub's availability report, the user's
explicit choice, or the REST or automation context. For repository-bound work, also identify the
repository, trunk, push remote, and authenticated principal; for a mutation, record the current
branch, dirty paths, relevant branch tips, and intended remote objects before changing state.

## Conditional references

The primary route points to these only when their branch is reached:

- [references/stack-design.md](references/stack-design.md) — plan layers before creating branches or
  splitting existing work.
- [references/troubleshooting.md](references/troubleshooting.md) — recover from a failure,
  divergence, adoption, restructuring, worktrees, or another branch manager.
