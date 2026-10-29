# Performance and Cost

Apply every section matching latency, runner cost, metrics, billing attribution, parallelism, dependency setup, caches, artifacts, or toolchains. Optimize the measured **critical path** against a named target.

## Name the target and baseline

Choose the objective before changing the graph:

- **Feedback latency:** wall-clock time until the required result.
- **Throughput:** completed runs under runner, service, or API limits.
- **Cost:** billed runner time, larger-runner spend, storage, and transfer.
- **Reliability under load:** queue delay, cancellation waste, and cache stability.

Use representative run and job timings, queue time, cache hit and transfer data, artifact sizes, and runner labels. Compare like-for-like commits and warm or cold states. A baseline contains multiple representative runs. When run data is inaccessible, model the dependency graph and label the expected improvement as unmeasured.

## Collect and attribute evidence

Use Actions usage metrics to find minutes consumed by workflow, job, repository, operating system, and runner type. Use performance metrics to compare average run time, job time, queue time, and failure rate. Record the metric scope, time window, runner class, and warm or cold state so the baseline remains comparable. If the required view is inaccessible, name the missing role or report rather than substituting an unrelated metric.

For cost attribution:

- Use the detailed billing usage report when workflow identity matters. Its `workflow_path` field attributes Actions usage; summarized reports omit that dimension.
- Identify GitHub-generated workflows by their current `workflow_path`, actor, and product-specific Actions label rather than display name alone. Treat those identifiers as a versioned external contract: verify them before changing a billing filter, dashboard, or alert.
- GitHub Code Quality currently reports deterministic scans under `dynamic/github-code-quality/codeql` with actor `github-code-quality`. Filters using the earlier `dynamic/github-code-scanning/codeql` path or `github-advanced-security` actor no longer isolate Code Quality. Code Quality and code scanning can both display the workflow name `CodeQL`, so that name is not a reliable discriminator.
- When estimating a generated product's total cost, separate Actions compute from product licenses, AI credits, storage, and other metered dimensions. Do not present Actions minutes as the whole product cost.

Sources: [Actions metrics](https://docs.github.com/en/actions/concepts/metrics), [billing reports](https://docs.github.com/en/billing/reference/billing-reports), [Code Quality workflow identification](https://docs.github.com/en/code-security/reference/code-quality/codeql-detection), [Code Quality costs](https://docs.github.com/en/code-security/how-tos/maintain-quality-code/view-and-manage-cost), and the [Code Quality workflow-path change](https://github.blog/changelog/2026-08-20-separate-github-actions-path-for-github-code-quality/).

## Execution graph

Expose independent work at the earliest safe point. Choose the parallelism boundary from isolation needs and measured overhead:

- **Jobs:** independently runnable lint, test, build, and scan work that needs separate permissions, environments, status checks, retries, runners, or resource limits.
- **Parallel group:** independent steps that share one runner and must all finish before the next step.
- **Background lifecycle:** a `run` or `uses` step with an `id` that overlaps later work or provides a service.
- **Sequential steps:** tightly coupled work where runner startup or artifact transfer costs more than overlap saves.

For job edges:

- Add `needs` only for required data, isolation, or ordering.
- Run fast, high-signal failures early without delaying independent work.
- Build once and fan out an immutable artifact when downstream jobs need the same output.
- Keep shared writes race-free; jobs provide isolation, while parallel and background steps share CPU, memory, disk, network, workspace, and permissions.

### Step concurrency

In every job you create or change, find steps that consume none of each other's outputs, files, or side effects, and run them in a `parallel` group; run long-lived services as `background` steps. Keep a step sequential when it writes paths, ports, or tool caches that a concurrent step uses, when order matters, or when CPU-bound steps would contend for a 2- or 4-core runner; a tool that already parallelizes internally gains little from overlap. Outside the requested change, report overlap opportunities with step timings or a labeled model instead of restructuring untouched jobs.

```yaml
steps:
  - parallel:
      - name: Build frontend
        run: npm run build:frontend
      - name: Build backend
        run: npm run build:backend
  - name: Test assembled build
    run: npm test
```

`parallel` is shorthand for background steps followed by an implicit barrier. Use the explicit lifecycle when later work must overlap or consume one result:

```yaml
steps:
  - name: Start API
    id: api
    run: npm start
    background: true
  - name: Wait for API readiness
    run: curl --fail --retry 20 --retry-delay 1 --retry-connrefused http://127.0.0.1:3000/health
  - name: Test API
    run: npm test
  - cancel: api
```

- Probe readiness before using a background service; launch completion alone is insufficient.
- Keep the service in the step's foreground. A command that daemonizes, such as `docker run -d` or `nohup … &`, completes at launch, and `cancel` cannot reach the process it leaves behind.
- `wait` targets one step ID or an array, and `wait-all:` takes no arguments. `cancel` targets one ID and sends `SIGTERM`, then `SIGKILL` after a short grace period.
- Wait and cancel steps always run, even after a failure, and do not accept `if`. A background step's outputs and environment changes become available only after a wait that includes it; its failure fails that wait unless the background step sets `continue-on-error`.
- End every background step with an explicit wait or cancel. An implicit `wait-all` runs before post-job cleanup, so a service that is never cancelled holds the job until its timeout.
- At most ten background steps, including `parallel` members, run concurrently per job; additional steps queue.
- Native background and parallel syntax is unavailable inside composite actions; the composite itself can run in the background.
- Prefer native step concurrency to shell `&`, which interleaves logs and hides lifecycle, output, and failure semantics.

Verify `parallel`, `background`, `wait`, `cancel`, and concurrency-queue availability against the repository's GitHub.com or GHES version.

Sources: [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsbackground) and the [parallel-steps release note](https://github.blog/changelog/2026-06-25-actions-steps-can-now-be-run-in-parallel/).

## Checkout and dependency setup

- Use the repository's locked install command: `npm ci`, `pnpm install --frozen-lockfile`, Yarn Berry's `yarn install --immutable`, Yarn 1's `yarn install --frozen-lockfile`, or the ecosystem equivalent.
- Use setup actions when an exact runtime, package cache, authentication setup, or cross-runner consistency is part of the contract.
- Let checkout keep its shallow default when history and tags are unnecessary. Use sparse checkout for large repositories only when every required path, local action, and generated input is included.
- Reuse source checkout, dependency installation, code generation, and compilation within one job. Across isolated jobs, compare repetition with artifact-transfer and startup costs before consolidating.
- Put deterministic tool and dependency versions in repository-owned files when the ecosystem supports it.

Source: [actions/checkout](https://github.com/actions/checkout).

## Runner labels and toolchains

Resolve preinstalled tools from the exact runner image manifest. `-latest` labels and their software move over time.

- Verify every GitHub-hosted label against the current runner reference before keeping or adding it. A retired label fails its jobs, after scheduled brownout failures: `macos-14`, `macos-14-large`, and `macos-14-xlarge` retire on 2026-11-02, so move to `macos-15` or `macos-26` (`macos-latest`) arm64 labels. A `-latest` label migrates between OS versions: `ubuntu-latest` moves from Ubuntu 24.04 to 26.04 between 2026-10-19 and 2026-11-19. Test on the new image, and pin the previous explicit label only while a required tool is missing there.
- When the Xcode version is the contract, select an Xcode image label such as `xcode-27` or `xcode-27-xlarge`; each image carries one major Xcode version and runs only on Apple Silicon.
- Use a preinstalled binary directly only when its floating version is acceptable and the current manifest confirms it on every selected OS and architecture.
- For self-hosted runners, inspect and version the owned image or bootstrap process.
- When removing a setup action, run the underlying command and record the resolved version.
- Select the smallest runner that meets memory, CPU, disk, architecture, and network needs. Use a larger runner only when measured speedup or queue behavior justifies its cost.
- Set bounded job and step timeouts for work that can hang or consume scarce capacity.

Sources: [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners), the [macOS 14 retirement](https://github.blog/changelog/2026-10-01-github-actions-macos-14-runner-image-retirement/), the [Ubuntu 26.04 migration](https://github.blog/changelog/2026-09-17-ubuntu-26-generally-available-and-latest-migration/), and the [Xcode 27 image](https://github.blog/changelog/2026-10-15-xcode-27-runner-image-generally-available/).

## Caches

A cache should save more time and cost than restore, validation, and save consume.

- Prefer setup-action cache support for npm, pnpm, Yarn, pip, Gradle, Maven, RubyGems, Go, and .NET when it matches the repository. These caches normally store package-manager data rather than an installed dependency tree.
- Derive custom cache keys from the runner OS and architecture, runtime or tool version, and exact lockfile or source hash that determines the contents.
- Use restore prefixes only when a partial match remains correct after the normal locked install or rebuild.
- Cache only dependencies or expensive rebuildable intermediates. Keep secrets, credentials, release artifacts, and opaque executable state in their authoritative stores.
- Keep cache key cardinality and paths bounded to prevent eviction churn. Review hit rate, restore and save duration, entry size, retention, repository limits, and read-only cache warnings.
- Give consumers that should not publish shared state `cache-mode: read` and a restore-only cache step so no save is attempted. Give a trusted job that rebuilds from a clean state and publishes the cache `cache-mode: write-only`.
- An operation the effective mode denies does not fail: a denied restore is a cache miss, and a denied save is skipped with an informational log line. After a `cache-mode` change, read the effective mode from `ACTIONS_CACHE_MODE` before diagnosing keys or hit rates.

For any untrusted producer or privileged consumer, also apply the [cache-poisoning chain](security.md#cache-poisoning-chain).

Source: [GitHub Actions dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching).

## Artifacts

Use artifacts to transfer immutable results or preserve evidence. Use caches for acceleration.

- Upload a shared build once, then download the same artifact ID or digest in every consumer.
- Transfer only files downstream jobs need; exclude dependency trees and temporary data when rebuilding is cheaper than compression and transfer.
- Tune compression only for large measured payloads; incompressible data can trade substantial CPU for negligible size reduction.
- Give matrix producers unique names and upload shared content once.
- At a privilege boundary, apply the [artifact-promotion rules](security.md#artifact-promotion).

Sources: [downloading workflow artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts) and [actions/upload-artifact](https://github.com/actions/upload-artifact).

## Matrices and concurrency

Use [`reliability.md`](reliability.md#matrices) to preserve matrix and concurrency semantics, then evaluate their cost:

- A matrix earns its startup overhead when each combination represents a required compatibility result or useful partition.
- `max-parallel` protects scarce runners and rate-limited services; it may increase wall-clock time while improving throughput stability.
- Cancel obsolete runs early. Preserve queued deployment and release runs whose side effects remain meaningful.
- Keep setup, checkout, and artifact transfers proportional to required matrix combinations.

Source: [larger concurrency queues release note](https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues/).

## Performance criterion

Complete when the critical path contains no unnecessary edge or repeated build; parallel boundaries reflect isolation and measured overhead; background services have readiness and termination; toolchains and runners are intentional; cache benefit exceeds cache cost without trust escalation or churn; artifact transfer is minimal and immutable; every cost filter uses a verified attribution dimension; and the target metric has representative before-and-after evidence or an explicit measurement gap.
