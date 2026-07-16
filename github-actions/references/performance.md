# Performance and Cost

Apply every section matching latency, runner cost, parallelism, dependency setup, caches, artifacts, or toolchains. Optimize the measured **critical path** against a named target.

## Name the target and baseline

Choose the objective before changing the graph:

- **Feedback latency:** wall-clock time until the required result.
- **Throughput:** completed runs under runner, service, or API limits.
- **Cost:** billed runner time, larger-runner spend, storage, and transfer.
- **Reliability under load:** queue delay, cancellation waste, and cache stability.

Use representative run and job timings, queue time, cache hit and transfer data, artifact sizes, and runner labels. Compare like-for-like commits and warm or cold states. A baseline contains multiple representative runs. When run data is inaccessible, model the dependency graph and label the expected improvement as unmeasured.

## Execution graph

Expose independent work at the earliest safe point. Choose the parallelism boundary from isolation needs and measured overhead:

- **Jobs:** independently runnable lint, test, build, and scan work that needs separate permissions, environments, status checks, retries, runners, or resource limits.
- **Parallel group:** independent steps that share one runner and must all finish before the next step.
- **Background lifecycle:** a `run` or `uses` step that overlaps later work or provides a service; give it an `id`, probe readiness, and terminate or wait explicitly.
- **Sequential steps:** tightly coupled work where runner startup or artifact transfer costs more than overlap saves.

For job edges:

- Add `needs` only for required data, isolation, or ordering.
- Run fast, high-signal failures early without delaying independent work.
- Build once and fan out an immutable artifact when downstream jobs need the same output.
- Keep shared writes race-free; jobs provide isolation, while parallel and background steps share CPU, memory, disk, network, workspace, and permissions.

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
- `wait` targets one step ID or an array, `wait-all:` takes no arguments, and `cancel` targets one ID.
- Wait and cancel steps always run and do not accept `if`. Outputs and environment changes become available only after the matching wait; failures surface there unless the background step allows failure.
- Pair every background step with an explicit wait or cancel. The runner otherwise waits before post-job cleanup.
- At most ten background steps run concurrently per job; additional steps queue.
- Native background and parallel syntax is unavailable inside composite actions; the composite itself can run in the background.
- Prefer the native graph to shell `&`, which hides lifecycle, output, and failure semantics.

Verify `parallel`, `background`, `wait`, `cancel`, and concurrency-queue availability against the repository's GitHub.com or GHES version. If a configured linter lags current server syntax, report its version and the source-backed compatibility gap rather than weakening valid semantics.

## Checkout and dependency setup

- Use the repository's locked install command: `npm ci`, `pnpm install --frozen-lockfile`, Yarn Berry's `yarn install --immutable`, Yarn 1's `yarn install --frozen-lockfile`, or the ecosystem equivalent.
- Use setup actions when an exact runtime, package cache, authentication setup, or cross-runner consistency is part of the contract.
- Let checkout keep its shallow default when history and tags are unnecessary. Use sparse checkout for large repositories only when every required path, local action, and generated input is included.
- Reuse source checkout, dependency installation, code generation, and compilation within one job. Across isolated jobs, compare repetition with artifact-transfer and startup costs before consolidating.
- Put deterministic tool and dependency versions in repository-owned files when the ecosystem supports it.

## Runner toolchains

Resolve preinstalled tools from the exact runner image manifest. `-latest` labels and their software move over time.

- Use a preinstalled binary directly only when its floating version is acceptable and the current manifest confirms it on every selected OS and architecture.
- For self-hosted runners, inspect and version the owned image or bootstrap process.
- When removing a setup action, run the underlying command and record the resolved version.
- Select the smallest runner that meets memory, CPU, disk, architecture, and network needs. Use a larger runner only when measured speedup or queue behavior justifies its cost.
- Set bounded job and step timeouts for work that can hang or consume scarce capacity.

## Caches

A cache should save more time and cost than restore, validation, and save consume.

- Prefer setup-action cache support for npm, pnpm, Yarn, pip, Gradle, Maven, RubyGems, Go, and .NET when it matches the repository. These caches normally store package-manager data rather than an installed dependency tree.
- Derive custom cache keys from the runner OS and architecture, runtime or tool version, and exact lockfile or source hash that determines the contents.
- Use restore prefixes only when a partial match remains correct after the normal locked install or rebuild.
- Cache only dependencies or expensive rebuildable intermediates. Keep secrets, credentials, release artifacts, and opaque executable state in their authoritative stores.
- Keep cache key cardinality and paths bounded to prevent eviction churn. Review hit rate, restore and save duration, entry size, retention, repository limits, and read-only cache warnings.
- Use restore-only behavior for consumers that should not publish shared state.

For any untrusted producer or privileged consumer, also apply [`security.md`](security.md#cache-poisoning-chain).

## Artifacts

Use artifacts to transfer immutable results or preserve evidence. Use caches for acceleration.

- Upload a shared build once, then download the same artifact ID or digest in every consumer.
- Transfer only files downstream jobs need; exclude dependency trees and temporary data when rebuilding is cheaper than compression and transfer.
- Tune compression only for large measured payloads; incompressible data can trade substantial CPU for negligible size reduction.
- Give matrix producers unique names and upload shared content once.
- At a privilege boundary, apply the artifact-promotion rules in [`security.md`](security.md#artifact-promotion).

## Matrices and concurrency

Use [`reliability.md`](reliability.md#matrices) to preserve matrix and concurrency semantics, then evaluate their cost:

- A matrix earns its startup overhead when each combination represents a required compatibility result or useful partition.
- `max-parallel` protects scarce runners and rate-limited services; it may increase wall-clock time while improving throughput stability.
- Cancel obsolete runs early. Preserve queued deployment and release runs whose side effects remain meaningful.
- Keep setup, checkout, and artifact transfers proportional to required matrix combinations.

## Performance criterion

Complete when the critical path contains no unnecessary edge or repeated build; parallel boundaries reflect isolation and measured overhead; background services have readiness and termination; toolchains and runners are intentional; cache benefit exceeds cache cost without trust escalation or churn; artifact transfer is minimal and immutable; and the target metric has representative before-and-after evidence or an explicit measurement gap.

## Official sources

https://docs.github.com/api/article/body?pathname=/en/actions/reference/workflows-and-actions/workflow-syntax

https://docs.github.com/api/article/body?pathname=/en/actions/reference/runners/github-hosted-runners

https://docs.github.com/api/article/body?pathname=/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows

https://docs.github.com/api/article/body?pathname=/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts

https://github.com/actions/upload-artifact

https://github.com/actions/checkout

https://github.blog/changelog/2026-06-25-actions-steps-can-now-be-run-in-parallel/

https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues/
