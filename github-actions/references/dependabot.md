# Dependabot and Dependency Automation

Apply this reference when creating or reviewing `.github/dependabot.yml`, dependency-graph coverage, Dependabot alerts, private-registry access, or workflows that run for Dependabot pull requests.

Keep these control planes separate:

| Plane | What it does | Where it is governed |
| --- | --- | --- |
| Dependency inventory | Builds the dependency graph and supplies SBOM and alert inputs | Manifest parsing, dependency submission, and repository settings |
| Alerts | Reports vulnerable or malicious dependencies | Repository, organization, or enterprise security settings and triage rules |
| Security updates | Opens pull requests for vulnerable dependencies | Security settings plus applicable `dependabot.yml` customization |
| Version updates | Opens routine maintenance pull requests | `dependabot.yml` |
| Pull-request CI | Tests and automates Dependabot pull requests | GitHub Actions workflows, token policy, and Dependabot secrets |

`dependabot.yml` does not enable the dependency graph, alerts, malware alerts, or security updates. Automatic dependency submission populates the graph; it does not configure update pull requests. Workflows triggered by a Dependabot pull request are a separate execution path from Dependabot's own update jobs.

Sources: [about `dependabot.yml`](https://docs.github.com/en/code-security/concepts/supply-chain-security/about-the-dependabot-yml-file), [automatic dependency submission](https://docs.github.com/en/code-security/reference/supply-chain-security/automatic-dependency-submission), and [Dependabot on GitHub Actions](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-on-actions).

## Map the dependency surface from current support

Inventory every manifest, lockfile, workspace, subdirectory, vendored tree, generated manifest, private source, and runtime that participates in a build or release. For each ecosystem and directory, verify in GitHub's current support tables:

- the exact `package-ecosystem` identifier and recognized manifest or lockfile
- supported package-manager and runtime versions
- whether version updates, security updates, private registries, vendoring, dependency-graph submission, and dependency scope are supported
- whether full dependency resolution needs credentials, external code execution, or network access
- the GitHub.com plan or GHES version that supplies the capability

Do not infer one capability from another. A newly supported ecosystem can support version updates without security updates, or graph submission without dependency scope. Dependency scope is also manifest-specific; do not use a `runtime` or `development` label as a reliable triage signal until the current scope table confirms it for that manifest.

For `package-ecosystem: github-actions`, map the special discovery rules. The root directory covers workflows under `.github/workflows` and root action metadata. Repository-form `uses:` references are updateable; local actions and `docker://` container actions are not. Preserve the same-line release comment when Dependabot updates a SHA-pinned action. If the current SHA has no associated tag, Dependabot can select a repository commit rather than the latest release, so verify the replacement with the [external-reference procedure](../SKILL.md#when-an-external-reference-changes). Verify private-action access separately.

For pre-commit hooks, inspect `rev` semantics rather than assuming every SHA is release-bound. A SHA without a `# frozen:` constraint can advance to the default branch head; where reproducibility matters, use the supported version constraint and verify the changed SHA. For every ecosystem, fail with an exact coverage gap when the repository's package-manager or runtime version is below the current Dependabot floor.

Do not copy GitHub's ecosystem catalog into a configuration or report. Re-read the live tables, because supported ecosystems, versions, manifests, and capability combinations change independently.

Sources: [supported ecosystems and repositories](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories) and [supported ecosystems and manifests for dependency scope](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-manifests-for-dependency-scope).

Complete this gate when every build and release manifest, lockfile, ecosystem, directory, private source, and runtime has a current capability record or an exact unsupported-surface gap.

## Establish complete inventory and alert coverage

Enable and verify the dependency graph before treating an absence of alerts as evidence. Compare the graph with the repository inventory: a manifest missing from the graph is a coverage gap, not proof that it has no vulnerable dependencies.

Use automatic dependency submission only for a currently supported ecosystem whose build-time resolution adds material data beyond static analysis. GitHub currently resolves duplicate manifest data in this priority: user submission, Dependabot graph jobs, automatic submission, then static analysis. Verify the live order and manifest identity instead of assuming the newest workflow wins. If GitHub generates a submission workflow, inspect its runner label, network access, credentials, cache behavior, and manifest identity like any other workflow. On a self-hosted runner, narrow the runner group and use read-only package credentials.

Verify these settings independently:

- dependency graph
- Dependabot alerts
- Dependabot malware alerts, where the current platform and ecosystem support them
- Dependabot security updates
- grouped security updates, if deliberately selected

Treat malware as an incident signal, not a routine version-update request. Remove or downgrade the package immediately, determine whether it executed in developer, CI, build, or release environments, invalidate affected caches and artifacts, and rotate credentials that could have been exposed. Account for internal-package name collisions before dismissing a malware alert.

Sources: [automatic dependency submission](https://docs.github.com/en/code-security/reference/supply-chain-security/automatic-dependency-submission), [configuring Dependabot alerts](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-dependabot-alerts), [configuring security updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates), [Dependabot malware alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/malware-alerts), and the [malware ecosystem expansion](https://github.blog/changelog/2026-07-28-dependabot-alerts-on-malicious-packages-across-more-ecosystems/).

## Shape `dependabot.yml` from the inventory

Place `.github/dependabot.yml` or `.github/dependabot.yaml` on the default branch. Use version `2`, then create one intentional `updates` block for each supported ecosystem and manifest location. Use `directory` for one location or `directories` only where the current ecosystem supports it. Exclude generated fixtures, examples, or vendored content only after proving they are not shipped, executed, or used to resolve production dependencies.

For each block, justify:

- cadence and time zone from release velocity, review capacity, and CI cost
- directory coverage and the manifests Dependabot is expected to discover
- grouping boundaries from ownership, compatibility, rollback, and test coverage
- cooldown from supply-chain risk and the cost of delaying routine fixes
- pull-request backlog limits and ownership
- private registry selection and credential scope
- labels, commit-message, and branch-name customization required by repository automation

The following is a shape, not a universal configuration. Add only blocks whose manifests exist, and confirm every option against the current options reference:

```yaml
version: 2

updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      routine-minor-and-patch:
        applies-to: "version-updates"
        patterns:
          - "*"
        update-types:
          - "minor"
          - "patch"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      routine-actions:
        applies-to: "version-updates"
        patterns:
          - "*"
        update-types:
          - "minor"
          - "patch"
```

This keeps major version updates separate for focused review. It does not group security updates, configure private registries, or claim that weekly is right for every repository.

Source: [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference).

### Keep security fast and routine updates reviewable

GitHub currently applies a three-day default cooldown to version updates and bypasses that default for security updates. Re-read the current option before relying on that duration; configure `cooldown` explicitly when the delay is an operational contract. A cooldown reduces exposure to newly published mistakes or short-lived attacks. It does not protect against an established malicious release, compromised build tooling, or a dependency whose dangerous version remains published.

Use grouping to reduce review and CI noise without hiding risk:

- group related minor and patch version updates that share owners and tests
- leave major, production-critical, runtime, build-system, and low-confidence changes separate unless they form one tested release unit
- set `applies-to` explicitly; do not rely on its default
- order groups from specific to broad because the first matching group wins
- use cross-directory grouping only for the same ecosystem and a coherent repository contract
- use multi-ecosystem groups only when the components must be tested, released, and rolled back together
- give security updates their own narrow groups; never mix security and version updates

A larger group saves CI starts but widens the diff, rollback unit, and diagnostic search space. Prove that the grouped test suite covers the interaction, and split a failed group before bypassing a check.

Use `open-pull-requests-limit` as backpressure for version updates, not as a cure for an unreviewable queue. It does not replace ownership or alert response. If the repository wants security updates but no routine version PRs for an ecosystem, verify the current documented `0` behavior and preserve the security-update settings.

Apply `allow` before `ignore` in the mental model; an update matching both is ignored. Every ignore or exclusion that can affect a security update needs an exact package or range, reason, owner, expiry or review date, and compensating control. Prefer a temporary, reviewable exception to a broad wildcard.

Keep updates on the default branch unless the repository has a concrete release-flow requirement. `target-branch` moves version updates to another branch, but security update PRs still target the default branch and the block's customization no longer applies to them. Treat this as a coverage split, not merely a branch-name choice.

Customize Dependabot branch names only to satisfy Git ref limits or existing CI, ruleset, and ticketing contracts. Validate the rendered prefix, separators, template fields, group suffix, and maximum length. Do not build new automation around retired Dependabot merge, close, reopen, or cancel-merge comment commands; use native pull-request UI, GitHub CLI, or API behavior.

Sources: [optimizing version-update pull requests](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates), [customizing Dependabot pull requests](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs), [grouped security updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates), and [retired Dependabot comment commands](https://github.blog/changelog/2026-01-27-changes-to-github-dependabot-pull-request-comment-commands/).

## Authenticate private dependencies narrowly

Prefer organization-managed registry configurations when several repositories share one trust policy. Limit each configuration to selected repositories when practical. Prefer OIDC-issued short-lived credentials for currently supported providers; otherwise use a read-only token that can download only the required package namespace. Verify GitHub.com, plan, provider, and GHES support before selecting OIDC.

For repository configuration:

- define only required registries at the top level and attach only the required names to each update block; avoid `registries: "*"` without a coverage reason
- set npm registry scope and base-replacement behavior explicitly; never rely on `.npmrc` inference from a lockfile
- distinguish package-registry access from private Git repository access
- verify cross-organization internal-repository access at the enterprise policy boundary; broad internal access is not least privilege
- keep registry credentials out of the file and use Dependabot secrets with the exact supported interpolation syntax

Package managers may execute code while resolving dependencies. Registry access disables external code execution by default for the ecosystems that expose the `insecure-external-code-execution` option. Set it to `allow` only when the update cannot otherwise resolve, after tracing which code runs and which configured registries it can access. Record the exception, constrain credentials, and test it on an isolated runner.

Dependabot's service jobs are not ordinary repository workflows. GitHub documents that Dependabot update workflows can run even when Actions is disabled or ordinary allowed-actions policy would reject them. Do not treat the repository's Actions allowlist as a control over package-manager code inside Dependabot; use registry scope, external-code settings, dependency scripts, and runner isolation.

Sources: [private registries for Dependabot](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-access-to-private-registries), [organization registry configurations](https://docs.github.com/en/rest/private-registries/organization-configurations), [explicit npm registry scope](https://github.blog/changelog/2026-06-30-dependabot-no-longer-infers-npmrc/), [cross-organization internal access](https://github.blog/changelog/2026-05-11-cross-org-dependabot-access-for-internal-repositories/), and [Dependabot's Actions policy behavior](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions#dependabot-and-github-actions-policies).

## Preserve the Dependabot pull-request trust boundary

Treat bot authorship as identity, not as proof that updated source, packages, install scripts, generated code, or artifacts are safe. A Dependabot pull request can cause newly selected third-party code to execute during CI.

For Dependabot-triggered repository workflows, map the actual event and platform settings. GitHub applies fork-like restrictions to several events: `GITHUB_TOKEN` is read-only by default, Actions secrets are unavailable, and values in the `secrets` context come from Dependabot secrets. A manual rerun keeps the original privilege model. Do not broaden permissions or duplicate powerful Actions secrets into Dependabot secrets merely to make a failing job green.

When a Dependabot PR needs private dependencies:

- give the test job only read access to the required registry namespace
- store the same secret name in both stores only if ordinary and Dependabot runs genuinely need identical read-only access
- keep publish, release, deployment, signing, and cloud-write credentials out of dependency-update tests
- split privileged follow-up work from untrusted dependency installation and build output

Do not use `pull_request_target` to check out or execute the Dependabot head, updated lockfile, generated code, or artifacts. A metadata-only job can label or enable native auto-merge after verifying the repository, actor, pull-request author, update metadata, base branch, and required checks.

Auto-merge only a narrowly selected update class with required status checks and branch protection or rulesets enforced. Use immutable action references, review release and lockfile changes, and preserve human review for major, production, build-tool, native-code, grouped, low-test-confidence, or malware-remediation changes. If a merge queue requires a stronger GitHub App or user token, treat that credential as a separate privileged capability and do not expose it to the test job.

Sources: [Dependabot on GitHub Actions](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-on-actions), [troubleshooting Dependabot-triggered workflows](https://docs.github.com/en/code-security/reference/supply-chain-security/troubleshoot-dependabot/dependabot-on-actions), and [automating Dependabot with Actions](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions).

## Triage alerts by exploitability and ownership

Do not sort only by severity. Combine:

- malware or vulnerability type
- direct versus transitive relationship
- runtime versus development scope, only where the manifest supplies reliable scope
- exposed and reachable use in the repository
- fix availability and breaking-change cost
- severity and EPSS probability
- internet, privilege, and data exposure

Use alert filters to form operational queues, then assign a named owner or team. EPSS changes daily and estimates exploitation probability; it does not replace code reachability or business impact. An AI coding agent can prepare a draft remediation, but its assignment or pull request is not closure evidence. Require tests and review of the selected version, release provenance, manifest, lockfile, generated files, and behavior.

A dismissal or snooze needs a reason tied to the affected path, evidence, owner, and review date. Use delegated alert-dismissal review where governance requires separation of duties. Audit enablement changes, assignments, dismissals, and configuration changes; keep auto-triage rules narrow enough that they do not silently normalize a persistent risk.

Sources: [Dependabot alert filters](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-alerts-filters), [dependency-scope support](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-manifests-for-dependency-scope), [agent-assisted remediation](https://github.blog/changelog/2026-04-07-dependabot-alerts-are-now-assignable-to-ai-agents-for-remediation/), [Dependabot audit events](https://github.blog/changelog/2026-02-10-track-additional-dependabot-configuration-changes-in-audit-logs/), and [delegated dismissal review](https://github.blog/changelog/2025-12-19-you-can-now-require-reviews-before-closing-dependabot-alerts-with-delegated-alert-dismissal/).

## Validate operation, not only YAML

1. Parse the file as YAML and validate it with the repository's configured schema or Dependabot tooling. Confirm exact option names, types, group ordering, directory patterns, and registry references against the current options reference.
2. Verify the file is on the default branch and every intended manifest or lockfile maps to a deliberate update block. Confirm that overlapping coverage is intentional and supported. Record unsupported or intentionally excluded surfaces.
3. Verify dependency graph, alerts, malware alerts, security updates, grouped-security settings, private-registry configurations, and enterprise access policies independently in the platform.
4. Inspect one Dependabot job log per affected block. Confirm manifest discovery, package-manager and runtime compatibility, version resolution, registry authentication, external-code behavior, and the expected PR or documented no-update result.
5. Inspect the dependency graph source and completeness after static or automatic submission. Resolve duplicate or stale submissions by manifest identity rather than assuming the latest workflow won.
6. Exercise every affected repository workflow on a Dependabot pull request. Confirm actor and ref checks, read-only token behavior, Dependabot-secret availability, required checks, branch protection, labels, and auto-merge gates.
7. Review the first generated PR shape: target branch, group membership, branch length, commit message, labels, owners, release notes, manifest and lockfile diff, test coverage, and rollback unit.
8. Report inaccessible repository settings, org policy, GHES version, private registry, runner, job log, or live pull request as an exact verification gap.

Source: [Dependabot job logs](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-job-logs).

## Dependabot criterion

Complete when every build and release dependency surface is either covered by a currently supported graph, alert, security-update, and version-update path or recorded as an exact gap; every update block has intentional scope, cadence, grouping, cooldown, backlog, target-branch, and registry behavior; private access is least privilege and package-manager execution is contained; alert ownership and dismissal governance are explicit; affected Actions workflows preserve the Dependabot trust boundary; and YAML validation, job logs, graph evidence, and representative pull-request behavior prove the configuration or name the exact external blocker.
