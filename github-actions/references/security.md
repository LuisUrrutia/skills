# GitHub Actions Security

## GITHUB_TOKEN Permissions (Principle of Least Privilege)

**Prefer job-level permissions** for standalone workflows:

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

### Workflow-level permissions for reusable workflows

**Use workflow-level permissions** when calling reusable workflows with `secrets: inherit`, because called workflows inherit the caller's workflow-level permissions. Job-level permissions in the caller do NOT propagate to called workflows.

```yaml
# Caller must use workflow-level permissions for called workflows to inherit them
permissions:
  contents: write
  attestations: write
  packages: write
  id-token: write

jobs:
  release-sbom:
    uses: ./.github/workflows/release-sbom.yml
    secrets: inherit  # Inherits workflow-level permissions above

  release-docker:
    uses: ./.github/workflows/release-docker.yml
    secrets: inherit
```

**For called workflows (`workflow_call`):** Adding explicit permissions is good defense-in-depth (restricts what the called workflow can use), but not strictly required if the caller already has appropriate scope and the workflow is protected by an `environment:` gate.

## Script Injection Prevention

Always use `env:` instead of direct `${{ }}` interpolation in `run:` blocks. The `env:` pattern is strictly better and prevents injection by design. However, assign severity based on the source.

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

### Security finding (attacker-controlled, can contain shell metacharacters):
- `github.event.pull_request.title` / `.body`
- `github.event.issue.title` / `.body`
- `github.event.comment.body`
- `github.event.review.body`
- `github.event.commits.*.message` / `github.event.head_commit.message`
- `github.event.pull_request.head.ref` / `github.head_ref`

### Style/best practice (safe input, recommend `env:` for consistency):
- `github.repository` -- controlled by GitHub
- `github.sha` -- 40-char hex string
- `github.event.pull_request.number` -- always numeric
- `github.event.pull_request.user.login` -- restricted to `[a-zA-Z0-9-]`
- Step outputs from `jq` numeric extractions
- `github.event.inputs.*` in `workflow_dispatch` (only write-access users can trigger)

### When reviewing, always ask:
1. Who can trigger this workflow? (fork PR = untrusted, push to main = trusted)
2. What is the actual character set of the interpolated value?
3. Is there input validation before the value is used?

The recommendation is always the same (`env:`), but the severity determines whether it's a "fix this now" or a "clean this up when convenient".

## pull_request_target Event

Runs with base repository permissions and secrets, even for fork PRs. This grants fork PRs access to your secrets.

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

### When `pull_request_target` Is Actually Required

Before flagging `pull_request_target` as a risk, check if the workflow legitimately needs it. Common valid use cases:

1. **CLA/DCO bots** (e.g., `contributor-assistant/github-action`) -- need to comment on fork PRs, set status checks, and access private signature repos. The upstream action documents `pull_request_target` as required.

2. **Security scanning with platform tokens** (e.g., Semgrep with `SEMGREP_APP_TOKEN`) -- need secrets for API-connected scanning on fork PRs. Check the tool's docs for whether `pull_request_target` is their recommended setup.

3. **PR labeling/commenting bots** that need write access to fork PRs.

**When reviewing, evaluate:**
- Does the workflow check out fork code (`ref: github.event.pull_request.head.sha`)? If no, the risk is significantly lower.
- Is any attacker-controlled context (PR title, body, branch name) interpolated into `run:` blocks? If no, script injection is not possible.
- Does the upstream tool/action document `pull_request_target` as required? If yes, it's intentional.

**Only flag as a risk when:**
- The workflow checks out fork code AND runs it with secrets access
- Attacker-controlled context is interpolated into `run:` blocks without using `env:`
- The workflow could achieve the same result with `pull_request` or `workflow_run`

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

## Evaluating `git push -f`

Don't blanket-flag force push. Check the context:
- Is the branch newly created? Force push on a new branch = regular push.
- Is there a guard (branch existence check) before the force push?
- Is the branch protected? Force push to protected branches is blocked by GitHub.

Only flag when force push targets an existing branch with no protection.
