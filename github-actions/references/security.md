# Security and Trust Boundaries

Apply every section matching the workflow. Calibrate findings from the actual path between an entrant and a capability.

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

Specifying one permission sets every unspecified permission to `none`. Map current permission keys from the APIs and actions in use; examples include `contents`, `pull-requests`, `packages`, `actions`, `attestations`, and `artifact-metadata`. Scope `id-token: write` to the job that exchanges the OIDC token; it does not grant repository write access by itself.

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

For a privileged follow-up:

- verify the originating repository, workflow, event, conclusion, expected branch, and commit
- treat downloaded artifacts and outputs as untrusted; validate schema, identity, digest, and provenance before use
- execute base-repository code rather than contributor-controlled code
- expose only the permissions, secrets, OIDC, environment, network, and runner required for the privileged operation

A direct path from contributor-controlled code or generated source to a write token, secret, internal service, deployment, or persistent runner is a high-impact finding.

Current `actions/checkout` releases include guardrails against common fork pull-request checkouts in privileged events. Full-SHA, minor, and patch pins do not receive backports automatically. For every affected checkout, verify the selected commit contains the current guard, satisfies the runner floor, and has no unsafe opt-out. Treat the guard as defense in depth: it does not cover manual `git` or `gh` fetches, every trigger, unrelated repositories, or execution of untrusted artifacts.

## Dependencies and workflow governance

- Route every external action and reusable workflow through the [dependency verification procedure](../SKILL.md#when-an-external-reference-changes); keep its release tag or source URL in a same-line comment so update tooling can maintain it.
- A verified publisher badge establishes identity, while source review establishes behavior. Inspect release notes, action metadata, runner requirements, inputs, network access, and relevant source before giving a dependency data or capabilities.
- A local action referenced as `./path` executes files present in the job workspace. Map the checked-out repository and ref, and invoke only trusted workspace code from a privileged job. For same-repository reusable workflows, apply the [reusable-workflow contract](reliability.md#reusable-workflows).
- Set `persist-credentials: false` on checkout by default; enable persisted credentials only for authenticated Git operations later in the job.
- Pin container images by digest when they execute in a privileged or reproducible path.
- Account for allowed-actions policies, required full-SHA policies, dependency updates, dependency review, and ownership of workflow files. Report missing governance separately unless changing it is in scope.

## Secrets, OIDC, and environments

- Keep each static secret as a separate repository, organization, or environment secret; structured blobs weaken redaction.
- Prefer OIDC-issued short-lived credentials to long-lived cloud secrets.
- Bind cloud trust to the narrowest stable claims the provider supports: repository identity, audience, ref or protected environment, and reusable `job_workflow_ref` where applicable. Scope the subject to the intended branches and workflows.
- Gate deployments with protected environments and scope their secrets and OIDC trust to the deployment job.
- Pass secrets through environment variables or standard input rather than command-line arguments.
- Mask every dynamically produced or transformed sensitive value before another command can emit it. Keep sensitive values out of outputs, summaries, caches, and artifacts.
- Verify actual fork, Dependabot, bot, and environment-approval behavior instead of assuming secrets are present or absent.

## Artifact promotion

An artifact is a data channel. Establish trust from its producer, source run, commit, artifact ID, digest, and verified provenance.

- Build once, then promote the exact immutable artifact through protected environments.
- At a privilege boundary, verify the digest and an attestation or signature whose authority is unavailable to the producing low-trust job.
- Scope attestation generation to release software users will verify. Provenance becomes a control when the consumer verifies it against an explicit repository, workflow, ref or environment, and signer policy.
- Keep release and deployment authority out of the untrusted build job.
- Set the shortest retention that satisfies debugging, audit, and promotion.

## Cache-poisoning chain

Trace each cache as `producer → scope → consumer → capability`. The chain is exploitable when attacker-controlled files or execution can write content that a more privileged workflow restores and executes. An attacker who executes in a writable cache context can steal the cache service credentials and replace entries even when the YAML has no cache-save step.

Break both ends of the chain:

- Run contributor-controlled code in isolated pull-request scope; keep shared default-branch caches writable only by trusted workflows.
- Let only trusted code write shared caches; save only rebuildable, non-sensitive paths.
- Keep release and deployment workflows cache-free. When a privileged workflow must restore executable content, verify independent provenance or rebuild it before execution.
- After breaking a writer edge, delete affected entries or rotate keys before a privileged consumer restores them.
- A cache key supplies namespace; independent verification supplies provenance.

GitHub's low-trust cache write restrictions close some producer edges. Verify the current event allowlist and repository or enterprise cache policy. Use restore-only operations where the service grants read-only access, and treat every restored entry as untrusted rebuildable state.

## Runners and network reach

GitHub-hosted runners are ephemeral, but code in a job can still consume every capability available to that job. Public pull-request code belongs on an isolated GitHub-hosted runner or a clean, single-job ephemeral runner.

Persistent self-hosted runners expand one job's compromise into host, credential, container-socket, cloud-metadata, and internal-network persistence. Back just-in-time single-job registration with a freshly isolated environment; deregistration alone leaves reused hardware dirty.

For every self-hosted label:

- identify which repositories can target the runner group and which actors can trigger those workflows
- inventory host secrets, network routes, metadata services, shared volumes, and sibling workloads
- verify the live runner version and update policy against current GitHub.com or GHES requirements
- rebuild stale images and templates; auto-update is effective only when runners can reach the update service

## Platform execution protections

Inspect repository, organization, and enterprise settings that govern workflow execution: trigger and actor rules, fork approval, default token permissions, allowed actions, SHA-pinning policy, environment protection, and runner-group access. Where workflow-execution rulesets are available, evaluate them before enforcement and scope centralized rules with repository properties.

Platform policy forms an outer trust boundary. Pair it with least privilege and safe data handling inside every allowed workflow, and verify its enforcement state against the repository's GitHub.com plan or GHES version.

## Finding calibration

- **Critical/high:** executable influence from untrusted code or data reaches secrets, write authority, deployments, internal networks, artifact-signing authority, or persistent runners.
- **High/medium:** mutable dependencies, materially excessive permissions, unsafe artifact or cache promotion, broad OIDC trust, or missing provenance checks on privileged follow-ups.
- **Low/hardening:** a safer construction with no current attacker-controlled path, narrower scoping, governance, or defense in depth.

## Security criterion

Complete when every job's entrants, execution, and capabilities are mapped; every path from untrusted influence to a capability is blocked or reported with its exact execution step and impact; and policies, permissions, secrets, OIDC claims, refs, dependencies, artifacts, caches, environments, networks, runner isolation, and update posture are accounted for.

## Official sources

https://docs.github.com/api/article/body?pathname=/en/actions/reference/security/secure-use

https://docs.github.com/api/article/body?pathname=/en/actions/reference/security/securely-using-pull_request_target

https://docs.github.com/api/article/body?pathname=/en/actions/concepts/security/openid-connect

https://docs.github.com/api/article/body?pathname=/en/actions/concepts/security/artifact-attestations

https://docs.github.com/api/article/body?pathname=/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows

https://docs.github.com/api/article/body?pathname=/en/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/actions-policies/workflow-execution-protections

https://docs.github.com/api/article/body?pathname=/en/rest/actions/self-hosted-runners

https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/

https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/
