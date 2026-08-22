# Native stack through the GitHub API

Use this route when REST owns GitHub stack state: bots, integrations, stateless jobs, or an explicit
REST request. Plain Git owns branch ancestry and pushes. Perform only the requested operation.

## Establish the live contract

GitHub stacked PR APIs may change while in preview. Before each operation, open the current official
documentation and record the API version, methods, paths, fields, response states, and permissions
used by that operation:

- [REST endpoints for stacked PRs](https://docs.github.com/en/rest/pulls/stacks)
- [REST endpoints for pull requests](https://docs.github.com/en/rest/pulls/pulls)
- [Asynchronous pull-request merge](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request-asynchronously)

Use an authenticated HTTP client; `gh api` is one option. Inspect the repository, remotes,
authentication, and dirty tree before any mutation. Probe the documented read endpoint to
distinguish unavailable functionality from a wrong repository, unsupported version, or insufficient
permission.

The contract check is complete when the owner, repository, trunk, push remote, authenticated
principal, API version, planned requests, required permissions, and expected response states are
recorded from live sources.

## Inspect

Use the documented read endpoints to query the stack and its PRs. Paginate collections and preserve
the response needed to support the report.

Inspection is complete when the report identifies:

- stack number, trunk, and ordered PR numbers;
- every PR's head, base, draft state, merge state, and head SHA;
- any mismatch between Git ancestry and remote membership;
- any asynchronous operation still pending;
- any field that could not be established and the exact request that failed.

Stop after reporting those facts for a status, explanation, or review request.

## Mutation branches

Load one matching branch at a time. Load another only when it is explicitly included in the request
and the current operation's completion criterion is satisfied:

- [api-create.md](api-create.md) — create or adopt PRs, create a stack, or extend its top.
- [api-maintain.md](api-maintain.md) — restack branches, change review stage, restructure, or dissolve.
- [api-merge.md](api-merge.md) — merge the approved scope and observe asynchronous completion.

Every mutation branch uses the live contract established here. Refetch before writes, make creation
idempotent through prior lookup, and verify state from a fresh read rather than trusting a write
response.
