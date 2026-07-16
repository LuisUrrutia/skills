---
name: github-actions
description: "Harden GitHub Actions workflows: create workflow YAML or reusable workflows; modify existing workflow automation; audit Actions security, correctness, reliability, cost, or performance."
---

# GitHub Actions

Treat a workflow as production code with credentials. Anchor security on the **trust boundary**, performance on the **critical path**, and correctness on the **execution graph**. Preserve behavior deliberately and prove the changed path.

## Process

Select the requested branch first: audit without edits, modify an existing workflow, or create a workflow.

### 1. Map the affected pipeline

For an existing workflow, traverse every reachable local action and reusable workflow. Deduplicate source reads by immutable identity, but analyze every call edge with its caller's ref, inputs, secrets, permission ceiling, conditions, environment, and runner. When a reusable contract can change, find every affected caller. For creation, map repository conventions and candidate components implied by the requested behavior.

For every affected branch, identify:

- events, actors, refs, fork and Dependabot behavior, default-branch semantics, and governing Actions policies
- code, expressions, artifacts, caches, inputs, and network data each job consumes
- token permissions, secrets, OIDC claims, environments, and runner access each job receives
- the job and step graph, including `needs`, conditions, outputs, matrices, background lifecycles, concurrency, and cancellation
- package manager, lockfiles, scripts, runtime versions, runner labels, and existing CI conventions
- required checks, deployment ordering, release guarantees, and the behavior users depend on
- for performance or cost work, satisfy the [target and baseline gate](references/performance.md#name-the-target-and-baseline)

Load the anchored reference as soon as its observed context matches:

| Observed context | Load |
| --- | --- |
| An entrant can influence a job with authority | [Trust-boundary map](references/security.md#map-the-trust-boundary) and [token permissions](references/security.md#token-permissions) |
| A privileged or default-branch event handles contributor influence | [Privileged events](references/security.md#privileged-events) |
| An external dependency, checkout, local action, or workflow policy matters | [Dependencies and workflow governance](references/security.md#dependencies-and-workflow-governance) |
| Secrets, OIDC, environments, or cloud credentials matter | [Secrets, OIDC, and environments](references/security.md#secrets-oidc-and-environments) |
| Artifacts or caches cross jobs, workflows, refs, or trust levels | [Artifact promotion](references/security.md#artifact-promotion) or [cache-poisoning chain](references/security.md#cache-poisoning-chain) |
| A self-hosted runner or Actions policy matters | [Runners and network reach](references/security.md#runners-and-network-reach) or [platform execution protections](references/security.md#platform-execution-protections) |
| A `run:` block is created, changed, or reviewed | [Shell semantics](references/shell.md#select-shell-semantics-explicitly), [expression boundary](references/shell.md#cross-the-expression-boundary-through-env), [failure handling](references/shell.md#handle-failure-as-data-only-when-expected), and [workflow data](references/shell.md#write-workflow-data-safely) |
| GitHub API, `gh`, or `github-script` is used | [Choose the narrowest API](references/api.md#choose-the-narrowest-interface), then its matching interface section |
| Secret-scanning custom patterns are automated | [Secret scanning custom patterns](references/api.md#secret-scanning-custom-patterns) |
| Outputs, environment writes, or summaries are used | [Workflow channels](references/api.md#workflow-channels) |
| Events, filters, expressions, failure, cancellation, or timeouts matter | [Events and refs](references/reliability.md#events-and-refs), [expressions](references/reliability.md#expressions-and-conditions), or [failure](references/reliability.md#failure-cancellation-and-time-bounds) |
| Concurrency, matrices, or reusable contracts matter | [Concurrency](references/reliability.md#concurrency), [matrices](references/reliability.md#matrices), or [reusable workflows](references/reliability.md#reusable-workflows) |
| Latency, cost, parallelism, setup, runners, caches, or artifacts matter | [Name the target and baseline](references/performance.md#name-the-target-and-baseline), then the matching performance section |

**Complete when:** the branch is selected; every affected workflow, caller, reachable local dependency, and distinct call context is accounted for; every entrant, execution edge, capability, and behavioral contract is mapped; and performance work satisfies its linked target-and-baseline gate.

### 2. Shape the safe execution graph

For an audit, compare the mapped graph with the target below and record evidence-backed divergences without editing. For modification or creation, shape this target:

- Choose the least-privileged event that supplies the required context.
- Establish a deny-by-default token baseline and grant each job only its required permissions.
- Constrain untrusted values crossing into privileged operations so they cannot control execution, authority selection, destination, or side-effect scope.
- Add only data, isolation, or lifecycle edges; start independent work as soon as its dependencies allow.
- Make required-check, failure, retry, timeout, cancellation, and concurrency semantics explicit.
- Give deployments and releases protected environments, immutable inputs, and deliberate queueing.
- Use locked dependency installs and explicit shell semantics where scripts depend on them.
- Make every external dependency immutable through the verification procedure below.
- Shape a performance change against the linked target and baseline, accounting for startup, compute, cache, and artifact-transfer work.

**Complete when:** an audit has compared every mapped edge with every loaded rule; a mutating branch has a target graph where capabilities, trust crossings, ordering, required outcomes, and deployment semantics are justified; and a performance design has an evidence-backed expected impact ready for proof.

### 3. Execute the selected branch

#### Audit

Return findings ordered by impact. Each finding includes:

- severity and exact `file:line`
- triggering event, actor, or input
- concrete failure, privilege, or performance path
- smallest safe correction
- validation evidence or the exact evidence gap

A security finding needs a concrete path from untrusted influence to a capability. Label defense-in-depth and stylistic hardening separately. A performance finding needs a measured bottleneck or a clearly labeled model of the critical path. State explicitly when no findings remain.

#### Modify

Start from observed behavior. Trace each problem through its trigger, inputs, execution path, and result. Correct it at the source with the smallest cohesive change. Preserve package-manager, lockfile, runner, naming, and workflow conventions unless one causes the problem. Update every affected caller when a reusable-workflow contract changes.

#### Create

Build the smallest execution graph that satisfies the requested behavior. Reuse established local actions, reusable workflows, package commands, and naming instead of introducing a second convention. After drafting, remap the generated graph and load every newly matching reference.

#### When an external reference changes

Treat a new action, reusable workflow, container image, or explicit upgrade as a dependency change:

1. Identify the intended release and read its release notes and migration guidance.
2. Resolve an action or reusable-workflow tag through its own repository's commit endpoint so annotated tags yield the commit SHA:

   ```bash
   repo='OWNER/REPOSITORY'
   tag='REVIEWED_RELEASE'
   gh api "repos/$repo/commits/$tag" --jq .sha
   gh api "repos/$repo/releases/tags/$tag" --jq '{tag_name,html_url,body}'
   ```

3. Verify the SHA belongs to that repository; inspect source behavior, action metadata, runtime and runner floors, permissions, and input handling relevant to this workflow.
4. Update the immutable reference and human-readable release comment together. Pin container images by digest.

An explicit upgrade authorizes the compatible upgrades it names. During unrelated work, preserve existing versions unless one blocks the requested behavior or has a relevant security defect.

**Complete when every applicable branch gate passes:**

- **Audit:** every mapped edge and loaded rule is assessed, producing evidence-backed findings or an explicit no-findings result.
- **Modify:** every requested behavior is corrected at its source, affected callers are updated, and the resulting graph is remapped.
- **Create:** every requested behavior is present in the smallest conforming graph, and the generated graph is remapped.
- **Dependency change:** every changed reference resolves to the reviewed immutable object and its runtime contract remains compatible.

### 4. Prove the workflow

1. Run the repository's configured workflow lint command; otherwise run `actionlint` against every affected workflow.
2. For a modified local action, validate its metadata with the configured schema tool and exercise its declared inputs, outputs, entrypoint, post behavior, and representative caller.
3. Run each configured Actions security analyzer and reconcile its output with the trust-boundary map; static analysis supplements path tracing.
4. Run safe underlying commands from changed `run:` steps with the repository's locked dependency state. Use a documented dry-run for release or deployment commands.
5. For performance changes, satisfy the [performance criterion](references/performance.md#performance-criterion). Report inaccessible remote execution as the exact measurement gap.
6. Recheck the complete affected graph: event and policy semantics; permissions, secrets, OIDC, environments, and runners; dependency pins; local and reusable contracts; outputs, matrices, caches, artifacts, concurrency, background barriers, and `needs`.
7. Report exact commands and outcomes. Name an unavailable runner, credential, service, policy, or tool as a verification gap.

**Complete when:** every affected workflow and modified action manifest has passing configured validation or an exact tool blocker; every changed behavior has direct execution evidence or an exact external blocker; every security conclusion names the traced path; and every optimization satisfies the linked performance criterion.
