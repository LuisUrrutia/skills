# Dry-run probe output: Codex, round 3

- Host: Codex delegate, gpt-6.1-sol, reasoningEffort high, read-only
- Runtime: round-3 candidate arm, runtime manifest sha256 193d0f97546222fe6dce6b123757192c15543590f336fe14570c3a26313b938f, rendered probe sha256 23e95b58...
- Probe: stacked-pr-probes/probe-entry-points.md, round 3
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases F, H, I, J, K (verbatim)

Provider: OpenAI; model: gpt-6.1-sol; reasoning effort: high.

This is a read-only simulation. All commands below describe what would run in the independent case; no Git, GitHub, WorkTrunk, network, review child, or follow-up operation was executed. Only this requested answer file was created. The probe hash matches the supplied SHA-256.

In PR command examples, `$title` and `$body_file` denote the evidence-backed title and prepared ignored body file required by `pr`; the fixtures provide no diff, template, title, body, new PR number, or exact revision SHA from which to supply their actual values. These are command forms, not claims of publication. Each GitHub command uses the verified actor `dev`. The actor-verification prerequisite is satisfied by the common setup; otherwise it would require the bound `gh api user --jq .login` before the first write.

## F

Skills loaded, in order: `stacked-pr` (manual route), then `pr` in Create mode. The manual route uses `references/manual-chain.md` and `references/manual-create.md`, with `references/stack-design.md` when its planning step is reached. `pr` uses publication, review-gate, claims, review-packet and continuation references. Describe invoking `pr-followup` Drive for continuation without reading that other skill.

The caller has explicitly selected ordinary dependent PRs and already invokes Create. The Create exception therefore applies: `pr` does not hand back to `stacked-pr` recursively. Reuse the validated, exact-range, no-findings review report; no fresh review or commit is needed on the supplied facts. Confirm exact head repository, remote tip and base and prepare the review packet. Since `stack/02-api` is already pushed, no redundant push is needed.

PR-creating command:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "$title" --body-file "$body_file"
```

The manual-chain body carries the bottom-to-top map with PR #40 and the new PR, marking the current member. Once the new URL is known, refresh the map to contain its actual identifier and keep the maps accurate on the ordinary open chain members. Do not invent that identifier in advance. Verify the new PR's URL, exact head repository/ref/SHA, direct base, title/body and draft state; register its URL with the host.

`pr` returns `created`, with the verified new URL, head `stack/02-api`, base `stack/01-schema`, actual draft state, body character count/budget, detail-comment URL if any, validation and final review-report path/profile, commands/results and remaining work. It passes the verified publication state back to the authorized stack caller. Execute creation continuation: a linked ticket invokes `issue-workflow` under its verified policy, and Drive runs unless create-only was requested. The stack owner coordinates initial Drive passes and any remaining watches. Default draft creation is not an instruction to keep it draft forever; report the state actually verified after continuation.

No native-stack creation or `gh stack` mutation, no `wt` command, no permission question to use ordinary PRs. The manual route's extension-list observation is the supplied `gh extension list`; no install is required. No merge is authorized in this organization repository.

## H

Skills loaded, in order: `pr` in Create mode. Its publication, review-gate, claims, review-packet and continuation references apply. Describe invoking `pr-followup` Drive after publication without reading it.

Resolve the requested base `release/1.2` in the target repository and look up open PRs headed by that branch, including author and head repository. PR #50 belongs to `release-manager`, not `dev`. An open PR with a different author does not trigger the same-author stack rule. No request or caller places this PR in a stack, and no future dependent PR is specified. Do not load `stacked-pr` merely because the requested base is non-default.

Reuse the supplied validated exact-range review report with no findings, inspect the selected diff and repository conventions, prepare the packet and publish only the requested branch if it needs publishing, through the verified SSH `origin`:

```sh
git push -u origin HEAD:refs/heads/hotfix/rounding
```

This push form requires the verified current HEAD to be the selected `hotfix/rounding` head; verify the remote tip afterward. Do not assume the fixture says it was already pushed.

PR-creating command:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "$title" --body-file "$body_file"
```

Verify and register the result, then invoke Drive unless create-only. Report `created`, the actual URL, exact head/base/SHA, actual draft state, body budget, review report/profile, validation and pending continuation. Do not claim a native stack or modify #50. No `gh stack` or `wt` commands are needed, and no stack-conversion question is asked. No merge is authorized.

## I

Skills loaded, in order: `pr` in Create mode, then `stacked-pr` for the handoff. `pr` first reads its publication identity instructions and establishes identity/scope; it has not run its review gate when it transfers ownership. The receiving `stacked-pr` uses `references/cli-workflow.md`, `references/cli-create.md`, `references/stack-design.md` and the existing-PR/worktree adoption guidance in `references/troubleshooting.md`. Other owners, including `review-code-changes`, `pr` Review gate/Draft-only and `pr-followup` Drive, are invoked as described below without loading unrelated skill files for this dry run.

The decisive lookup is:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr list --repo acme/web --state open --head feature/data-model --json number,url,author,headRepository,headRepositoryOwner
```

PR #12 is authored by `dev`, and its head repository is exactly `acme/web`. Thus the requested base is the head branch of another open PR by the same author. `pr` classifies `feature/api-routes` as a stack layer even though the user did not say “stack.” Because Create was not invoked by `stacked-pr`, it invokes that owner with the original request before the review gate and returns that owner's result. It must not run `gh pr create` itself.

Handoff: create/publish the upper layer `feature/api-routes` against `feature/data-model`, retain existing PR https://github.com/acme/web/pull/12 against `main`, and adopt the verified chain `main <- feature/data-model <- feature/api-routes` as a native stack. Pass exact head/base identities and SHAs once resolved, the existing PR, committed state, repository `acme/web`, SSH remote `origin` and verified principal `dev`.

The receiving owner selects CLI: the supplied `gh extension list` reports installed `github/gh-stack` v0.3.0; its 2026-10-26 release is older than the default three-day cooldown on 2026-11-06. Git 2.50 and the extension meet the linked-worktree requirements. No installation, upgrade, manual-route fallback or conversion permission is required for this creation request. Existing branches/PR #12 do not independently select the manual route. A creation request is the exception to the conversion question required for other operations.

Before mutation, inspect current dirty paths/tips and actual local/remote tracking, preserve all existing tips, verify ancestry and read live help for each planned command. Use the supported adopt/init operation with branches ordered bottom-to-top and retain the existing tips; do not invent its flags from a cached example. The supplied facts do not establish whether adoption is already complete or whether a rebase is needed. WorkTrunk-linked worktrees are not a competing branch manager: `gh-stack` owns ancestry, pushes and membership. No worktree creation is requested or necessary; no `wt` command is inherent in the handoff.

There is no supplied validated review report in I. Before publishing the new layer, the stack owner invokes `pr` Review gate for its exact immediate-base range and obtains the prescribed fresh Codex/newest available Sol/xhigh `review-code-changes` report. It disposes of findings, reruns affected checks and re-reviews if needed; if that profile or other prerequisites are unavailable, publication is blocked rather than silently skipped. No review child is actually launched in this dry run.

Only `gh stack submit` creates the missing layer PR and native stack on this route. The documented non-interactive form is `--auto` with stdout not attached to a terminal, after verifying current help and supplying `--remote origin` on commands that accept it. Conceptually:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh stack submit --auto --remote origin
```

This is conditional on live help confirming these flags and the intended draft behavior; the dry run cannot execute that help. Do not use `--open` to change an existing PR's readiness unintentionally. If the active tracked stack contains unrelated layers, ask before submit, since non-interactive submission acts on all active layers. Otherwise the supplied two-layer creation needs no additional authorization.

After submit, invoke `pr` Draft-only for each PR the attempt created, apply its prepared title/body using bound `gh pr edit`, and carry no stack map in native-stack PRs. Reuse #12; change its body only to remove a stack map unless further changes are requested. Verify actual native membership through the documented stack endpoint, not merely local JSON or PR bases. Report the created upper PR, reused #12, verified heads/bases/states and stack number, then execute stack-coordinated Drive continuation. `pr` returns that owner's result; it does not fabricate a URL or claim success before these checks. No merge is authorized.

## J

Skills loaded, in order: `pr` in Create mode, with the same references and described Drive continuation as H.

The non-default-base lookup must filter by head repository as well as branch and author. PR #61 is authored by `dev` but headed by `dev/web:release/1.2`; its head repository is not the target `acme/web`. Exclude it when checking whether the target's base branch is another same-author PR head. The target repository has its own `release/1.2`; verify and use that branch. No stack handoff is triggered by this fork PR.

Reuse the validated exact-range review report; prepare and verify the packet. Publish `hotfix/rounding` through the verified SSH `origin` if necessary, verifying current selected HEAD and the remote result as in H:

```sh
git push -u origin HEAD:refs/heads/hotfix/rounding
```

PR-creating command:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "$title" --body-file "$body_file"
```

The head is the branch in `acme/web`, not a fork-qualified head; the base is `acme/web`'s branch, not PR #61's fork branch. Verify/register the new PR and invoke Drive unless create-only. Return `created` with actual URL, head/base/SHA, actual draft state, body budget, review evidence, validation and pending work. Do not modify #61 or ask to convert a stack. No `stacked-pr`, `gh stack` or `wt` command is needed. No merge is authorized.

## K

Skills loaded, in order: `worktrunk`, then its `references/switch.md` for the explicit base and non-persistent shell. Do not load `stack-worktree`: its description concerns a stacked-PR workflow, which this independent typo branch is not. Do not load `stacked-pr`, `pr` or `commit`: no dependent branch, publication or completed implementation is requested.

Run inside the repository, with stdin closed so an unavailable interactive approval fails rather than waits:

```sh
wt switch --create docs/typo --base main --format=json </dev/null
```

This explicitly creates the new branch/worktree off `main`. Read the returned destination path and use it as the working directory of subsequent commands because shell directory changes do not persist. Preserve normal configured hooks; do not use `--no-hooks`, `wt merge`, a raw Git worktree command or any `gh stack` operation. If an installed-version flag needs confirmation, read `wt switch --help` before executing; if `wt` is unavailable, report the blocker without substituting raw Git.

Report the created branch, actual worktree path and base `main` after verifying the result. No PR, typo edit, commit or stack is created. No question is needed on the supplied facts. If inspection finds no `.config/wt.toml`, suggest creating it under the user's standing rule; do not create it as part of this narrow request or pretend its presence is known.

## Files read and SHA-256

Relative skill paths below are relative to this exact root:

`arms/arm-4`


| File | SHA-256 |
| --- | --- |
| `probes/arm-4.md` | `23e95b58fa070b1df2e3c8f6647e8103cde9a34268ac6daf3914cfc73cb9d74c` |
| `stacked-pr/SKILL.md` | `1613cb23ba546cf43ffba2185e2ea2018c110180c28f71231e836b5081695297` |
| `pr/SKILL.md` | `868ab12421531652a4418e6f27378316c8ca591e6bf83d9788257580e67ae60d` |
| `worktrunk/SKILL.md` | `517081b22ef7a82fb63571fdbfba028fc4a0fac233a0649c6141357a3db09592` |
| `stacked-pr/references/manual-chain.md` | `132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7` |
| `stacked-pr/references/manual-create.md` | `bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0` |
| `stacked-pr/references/cli-workflow.md` | `903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710` |
| `stacked-pr/references/cli-create.md` | `e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5` |
| `stacked-pr/references/troubleshooting.md` | `d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc` |
| `stacked-pr/references/stack-design.md` | `4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296` |
| `pr/references/publication.md` | `e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f` |
| `pr/references/review-gate.md` | `67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d` |
| `pr/references/claims.md` | `ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887` |
| `pr/references/review-packet.md` | `7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3` |
| `pr/references/continuation.md` | `471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c` |
| `worktrunk/references/switch.md` | `a94d75dc3e23c3f41aafc7e6775f7b86380bd11dc9d06e6e7f1293e92621b8a2` |

Paths are relative to <scratch>.

## Case L (pr-followup eval 3), same runtime, rendered probe sha256 d35919dd...

Provider: OpenAI; model: gpt-6.1-sol; reasoning effort: high.

## Case L

This is `pr-followup` Drive scope for one ordinary PR, stopping at a verified current formal approval or a verified merge. The supplied facts do not establish a stack: `fix/null-total` targets `main`, no other open PR builds on it, and its base heads no other PR. No retained state is normal for a fresh standalone Drive task; it does not make this PR a stack.

### Skills loaded, in order

1. `pr-followup`, including `references/feedback.md`, `references/github-collection.md`, and `references/ci-and-observation.md`.
2. `pr`, for its identity/publication procedure, including `references/publication.md`. This supports the existing follow-up task; it does not start Create or its review gate.

No `stacked-pr` invocation and no `gh stack` command, including no speculative `gh stack submit` or stack-membership conversion. The extension version and repository's stack support are irrelevant to this standalone PR. Do not load `stack-worktree` or `worktrunk` just because the current checkout is WorkTrunk-managed; invoke `worktrunk` if an actual checkout operation becomes necessary. Do not load `github-actions` merely because a lint job failed; it becomes applicable if the repair changes workflow code.

### What I do first, in order

1. Select Drive scope and establish fresh task state. Resolve the exact open draft PR https://github.com/acme/web/pull/77, author, head repository/ref/SHA, base ref/SHA, merge requirements, and local checkout identity. Use the verified actor `dev` with `pr`'s binding for every `gh` command; do not switch the machine's active account. Confirm this is an authored PR rather than one the actor only reviewed, which would route to `pr-review-followup`. Preserve unrelated work and index state. Record the Drive start time and current revision. Match the checkout to the actual PR head before editing; use `worktrunk` if switching is necessary.
2. Register the PR with the host if not already registered. Continue directly under `pr-followup`: its stack handoff is conditional on an actual stack or dependent chain, which the case excludes. Do not run a stack bootstrap before repairing lint.
3. Collect all published feedback and CI evidence for the current revision, with complete pagination: inline comments and replies, resolved/outdated threads, formal reviews, conversation comments, check annotations and summaries, status contexts, and reviewer output in job logs, including successful jobs. Read the failing lint job's command, error, and relevant source. Resolve required and optional checks and expected automated reviewers. Inaccessible evidence remains unknown. Recheck head/base after collection and before acting.
4. Evaluate the lint failure and each feedback item against current code and the intended contract. Describe invoking `debug` if the cause is uncertain; investigate before editing. Make a supported root-cause repair rather than weakening lint or rerunning an unexplained failure. If workflow code must change, load `github-actions` at that boundary. Mere base advancement is not a reason to rebase this ordinary PR.
5. Verify the repair with applicable behavioral checks, build/compile, and a broader smoke path, using `verify` and the project's execution recipe as needed. Invoke `commit` for the coherent repair. Publish through `pr` Update after its identity, SSH destination, exact revision, and remote-tip checks; refresh the whole PR description from the verified published diff. Load its claims/review-packet references when composing those claims. Recollect evidence for the new remote head. For reviewer replies invoke `comment-style` before drafting, then follow each thread's disposition and verify the reply/resolution. Invoke `issue-workflow` only when linked-ticket policy or an outside-scope tracking ticket requires it.
6. Keep the PR draft while the lint failure or any other readiness prerequisite remains. Once a fresh current head/base snapshot proves all applicable CI passed, all observed feedback is settled, and no known repair/conflict/active automated reviewer remains, mark ready under the existing Drive authorization and verify the remote state. Reconcile a linked ticket's ready event if its policy requires it. Immediately collect a fresh post-ready snapshot and account for workflows/reviewers newly triggered or unblocked by ready state; draft-era evidence does not establish their completion.
7. Continue the repair/verify/publish loop until the requested stop. Since `acme/web` is an organization repository, the personal-repository automatic merge policy does not apply, and “until approval” does not authorize merging. Verify a formal approval against the current revision and repository policy; green lint or a bot success comment alone is insufficient. As this task is explicitly a test sub-agent, do not arm a host watch: return the exact PR URL, head SHA, and pending checks/review state to the parent, which owns continued observation. In a non-delegated Drive session, the owner would arm the resumable host watch after its final snapshot and yield while waiting, with the documented coverage limitations, rather than poll.

These are dry-run actions, not executed repairs or GitHub operations. No actual Git, GitHub, network, checkout, watch, or subagent action was taken.

## Files read and SHA-256

The probe digest matched the supplied value. Paths below use these exact prefixes:

- `probe/` = `probes/`
- `root/` = `arms/arm-4/`

| File | SHA-256 |
| --- | --- |
| `probe/arm-4-l.md` | `d35919dde23ddf7667097571b6d448f34c77a5ca4ba5db420ec11c43266dd9e4` |
| `root/pr-followup/SKILL.md` | `9d7b8f0615d20e6be2f42564a672ed1aa178c1dfdd0b550b6e9fb59a3dd85b6c` |
| `root/pr-followup/references/feedback.md` | `c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd` |
| `root/pr-followup/references/github-collection.md` | `38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400` |
| `root/pr-followup/references/ci-and-observation.md` | `0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c` |
| `root/pr/SKILL.md` | `868ab12421531652a4418e6f27378316c8ca591e6bf83d9788257580e67ae60d` |
| `root/pr/references/publication.md` | `e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f` |
