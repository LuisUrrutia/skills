# Reliability and Workflow Semantics

Apply every section matching the trigger, approval gate, expression, matrix, concurrency, failure, or reusable-workflow contract. Reliability means the observed result matches the event and failure semantics, including cancellation.

## Events and refs

Resolve semantics for each configured event from its current payload and ref rules rather than assuming all triggers expose the same context.

- On `pull_request`, branch filters match the base branch; use `github.head_ref` when head-branch identity is required.
- Path filters are not evaluated for tag pushes. Branch and path filters combine with logical AND; positive and negative patterns are order-sensitive.
- A workflow skipped by branch, path, or commit-message filtering can leave its required check pending. Keep a required workflow trigger stable and gate work inside it when the repository rules require a conclusion.
- Route any held or awaiting-approval state through [approval gates and held runs](#approval-gates-and-held-runs); valid workflow syntax does not guarantee that a run or job may start.
- For `workflow_run`, validate the source workflow, repository, event, conclusion, branch, and commit before consuming its outputs. Load the security reference when the follow-up has greater authority.
- For `workflow_dispatch` and `workflow_call`, preserve declared input types. Treat values reaching shell or JavaScript as data even when the UI constrains them.
- Confirm which default-branch copy of a workflow GitHub uses for the selected event, especially for scheduled, manual, issue, release, and chained workflows.
- For a wall-clock schedule, set an IANA `timezone`; the default is UTC. A scheduled time skipped during the spring daylight-saving transition advances to the next valid local time, so choose the hour deliberately. Scheduled workflows run the latest default-branch commit and can be delayed during high Actions load.

Source: [events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).

## Approval gates and held runs

Classify the gate before diagnosing a run that has not started:

- **Contributor or bot pull-request approval:** repository, organization, or enterprise policy can require a maintainer with write access to approve a fork or generated pull-request workflow. Inspect the actor and effective policy; a fork run awaiting approval for more than 30 days is deleted. Use the documented fork-run REST approval endpoint only for the gate it covers.
- **Automatic malicious-workflow hold:** GitHub can hold a run it identifies as potentially malicious in a public GitHub.com repository. A collaborator with write access must approve it through an authenticated web session; no repository setting or REST approval substitutes for that review. The run then continues normally. This automatic hold does not apply to GitHub Enterprise Server.
- **Environment protection:** required reviewers, wait timers, and custom protection apps gate a job that references the environment. Environment secrets remain unavailable until the applicable rules pass; apply the [`deployment` decision](security.md#secrets-oidc-and-environments) before assuming every environment gate creates a deployment.
- **Workflow execution protection:** actor and event rulesets can deny execution before a workflow runs. Treat that outcome as a policy denial rather than an approval queue, and verify the effective repository, organization, or enterprise ruleset.

For each gate, record its scope, owner, approval or bypass channel, expiration, and behavior after approval. Treat a held or awaiting-approval run as an external manual gate, not a job failure or runner-queue bottleneck. Keep least privilege and trust-boundary controls inside every workflow that the platform permits to run.

Sources: [approving workflow runs from forks](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks), [fork-run approval API](https://docs.github.com/en/rest/actions/workflow-runs#approve-a-workflow-run-for-a-fork-pull-request), [bot-created pull-request approval](https://github.blog/changelog/2026-06-11-bot-created-pull-requests-can-run-workflows-if-approved/), [automatic malicious-workflow holds](https://github.blog/changelog/2026-07-28-github-actions-holds-potentially-malicious-workflows-for-approval/), [deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments), and [workflow execution protections](https://docs.github.com/en/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/actions-policies/workflow-execution-protections).

## Expressions and conditions

Check context availability at the exact YAML key where an expression appears. A context that exists in a step may be unavailable in `concurrency`, a job-level `if`, or a reusable-workflow declaration.

- Keep native booleans and numbers as typed `inputs` values; use `fromJSON` only when converting string channels intentionally.
- Distinguish a step's `outcome` before `continue-on-error` from its resulting `conclusion`.
- A missing or skipped producer can yield an empty output. Guard optional outputs before parsing or using them as identifiers.
- Job-level `if` is evaluated before matrix expansion. Put combination-specific conditions on steps or encode supported combinations in the matrix.
- Use `case(predicate, value, ..., default)` for ordered multi-branch value selection. The first true predicate wins. Prefer it to `condition && value || fallback` when a selected value can be false, zero, or empty.
- An `if` without a status-check function has an implicit `success()` condition. Use `failure()`, `cancelled()`, or `!cancelled()` deliberately for diagnostics and cleanup.
- Use `!cancelled()` for most post-processing. Reserve `always()` for a step that must run after cancellation and cannot block on an unavailable dependency.

Sources: [expression evaluation](https://docs.github.com/en/actions/reference/evaluate-expressions-in-workflows-and-actions) and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

## Failure, cancellation, and time bounds

Make each non-success state intentional:

- Keep build, test, security, package, release, and deployment failures blocking unless the surrounding contract explicitly consumes failure as data.
- Use `continue-on-error` only when a later condition reads the outcome or the step is intentionally informational.
- Give network calls bounded, idempotency-aware retries rather than hiding deterministic failures.
- Set job and step `timeout-minutes` from observed upper bounds for commands that can hang or consume scarce runners.
- Ensure cancellation reaches child processes and apply the [`background` lifecycle](performance.md#execution-graph) to services.
- Put diagnostic uploads behind `if: ${{ !cancelled() }}` or another explicit status condition and keep them free of secrets.

## Concurrency

Choose the meaning of an older run before adding a concurrency group:

- **Obsolete:** cancel superseded branch or pull-request CI.
- **Serialized:** retain deployment or release runs in a queue.
- **Independent:** omit concurrency because every run remains meaningful.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

For a serialized deployment:

```yaml
concurrency:
  group: deploy-${{ inputs.environment }}
  queue: max
  cancel-in-progress: false
```

Concurrency groups are repository-wide and case-insensitive. Include workflow and target identity so unrelated automation cannot collide. The default retains at most one pending run and replaces it with a newer arrival. `queue: max` retains up to 100 pending runs, cannot be combined with `cancel-in-progress: true`, and orders waiting runs by when they entered the queue rather than guaranteeing dispatch order. Verify feature availability against the repository's GitHub.com or GHES version.

Source: [workflow and job concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

## Matrices

Use a matrix only for a supported compatibility or partitioning contract:

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest]
    node: [20, 22]
```

- Keep the default fail-fast behavior when an early failure makes remaining combinations valueless; set `fail-fast: false` when every compatibility result is required.
- Use `include` for exceptional metadata and `exclude` for unsupported combinations.
- Set `max-parallel` when jobs share rate-limited services, deployment targets, or scarce runners.
- Define every referenced matrix key for every combination that reaches it.
- Batch work in one command when setup and reporting overhead exceed the isolated work and separate results carry no contract.

## Reusable workflows

Treat `workflow_call` as a versioned contract with an explicit API:

- Declare typed inputs, named secrets, and workflow outputs.
- Apply the caller [permission ceiling](security.md#token-permissions) and let the called workflow maintain or reduce it.
- Prefer named secrets; use `secrets: inherit` only when the contract genuinely needs the caller's secret set.
- Environment secrets originate from the environment declared by a job in the called workflow; `workflow_call` passes inputs and declared secrets through separate channels.
- Apply the [dependency verification procedure](../SKILL.md#when-an-external-reference-changes) to external reusable workflows. Same-repository `$/.github/workflows/name.yml` and `./.github/workflows/name.yml` references resolve from the caller's commit; neither accepts an `@ref`. Prefer `$/` on GitHub.com; it is unavailable on GHES.
- Update every caller when inputs, secrets, permissions, outputs, runner requirements, or failure semantics change.
- Keep nesting and matrix fan-out within the limits of the repository's GitHub.com or GHES version.

Source: [reusing workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

## Reliability criterion

Complete when every event resolves to the intended workflow copy, ref, and actor policy; every approval, hold, and policy denial has its scope, owner, channel, and expiration accounted for; every expression uses a context available at its location; required checks reach a conclusion; success, failure, cancellation, retry, and timeout behavior are explicit; concurrency and matrices preserve every meaningful run; and each reusable-workflow caller agrees with the called contract.
