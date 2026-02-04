# GitHub Actions Security

## GITHUB_TOKEN Permissions (Principle of Least Privilege)

Declare permissions explicitly at the narrowest scope (job-level preferred):

```yaml
jobs:
  build:
    permissions:
      contents: read
  deploy:
    permissions:
      contents: read
      deployments: write
```

- Grant only the specific permissions each job needs
- Use `permissions: {}` to disable all permissions when unused
- Fork-triggered workflows receive read-only permissions by default
- Common permissions: `contents`, `issues`, `pull-requests`, `packages`, `deployments`, `id-token`

## Script Injection Prevention

User-controlled input can be exploited if interpolated directly into `run:` blocks.

**Attacker-controllable contexts:**
`github.event.issue.title`, `github.event.issue.body`, `github.event.pull_request.title`, `github.event.pull_request.body`, `github.event.comment.body`, `github.event.review.body`, `github.event.commits.*.message`, `github.event.head_commit.message`, `github.event.pull_request.head.ref`, `github.head_ref`

**Mitigation - use environment variables:**

```yaml
- name: Check PR title
  env:
    TITLE: ${{ github.event.pull_request.title }}
  run: |
    if [[ "$TITLE" =~ ^octocat ]]; then
      echo "PR title starts with 'octocat'"
    fi
```

## pull_request_target Event

Runs with base repository permissions and secrets, even for fork PRs. This grants fork PRs access to your secrets.

**Safe uses:** Labeling, commenting, adding reviewers (operations that read only from base branch)

**Unsafe pattern:**
```yaml
on: pull_request_target
steps:
  - uses: actions/checkout@v4
    with:
      ref: ${{ github.event.pull_request.head.sha }}  # Untrusted fork code
  - run: npm install && npm run build  # Executes with secrets access
```

**For fork PR CI builds, use two workflows:**
1. `pull_request`: Build/test in fork's context (no secrets)
2. `workflow_run`: Privileged operations after first workflow succeeds

## Secrets Best Practices

- Never print secrets in logs (use `::add-mask::`)
- Don't pass secrets to untrusted actions
- Rotate secrets regularly
- Use OIDC for cloud providers instead of long-lived credentials

```yaml
- name: Mask dynamic secret
  run: |
    token=$(generate-temp-token)
    echo "::add-mask::$token"
    echo "TOKEN=$token" >> "$GITHUB_ENV"
```
