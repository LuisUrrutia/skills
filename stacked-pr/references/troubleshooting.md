# Troubleshooting, recovery, and interoperability

Open this reference only for a matching failure or nonstandard workflow.

## Diagnose before recovery

Capture `git status --short --branch`, relevant local and remote branch tips, PR bases, and the
native stack's JSON view when available. Preserve those refs until recovery is verified.

Read live help for the failed command and its current continuation, abort, or cleanup forms. Classify
the failure from observed stderr and state rather than a cached exit-code table. Current CLI help and
GitHub documentation are authoritative for preview behavior.

Diagnosis is complete when the failing operation, last confirmed state, affected refs or PRs,
recoverable pre-operation tips, and one evidence-backed recovery branch are identified.

## Interrupted or conflicting rebase

Resolve only the files reported by Git, stage them, and use the continuation form shown by current
CLI help. Repeat for later layers. Use the current abort form when recovery must restore the
pre-operation stack, then verify the recorded tips.

Recovery is complete when no rebase remains active, the worktree is clean except for preserved
unrelated paths, every affected layer contains its parent, layer checks pass, and the stack reports
no rebase need.

## Local and remote stacks diverged

Compare both chains, branch heads, PR bases, and unique commits. When they contain different work,
show the differences and obtain the user's choice of source before mutation.

- To keep GitHub's chain, remove only stale local tracking and reacquire the remote stack through the
  current supported checkout operation.
- To keep the verified local chain, remove the conflicting grouping through the current supported
  operation, then resubmit the local order.

Divergence is resolved when local and GitHub order, heads, bases, and trunk agree and every original
commit remains reachable in the chosen chain or a preserved ref.

## Adopt existing branches or PRs

Choose ownership first:

- Local branches owned by `gh-stack`: use the current adopt/init operation with existing branches
  ordered bottom-to-top.
- Branches managed elsewhere: use the current link operation or the API route so GitHub owns only
  remote membership.
- Existing stack extension: append only above the verified current top.

Read live help before writing metadata. Linking is additive unless current documentation proves
otherwise; verify every PR base and resulting position after the operation.

Adoption is complete when the chosen owner is unambiguous, ancestry and PR bases form the intended
chain, local metadata exists only where requested, and no PR was duplicated.

## Move a tracked chain to manual

Use this section when routing or the user moves a chain that `gh-stack` tracks to the manual route.
First record every branch tip and PR base from the stack view. Then read live help for the commands
that remove local tracking and that unstack PRs on GitHub.

When the user explicitly asked for ordinary dependent PRs, unstack the eligible PRs on GitHub and
remove the local tracking together, because a retained native stack keeps its merge constraints.
Otherwise remove only the local tracking and leave the PRs, branches, and GitHub stack unchanged,
unless the request includes dissolving it. Make no Git write while local tracking remains.

After a requested dissolution, GitHub may keep some PRs stacked, for example while they are queued
for merge. The CLI then leaves local tracking in place. Report the remaining stack and obtain the
user's decision before continuing. If the user proceeds, remove local tracking with the local-only
form and confirm that the stack view no longer reports the chain before any Git write.

Migration is complete when the stack view no longer reports the chain, every recorded tip and PR
base is unchanged, the GitHub stack is in the requested state and recorded as retained or
dissolved, and the manual-chain inspection reports the same bottom-to-top order from Git ancestry
and PR bases.

## Rebuild an oversized branch

Preserve its name and tip SHA. Load [stack-design.md](stack-design.md), create the planned bottom
branch from the trunk, then replay only the paths, hunks, or commits owned by each layer. Use
`git diff`, `git show`, `git restore --source`, or a non-committing cherry-pick according to the
source history; inspect the staged diff before every commit.

Rebuild is complete only when the combined top diff equals the intended source diff, each layer
contains one planned concern, checks pass at every layer, and the preserved source ref still reaches
every original commit. Create or link PRs only after all four checks pass.

## Restructure a native stack

Preserve the old tips and combined top diff. Read current CLI and REST documentation for supported
membership edits. When no non-interactive in-place operation supports the request, dissolve only the
grouping, rewrite Git ancestry bottom-up, recreate metadata in the requested order, and reuse
eligible PRs.

Restructuring is complete when Git ancestry and PR bases prove the requested order, the combined top
diff changed only as requested, GitHub membership agrees, and old tips remain recoverable until
verification finishes.

## Worktrees and other branch managers

When worktrees, Jujutsu, Sapling, git-town, or another tool owns branches, keep navigation and
rebasing in that owner. Use the CLI link operation or API route only to publish remote stack
membership. Branches checked out in another worktree require explicit replay because Git cannot
silently move those refs.

Interoperability is complete when exactly one tool owns local ancestry, GitHub membership matches
that ancestry, every worktree points at its intended layer, and the operating procedure names the
owner for navigation, rebase, push, and remote membership.
