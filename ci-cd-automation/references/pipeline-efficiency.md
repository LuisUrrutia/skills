# Pipeline efficiency without lost coverage

Read when changing path filters, caches, job topology, shards, runner capacity,
or a speed/cost target. Use the platform specialist for its syntax and semantics.

## Measure the waiting path

Use run, job, and step timestamps for comparable revisions and workloads. Separate
queue and approval waits, setup, execution, and artifact transfer. Measure developer
wait and runner cost separately. The longest dependent chain determines completion
time; summing every concurrent job does not.

Compare several runs where available, including spread and cold/warm cache state.
If there is no measured baseline, give a hypothesis and the runs needed to test it.
Change the limiting part first and preserve required coverage. Extra shards add
setup and may increase cost or contention; caches can cost more to restore than
the work they save. Keep test isolation and resource ownership intact.

Credit improvements only from comparable executed work at the changed revision.
Report time saved, runner cost, failures/skips, and uncertainty. Do not impose a
universal duration target, mandatory timing ledger, or test-runner configuration.

## Make selection conservative

Changed-path detection must include dependent packages and shared build inputs:
lockfiles, toolchain configuration, generators, and workflow/task definitions.
Use the comparison range that covers all unverified changes, including work skipped
by a superseded run. If that range or dependency graph is unavailable, run the
broader checks.

Define expected coverage independently of discovered tasks. Verify that each
selected workspace and shard actually ran its required checks; a successful root
command may silently skip a missing script. A final required result must account
for exclusions and propagate failed, cancelled, or missing prerequisites. Test both
the changed and unchanged paths before relying on a filter.

## Preserve state and cache boundaries

Separate disposable validation from publishing and deployment. Cancel obsolete
validation only when its effects are safe to discard. A deployment cancelled by
another run can continue remotely or leave partial state; target serialization and
an explicit supersession policy must cover retries, manual reruns, and recovery too.

Key cached results by every input that changes their meaning. Isolate writers and
trust domains; validate integrity where cached output crosses a release boundary.
A cache miss should perform the work. Do not let a broad fallback cache or stale
artifact silently establish eligibility for a different candidate.

Keep essential commands executable through the project's task interface. Extract
shared workflow components for actual repetition with explicit inputs, outputs,
permissions, and ownership. Check their consumers when changing a common component.
