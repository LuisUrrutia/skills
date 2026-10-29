# Workflow Lockfiles

Apply this reference when a repository tracks `.github/workflows/actions.lock`, or when lockfile adoption or the **Require lockfile** policy is in scope.

A lockfile makes a workflow run the commits it records; it does not make those commits safe. Review each dependency through the [external-reference procedure](../SKILL.md#when-an-external-reference-changes) before locking it.

## Coverage

Onboarding is per workflow. For each workflow listed in the `workflows` section, every step-level action, including the actions that composite actions use, must have an entry, and the job runs the recorded `commit`. GitHub rejects a locked commit that is unreachable from its recorded `ref` in the action's own repository, such as a fork-only commit. After onboarding, allowed-actions policies evaluate the locked SHAs, so tag-based allowlist entries stop matching. The lockfile satisfies the full-SHA pinning policy for onboarded workflows only.

The lockfile does not cover:

- reusable workflows called at `jobs.<job_id>.uses`: pin an external one by full SHA. The lockfile of the repository that defines it covers its dependencies, and **Require lockfile** blocks the caller when that repository has not onboarded it.
- container images, including `docker://` steps, job containers, and services: pin them by digest.
- `./` local actions and the actions they use.
- inputs, secrets, and runner images.

## Change locked dependencies

`gh actions-lock` is pre-1.0 and supports GitHub.com and GHE.com, not GHES; its `--help` output is authoritative for the installed version. Use v0.3.0 or newer: earlier versions do not lock actions inside `parallel:` groups.

1. Edit `uses:` in the repository's existing form; a readable tag is valid in an onboarded workflow.
2. Run `gh actions-lock <workflow-path>...` for the affected workflows. A run without paths scans every workflow, onboards each one not yet listed, and prunes entries for deleted workflows; add `--no-onboard` to update listed workflows without onboarding others. A run with any blocking error writes nothing.
3. Resolve every finding from its `remediation` and `doc_url`. Exit code `1` means blocking findings remain; `2` means the tool failed.
   - `ref-moved` on a branch or partial version, or `tag-commit-mismatch`: review the upstream history, then run `gh actions-lock --relock`.
   - `unreachable-pin`, `misleading-sha`, or `repo-replaced`: stop and ask the user. `--accept-moved` is a human decision made after checking why the commit moved; in CI or other automation it would accept a tampered pin.
   - `retryable: true`: rerun later without editing.
4. Resolve a `local-action` error by choosing where the action's code comes from. `--migrate-local-actions` rewrites same-repository `./` references to `$/`, which runs the action at the workflow's commit instead of from the checked-out workspace; prefer it unless the job deliberately runs a local action from another ref or repository (see [local-action semantics](security.md#dependencies-and-workflow-governance)). `--ignore-local-actions` keeps `./` with a warning; in an onboarded workflow, a remote action used by that local action without its own entry fails the job at that step.
5. Review the full diff. The tool narrows a partial version such as `v4` to the exact tag it locked unless `--no-narrow` is passed. A changed `commit` is a dependency change. A changed `owner_id` or `repo_id` can signal a transfer or substitution; investigate it before accepting it. A floating ref moved back to an older commit is not detected, so review lockfile diffs or use exact tags.
6. Run `gh actions-lock --verify`. `--verify-local` checks coverage only, not provenance.

Regenerate the lockfile only with the tool. To clear an error, restore the lockfile from the default branch and rerun the tool rather than deleting it: deletion re-resolves every ref and silently accepts moved tags.

## CI and enforcement

- Add a verify job that runs `gh actions-lock --verify` on pull requests, pushes to the default branch, and a schedule that catches re-pointed tags. Give it `contents: read`, pin the extension with `gh extension install github/gh-actions-lock --pin <reviewed-tag>`, and supply a token that can read private or internal action repositories. Then lock the verify workflow itself.
- A job that regenerates and pushes the lockfile needs `contents: write`, branch rules that allow the push, and a credential with workflow-file write access. Keep that credential out of workflows that run untrusted pull-request code.
- Add `.github/workflows/actions.lock` to `CODEOWNERS` and require code-owner review.
- **Require lockfile** blocks every targeted workflow that is not onboarded, including one with no `uses:`. Pilot it in Evaluate mode, available only on GitHub Enterprise Cloud, and read Policy insights. Activate it only after `--verify` passes for every targeted workflow.
- On GHE.com, the job's `GITHUB_TOKEN` cannot read github.com actions; pass a permissionless github.com token through `GH_ACTIONS_LOCK_GITHUB_COM_TOKEN`.

Sources: [workflow dependency lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles), [locking workflow dependencies](https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies), [enforcing lockfiles](https://docs.github.com/en/actions/how-tos/administer/enforce-workflow-lockfiles), the [Require lockfile policy](https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution#require-lockfile), the [gh-actions-lock README](https://github.com/github/gh-actions-lock), its [troubleshooting guide](https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md) and [v0.3.0 release notes](https://github.com/github/gh-actions-lock/releases/tag/v0.3.0), and the [general availability release note](https://github.blog/changelog/2026-10-28-github-actions-workflow-lockfiles-are-generally-available/).

## Lockfile criterion

Complete when every affected workflow's onboarding state is deliberate; every changed entry's commit and source identity is reviewed; uncovered reusable-workflow calls and container images are pinned; every blocking finding is fixed or escalated to the user; and `gh actions-lock --verify` passes or its exact blocker is reported.
