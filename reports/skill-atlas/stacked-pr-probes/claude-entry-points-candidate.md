# Dry-run probe output: Claude Code, final candidate

- Host: Claude Code general-purpose subagent, claude-opus-5-5, default effort, read-only
- Runtime: final candidate arm, runtime manifest sha256 ed11f25c9b81711a735db07f9744249f6d61f9882c4164b7ca3559fa10889ef8, rendered probe sha256 df55ff91...
- Probe: stacked-pr-probes/probe-entry-points.md
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases A-H (verbatim)

Model: Claude Opus 5.5 (claude-opus-5-5)

Notation: `$B` stands for the actor binding `GH_TOKEN="$(gh auth token --hostname github.com --user <actor> || echo none)"`, where `<actor>` is the verified actor. Every `gh` command (including `gh stack`) carries it (pr/references/publication.md "GitHub account"). No review-size cap is set in any case, so `pr` Check cap mode is never invoked. No case names a ticket, so `issue-workflow` is never invoked.

## A. Stacked PR from `ci/carry-approval` plus new `storybook/anchored-clock`

**Skills loaded, in order**
1. `stacked-pr`. The work will be published as stacked PRs. Its description says to load it together with any project skill that also covers stacks, because it opens the PRs as a native GitHub stack. Route files: `references/cli-workflow.md`, `references/cli-create.md`, `references/stack-design.md`, and `references/troubleshooting.md` (to adopt the existing branch and handle worktrees).
2. `stack-worktree` (project skill). Used only for worktree setup: `wt list`, `wt switch --create` with a base, the `.config/wt.toml` pre-start hooks, and port overrides. Its PR mechanics do not apply: `gh pr create --base <parent>`, `git push -u origin`, and the "Stacked on #N" line in the description. stacked-pr says a project skill that opens layers as ordinary PRs does not select the manual route, and the selected route owns PR creation, pushes, rebases and PR bodies.
3. `worktrunk` plus `references/switch.md`, because layer 2 needs a `wt` worktree with a non-default base. worktrunk tells you to load `stacked-pr` first, and that is already done.
4. `pr`, in Review gate mode for each new layer, then in Draft-only mode for each PR that submit creates.
5. `pr-followup`, in Drive mode for each layer. stacked-pr's "Follow up layers" section requires this.

`commit` (layer-2 commits), `review-code-changes` (inside the gate) and `comment-style` (any Drive replies) are invoked, not read.

**Routing record.** Operation: create a 2-layer native stack and adopt the existing branch as the bottom layer. Route: CLI. The deciding observation is `gh extension list` → `gh stack github/gh-stack v0.3.0`; the user asked for a stacked PR, not ordinary dependent PRs. Repository `acme/web`, trunk `main`, push remote `origin` (SSH), verified actor. Before any mutation, record the current branch, dirty paths, the tip of `ci/carry-approval`, and `origin/main`.

**Live contract** (cli-workflow.md): `git status --short --branch`, `git remote -v`, `git --version` (2.50 ≥ 2.36), `$B gh auth status`, `$B gh extension list`, `$B gh release list -R github/gh-stack --exclude-pre-releases --json tagName,publishedAt`.
- v0.3.0 was published 2026-10-26, 11 days ago, which is past the 3-day cooldown. It is the eligible release and the installed one, so no upgrade is needed.
- v0.3.0 is at least v0.2.0, so the stack may span worktrees.
- Read `gh stack {init,add,view,rebase,push,submit} --help` and pass `--remote origin` wherever it is accepted.

**Plan** (stack-design.md):
- L1 `ci/carry-approval`: the existing CI change.
- L2 `storybook/anchored-clock`: the new change. It may take inputs only from L1 or `main`.
- Record each layer's verification command.
- If L2 turns out not to depend on L1, stack-design says it belongs in a separate stack. Raise that with the user before building.

**Build and adopt**
- `wt list`
- `wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json`
  - Use the explicit parent, because WorkTrunk otherwise bases the branch on `main` (troubleshooting.md "Worktrees").
  - Take the worktree path from the JSON output.
  - The pre-start hooks run automatically. If they need approval, ask the user to run `wt config approvals add` in an interactive terminal.
- Adopt both branches bottom-to-top with the adopt form of `gh stack init` that live help shows: trunk `main`, then `ci/carry-approval`, then `storybook/anchored-clock`. Keep the existing tips and verify ancestry first.
- Implement L2 in its worktree. Stage explicit paths, commit through `commit`, and run the layer checks.
- Build is complete when the JSON stack view shows the planned order, the ancestry is correct, the checks pass, and no rebase is needed.

**Review gate.** Invoke `pr` in Review gate mode bottom-up:
- L1: `<merge-base origin/main>..ci/carry-approval`
- L2: `ci/carry-approval..storybook/anchored-clock`

Each review runs in a fresh Codex context with the newest Sol model at `xhigh` (in T3 Code, a `delegate_task` child). Fixes to L1 cascade with the current `gh stack rebase` form before L2 is reviewed.

**Command that creates both PRs** (one command; no `gh pr create`, no `git push -u`):
```
$B gh stack submit --auto --remote origin | cat
```
- Stdout is not a TTY.
- No `--open`, so both PRs are drafts, which is `pr`'s default.
- It pushes both branches and creates PR1 (`ci/carry-approval` → `main`), PR2 (`storybook/anchored-clock` → `ci/carry-approval`) and the native stack.

If submit reports stacks as unavailable, read the stack-list endpoint and the repository as the same principal. Only a 404 from the list while the repository read succeeds counts as unavailable. Decline any offer to create regular PRs.

**After submit**
1. Invoke `pr` Draft-only for each new PR, then run `$B gh pr edit <url> --title <t> --body-file <f>`. The bodies have no stack map and no "Stacked on" line.
2. Do a fresh `gh pr view` read of the heads, bases, titles, bodies and draft state.
3. Read the documented stack endpoint (https://docs.github.com/en/rest/pulls/stacks) to prove that both PRs are in one native stack, bottom-to-top.
4. If the stack is missing or split, classify the stderr and rerun submit once. If it is still wrong, report a blocker with the PR URLs.

**Follow-up**
- stacked-pr stays the single mutation owner. It runs a `pr-followup` Drive pass for PR1 and for PR2. Each pass returns its head/base, result and pending watch action to stacked-pr and does not arm a watch.
- Repairs are pushed through gh-stack (cli-maintain), and bodies are updated through `pr` Update.
- The retained state records native membership, so later wakes do not re-submit.
- In T3 Code, stacked-pr arms both `watch_pull_request` watches in one batched invocation and ends the turn.
- Drive marks each settled draft ready with `gh pr ready <url>`.
- `acme/web` belongs to an org, so the personal-repository merge policy does not apply. Drive stops at a current formal approval for each PR. A merge needs the user's explicit approval of the exact PR set and merge method; stacked-pr then lands the PRs bottom-up.

**Reported:** the routing record, both PR URLs and numbers, the stack number, the heads, bases and draft states, the gate results, and Drive status `waiting`. **Asked:** only the L2-dependency question, if it arises.

## B. `pr` Create for the bottom layer, called by a caller that loaded `stack-worktree`

**Skills:** `pr` (invoked) → `stacked-pr` (handoff).

`pr` resolves the operation from the request alone:
- The request places this PR in a stack ("Bottom of a 2-layer stack"), and another PR will build on it. This makes it a stack layer, which belongs to `stacked-pr`, because `gh pr create` would leave it outside GitHub's native stack.
- `stacked-pr` did not invoke this Create. So, before the review gate, `pr` invokes `stacked-pr` with the request and returns its result.

`pr` itself runs no review gate, no push, no `gh pr create` and no `gh stack` command.

**Handoff payload:** branch `ci/carry-approval`, commit 0e5c9c4 on `origin/main` 2105bea, base `main`, bottom of a planned 2-layer stack, draft by default. The caller's `stack-worktree` keeps worktree setup only.

**What stacked-pr then does**
1. Routes to CLI from `gh extension list` (v0.3.0). stack-worktree does not select the manual route.
2. Adopts `ci/carry-approval` with the `gh stack init` adopt form.
3. Invokes `pr` Review gate on `2105bea..0e5c9c4`.
4. Creates the PR with `$B gh stack submit --auto --remote origin | cat`.
5. Invokes `pr` Draft-only and applies the title and body with `gh pr edit`. The body has no stack map.
6. Reports a single layer with native membership **pending** until layer 2 exists.
7. Runs the Drive pass.

**Return:** `pr` returns `handed-off` and passes stacked-pr's result (URL, head/base, draft state, pending membership, gate result) back to the caller.

## C. `worktrunk`: stacked worktree for `storybook/anchored-clock` on PR #2488

**Skills, in order**
1. `worktrunk` (invoked). For a stacked branch, it says to load `stacked-pr` first; `wt` handles only the worktree.
2. `stacked-pr` → `cli-workflow.md`, `cli-create.md`, `stack-design.md`, `troubleshooting.md` (to adopt the untracked #2488 and handle worktrees).
3. `stack-worktree` (project hooks and setup only).
4. worktrunk `references/switch.md`.
5. `pr` (Review gate for the new layer, then Draft-only for the new PR).
6. `pr-followup` (Drive).

**Route:** CLI (`gh extension list` → v0.3.0; nobody asked for ordinary PRs). #2488 is not tracked by any tool, so the mutation first adopts it, keeping its tip.

**Worktree commands**
```
wt list
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
```
- Use the explicit base, because WorkTrunk otherwise uses `main`.
- Use the JSON path as the working directory for later commands.
- The `.config/wt.toml` pre-start hooks run.
- Do not use `wt merge` or `wt step` rebase/push/squash on these layers.

**Then**
1. Adopt bottom-to-top with the adopt form of `gh stack init`: `ci/carry-approval` (#2488, tip unchanged), then `storybook/anchored-clock`.
2. Implement and commit L2 through `commit`, then run the checks.
3. Invoke `pr` Review gate on `ci/carry-approval..storybook/anchored-clock`.

**The PR is created by** `$B gh stack submit --auto --remote origin | cat`, not by `gh pr create`. Submit:
- reuses #2488;
- creates the draft PR `storybook/anchored-clock` → `ci/carry-approval`;
- links both PRs into one native stack.

Leave out `--open`, because it would also mark #2488 ready.

**After submit**
1. Invoke `pr` Draft-only for the new PR and apply it with `gh pr edit`.
2. Change #2488 only to remove a stack map if it has one, and keep its stage.
3. Verify through the stack endpoint that #2488 is the bottom and the new PR is the top.

**Reported:** the new PR URL, #2488 reused, the stack number, and the gate result. The Drive pass runs for the new layer. The owner reuses any existing watch on #2488 and arms the new layer's watch in the batch.

## D. `pr-followup` Drive on #2488/#2493, which are not a native stack

**Skills:** `pr-followup` (with `ci-and-observation.md`, `feedback.md`, `github-collection.md`) → `stacked-pr` (with `cli-workflow.md`, `cli-create.md`, `troubleshooting.md` for adoption).

**First**
1. Resolve the exact URLs, heads (refs and SHAs), bases, open state and draft state of #2488 and #2493.
2. Register both PRs with the host if they are not registered yet.
3. The retained state records neither native membership nor the user's choice of ordinary PRs, and the user asked for a stacked PR. So `pr-followup` invokes `stacked-pr` with both PRs and the originating request. This counts as **submitting** the stack; it is not a conversion that needs a question.
4. Meanwhile, `pr-followup` collects and evaluates feedback on both PRs (read-only). Repairs, publication and watches wait.

**stacked-pr**
1. Routes to CLI and runs the live-contract checks.
2. Adopts the existing branches bottom-to-top with the adopt form of `gh stack init`, keeping the tips. It checks that #2493's head contains `ci/carry-approval`.
3. There are no new layers, so there is no Review gate.
4. Runs `$B gh stack submit --auto --remote origin | cat` without `--open`, so both drafts stay drafts. This creates no new PR; it links the existing PRs.
5. Removes any stack map from the two reused bodies with `gh pr edit`.
6. Verifies through the stack endpoint.

**Must be true before the Drive passes continue**
- stacked-pr's result is recorded.
- A fresh GitHub read shows #2488 (base `main`) and #2493 (base `ci/carry-approval`) with unchanged heads, still drafts, and bodies without a stack map.
- The stack endpoint places both PRs in one native stack, in the order #2488, #2493.
- stacked-pr is the single mutation owner. Repairs are pushed through gh-stack, never through a plain `git push`, and the owner arms the watches in one batch.

If stacked-pr reports a blocker instead, repairs and publication stay paused until the user chooses ordinary dependent PRs or the API route, and that choice is recorded.

## E. Plain PR for `fix/null-total`

**Skills:** `pr` (with `publication.md`, `review-gate.md`, `claims.md`, `review-packet.md`, `continuation.md`) → `pr-followup` Drive through continuation.

**Why it is not a stack layer:** the user never mentioned stacks, the base `main` is the default branch, and no PR builds on this branch.

**Steps**
1. `$B gh pr list --repo acme/web --state all --head fix/null-total --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft` → no PR.
2. `git fetch origin main` and verify `origin/main`.
3. Reuse the validated review report for the exact `<merge-base>..<head>` range. It has no findings.
4. Read the templates and recent merged PRs, then compose the title and body.
5. `git push -u origin HEAD:refs/heads/fix/null-total` and confirm the remote tip.

**PR-creating command**
```
$B gh pr create --repo acme/web --base main --head fix/null-total --draft --title "<title>" --body-file <ignored-tmp>/pr-body.md
```

**After creation:** verify the result, register the PR with the host, and run `pr-followup` Drive, which arms `watch_pull_request`. No `gh stack` commands.

**Reported:** `created`, the URL, head/base, draft state, body length against its budget, and the gate result (reused, no findings).

## F. `pr` Create called from stacked-pr's manual route for `stack/02-api` on `stack/01-schema`

**Skills:** `pr` and its references only. `stacked-pr` invoked this Create, so `pr` does not hand off.

**Steps**
1. Exact PR lookup for `stack/02-api` → none.
2. The base is not the default branch, so run `$B gh pr list --repo acme/web --state open --head stack/01-schema --json number,url,author` → #40, the caller's chain.
3. Fetch and verify the base.
4. Reuse the validated report for `<merge-base stack/01-schema>..stack/02-api`. It has no findings.
5. Compose the title and body from repository conventions. Include the bottom-to-top chain map that marks this PR as current: a manual chain gets no native grouping, so every open PR in it carries the map.
6. The branch is already pushed. Verify that the remote tip equals the local HEAD; do not push.

**PR-creating command**
```
$B gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "<title>" --body-file <ignored-tmp>/pr-body.md
```

**After creation:** do a fresh read of the base, head SHA, title, body (with the map) and draft state, then register the PR with the host. No `gh stack` commands.

**`pr` returns `created` to stacked-pr with:**
- the URL, head/base SHAs and draft state;
- body length against its budget;
- the gate result (reused report, no findings);
- the commands that ran and their results;
- coordination that the body leaves out: stacked-pr must add the new PR to #40's map.

Following continuation, `pr` returns to the caller's authorized loop and does not start its own Drive. stacked-pr's "Follow up layers" runs the Drive pass and arms the watch.

## G. T3 Code wake on #2501 (bottom layer, native membership pending), one new review comment

**Skills:** `pr-followup` resumed with its retained state (`ci-and-observation.md` including its T3 Code subsection, `feedback.md`, `github-collection.md`). As needed: `commit`, `comment-style`, `pr` Update, and `stacked-pr` (owner, `cli-maintain.md`) for publication.

The retained state records a single layer's pending membership, so `pr-followup` does **not** re-invoke stacked-pr to submit.

**On this wake, in order**
1. **Read remote state before acting.** Read #2501's current open and draft state, head SHA, `main` SHA, merge state and review decision. Reconcile any ready event that was observed. Check the events T3 does not wake on: checks that started after the last wake, threads resolved without a comment, a merge, base advancement or BEHIND state, another actor marking the PR ready, and comments by T3's own account. Confirm the PR is not merged. Because `acme` is an org, the personal-repository merge policy does not apply.
2. **Collect every channel**, not only the notified comment: inline comments, reviews, conversation comments, paginated GraphQL review threads, check runs and annotations, statuses, and Actions reviewer logs. Update the ledger.
3. **Evaluate the new comment.** Locate its current code target, state the claim, and decide: Apply, Already fixed, Disproved, Question, Needs decision, or Outside scope.
4. **If the decision is Apply:**
   1. Make the smallest coherent fix on `api/routes`, with no upper layer yet.
   2. Run the narrow test, the build and a smoke check.
   3. Commit through `commit`.
   4. Publish through the stack owner, stacked-pr, with gh-stack's current safe push form with lease protection, never a plain `git push`.
   5. Read the remote head again and invalidate the old CI evidence.
   6. Invoke `pr` Update to rewrite the whole body. The body has no stack map.
   7. Word the reply through `comment-style`, citing the published commit, then post it in the thread and resolve the thread.

   **For the other decisions:**
   - Disproved or an answered question: reply with the evidence and leave the thread open.
   - Needs decision: tell the user what must be confirmed and by whom. Before that turn ends for the user, run `unwatch_pull_request`.
   - Outside scope: create a ticket through `issue-workflow` Publish, reply with the link, then resolve the thread.
5. **Take a fresh snapshot.** CI on the new head is pending, so #2501 stays a draft.
6. **Return the pass to the stacked-pr owner:** head/base, result, and pending watch action. The existing #2501 watch stays armed; reuse it and do not re-arm it. Native membership stays pending until layer 2 exists. End the turn.

## H. PR for `hotfix/rounding` against `release/1.2`

**Skills:** `pr` (with its references) → `pr-followup` Drive through continuation.

**Steps**
1. The base is not the default branch, so run `$B gh pr list --repo acme/web --state open --head release/1.2 --json number,url,author` → #50, authored by `release-manager`. That is **not** the verified actor.
2. The stack-layer test requires a base that is the head of another open PR **by the same author**. That test fails here. The request also does not mention a stack, and no PR builds on this branch. So this is an ordinary Create: no `stacked-pr` handoff and no `gh stack` commands.
3. Exact PR lookup for `hotfix/rounding` → none.
4. `git fetch origin release/1.2` and verify the ref.
5. Reuse the validated review report for `<merge-base origin/release/1.2>..hotfix/rounding`.
6. Compose the title and body.
7. `git push -u origin HEAD:refs/heads/hotfix/rounding` and confirm the remote tip.

**PR-creating command**
```
$B gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "<title>" --body-file <ignored-tmp>/pr-body.md
```

**After creation:** verify the result, register the PR with the host, and run Drive.

**Reported:** `created`, the URL, head/base, draft state, budget, and the gate result. Report one coordination point in the return rather than in the body: the base `release/1.2` is the head of open #50 (→ `main`), owned by `release-manager`. Nothing is asked.

## Files read (sha256)

```
df55ff91350cfcf3932932d2dfbd5c0533dc3c2ae726e65772fe8f9b4022cb77  probes/arm-3.md
c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2  arms/arm-3/stack-worktree/SKILL.md
1613cb23ba546cf43ffba2185e2ea2018c110180c28f71231e836b5081695297  arms/arm-3/stacked-pr/SKILL.md
903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710  arms/arm-3/stacked-pr/references/cli-workflow.md
e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5  arms/arm-3/stacked-pr/references/cli-create.md
0eaecaabad806aaa60a65ddb68572b829a6ebf6504cddc75532c4e6930cf2f83  arms/arm-3/stacked-pr/references/cli-maintain.md
4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296  arms/arm-3/stacked-pr/references/stack-design.md
d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc  arms/arm-3/stacked-pr/references/troubleshooting.md
8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b  arms/arm-3/stacked-pr/references/api-workflow.md
132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7  arms/arm-3/stacked-pr/references/manual-chain.md
bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0  arms/arm-3/stacked-pr/references/manual-create.md
5f1652ecee628096eed822ae72ca4aea79b8cbb1ad3bc988ebf009f94709470a  arms/arm-3/pr/SKILL.md
67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d  arms/arm-3/pr/references/review-gate.md
e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f  arms/arm-3/pr/references/publication.md
471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c  arms/arm-3/pr/references/continuation.md
ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887  arms/arm-3/pr/references/claims.md
7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3  arms/arm-3/pr/references/review-packet.md
9d7b8f0615d20e6be2f42564a672ed1aa178c1dfdd0b550b6e9fb59a3dd85b6c  arms/arm-3/pr-followup/SKILL.md
0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c  arms/arm-3/pr-followup/references/ci-and-observation.md
c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd  arms/arm-3/pr-followup/references/feedback.md
38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400  arms/arm-3/pr-followup/references/github-collection.md
517081b22ef7a82fb63571fdbfba028fc4a0fac233a0649c6141357a3db09592  arms/arm-3/worktrunk/SKILL.md
a94d75dc3e23c3f41aafc7e6775f7b86380bd11dc9d06e6e7f1293e92621b8a2  arms/arm-3/worktrunk/references/switch.md
```
Paths are relative to <scratch>.
