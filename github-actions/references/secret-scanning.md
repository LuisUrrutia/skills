# Secret-Scanning Custom Patterns

Apply this reference when a workflow prepares or reconciles secret-scanning custom patterns. Also apply the [narrowest GitHub API interface](api.md#choose-the-narrowest-interface) and its matching transport section.

## REST contract

GitHub's REST API supports custom-pattern operations for secret-scanning customers at repository, organization, and enterprise scope:

- `GET .../secret-scanning/custom-patterns` lists patterns.
- `POST .../secret-scanning/custom-patterns` bulk-creates patterns.
- `PATCH .../secret-scanning/custom-patterns/{pattern_id}` updates one pattern.
- `DELETE .../secret-scanning/custom-patterns` bulk-deletes patterns.

Use the current API version header; the initial GA contract uses `X-GitHub-Api-Version: 2026-03-10`. Resolve the token requirement for the exact endpoint instead of assuming the job's default `GITHUB_TOKEN` has administrative scope. Verify the current request and permission contract in the [custom-pattern REST API](https://docs.github.com/en/rest/secret-scanning/custom-patterns).

## Concurrent updates and deletion

Carry `custom_pattern_version` through update and delete requests as the optimistic-concurrency token. Handle `412 Precondition Failed` by rereading state rather than overwriting a concurrent edit. Set `post_delete_action` deliberately because deletion can either remove associated alerts or resolve them as pattern-deleted.

## Publication boundary

REST automation prepares and reconciles pattern definitions. Dry runs and final publishing remain UI operations, so keep those human gates visible in the workflow. See the [custom-pattern REST API release contract](https://github.blog/changelog/2026-07-13-create-and-manage-secret-scanning-custom-patterns-via-rest-api/).

## Secret-scanning criterion

Complete when the endpoint scope and token permission are exact; request and response shapes are validated; updates and deletions preserve `custom_pattern_version`; conflicts reread current state; deletion behavior is deliberate; and the workflow leaves dry-run and publication gates visible.
