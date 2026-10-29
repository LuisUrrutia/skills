# Security and Trust Boundaries

Apply every section matching the workflow. Calibrate findings from the actual path between an entrant and a capability.

Base reference: [secure use of GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).

## Map the trust boundary

For each job, identify three things together:

1. **Entrants:** trigger actor, checked-out ref, event payload, workflow inputs, downloaded artifacts, restored caches, action outputs, and network responses.
2. **Execution:** shell and JavaScript interpolation, package lifecycle scripts, third-party and local actions, containers, generated code, and background processes.
3. **Capabilities:** `GITHUB_TOKEN`, secrets, OIDC, writable checkout credentials, artifact and attestation authority, deployments, internal networks, and persistent runner state.

Fork pull requests, Dependabot, issue and review text, branch names, workflow inputs, downloaded artifacts, caches, and external responses can be untrusted. Repository code is also untrusted when a privileged event checks out or executes a contributor-controlled ref.

## Token permissions

Use a workflow-level deny-by-default baseline, then grant each job only the permission keys its calls require:

```yaml
permissions: {}

jobs:
  test:
    permissions:
      contents: read

  publish:
    permissions:
      contents: read
      packages: write
      id-token: write
```

Specifying one permission sets every unspecified permission to `none`. Map current permission keys from the APIs and actions in use; examples include `contents`, `pull-requests`, `packages`, `actions`, `attestations`, `artifact-metadata`, and `vulnerability-alerts` for reading Dependabot alerts. Scope `id-token: write` to the job that exchanges the OIDC token; it does not grant repository write access by itself.

Every action in a job can access `github.token`; inspect action behavior before placing it in a job with authority.

For a job that calls a reusable workflow, job-level permissions are the maximum available to the called workflow:

```yaml
jobs:
  label:
    permissions:
      contents: read
      pull-requests: write
    uses: ./.github/workflows/label.yml
```

The caller sets the permission ceiling; the called workflow maintains or reduces it. Secret passage is a separate channel. Repository, organization, enterprise, fork, and Dependabot policies can further reduce or block the requested authority.

## Expressions and generated code

GitHub expands `${{ ... }}` before generating a `run:` script or `github-script` program. An untrusted expression embedded in either block becomes source code rather than data.

- For `run:`, apply the [shell expression boundary](shell.md#cross-the-expression-boundary-through-env).
- For `github-script`, apply the [structured JavaScript boundary](api.md#structured-api-access-with-github-script).
- For `with:`, inspect how the receiving action parses the value before passing attacker-controlled data or secrets.

Trace every interpolation from its source to the generated program and resulting capability. A restricted character set lowers exploitability but leaves the code-generation boundary in place.

## Privileged events

`pull_request_target`, `workflow_run`, `issue_comment`, and other default-branch workflows can combine untrusted influence with base-repository authority. Keep privileged jobs metadata-only, or split untrusted build and test work into an unprivileged `pull_request` workflow and a narrowly privileged follow-up.

In a public repository with no applicable Actions event policy, GitHub's default policy blocks `pull_request_target`. For a repository that used the default before general availability (2026-09-17), it runs in evaluate mode until enforcement on 2026-12-02; verify the current enforcement state for any other repository. Prefer `pull_request` where it supplies the required context. A workflow that must keep `pull_request_target` needs an event policy that explicitly allows the trigger, preferably scoped to that workflow file; check policy insights for runs the default would block.

For a privileged follow-up:

- verify the originating repository, workflow, event, conclusion, expected branch, and commit
- treat downloaded artifacts and outputs as untrusted; validate schema, identity, digest, and provenance before use
- execute base-repository code rather than contributor-controlled code
- expose only the permissions, secrets, OIDC, environment, network, and runner required for the privileged operation

A direct path from contributor-controlled code or generated source to a write token, secret, internal service, deployment, or persistent runner is a high-impact finding.

Current `actions/checkout` releases include guardrails against common fork pull-request checkouts in privileged events. Full-SHA, minor, and patch pins do not receive backports automatically. For every affected checkout, verify the selected commit contains the current guard, satisfies the runner floor, and has no unsafe opt-out. Treat the guard as defense in depth: it does not cover manual `git` or `gh` fetches, every trigger, unrelated repositories, or execution of untrusted artifacts.

Sources: [secure use of `pull_request_target`](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target), its [default policy](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target#default-policy-for-pull_request_target) and [moved enforcement date](https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/), and the [safer checkout defaults release note](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/).

## Dependencies and workflow governance

- Route every external action and reusable workflow through the [dependency verification procedure](../SKILL.md#when-an-external-reference-changes); keep its release tag or source URL in a same-line comment so update tooling can maintain it.
- A verified publisher badge establishes identity, while source review establishes behavior. Inspect release notes, action metadata, runner requirements, inputs, network access, and relevant source before giving a dependency data or capabilities.
- On GitHub.com, `$/path` resolves a local action from the repository of the running workflow or action at its running commit and needs no checkout. A `./path` reference instead executes files from the checked-out job workspace and inherits that checkout's repository and ref. `$/` is unavailable on GHES. Map the exact source before invoking local code from a privileged job. For same-repository reusable workflows, apply the [reusable-workflow contract](reliability.md#reusable-workflows). See [local-action reference semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsuses).
- Set `persist-credentials: false` on checkout by default; enable persisted credentials only for authenticated Git operations later in the job.
- Pin container images by digest when they execute in a privileged or reproducible path.
- Apply [workflow lockfiles](lockfiles.md) for coverage, onboarding, and enforcement when the repository tracks `.github/workflows/actions.lock`.
- Account for allowed-actions policies, required full-SHA policies, workflow lockfiles and the Require lockfile policy, dependency updates, dependency review, and ownership of workflow files. Report missing governance separately unless changing it is in scope.

## Secrets, OIDC, and environments

- Keep each static secret as a separate repository, organization, or environment secret; structured blobs weaken redaction.
- Prefer OIDC-issued short-lived credentials to long-lived cloud secrets.
- Bind cloud trust to the narrowest stable claims the provider supports: repository identity, audience, ref or protected environment, and reusable `job_workflow_ref` where applicable. Scope the subject to the intended branches and workflows.
- Gate deployments with protected environments and scope their secrets and OIDC trust to the deployment job.
- Decide whether a job's environment represents a deployment. Set `deployment: false` for CI or test jobs that need environment secrets, variables, branch policies, or built-in approvals without creating a deployment record.
- With `deployment: false`, wait timers and required reviewers still apply. A custom deployment protection app requires a deployment object, so an environment that enables one makes the job fail instead of requesting approval.
- Pass secrets through environment variables or standard input rather than command-line arguments.
- Treat GitHub App installation tokens as opaque strings. They now run about 520 characters with the `ghs_` prefix, so a fixed-length or legacy-pattern check, size-limited storage or header, or format-based redaction rule can reject, truncate, or leak them. Remove any `X-GitHub-Stateless-S2S-Token` request header; GitHub ignores it after 2026-11-30.
- Mask every dynamically produced or transformed sensitive value before another command can emit it. Keep sensitive values out of outputs, summaries, caches, and artifacts.
- Verify actual fork, Dependabot, bot, and environment-approval behavior instead of assuming secrets are present or absent.

Sources: [OpenID Connect security](https://docs.github.com/en/actions/concepts/security/openid-connect), [using environments without deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments#using-environments-without-deployments), and [stateless installation tokens](https://github.blog/changelog/2026-10-02-stateless-github-app-installation-tokens-rolled-out/).

## Artifact promotion

An artifact is a data channel. Establish trust from its producer, source run, commit, artifact ID, digest, and verified provenance.

- Build once, then promote the exact immutable artifact through protected environments.
- At a privilege boundary, verify the digest and an attestation or signature whose authority is unavailable to the producing low-trust job.
- Scope attestation generation to release software users will verify. Provenance becomes a control when the consumer verifies it against an explicit repository, workflow, ref or environment, and signer policy.
- Keep release and deployment authority out of the untrusted build job.
- Set the shortest retention that satisfies debugging, audit, and promotion. Use an artifact's `retention-days` to shorten one artifact; the repository, organization, or enterprise retention setting also deletes checks, workflow runs, and statuses, including third-party ones.

Sources: [artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations) and the [expanded retention release note](https://github.blog/changelog/2026-10-01-actions-retention-now-covers-checks-runs-and-statuses).

## Cache-poisoning chain

Trace each cache as `producer → scope → consumer → capability`. The chain is exploitable when attacker-controlled files or execution can write content that a more privileged workflow restores and executes. An attacker who executes in a writable cache context can steal the cache service credentials and replace entries even when the YAML has no cache-save step.

Break both ends of the chain:

- Run contributor-controlled code in isolated pull-request scope; keep shared default-branch caches writable only by trusted workflows.
- Let only trusted code write shared caches; save only rebuildable, non-sensitive paths.
- Keep release and deployment workflows cache-free with `cache-mode: none`. When a privileged workflow must restore executable content, verify independent provenance or rebuild it before execution.
- After breaking a writer edge, delete affected entries or rotate keys before a privileged consumer restores them.
- A cache key supplies namespace; independent verification supplies provenance.

GitHub's low-trust cache write restrictions close some producer edges. Verify the current event allowlist and repository or enterprise cache policy. Set `cache-mode` (`read`, `write`, `write-only`, or `none`) at workflow or job level to the least access each job needs; the cache service enforces it. An explicit `write` or `write-only` overrides the read-only default for low-trust triggers. A called reusable workflow can request `write` unless its calling job sets or inherits an explicit `cache-mode`, so cap a low-trust caller with `cache-mode: read`. A called workflow that requests more than the caller's explicit mode, including `write-only` under a `read` caller, fails validation and the run does not start. Treat every restored entry as untrusted rebuildable state.

Sources: [dependency caching security](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching), [`cache-mode` access control](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#controlling-cache-access-with-cache-mode), and the [read-only cache release note](https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers/).

## Runners and network reach

GitHub-hosted runners are ephemeral, but code in a job can still consume every capability available to that job. Public pull-request code belongs on an isolated GitHub-hosted runner or a clean, single-job ephemeral runner.

Persistent self-hosted runners expand one job's compromise into host, credential, container-socket, cloud-metadata, and internal-network persistence. Back just-in-time single-job registration with a freshly isolated environment; deregistration alone leaves reused hardware dirty.

For every self-hosted label:

- identify which repositories can target the runner group and which actors can trigger those workflows
- inventory host secrets, network routes, metadata services, shared volumes, and sibling workloads
- verify the live runner version and update policy against current GitHub.com or GHES requirements; the runner `deprecations/{version}` REST endpoint returns a version's registration and runtime deprecation dates
- on GitHub.com, a runner below 2.329.0 cannot register, and a runner that misses any runner release for more than 30 days after its publication stops receiving jobs
- rebuild stale images and templates; auto-update is effective only when runners can reach the update service

For an IP allowlist or egress firewall between runners and other services:

- Sync GitHub-hosted runner ranges from the `actions` array of `GET /meta`, which changes weekly, rather than from cloud-provider ranges. Eligible 2- and 4-core Linux runners also run on AWS, so a rule that allows only Azure or Microsoft-owned ranges, including Microsoft Entra Conditional Access, can block them.
- To expose an internal resource, prefer a larger runner with static IP addresses or private networking, which stays outside the multi-cloud pool, or a self-hosted runner; GitHub advises against allowlisting the hosted ranges.
- A runner behind an egress allowlist needs the hosts in `domains.actions` of `GET /meta`, including Actions blob storage (`productionresultssa*.blob.core.windows.net`); a missing host interrupts job logs and summaries.

Sources: [self-hosted runner REST API](https://docs.github.com/en/rest/actions/self-hosted-runners), [hosted-runner IP addresses](https://docs.github.com/en/actions/reference/runners/github-hosted-runners#ip-addresses), [multi-cloud compute](https://github.blog/changelog/2026-10-28-github-actions-adds-multi-cloud-compute-to-improve-reliability/), [Actions blob storage hosts](https://github.blog/changelog/2026-10-22-meta-api-endpoints-updated-for-actions-blob-storage/), the [minimum runner version requirements](https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/), and the [enforcement date change](https://github.blog/changelog/2026-09-28-self-hosted-runner-version-enforcement-date-has-moved).

## Platform execution protections

Inspect repository, organization, and enterprise settings that govern workflow execution: trigger and actor rules, fork approval, default token permissions, allowed actions, SHA-pinning policy, environment protection, and runner-group access. Where evaluate mode is available, evaluate workflow execution protections before enforcement. Scope centralized rules with repository properties or individual workflow files, and use the Actions policies REST API when policy is managed as code.

Platform policy forms an outer trust boundary. Pair it with least privilege and safe data handling inside every allowed workflow, and verify its enforcement state against the repository's GitHub.com plan or GHES version.

Sources: [workflow execution protections](https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution) and the [general availability release note](https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available).

## Finding calibration

- **Critical/high:** executable influence from untrusted code or data reaches secrets, write authority, deployments, internal networks, artifact-signing authority, or persistent runners.
- **High/medium:** mutable dependencies, materially excessive permissions, unsafe artifact or cache promotion, broad OIDC trust, or missing provenance checks on privileged follow-ups.
- **Low/hardening:** a safer construction with no current attacker-controlled path, narrower scoping, governance, or defense in depth.

## Security criterion

Complete when every job's entrants, execution, and capabilities are mapped; every path from untrusted influence to a capability is blocked or reported with its exact execution step and impact; and policies, permissions, secrets, OIDC claims, refs, dependencies, artifacts, caches, environments, deployment-record intent, networks, runner isolation, and update posture are accounted for.
