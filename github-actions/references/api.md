# GitHub API and Workflow Channels

Apply the sections matching each API call, workflow output, environment write, or summary.

## Choose the narrowest interface

- Use `actions/github-script` for short REST or GraphQL operations that benefit from authenticated Octokit, pagination, and structured JavaScript.
- Use `gh api` when the surrounding step is already shell-based or the endpoint is easier to express directly.
- Use a dedicated action when it provides a maintained domain contract that would otherwise be reimplemented.

Every interface still needs explicit `GITHUB_TOKEN` permissions in the job.

## Structured API access with `github-script`

Pin the action to a verified commit SHA. Retries fit reads and idempotent operations; a repeated create or dispatch request can duplicate side effects.

```yaml
- name: Count open pull requests
  id: pulls
  uses: actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd # v8.0.0
  with:
    retries: 3
    script: |
      const pulls = await github.paginate(github.rest.pulls.list, {
        owner: context.repo.owner,
        repo: context.repo.repo,
        state: 'open',
        per_page: 100
      })
      core.setOutput('count', pulls.length)
```

The action's default terminal status codes are `400,401,403,404,422`. Handle a rate-limit `403` with response-aware delay rather than making every authorization failure retryable.

Version 8 runs on Node 24 and requires Actions Runner `v2.327.1` or newer. Verify that floor before using this example on self-hosted runners.

Pass dynamic expressions through step-level `env` and read them from `process.env`; direct `${{ ... }}` inside `script:` is evaluated as JavaScript source before execution.

## Shell API access with `gh`

Pass authentication and dynamic path components through `env`. Request every page when the answer is not intentionally capped, and make an empty or malformed response fail when the contract requires data.

```yaml
- name: Read latest release
  env:
    GH_TOKEN: ${{ github.token }}
    REPOSITORY: ${{ github.repository }}
  shell: bash
  run: |
    set -u
    tag=$(gh api "repos/$REPOSITORY/releases/latest" --jq '.tag_name | select(length > 0)')
    if [[ -z "$tag" ]]; then
      printf '%s\n' 'Latest release response has no tag' >&2
      exit 1
    fi
    printf 'tag=%s\n' "$tag" >> "$GITHUB_OUTPUT"
```

For retries, classify the operation first:

- retry reads and idempotent writes on transient `5xx`, connection failures, and rate limits
- honor `Retry-After` or rate-limit reset metadata
- use bounded exponential backoff with jitter
- make authentication, authorization, validation, and contract failures terminal
- give non-idempotent writes a lookup key or reconciliation step before retrying

## Secret scanning custom patterns

GitHub's REST API supports custom-pattern CRUD for secret scanning customers at repository, organization, and enterprise scope:

- `GET .../secret-scanning/custom-patterns` lists patterns.
- `POST .../secret-scanning/custom-patterns` bulk-creates patterns.
- `PATCH .../secret-scanning/custom-patterns/{pattern_id}` updates one pattern.
- `DELETE .../secret-scanning/custom-patterns` bulk-deletes patterns.

Use the current API version header; the initial GA contract uses `X-GitHub-Api-Version: 2026-03-10`. Resolve the token requirement for the exact repository, organization, or enterprise endpoint instead of assuming the job's default `GITHUB_TOKEN` has administrative scope.

Carry `custom_pattern_version` through update and delete requests as the optimistic-concurrency token, and handle `412 Precondition Failed` by rereading state rather than overwriting a concurrent edit. Set `post_delete_action` deliberately because deletion can either remove associated alerts or resolve them as pattern-deleted.

REST automation prepares and reconciles pattern definitions. Dry runs and final publishing remain UI operations, so keep those human gates visible in the workflow rather than claiming end-to-end publication.

## Workflow channels

Use the channel whose scope matches the data:

```yaml
- name: Export version
  id: version
  shell: bash
  run: printf 'value=%s\n' "1.2.3" >> "$GITHUB_OUTPUT"

- name: Export build date
  shell: bash
  run: printf 'BUILD_DATE=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$GITHUB_ENV"

- name: Summarize
  shell: bash
  run: printf '## Build results\n\nPassed.\n' >> "$GITHUB_STEP_SUMMARY"
```

Map step outputs to job outputs before a downstream job consumes them. Map job outputs to `on.workflow_call.outputs` before a caller consumes reusable-workflow data.

Pass arbitrary multiline content through a file or artifact rather than a static delimiter. Register generated sensitive values with `::add-mask::` before another command can emit them.

## API review criterion

The job has the exact API permission, pagination matches the endpoint, retries preserve idempotency, response shape and emptiness are checked, optimistic-concurrency tokens are preserved, required UI gates remain visible, untrusted values stay out of generated shell, and each output crosses the correct scope boundary.

## Official sources

https://github.com/actions/github-script

https://docs.github.com/api/article/body?pathname=/en/actions/reference/workflows-and-actions/workflow-commands

https://docs.github.com/api/article/body?pathname=/en/rest/secret-scanning/custom-patterns

https://github.blog/changelog/2026-07-13-create-and-manage-secret-scanning-custom-patterns-via-rest-api/
