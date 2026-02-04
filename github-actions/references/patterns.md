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

## Caching Patterns

### Node.js (npm)

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

### Node.js (pnpm)

```yaml
- uses: pnpm/action-setup@v3
  with:
    version: 8

- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'
```

### Node.js (yarn)

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'yarn'
```

### Python (pip)

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
```

### Rust (cargo)

```yaml
- uses: Swatinem/rust-cache@v2
```

### Go

```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'
    cache: true
```

### Custom Cache

```yaml
- uses: actions/cache@v4
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
      - uses: actions/setup-node@v4
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
      - uses: actions/setup-node@v4
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
      - run: echo "Deploying to ${{ inputs.environment }}"
```
