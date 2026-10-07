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

Choose one primary route, load its file, select the requested operation there, and stop when that
operation's completion criterion is satisfied. For a request that explicitly includes several
operations, complete them in dependency order and satisfy each criterion before loading the next.

Decide the route in this order:

1. **Stack-aware CI and integrations** when the fix changes a workflow, bot, GraphQL client, or
   webhook because of stack state. Product-code and test failures use another route. Load
   [references/automation.md](references/automation.md).
2. **API** when REST owns the state: a bot, integration, stateless job, or explicit REST request
   performs a native-stack operation. Load [references/api-workflow.md](references/api-workflow.md).
3. Otherwise run `gh extension list` and record the result.
   - **Manual** when the user explicitly asks for ordinary dependent PRs instead of a native stack,
     when GitHub reports native stacks unavailable for the repository, or when installing the
     absent extension is prohibited or fails. Load
     [references/manual-chain.md](references/manual-chain.md).
   - **CLI** otherwise: `github/gh-stack` is installed, or it is absent and may be installed.
     The route installs it only when the operation needs it. Load
     [references/cli-workflow.md](references/cli-workflow.md).

When several conditions hold at once, the user's explicit choice outranks GitHub's report, which
outranks the extension listing. A user who explicitly asked for a native stack never gets the manual
route: report a prohibited or failed install, or GitHub's report, as a blocker, and use the API
route only with the user's authorization.

GitHub reports native stacks unavailable through a failed native-stack read, link, or submit;
routing does not probe for it. If that report appears during a mutation on the CLI route and the
user did not ask for a native stack, record it as the deciding observation and move the chain to
manual through the migration section of troubleshooting.md. During a read-only request, report it
and keep inspecting through Git and PR reads without changing tracking or ownership.

Existing branches and PRs that no tool tracks yet do not decide the route. On the CLI route, a
mutation adopts them first as part of the requested operation, through the adopt step in
cli-create.md and the adoption section of troubleshooting.md, keeping every existing tip. Branches
that another tool manages follow the interoperability section there instead. Read-only requests
inspect untracked branches without writing tracking.

Keep one mutation owner throughout an operation. Reading through another interface is safe, but
switching writers during a mutation can desynchronize local tracking and GitHub state. Once the
stack view shows that `gh-stack` tracks a chain, a plain `git rebase` or push on its branches
switches the writer. When the user explicitly moves such a chain to manual, migrate ownership
through troubleshooting.md first.

Routing is complete when the requested operation, the route, and the observation that decided it
are recorded, such as the extension listing, a failed install, GitHub's report, the user's explicit
choice, or the REST or automation context. For repository-bound work, also identify the
repository, trunk, push remote, and authenticated principal. Before a mutation, record the current
branch, dirty paths, relevant branch tips, and intended remote objects.

## Conditional references

The primary route points to these only when their branch is reached:

- [references/stack-design.md](references/stack-design.md) — plan layers before creating branches or
  splitting existing work.
- [references/troubleshooting.md](references/troubleshooting.md) — recover from a failure,
  divergence, adoption, restructuring, worktrees, or another branch manager.
