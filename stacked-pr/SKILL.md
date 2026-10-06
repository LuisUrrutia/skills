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
the selected route. Before publishing new code or creating PRs, measure additions
plus deletions for each layer's full `<base-sha>...<head-sha>` diff against its
actual immediate PR base, including tests, generated text and lockfiles. Use
Git's `--shortstat` totals and `--numstat` for binary entries; record revisions and
binary review burden separately. Never count an upper layer cumulatively against
trunk. Splitting commits does not shrink a PR. An unavailable count blocks publication;
an over-cap layer returns to `task-breakdown` before publication. Recheck after base
or head changes. Scope this gate to publication; read-only inspection can report it.

## Route the request

Choose one primary route. Load its file, select the requested operation there, and stop when that
operation's completion criterion is satisfied. For a request that explicitly includes several
operations, complete them in dependency order and satisfy each criterion before loading the next:

- **CLI** — local development, navigation, submit, sync, or cascading rebases owned by
  `github/gh-stack`. Load [references/cli-workflow.md](references/cli-workflow.md).
- **API** — perform a concrete native-stack operation through REST, whether interactive or
  automated. Load [references/api-workflow.md](references/api-workflow.md).
- **Manual** — GitHub reports native stacks unavailable, or the user wants ordinary dependent PRs.
  Load [references/manual-chain.md](references/manual-chain.md).
- **Stack-aware CI and integrations** — load
  [references/automation.md](references/automation.md) when the fix changes a workflow, bot, GraphQL
  client, or webhook because of stack state. Product-code and test failures use CLI, API, or manual.

Keep one mutation owner throughout an operation. Read-only inspection through another interface is
safe; switching writers during a mutation can desynchronize local tracking and GitHub state.

Routing is complete when the requested operation and primary route are identified. For
repository-bound work, also identify the repository, trunk, push remote, and authenticated
principal; for a mutation, record the current branch, dirty paths, relevant branch tips, and
intended remote objects before changing state.

## Conditional references

The primary route points to these only when their branch is reached:

- [references/stack-design.md](references/stack-design.md) — plan layers before creating branches or
  splitting existing work.
- [references/troubleshooting.md](references/troubleshooting.md) — recover from a failure,
  divergence, adoption, restructuring, worktrees, or another branch manager.
