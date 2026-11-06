# Dry-run probe output: Codex, round 4

- Host: Codex delegate, gpt-6.1-sol, reasoningEffort high, read-only
- Runtime: round-4 candidate arm, runtime manifest sha256 0d4a5d41e97079a9339ccf831f3944cec6cefe45166ea6de6e257c7c2afe7918, rendered probe sha256 a773e038...
- Probe: stacked-pr-probes/probe-entry-points.md, round 4
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases F, H, I, J (verbatim)

Provider: OpenAI; model: gpt-6.1-sol; reasoning effort: high.

Read-only dry run. All Git, GitHub, gh stack, wt, review, publication and follow-up operations below are descriptions, not executions. No subagents were started. The supplied probe's SHA-256 matches a773e038ddd8a320520cadd252a91b957d591b68a8f3f4b52f7e326a7b7bbdee.

The skill orders below describe each independent case's workflow. Other invoked skills are described without reading them, as instructed by the probe. The final inventory records every file actually read across the dry run, including the machine-local rules required by the session.

Common publication rules

Use acme/web, origin's verified SSH destination, and actor dev. Bind every proposed gh command to dev. The setup supplies the actor verification; do not switch the machine's active account. Verify exact head repository/ref/SHA, base, current branch, remote tip and exact PR immediately before mutation, and verify the result afterward. A failed or incomplete requested-base lookup blocks creation; it is not evidence of no PR.

The fixture does not supply diffs, titles, template content, body measurements, report paths, new PR numbers or validation commands. In creation commands, "$verified_title" and "$verified_body_file" denote the evidence-based title and ignored temporary body file prepared in a real run under pr's claims, review-packet and publication references. They are not invented evidence, nor files created in this dry run. Default creation is draft. Default draft state is not an instruction to keep a PR draft during follow-up.

F. Explicit manual dependent-PR route

Skills, in order: stacked-pr (already the caller; manual-chain.md, manual-create.md and stack-design.md as applicable to its creation operation), then pr Create (publication.md, review-gate.md, claims.md, review-packet.md, continuation.md). Follow-up invokes pr-followup Drive under the caller's coordination. No commit or new review invocation is needed because the branch is already pushed and the validated report covers the exact publishable range with no findings.

Requested-base lookup:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:stack/01-schema -f state=open
```

Keep only results whose head.repo.full_name is acme/web and confirm #40's exact identity. The author of #40 is not supplied; there is no need to guess it: the caller already selected the explicit manual route. pr must not hand back to stacked-pr recursively merely because the base heads an open PR.

PR-creating command:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "$verified_title" --body-file "$verified_body_file"
```

The manual owner retains topology and ensures the bottom-to-top map is accurate on every open non-native member, including #40 and the new PR, marking each current member appropriately. Use the actual returned URL/number; none is provided here.

pr returns the verified creation result to its authorized stacked-pr caller: created URL, head stack/02-api and exact SHA, base stack/01-schema, draft state, title/body and length against the measured budget, supplied review report/profile with no findings, validation evidence, command results, detail-comment URL if applicable, and any remaining work. Return to the authorized caller's loop rather than nesting another one. The stack owner arranges each new layer's initial pr-followup Drive pass and pending watch action, completes authorized repairs, then batches remaining T3 watches and yields. Creation itself does not authorize merging in this organization repository.

gh stack commands: none required by this case's already-selected manual route. Do not invent a tracked native chain requiring migration.
wt commands: none; no worktree lifecycle operation is requested.
Asked: no additional permission to create this ordinary dependent PR. Report unknown evidence rather than inventing test results.

H. Different-author release PR

Skills, in order: pr Create (publication.md, review-gate.md, claims.md, review-packet.md, continuation.md), then invoke pr-followup Drive. Do not load stacked-pr just because the explicit base differs from main.

Requested-base lookup:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:release/1.2 -f state=open
```

Filter head.repo.full_name == acme/web and inspect the returned user.login. #50 is authored by release-manager, not dev. The same-author stack trigger therefore does not apply. Neither the request nor another stated caller places this PR in a stack; no later dependent PR is specified. Retain the user's verified explicit base release/1.2.

Reuse the supplied exact-range, no-findings review report. Prepare the title/body from the actual change; publish hotfix/rounding if it is not already pushed, through origin's SSH destination, after the publication checks.

PR-creating command:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "$verified_title" --body-file "$verified_body_file"
```

Verify and register the resulting PR with the host. Report its actual URL, exact head/base, draft state, body budget, validation and reused gate result; then continue into pr-followup Drive because the user did not request create-only. Drive owns feedback/CI repair and readiness; follow the host's watch adapter when waiting. No automatic merge authority follows from a creation request in this organization repository.

gh stack commands: none.
wt commands: none.
Asked: no stack-conversion question and no additional creation permission.

I. Same-author, same-repository base PR

Skills, in order: pr for identity/scope (publication.md first, before gh), then stacked-pr before pr's Create review gate; load cli-workflow.md, cli-create.md, stack-design.md and troubleshooting.md for adopting existing branches/PRs in linked worktrees. Use the repository's stack-worktree skill together with stacked-pr, and worktrunk for worktree lifecycle if needed. The project skill's ordinary gh pr create example does not override stacked-pr's native creation owner. Later invoke pr Review gate, pr Draft-only for the submitted PR's presentation, and pr-followup Drive under the stack owner. Describe review-code-changes invocation without loading it here.

Requested-base lookup:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:feature/data-model -f state=open
```

Retain head.repo.full_name == acme/web. #12 has that exact head repository/ref and author dev, the intended author of the new PR. This satisfies pr's stack-layer trigger even though the user never says "stack" and there is only one commit on the new branch.

pr must hand off to stacked-pr with the original creation request and return its result. It must not first run its Create review gate, create an ordinary PR, or ask the user to opt into the default native route.

The handoff carries acme/web, origin, actor dev, trunk main, existing #12, its exact head/base/state, new branch feature/api-routes, requested immediate base feature/data-model, local and remote tips, dirty-state evidence and any existing review/validation evidence. A report is not supplied for this case; all work being committed is not a substitute for a review.

The owner selects CLI, because github/gh-stack v0.3.0 is installed and the user did not explicitly choose ordinary dependent PRs. The release is eleven days old and passes the default three-day cooldown. Git 2.50 and gh-stack v0.3.0 support the linked-worktree setup; WorkTrunk is not another branch manager. No installation, upgrade or manual fallback is justified by the fixture.

Plan/adopt the existing two-layer chain main <- feature/data-model (#12) <- feature/api-routes, preserving tips and verifying ancestry and incremental diffs. Inspect current tracking and GitHub membership rather than assuming either. The requested operation is creation/submission, so missing native membership alone does not require a separate conversion question. Ask before submit only if an observed active tracked layer lies outside the authorized request, or another material ambiguity appears.

Proposed gh stack help/version steps include:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh stack --version
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh stack init --help
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh stack submit --help
```

Derive the installed CLI's JSON-view and adoption forms from live help; do not invent their flags or perform them in the dry run. Use --remote origin wherever the actual command accepts it. If already tracked, preserve that ownership instead of duplicating tracking.

Invoke pr Review gate for the new layer against its immediate parent. Because no validated report is supplied in I, obtain the specified fresh Codex/newest-Sol/xhigh review-code-changes report in a real run, resolve findings, and rerun as the gate requires. There is no subagent execution in this dry run. Apply any configured size cap using pr Check cap; no cap is supplied here.

Only gh stack submit creates the missing PR and native grouping on the CLI route. The reference's current submit skeleton is:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh stack submit --remote origin --auto </dev/null
```

This is a proposed skeleton conditional on installed help confirming its flags and requested draft representation. Inspect that help before executing; do not claim an unverified draft behavior. Do not use --open to mark the reused #12 ready unless authorized; preserve its existing state. There is no gh pr create command on this route.

After submit, use pr Draft-only to prepare the newly created PR's verified title/body, then apply it through the CLI owner's gh pr edit operation without a stack map. Preserve #12's presentation except removal of a stale stack map if necessary. Verify the documented stack endpoint proves both members belong to one native stack in the correct order; PR bases or a successful submit exit alone do not prove membership.

wt commands: none are necessary to create already-existing branches' PRs from the supplied linked worktree. Keep WorkTrunk for any lifecycle/navigation actually needed, and gh-stack for tracking, submission and ancestry. Do not create redundant worktrees, run wt merge, or substitute the project's plain Git rebase/push recipe.

Report handed-off at the original pr boundary, with the routing reason. The eventual stack result reports the reused #12, newly returned PR URL, exact heads/bases, verified native membership and stack identifier, gate/validation evidence, and initial Drive results. Coordinate follow-up watches through the single stack owner; no merge is authorized merely by this request.

J. Same branch name, fork head

Skills, in order: pr Create (publication.md, review-gate.md, claims.md, review-packet.md, continuation.md), then invoke pr-followup Drive. No stacked-pr handoff is triggered by the fork result.

Requested-base lookup:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:release/1.2 -f state=open
```

The owner qualifier acme selects the target repository's branch. Keep only results whose head.repo.full_name is acme/web. #61's head is dev/web:release/1.2, so it is not the target base's PR even though its branch name and author match. A broad branch-only result must not cause a stack handoff. The verified target acme/web:release/1.2 heads no open PR.

Reuse the supplied exact-range, no-findings review report. Prepare evidence-based copy, publish the selected branch via SSH if needed, and retain the explicitly requested release/1.2 base.

PR-creating command:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "$verified_title" --body-file "$verified_body_file"
```

Verify/register the result, report its actual URL, exact head/base, draft state, body budget, validation and reused gate result, then invoke pr-followup Drive under the creation request. Do not change or stack #61. No automatic merge authority is supplied.

gh stack commands: none.
wt commands: none.
Asked: no stack-conversion question or additional creation permission.

Files actually read and SHA-256

```text
a773e038ddd8a320520cadd252a91b957d591b68a8f3f4b52f7e326a7b7bbdee  probes/arm-5.md
f8d840bfc87aae6c8b540d40f6ce2fd1026fe0972c9b2e463fa7c09b62ff94db  arms/arm-5/pr/SKILL.md
1613cb23ba546cf43ffba2185e2ea2018c110180c28f71231e836b5081695297  arms/arm-5/stacked-pr/SKILL.md
e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f  arms/arm-5/pr/references/publication.md
67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d  arms/arm-5/pr/references/review-gate.md
ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887  arms/arm-5/pr/references/claims.md
7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3  arms/arm-5/pr/references/review-packet.md
471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c  arms/arm-5/pr/references/continuation.md
132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7  arms/arm-5/stacked-pr/references/manual-chain.md
903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710  arms/arm-5/stacked-pr/references/cli-workflow.md
bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0  arms/arm-5/stacked-pr/references/manual-create.md
e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5  arms/arm-5/stacked-pr/references/cli-create.md
d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc  arms/arm-5/stacked-pr/references/troubleshooting.md
4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296  arms/arm-5/stacked-pr/references/stack-design.md
c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2  arms/arm-5/stack-worktree/SKILL.md
517081b22ef7a82fb63571fdbfba028fc4a0fac233a0649c6141357a3db09592  arms/arm-5/worktrunk/SKILL.md
```


Paths are relative to <scratch>.
