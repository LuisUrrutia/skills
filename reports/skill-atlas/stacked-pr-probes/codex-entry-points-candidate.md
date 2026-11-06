# Dry-run probe output: Codex, final candidate

- Host: Codex delegate, gpt-6.1-sol, reasoningEffort high, read-only
- Runtime: final candidate arm, runtime manifest sha256 ed11f25c9b81711a735db07f9744249f6d61f9882c4164b7ca3559fa10889ef8, rendered probe sha256 df55ff91...
- Probe: stacked-pr-probes/probe-entry-points.md
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases A-H (verbatim)

Provider: OpenAI; model: gpt-6.1-sol; reasoning effort: high.

This is a dry-run answer. No Git, GitHub, network, implementation, review, publication or watch operation below was executed. The probe's SHA-256 matches the supplied value. Only the requested answer file was created.

Shared conventions

`actor` below means the already verified authenticated actor; the fixture does not supply its login. Every proposed `gh` command, including reads and help, uses this binding:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh api user --jq .login
```

Before the first write, that must print the intended actor. Never switch the active account. Git transport stays on the verified SSH origin. Titles, bodies, body-file paths and unpublished revision SHAs are not supplied, so variables below represent values prepared and verified through `pr`, not invented content. These commands describe a real run; this dry run creates no body files.

For native-stack cases, load `stacked-pr` and select CLI: the installed v0.3.0 is the newest eligible release, Git 2.50 is sufficient, linked WorkTrunk worktrees are supported, and no install or upgrade is needed. WorkTrunk owns worktree lifecycle; `gh-stack` owns branch tracking, submission, cascading rebases and pushes. The project's ordinary-PR examples do not override that division.

Read live help before each planned stack command, including init/adoption, view, submit and any maintenance command. In particular:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh stack init --help
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh stack submit --help
```

The supplied files explicitly give `submit --auto` as the current non-interactive creation form and require the selected remote on commands accepting it. The PR-creating command below is therefore the documented form, subject to that mandatory live-help check, with stdout not attached to a terminal:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh stack submit --auto --remote origin
```

Omit `--open`: it also readies reused drafts. The files do not specify exact init/adoption or JSON-view argument syntax. I would derive those from help in a real run; I cannot honestly claim to have verified their exact syntax here. Before any native mutation, record branch, dirty paths, tips, trunk, remote, actor and intended remote objects. Adopt existing branches without moving their tips and verify their bottom-to-top order and ancestry.

Before publishing each new layer, invoke `pr` in Review gate mode against its immediate base, bottom-up. Invoke `review-code-changes` as that gate directs: fresh Codex context, newest available Sol, explicitly `xhigh`, exact merge-base-to-head scope; reuse a supplied validated report only if it meets that profile and scope. Fix and verify findings before publication; the stack owner restacks affected layers. Invoke `commit` at atomic implementation boundaries. These other skills are described, not read or run. No review-size cap is supplied; if one exists in actual task rules, run `pr` Check cap for each immediate-base diff before publication.

A. Existing CI layer, then new Storybook layer

Load order: `stack-worktree` for the project's worktree setup; `stacked-pr` immediately for stack ownership and native publication; `worktrunk` before any `wt` operation; `pr` for per-layer Review gate and later Draft-only presentation; `pr-followup` for Drive. The stack references are CLI workflow → CLI create → stack design and troubleshooting for existing branches/linked worktrees; worktrunk's switch reference supplies explicit-base and shell-directory handling. For actual workflow edits, invoke `github-actions`; publishing a CI change as a stack does not itself select stacked-pr's stack-aware automation route. That route applies only if the implementation changes CI because of stack state.

Plan: `main <- ci/carry-approval <- storybook/anchored-clock`. Keep the existing CI commit as layer 1; implement and test the new concern only in layer 2. Inspect first:

```sh
wt list
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
```

Continue in the returned worktree directory. Preserve the project's setup hooks; if approvals are missing, report the required interactive `wt config approvals add` step rather than bypassing hooks. Commit layer 2 through `commit`, run its behavioral/build/smoke checks, and adopt the existing bottom and new top into one CLI stack while preserving their tips. Review each layer against its parent. Do not push with the project's standalone `git push` recipe once gh-stack owns the chain.

After both layers are ready, the single `gh stack submit --auto --remote origin` command above creates both PRs, with bases `main` and `ci/carry-approval`. No `gh pr create` is used for either. If submitting the bottom first is useful, that same command initially creates only the bottom, whose membership is reported as pending; after implementing/adopting the top, a second submit reuses the bottom, creates the top and links the native stack. Never submit an unwritten or empty top as though it were implemented.

Invoke `pr` Draft-only for each newly created PR, then apply its verified title/body with actor-bound `gh pr edit "$pr_url" --title "$pr_title" --body-file "$body_file"`. Native bodies carry no manual stack map. Fresh PR reads must prove identity, revisions, bases, content and draft state; a fresh documented stack-endpoint read must prove one native stack in bottom-to-top order. CLI view and PR bases alone do not prove membership. Report created/reused URLs and stack number, plus actual checks and review results. Do not ask again whether the user wants a stack: that is explicit.

Run a Drive pass for every layer before waiting. Each pass returns head/base, results and pending watch actions to the stack owner. Complete authorized repairs, refresh affected layers and batch all remaining unwatched layer watches in one host invocation, then yield; reuse existing watches. A first layer waiting never postpones the top's first pass. As this test sub-agent, I would return those watch actions to the parent rather than arm watches myself. In this organization repository, the personal-repository merge authorization does not apply; no merge is authorized by creation alone.

B. `pr` Create called for the planned bottom

Load order: caller's existing `stack-worktree` → `pr` → `stacked-pr`; then CLI workflow/create, stack design and troubleshooting. `worktrunk` is needed if lifecycle operations arise; `pr-followup` follows submission.

`pr` recognizes the explicit planned stack even though the current base is `main`. Before its own Create review gate, it hands the whole request to `stacked-pr` and returns that owner's result. Pass `acme/web`, branch `ci/carry-approval`, head `0e5c9c4`, base `main` at `2105bea`, no existing PR, the planned second layer, publication authority and worktree context. Do not run `gh pr create`.

The owner adopts the bottom preserving its tip, invokes `pr` Review gate, and creates the bottom through the actor-bound `gh stack submit --auto --remote origin`. If layer 2 does not yet exist, report native membership pending until it does. The owner uses `pr` Draft-only for presentation and runs Drive under its coordination. Return created/handed-off or blocked with the actual URL, exact revisions, draft state, review and verification results, and pending membership; do not invent completed two-layer membership.

C. Worktrunk asked to create a dependent worktree and its PR

Load order: `worktrunk` → `stacked-pr` before the dependent worktree operation; CLI workflow/create, stack design and troubleshooting; worktrunk switch reference; then `pr` Review gate/Draft-only and `pr-followup`. `stack-worktree` may supply the project's setup guidance alongside these owners.

```sh
wt list
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
```

Use the returned directory. A new branch initially has no incremental change: implement/commit/verify the intended top before opening its PR; the prompt supplies no implementation to fabricate. Adopt the existing bottom branch and new top into gh-stack. Reuse https://github.com/acme/web/pull/2488, preserving its state and tip. The actor-bound `gh stack submit --auto --remote origin` creates the top PR and groups both natively; it does not duplicate the bottom. Its base is `ci/carry-approval`. Remove any manual map from the reused bottom, compose the new PR through `pr` Draft-only, verify native membership remotely and continue coordinated Drive. Do not use `gh pr create`, `wt merge`, or worktrunk push/rebase steps on the tracked layers.

D. Drive discovers an ordinary chain despite the originating stack request

Load order: `pr-followup` → `stacked-pr` before repairs, publication or watches; CLI workflow/create, stack design and troubleshooting; `pr` for publication identity/presentation; follow-up's feedback, collection and observation references. Load `worktrunk` only if checkout lifecycle is required.

First invoke `stacked-pr` with https://github.com/acme/web/pull/2488, https://github.com/acme/web/pull/2493 and the original stack request. This is submission of the requested stack, not a new optional conversion question. Collection/evaluation may continue meanwhile, but mutation and watches wait for its result.

The owner adopts the two branches without moving tips and submits with the actor-bound `gh stack submit --auto --remote origin`, reusing both PRs and keeping both drafts by omitting `--open`. Remove manual maps. A fresh stack-endpoint read must prove both PRs are in one ordered native stack, and PR reads must verify expected heads/bases and draft states. Record the result and the single mutation owner before continuing Drive repairs/publication/watch actions. If submission or membership verification fails, report the exact blocker and keep dependent work paused; ordinary bases alone are insufficient. Do not create replacement PRs or silently choose manual mode.

E. Standalone `fix/null-total`

Load order: `pr`, its publication/review-gate/claims/review-packet/continuation references, then `pr-followup` after verified creation. Reuse the exact-range validated review report if it meets the gate's required profile. No stack or worktree skill is needed merely to publish an already selected standalone branch.

After exact-PR recheck, verified SSH push and prepared title/body:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh pr create --repo acme/web --base main --head fix/null-total --draft --title "$pr_title" --body-file "$body_file"
```

No `gh stack` command or stack handoff. Verify/register the result, report created URL/head/base/draft, review/validation and body budget, and continue Drive unless explicitly create-only. Default draft does not mean keep-draft.

F. Explicit manual route calls `pr` Create

Load order: caller's `stacked-pr` → manual-chain → manual-create → stack-design → `pr` and its creation references; then `pr-followup` under the existing owner. Reuse the qualified exact-range validated review. Because `stacked-pr` itself invoked Create, `pr` does not recurse or redirect it to native submission.

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "$pr_title" --body-file "$body_file"
```

No `gh stack submit`. The manual owner keeps a bottom-to-top map on every open ordinary PR, including https://github.com/acme/web/pull/40 and the new PR, marking each current layer. Verify the already pushed head, immediate base and new PR state. Return `created`, URL, verified head/base, draft state, body budget, validation and review-gate report/profile to `stacked-pr`; return to its authorized Drive coordination rather than nesting an independent loop or arming a watch from this child. Report the chain as ordinary dependent PRs, as the user explicitly chose.

G. Watch wake for the pending bottom layer

Load/resume order: `pr-followup` with retained task state → feedback/github-collection and ci-and-observation references. Preserve the already established `stacked-pr` owner. If publication is required, invoke `pr` Update with its publication rules; invoke `worktrunk` only for necessary lifecycle operations. Load the owner's maintenance reference only if a maintenance operation is actually needed. Do not initiate another Create/submission handoff merely because membership is still pending.

1. Refresh https://github.com/acme/web/pull/2501, actual head/base SHAs, draft/open/merged state and current review/check state. Reconcile a newly observed ready event if applicable, then check merge/closure and valid approval stopping conditions. `acme` is an organization, so no personal-repository auto-merge policy applies.
2. Retain `api/routes` on `main` as the submitted bottom of a planned stack, with pending membership until layer 2 exists. That retained pending result expressly satisfies the follow-up routing guard; the watch comment is no reason to ask about conversion or resubmit.
3. Reread the new published review comment and its entire thread, including changed replies, and collect all current feedback channels with complete pagination. Refresh formal reviews, conversation comments, checks/annotations/summaries and reviewer logs; recheck resolved/outdated threads. Notifications are prompts to reread, not the complete inbox.
4. Evaluate against current code/evidence. Apply a supported fix, verify behavioral/build/smoke checks, invoke `commit`, and coordinate publication/cascades through the existing stack owner. Refresh the whole PR body through `pr` Update after a material push. No new PR-creating command and no unconditional `gh stack` command is required on this wake.
5. Invoke `comment-style` before any reply. For a published fix, reply with the verified revision and resolve; for a disproved claim or answered question, reply with evidence and leave open for the reviewer; for an outside-scope correct finding, invoke `issue-workflow` Publish for a tracking ticket before the required reply/resolution; for a critical decision, ask the user and pause that item. Report failed replies/resolutions as unfinished.
6. Rebuild the current snapshot and evaluate draft readiness only after all its gates pass. If readied, perform a fresh post-ready observation pass. Return this layer's result and pending watch action to the existing stack owner; refresh other affected layers before waiting. Reuse the existing watch if waiting, or let the owner batch missing watches. A child never arms one. Unwatch for a verified stop or a user handback/blocker/question under the host rules; do not poll. Report meaningful changes with actual checks and remaining work, never claim pending native membership is already complete.

H. Hotfix against another author's release PR

Load order: `pr` and its normal creation references → `pr-followup` after creation. Collect open PRs headed by the non-default base and verify https://github.com/acme/web/pull/50 is authored by `release-manager`, a different user. There is no explicit stack request, planned dependent child, or same-author base PR. The mere existence of that different-author PR does not trigger the automatic stack handoff.

After the qualified supplied review, verified SSH publication and exact-PR recheck:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "$pr_title" --body-file "$body_file"
```

No `gh stack` operation and no request to convert the release manager's PR. Verify/register and report the hotfix PR and its actual base, then continue ordinary Drive. Do not alter the other author's PR or infer merge authority.

Read inventory and SHA-256

`R` below expands exactly to `<scratch>/arms/arm-3`. Every `R/…` entry identifies one file actually read. No other scratchpad file was read. The two machine/personal rule files were read as explicitly required by the enclosing AGENTS instructions. An attempted read of `R/github-actions/SKILL.md` returned `No such file or directory`; no contents were read and there is no hash to report. No other skill source was substituted.

```text
8d16938aa89dbb3d3d10ad4c0e8e3cd889ee49cb5c98e5c71be959ebad256bd0  <personal rules file>
91dbbe6b14981106b6d7a5bc6f46e8f93f064274a4662d33c91ba5bbd971593f  <personal rules file>
df55ff91350cfcf3932932d2dfbd5c0533dc3c2ae726e65772fe8f9b4022cb77  <scratch>/probes/arm-3.md
c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2  R/stack-worktree/SKILL.md
1613cb23ba546cf43ffba2185e2ea2018c110180c28f71231e836b5081695297  R/stacked-pr/SKILL.md
5f1652ecee628096eed822ae72ca4aea79b8cbb1ad3bc988ebf009f94709470a  R/pr/SKILL.md
9d7b8f0615d20e6be2f42564a672ed1aa178c1dfdd0b550b6e9fb59a3dd85b6c  R/pr-followup/SKILL.md
517081b22ef7a82fb63571fdbfba028fc4a0fac233a0649c6141357a3db09592  R/worktrunk/SKILL.md
903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710  R/stacked-pr/references/cli-workflow.md
e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5  R/stacked-pr/references/cli-create.md
d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc  R/stacked-pr/references/troubleshooting.md
132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7  R/stacked-pr/references/manual-chain.md
bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0  R/stacked-pr/references/manual-create.md
4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296  R/stacked-pr/references/stack-design.md
8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b  R/stacked-pr/references/api-workflow.md
e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f  R/pr/references/publication.md
67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d  R/pr/references/review-gate.md
471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c  R/pr/references/continuation.md
ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887  R/pr/references/claims.md
7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3  R/pr/references/review-packet.md
c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd  R/pr-followup/references/feedback.md
38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400  R/pr-followup/references/github-collection.md
0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c  R/pr-followup/references/ci-and-observation.md
a94d75dc3e23c3f41aafc7e6775f7b86380bd11dc9d06e6e7f1293e92621b8a2  R/worktrunk/references/switch.md
```
