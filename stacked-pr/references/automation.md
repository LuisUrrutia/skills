# Stack-aware CI and integrations

Load this file when the fix changes a GitHub Actions workflow, bot, GraphQL client, or webhook
because of stack membership, position, size, or trunk. Product-code, test, lint, and build failures
use the normal stack route even when Actions reports them.

Routing is complete when the automation artifact and the stack-specific behavior are identified.

## Establish the live event contract

Native stack schemas may change while in preview. Before editing production automation, open the
current official documentation and, when available, capture one payload from the target repository:

- [Stacked PR APIs and webhooks](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests-apis-and-webhooks)
- [Optimizing CI for stacked PRs](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests)

Record the current field paths, nullability, position semantics, API version, permissions, and event
delivery behavior that the change uses. The contract check is complete when every referenced field
and permission is supported by a live source or target payload.

## GitHub Actions

Choose the execution policy before writing expressions:

- run fast, layer-specific checks for every PR;
- run whole-feature checks only for the current top layer;
- run merge gates only for the lowest currently unmerged layer.

Derive top, bottom, position, size, and trunk expressions from the live payload. Guard stack-specific
field access and preserve the equivalent ordinary-PR path when the workflow serves both kinds.
Validate workflow syntax and exercise stacked and ordinary event fixtures.

CI work is complete when each job runs at the intended position, stack fields are null-safe,
ordinary PR behavior is preserved, and repository-specific workflow validation passes.

## Stack mutations

When automation creates, extends, maintains, restructures, or merges a native stack, load
[api-workflow.md](api-workflow.md) and then its matching mutation branch. That route is the
source of truth for ordering, idempotency, concurrency, and terminal verification. Do not duplicate
its mutation sequence in the workflow documentation.

## GraphQL and webhooks

Read current GraphQL schema documentation before selecting fields and paginate stack entries. Use
REST for any stack mutation that GraphQL exposes only as a read.

Treat one stack as multiple PR event streams. Make handlers idempotent, tolerate absent stack data,
and key stack-wide effects with the current stack identity plus the head/base state that makes the
effect unique. Verify redelivery, out-of-order delivery, and ordinary-PR fixtures.

GraphQL or webhook work is complete when all selected fields exist in the live schema, pagination
and absent-stack cases are handled, repeated or reordered events do not duplicate effects, and the
target repository's fixtures pass.
