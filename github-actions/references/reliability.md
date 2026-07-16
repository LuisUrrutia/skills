# Reliability and Workflow Semantics

Apply every section matching the trigger, expression, matrix, concurrency, failure, or reusable-workflow contract. Reliability means the observed result matches the event and failure semantics, including cancellation.

## Events and refs

Resolve semantics for each configured event from its current payload and ref rules rather than assuming all triggers expose the same context.

- On `pull_request`, branch filters match the base branch; use `github.head_ref` when head-branch identity is required.
- Path filters are not evaluated for tag pushes. Branch and path filters combine with logical AND; positive and negative patterns are order-sensitive.
- A workflow skipped by branch, path, or commit-message filtering can leave its required check pending. Keep a required workflow trigger stable and gate work inside it when the repository rules require a conclusion.
- Account for fork, Dependabot, bot, and first-time-contributor approval rules; a syntactically valid workflow may still be blocked by repository or organization policy.
- For `workflow_run`, validate the source workflow, repository, event, conclusion, branch, and commit before consuming its outputs. Load the security reference when the follow-up has greater authority.
- For `workflow_dispatch` and `workflow_call`, preserve declared input types. Treat values reaching shell or JavaScript as data even when the UI constrains them.
- Confirm which default-branch copy of a workflow GitHub uses for the selected event, especially for scheduled, manual, issue, release, and chained workflows.

## Expressions and conditions

Check context availability at the exact YAML key where an expression appears. A context that exists in a step may be unavailable in `concurrency`, a job-level `if`, or a reusable-workflow declaration.

- Keep native booleans and numbers as typed `inputs` values; use `fromJSON` only when converting string channels intentionally.
- Distinguish a step's `outcome` before `continue-on-error` from its resulting `conclusion`.
- A missing or skipped producer can yield an empty output. Guard optional outputs before parsing or using them as identifiers.
- Job-level `if` is evaluated before matrix expansion. Put combination-specific conditions on steps or encode supported combinations in the matrix.
- An `if` without a status-check function has an implicit `success()` condition. Use `failure()`, `cancelled()`, or `!cancelled()` deliberately for diagnostics and cleanup.
- Use `!cancelled()` for most post-processing. Reserve `always()` for a step that must run after cancellation and cannot block on an unavailable dependency.

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
- Apply the [dependency verification procedure](../SKILL.md#when-an-external-reference-changes) to external reusable workflows. A same-repository `./.github/workflows/name.yml` reference resolves from the caller's commit.
- Update every caller when inputs, secrets, permissions, outputs, runner requirements, or failure semantics change.
- Keep nesting and matrix fan-out within the limits of the repository's GitHub.com or GHES version.

## Reliability criterion

Complete when every event resolves to the intended workflow copy, ref, and actor policy; every expression uses a context available at its location; required checks reach a conclusion; success, failure, cancellation, retry, and timeout behavior are explicit; concurrency and matrices preserve every meaningful run; and each reusable-workflow caller agrees with the called contract.

## Official sources

https://docs.github.com/api/article/body?pathname=/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

https://docs.github.com/api/article/body?pathname=/en/actions/reference/workflows-and-actions/workflow-syntax

https://docs.github.com/api/article/body?pathname=/en/actions/reference/evaluate-expressions-in-workflows-and-actions

https://docs.github.com/api/article/body?pathname=/en/actions/how-tos/reuse-automations/reuse-workflows

https://docs.github.com/api/article/body?pathname=/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
