# Common Workflow Patterns

## Concurrency Control

Cancel in-progress runs when a new commit is pushed:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

For deployments, don't cancel but queue instead:

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```

### When NOT to Use Concurrency Control

Not all workflows need concurrency groups. Omit concurrency control for:

- **Security scanning workflows** (CodeQL, Scorecard, Semgrep on push) -- each push should be scanned independently. Cancelling in-progress scans could miss vulnerabilities.
- **Scheduled workflows** -- these run on a cron schedule and should complete every time.
- **One-shot workflows** that are unlikely to have overlapping runs.

Use concurrency control primarily for:
- CI workflows on PRs (cancel outdated runs when new commits are pushed)
- Deployment workflows (queue deployments, don't cancel in-progress ones)
- Release workflows (queue, don't cancel)

## Caching Patterns

### Node.js (npm)

```yaml
- uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238  # v6.2.0
  with:
    node-version: '20'
    cache: 'npm'
```

### Node.js (pnpm)

```yaml
- uses: pnpm/action-setup@9fd676a19091d4595eefd76e4bd31c97133911f1  # v4.2.0
  with:
    version: 8

- uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238  # v6.2.0
  with:
    node-version: '20'
    cache: 'pnpm'
```

### Node.js (yarn)

```yaml
- uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238  # v6.2.0
  with:
    node-version: '20'
    cache: 'yarn'
```

### Python (pip)

```yaml
- uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405  # v6.2.0
  with:
    python-version: '3.12'
    cache: 'pip'
```

### Rust (cargo)

```yaml
- uses: Swatinem/rust-cache@401aff9a7a08acb9d27b64936a90db81024cff97  # v2.8.2
```

### Go

```yaml
- uses: actions/setup-go@7a3fe6cf4cb3a834922a1244abfce67bcef6a0c5  # v6.2.0
  with:
    go-version: '1.22'
    cache: true
```

### Custom Cache

```yaml
- uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306  # v5.0.3
  with:
    path: |
      ~/.cache/custom
      ./build
    key: ${{ runner.os }}-custom-${{ hashFiles('**/config.json') }}
    restore-keys: |
      ${{ runner.os }}-custom-
```

## Matrix Strategies

### Multi-platform

```yaml
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
```

### Multi-version

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238  # v6.2.0
        with:
          node-version: ${{ matrix.node }}
```

### Combined Matrix

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20]
        exclude:
          - os: macos-latest
            node: 18
        include:
          - os: ubuntu-latest
            node: 20
            coverage: true
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238  # v6.2.0
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
      - if: matrix.coverage
        run: npm run coverage
```

## Conditional Execution

### Path-based triggers

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - '**/*.md'
      - 'docs/**'
```

### Job conditions

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

### Step conditions

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

- name: Upload coverage
  if: success() && matrix.coverage
  run: npm run coverage:upload
```

## Reusable Workflows

### Caller workflow

```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: production
    secrets:
      deploy-token: ${{ secrets.DEPLOY_TOKEN }}
```

### Reusable workflow

```yaml
# .github/workflows/reusable.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy-token:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - env:
          ENVIRONMENT: ${{ inputs.environment }}
        run: echo "Deploying to $ENVIRONMENT"
```
