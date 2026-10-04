---
name: ci-cd-automation
description: Design, review, or improve CI/CD pipeline structure, checks, artifact promotion, delivery gates, speed, or cost.
---

# CI/CD automation

Define what runs, what each stage proves, and what permits a candidate to advance.
Keep provider syntax and configuration with the platform specialist. A design or
review request produces recommendations; a setup request includes implementation
within the user's existing authorization.

## Establish the delivery contract

Inspect repository commands, lockfiles, workflow definitions and their called
scripts, release conventions, deployment configuration, and recent runs when
available. Resolve discrepancies between documentation and execution.

Identify independently releasable units, supported targets, data changes, external
consumers, and the required evidence for acceptance. Establish whether delivery
stops at a releasable artifact or automatically deploys it. Preserve established
approval policy, availability requirements, and cost limits; ask only about an
unresolved choice that materially changes the design. Do not invent environments,
coverage quotas, or manual approvals for every project.

## Choose stages by their purpose

Use existing commands as the shared local/CI interface. Select checks against
concrete failure modes and place each before the decision it protects.

| Phase | Contents to select for this project | Evidence that permits progress |
| --- | --- | --- |
| Change validation | Applicable format/lint/type checks, focused behavior and integration tests, build/package checks, security and compatibility checks | Required work actually ran for the candidate; failures block the dependent decision |
| Release candidate | Resolve the integrated revision, build/package with recorded inputs, test the distributable, record identity and required supply-chain evidence | The exact candidate meets release criteria; a PR's earlier result cannot establish a different revision |
| Delivery/deployment | Validate target configuration and eligibility, apply the release policy, promote/publish or deploy, then verify at the consumer boundary | Artifact identity, target state, and acceptance signals agree |
| Periodic maintenance | Expensive broader suites, dependency/security refresh, recovery exercises, cleanup as justified | A responsible owner receives actionable failures; scheduled work does not replace a required release gate |

Model a dependency graph. Parallelize independent work; keep ordering where one
stage consumes another's output. Separate build, test, publish, and deployment
authority even when the provider represents them in one workflow.

## Preserve evidence across stages

- Define each stage's trigger, exact inputs, dependencies, execution identity,
  command, output, and pass/fail/skip/cancel behavior. Missing, stale, empty, or
  failed required evidence prevents promotion. A justified exclusion is explicit.
- Record source revision, build inputs, artifact digest, and check results. Promote
  the verified artifact without rebuilding it; keep environment configuration
  separate where possible. If a target requires a distinct build, verify that
  output and record its relationship to the source candidate.
- Bind promotion and required approvals to the verified artifact identity. A branch,
  job name, or mutable tag cannot identify the exact candidate being approved.
- Treat caches as acceleration, not release evidence. Verify the artifact's origin
  and integrity at consumption; generating a signature or provenance alone is not
  a verification gate. Retain artifacts and evidence needed for recovery.
- Isolate untrusted code and its outputs from publishing/deployment credentials,
  trusted runners, and writable caches. Grant each stage only the authority it
  needs, with protected secrets and short-lived credentials where supported.

## Make deployment recoverable

Choose rollout and observation depth from compatibility, traffic, and recovery
cost. Define acceptance and abort signals, observation bounds, and the recovery
owner before rollout. No telemetry is an unknown outcome, not a healthy release.

Isolate independent targets; serialize competing writes to the same target and
reject obsolete candidates. Bound execution and retries. Before retrying or
cancelling a mutating step, establish its actual state and whether repetition is
safe. Reverting code cannot undo every data change or external effect.

For migrations, multiple services, package/mobile releases, or ambiguous recovery,
read [delivery-boundaries.md](references/delivery-boundaries.md). For path filters,
caching, sharding, or speed/cost changes, read
[pipeline-efficiency.md](references/pipeline-efficiency.md).

## Implement and verify the contract

Give the platform specialist the stage graph, trust boundaries, artifact contract,
and acceptance cases; use `github-actions` for GitHub Actions. If no specialist is
available, use current primary provider documentation for authorized implementation
and report that gap. Keep provider rules out of this skill. `pr-followup` owns an
existing PR's failing checks and feedback.

Use `verify` for execution evidence and `verification-authoring` for authorized
creation or maintenance of project-local verification recipes. When implementing
or executing authorized checks, exercise the normal path and relevant failure,
skip, stale-candidate, and interrupted-run paths in an isolated environment.
A parsed configuration does not prove scheduling, deployed health, or recovery.
State which behaviors still require provider or target access. Designing automation
grants no additional authority to publish, deploy, or change protection settings.

Return the stage graph and concise stage contracts, key choices and exclusions,
implementation changes, and observed checks with remaining gaps. When file changes
are authorized, record durable decisions in the project's existing CI/CD
documentation; otherwise include them in the response.

For requested source maintenance, read
[upstream-updates.md](references/upstream-updates.md).
