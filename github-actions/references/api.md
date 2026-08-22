# GitHub API and Workflow Channels

Apply the sections matching each API call, workflow output, environment write, or summary.

## Choose the narrowest interface

- Use `actions/github-script` for short REST or GraphQL operations that benefit from authenticated Octokit, pagination, and structured JavaScript.
- Use `gh api` when the surrounding step is already shell-based or the endpoint is easier to express directly.
- Use a dedicated action when it provides a maintained domain contract that would otherwise be reimplemented.

Every interface still needs explicit `GITHUB_TOKEN` permissions in the job.

## Structured API access with `github-script`

Pin the action to a verified commit SHA. Retries fit reads and idempotent operations; reconcile non-idempotent writes before retrying them.

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

Source: [actions/github-script documentation](https://github.com/actions/github-script).

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

## Workflow dispatch

The REST endpoint that creates a `workflow_dispatch` event returns HTTP `200` with `workflow_run_id`, `run_url`, and `html_url`. Capture that response and use the returned run ID for status, logs, cancellation, or downstream links instead of correlating a run by creation time, workflow name, or commit alone.

A dispatch is non-idempotent. After a transport failure with no usable response, reconcile against a caller-supplied correlation input when the target workflow supports one; otherwise report the ambiguous result instead of retrying blindly and possibly creating a second run. Check the response object before exposing its fields as workflow outputs.

Source: [create a workflow dispatch event](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event).

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

Source: [GitHub Actions workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands).

## API review criterion

The job has the exact API permission, pagination matches the endpoint, retries preserve idempotency, dispatches retain their returned run identity or report ambiguity, response shape and emptiness are checked, untrusted values stay out of generated shell, and each output crosses the correct scope boundary.
