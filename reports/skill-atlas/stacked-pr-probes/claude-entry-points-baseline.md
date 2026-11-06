# Dry-run probe output: Claude Code, baseline

- Host: Claude Code general-purpose subagent, claude-opus-5-5, default effort, read-only
- Runtime: baseline arm (f2150614), rendered probe sha256 a08ce8cd... (cases A-F) and f662e403... (cases G-H)
- Probe: stacked-pr-probes/probe-entry-points.md
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases A-F (verbatim)

Model: Claude Opus 5.5 (claude-opus-5-5)

# Dry-run answer: probe arm-2

Paths are relative to the skills root `.../scratchpad/arms/arm-2`. Every `gh` command below runs under the actor binding `GH_TOKEN="$(gh auth token --hostname github.com --user <actor> || echo none)" gh …` (pr/references/publication.md:17-23). I leave the binding out of the commands below to keep them short. `<actor>` is the verified login, which the probe does not name. Flags marked "(live help)" come from `gh stack <cmd> --help`, as stacked-pr/references/cli-workflow.md:44-47 requires. The skills give no exact spelling for them.

## A. "Implement it as a stacked PR, with the other change on top"

**Skills loaded, in order**

1. `stacked-pr`. The user asks for stacked PRs, and this skill owns stack design, topology, submission and the follow-up handoff (pr/SKILL.md:11-14). Routing (stacked-pr/SKILL.md:63-77): this is not stack-aware CI work, because layer 1 changes CI but the request does not change automation because of stack state. It is not API work. `gh extension list` shows `github/gh-stack v0.3.0`, and the user did not ask for ordinary dependent PRs. The route is therefore **CLI**, which means a native stack ("Any other request for stacked or dependent PRs asks for a native stack", :77). Then, in order:
   - `references/cli-workflow.md` (the route file),
   - `references/cli-create.md` (create, adopt and submit),
   - `references/stack-design.md` (the Plan step requires it, cli-create.md:8),
   - `references/troubleshooting.md` (cli-create.md:10-11 requires it for layers in other worktrees; I use the "Adopt" and "Worktrees" sections),
   - `references/api-workflow.md` (only for the stack-list endpoint that verifies membership, cli-create.md:45,56).
2. `stack-worktree` (project skill). I load it only for the repository's worktree conventions: run `wt list` first, give each layer its own worktree, approve pre-start hooks, and override ports. I do **not** follow its `gh pr create --base <parent>`, `git push -u`, "Stacked on #123" line, or `git rebase --update-refs` plus `git push --force-with-lease` steps (stack-worktree/SKILL.md:49,125-151). On the CLI route only `gh stack submit` creates layer PRs (cli-create.md:33-36). A native-stack PR carries no stack map (stacked-pr/SKILL.md:19-22). A plain rebase or push switches the writer away from gh-stack (stacked-pr/SKILL.md:96-100). Weak point: stack-worktree never mentions native stacks, so an agent that loads it first and follows it would open ordinary PRs.
3. `worktrunk` and `references/switch.md`. These give the `wt switch --create … --base …` form and the `--format=json` path handoff for non-persistent shells (switch.md:19-24,57).
4. Skills I invoke but do not read: `pr` in Review gate mode for each new layer, bottom-up (stacked-pr/SKILL.md:52-54), which runs `review-code-changes` in a fresh Codex context on the newest Sol model at `xhigh`; `commit` for layer 2; `pr` in Draft-only mode for each PR's title and body after submit (cli-create.md:52-54); and `pr-followup` Drive for each layer. `pr` Check cap runs only if a cap exists, and none is stated. `issue-workflow` runs only if a ticket is referenced. `github-actions` is not needed to publish.

**Commands**

Live contract (cli-workflow.md:17-26):
```
gh extension list
git status --short --branch
git remote -v
git --version
gh auth status
gh release list -R github/gh-stack --exclude-pre-releases --json tagName,publishedAt
```
- Git 2.50 is at least 2.36.
- v0.3.0 was published on 2026-10-26. It is 11 days old, which passes the default 3-day cooldown. It is already installed, so there is no reinstall.
- v0.3.0 is at least v0.2.0, so a stack can span worktrees (cli-workflow.md:41-42).
- I read `--help` for init, submit, the JSON view and rebase/sync, and pass `--remote origin` to every command that accepts it.

Plan (stack-design.md):
- L1 `ci/carry-approval` on `main`: the existing CI commit, with its tip kept.
- L2 `storybook/anchored-clock` on L1: the new change.

I record L2's dependency on L1. If L2 has none, stack-design.md:31-32 says it belongs in a separate stack, so I tell the user that before building. The user's explicit choice still decides. Before the first mutation, I record the current branch, dirty paths, the tips of `ci/carry-approval` and `origin/main`, and the remote objects I intend to create.

Build. Create the stack before implementing (stack-design.md:54; troubleshooting.md:121-126):
```
git merge-base --is-ancestor origin/main ci/carry-approval
wt list
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
gh stack init --remote origin ci/carry-approval storybook/anchored-clock   # adopt form, bottom-to-top (live help)
gh stack <JSON view> (live help)                                          # order correct, tips unchanged
```
- If `wt hook show` still shows `(requires approval)`, the user must run `wt config approvals add` in a real terminal. I report that.
- In the new worktree path, I implement L2, stage explicit paths, commit through `commit`, and run the layer checks.
- Then I confirm `git merge-base --is-ancestor ci/carry-approval storybook/anchored-clock` and check the JSON view again.

Review gate: `pr` Review gate mode first for `origin/main..ci/carry-approval`, then for `ci/carry-approval..storybook/anchored-clock`, with exact SHAs. If L1 needs fixes, I restack through `gh stack` before L2 is reviewed.

**Creating the PRs.** One command creates both PRs and the native stack, and pushes both branches:
```
gh stack submit --auto --remote origin | cat     # stdout not a TTY; draft by default; no --open (live help)
```
No `gh pr create` and no `git push -u` runs.

After submit:
- For each PR, `pr` Draft-only produces the copy, and I apply it with `gh pr edit <url> --title <title> --body-file <file>`. The body has no stack map.
- I read the stack endpoint (https://docs.github.com/en/rest/pulls/stacks) to confirm one stack containing [L1, L2]. If the stack is missing or split, I rerun submit once. If it is still wrong, I report a blocker.
- I run a fresh `gh pr view` for each PR to check head, base, title, body and draft state.

**Follow-up.** For each PR, `pr-followup` runs one Drive pass. Each pass returns its head/base, result and pending watch action to `stacked-pr`. `stacked-pr` makes the repairs and restacks, then arms both watches in **one batched host invocation** (T3 Code: `watch_pull_request`) and ends the turn (stacked-pr/SKILL.md:108-116; ci-and-observation.md:127-131). `acme/web` is an organization repository, so the personal-repository merge policy does not apply. Merging needs explicit user approval of the exact PRs and merge method (pr-followup/SKILL.md:181-190).

**Report.**
- Route and the observation that decided it: the `gh extension list` line.
- Repository, trunk, remote and actor.
- The layer plan.
- Both PR URLs and the stack number.
- Draft state and the review-gate results.
- The watches I armed.
- Remaining work: human review, and merge approval.

**Questions.** I ask only if L2 does not depend on L1, or if hook approval is needed.

## B. `pr` Create for the bottom layer, from a caller that loaded `stack-worktree`

Skills: `pr`, with `references/publication.md` (GitHub account). It then routes to `stacked-pr`.

1. Operation: Create.
2. Identity and scope. These are all reads:
   - Branch, status, remotes, upstream and HEAD.
   - `origin` = `git@github.com:acme/web.git` maps to `acme/web`.
   - Exact PR lookup: `gh pr list --repo acme/web --state all --head ci/carry-approval --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`. It returns empty.
   - `git fetch origin`, then confirm that `origin/main` = `2105bea`.
   - Record the revision `2105bea..0e5c9c4`.
3. Base step: "Route dependent-branch topology to `stacked-pr`" (pr/SKILL.md:62), and `stacked-pr` owns stack **submission** (pr/SKILL.md:12). The caller declares this branch the bottom of a 2-layer stack. Stacks are enabled and gh-stack is installed, so its PR belongs to `stacked-pr`'s CLI route. There, `gh pr create` or `pr` Create would produce an ordinary PR outside any stack (cli-create.md:33-36). I therefore do not follow the caller's stack-worktree recipe (`gh pr create --base main` plus a "Stacked on" line).
4. **No push and no PR-creating command from `pr`. It hands off to `stacked-pr`** within the request. It passes `acme/web`, `origin` (SSH), the actor, `ci/carry-approval@0e5c9c4`, base `main@2105bea`, "bottom of 2, layer 2 planned", and the empty lookup result. The review gate for `2105bea..0e5c9c4` runs when `stacked-pr` invokes `pr` in Review gate mode.
5. What `stacked-pr` then does, outside `pr`: `gh extension list` (CLI route), then `gh stack init` to adopt `ci/carry-approval` with its tip kept. The PR is created only by `gh stack submit --auto --remote origin | cat`. It can submit now and report membership as pending until a second layer exists (cli-create.md:59-60), or submit both layers together once L2 is built. After the PR exists, `pr` Draft-only writes the title and body (no map), applied with `gh pr edit`.

`gh stack` commands from `pr` itself: none.

`pr` reports: no PR created by `pr`, the reason for the routing, and the verified identity and revision for the owner. Gap: `pr`'s return statuses (`created`, `updated`, `draft-only`, `blocked`, pr/SKILL.md:152) have no "handed off" status. The rule that a stack layer must not use `gh pr create` exists only in stacked-pr/cli-create.md, not in `pr`.

## C. `worktrunk`: "create a stacked worktree for storybook/anchored-clock on ci/carry-approval (#2488), then open its PR"

Skills:
- `worktrunk` and `references/switch.md`, for the non-default base.
- `stacked-pr` (with cli-workflow, cli-create, stack-design, troubleshooting) for "open its PR". A PR based on another open PR's branch is a dependent-PR request, and that means a native stack (stacked-pr/SKILL.md:77). Worktrunk owns only the worktree lifecycle.
- Invoked without reading: `commit`, `pr` Review gate, `pr` Draft-only and `pr-followup`.

Worktree:
```
wt list
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
```
Work continues in the path from the JSON result. Pre-start hooks copy `node_modules` and `.env` and run `npm install`.

PR. `stacked-pr` takes the CLI route. #2488 is an untracked ordinary PR, and a create request adopts it first and ends with submit (stacked-pr/SKILL.md:89-94; cli-workflow.md:4-8):
```
gh extension list
gh stack init --remote origin ci/carry-approval storybook/anchored-clock   # adopt, #2488's head tip unchanged (live help)
```
- I implement L2 and commit it. GitHub cannot open a PR for a branch with no commits.
- `pr` Review gate checks `ci/carry-approval..storybook/anchored-clock`.
- Then:
```
gh stack submit --auto --remote origin | cat    # no --open: it would also mark #2488 ready
```
Submit reuses #2488, creates the `storybook/anchored-clock` PR, and links both into one native stack. No `gh pr create --base ci/carry-approval` runs.

After submit:
- `pr` Draft-only writes the new PR's title and body, applied with `gh pr edit`.
- On #2488 I only remove a stack map if one exists, and keep its stage.
- I verify the stack endpoint and do fresh PR reads.
- One Drive pass runs for the new layer, and `stacked-pr` arms the watches in one batch, reusing any existing watch on #2488.

Report:
- The worktree path, the adoption result, and the new PR URL.
- #2488 reused, and the stack number.
- The review gate result and the watches.

Nothing needs to be asked, because this is a create request.

## D. `pr-followup` Drive on #2488 and #2493, which form no native stack

Skills:
- `pr-followup`, with `references/ci-and-observation.md` before any watch.
- Then `stacked-pr` (with cli-workflow, cli-create, troubleshooting "Adopt"). `stacked-pr` owns stack topology and rebases, and each stack has exactly one mutation owner (pr-followup/SKILL.md:55-56). Stack passes return to that owner before any watch is armed (ci-and-observation.md:127-131). No owner is running.

**First, read only.** I run `gh pr view` on both PRs to get the URL, head ref/SHA, base ref/SHA, open state and draft state. The user asked for a stacked PR, which means a native stack, but these are ordinary PRs. Before any repair, publication, ready transition or watch, I invoke `stacked-pr` to own the stack.

`stacked-pr`:
1. `gh extension list` gives the CLI route, because the user never asked for ordinary dependent PRs.
2. The user's stacked-PR creation request was never completed: its criterion is stack-endpoint membership (cli-create.md:62-64). That makes this a create request, which "ends with the submit step" (cli-workflow.md:7-8). If the user had not asked for a stack, cli-workflow.md:8-11 would require me to ask before converting, and a "no" would move the PRs to the manual route with stack maps.
3. Run:
```
gh stack init --remote origin ci/carry-approval <#2493 head branch>   # adopt, tips unchanged (live help)
gh stack <JSON view>
gh stack submit --auto --remote origin | cat                          # no --open: both stay drafts
```
Submit reuses both PRs and creates none. I edit them only to remove a stack map, for example a "Stacked on #2488" line: `gh pr edit <url> --body-file <file>`.

**Before the Drive passes continue, all of these must be true:**
1. `stacked-pr` (gh-stack) is the only mutation owner. Its JSON view lists `ci/carry-approval` and #2493's head in order, with the recorded tips unchanged.
2. Fresh reads show #2488 with base `main`, #2493 with base `ci/carry-approval`, both still drafts, and no stack map in either body.
3. The stack endpoint places #2488 then #2493 in one native stack. Otherwise one of these blockers is reported, and the PRs are never called a stack:
   - Stacks unavailable: a 404 on the stack list while the repository read succeeds. I offer ordinary dependent PRs.
   - Linking failed after one retry. I report the PR URLs.
4. Then one Drive pass runs per layer. Each pass returns its head/base, result and pending watch to `stacked-pr` and never arms its own watch. Rebases go through `gh stack`, not plain git. `stacked-pr` arms both watches in one batched host invocation and ends the turn. Nothing merges without explicit user approval, because this is an organization repository.

## E. "Create a PR for my branch fix/null-total" (no stack)

Skills: `pr` only, in Create mode, with publication, review-gate and continuation. I do not load `stacked-pr`, because there is no dependent branch and no stack request.

Steps:
1. Run `gh pr list --repo acme/web --state all --head fix/null-total --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`. It returns empty.
2. Run `git fetch origin` and verify `origin/main`.
3. Review gate: reuse the supplied validated report for the exact range if its recorded profile is Codex, the newest Sol model, at `xhigh` (review-gate.md:9-20). Otherwise run the gate. It has no findings.
4. Push and confirm the remote tip:
```
git push -u origin HEAD:refs/heads/fix/null-total
```
5. Confirm `gh api user --jq .login` prints the actor.
6. Create the PR:
```
GH_TOKEN="$(gh auth token --hostname github.com --user <actor> || echo none)" gh pr create --repo acme/web --base main --head fix/null-total --draft --title "<title>" --body-file <ignored-temp-body-file>
```
7. Verify with `gh pr view` and register the PR with the host.
8. Continue: `issue-workflow` if a ticket exists, then `pr-followup` Drive, which arms the host watch (`watch_pull_request` in T3 Code).

`gh stack`: none. Report: `created`, with URL, head/base, draft state, body length against its budget, the review gate result and the commands run.

## F. `pr` Create, invoked by `stacked-pr` on the manual route, for stack/02-api on stack/01-schema (#40)

Skills: `pr` in Create mode, with publication, review-gate and continuation. `pr` does not route back to `stacked-pr`: the caller already owns the topology, and `pr` only publishes.

Steps:
1. Exact-head lookup, required before creation (manual-create.md:16): `gh pr list --repo acme/web --state all --head stack/02-api --json …`. It returns empty.
2. Run `git fetch origin`. Verify that `origin/stack/01-schema` equals #40's head SHA and that #40 is open, then record the exact SHAs.
3. Reuse the supplied review report, after the same profile check as in E.
4. The branch is already pushed, so I only confirm that the remote `stack/02-api` tip equals HEAD. There is no new push.
5. The body carries the bottom-to-top map with the current PR marked, for example "Stack: #40 → **this PR**" (manual-create.md:18-19; stacked-pr/SKILL.md:19-22).
6. Confirm `gh api user --jq .login`.
7. Create the PR:
```
GH_TOKEN="$(gh auth token --hostname github.com --user <actor> || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "<title>" --body-file <ignored-temp-body-file>
```
8. Verify the result.

`gh stack`: none, because this is the manual route.

**What `pr` returns to `stacked-pr`:**
- `created`, with the URL and number.
- Head `stack/02-api@<sha>`, base `stack/01-schema@<sha>`, and draft state.
- Body length against its budget, and any detail-comment URL.
- Validation, and the review gate result: the reused report path and profile, with no findings.
- The commands run and their results.
- Remaining coordination: #40's body needs the same map with the new PR number. That is the caller's job, through `pr` Update.

Continuation: `pr` hands its Drive pass to the caller's existing follow-up loop instead of starting its own (continuation.md:23). The pass returns its pending watch to `stacked-pr`, which arms all watches in one batch.

## Files read (sha256)

Paths are relative to `<scratch>/`.

| File | sha256 |
| --- | --- |
| probes/arm-2.md | a08ce8cd01d8f16caf4687bf110171e94a7d72d5a6c8c8602e8c3f775c79c9cc |
| arms/arm-2/stacked-pr/SKILL.md | 2e675d9a813fffc7dee5e8e8e917c275db9204fe1fe7613aa52eac0dbc00e51d |
| arms/arm-2/stacked-pr/references/cli-workflow.md | 903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710 |
| arms/arm-2/stacked-pr/references/cli-create.md | e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5 |
| arms/arm-2/stacked-pr/references/stack-design.md | 4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296 |
| arms/arm-2/stacked-pr/references/troubleshooting.md | d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc |
| arms/arm-2/stacked-pr/references/api-workflow.md | 8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b |
| arms/arm-2/stacked-pr/references/manual-chain.md | 132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7 |
| arms/arm-2/stacked-pr/references/manual-create.md | bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0 |
| arms/arm-2/stack-worktree/SKILL.md | c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2 |
| arms/arm-2/worktrunk/SKILL.md | aba8d9fd202de9144b8ef0a7f945c8db487aeac53c3aaf7ad1341013a0e5bf94 |
| arms/arm-2/worktrunk/references/switch.md | a94d75dc3e23c3f41aafc7e6775f7b86380bd11dc9d06e6e7f1293e92621b8a2 |
| arms/arm-2/pr/SKILL.md | 5ba92f094b67fa2f928b9c181bdc26adfa68c5fbe74e16de7a8fe127100a009f |
| arms/arm-2/pr/references/publication.md | e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f |
| arms/arm-2/pr/references/review-gate.md | 67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d |
| arms/arm-2/pr/references/continuation.md | 471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c |
| arms/arm-2/pr-followup/SKILL.md | a61c0704f1b5343a18c1bbbea729f76166c52f4a0b5aa26cd9b54dc375d13531 |
| arms/arm-2/pr-followup/references/ci-and-observation.md | 0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c |

I did not read `pr/references/claims.md` or `review-packet.md`, because no command above depends on the body wording. The same goes for the other `pr-followup` references and the remaining `stacked-pr` branches, and for `commit` and `github-actions`.

## Cases G-H (verbatim)

Model: Claude Opus 5.5 (claude-opus-5-5)

# Probe arm-2-gh: answers

## Case G: T3 Code wake on draft PR #2501 (bottom layer, stack owned by `stacked-pr`)

### Skills loaded, in order

1. `pr-followup/SKILL.md`. The wake resumes Drive scope with the retained task state.
2. `pr-followup/references/ci-and-observation.md`, including its T3 Code subsection. The skill requires it before keeping, re-arming or stopping a watch.
3. `pr-followup/references/feedback.md`, then `pr-followup/references/github-collection.md`, which feedback.md requires.
4. `pr/references/publication.md` (GitHub account and "Before writing"). These identity checks run before the first write: a reply, a resolution or a push.
5. `stacked-pr/SKILL.md`, in its role as the stack's single mutation owner. It receives this layer's pass and owns any push.
6. Only on the Apply path: `stacked-pr/references/cli-workflow.md` (the CLI route, because gh-stack v0.3.0 is installed), then `stacked-pr/references/cli-maintain.md` ("Edit one layer and cascade upward" and "Push"), then `pr` Update with `claims.md` and `review-packet.md` to rewrite the whole body.
7. Invoked only when needed, not read here: `verify`, `commit`, `comment-style` (before any reply), `debug` or `review-code-changes` for an uncertain claim, and `issue-workflow` (Publish for an outside-scope ticket; `pr-ready` or `pr-merged` only when a linked ticket's policy selects it).

### Steps, in order

1. **Treat the wake as a prompt to reread GitHub, not as the full inbox.** Bind every `gh` call to the verified actor: `GH_TOKEN="$(gh auth token --hostname github.com --user <actor> || echo none)" gh …`. Refresh https://github.com/acme/web/pull/2501: open, closed or merged state; `isDraft`; head `api/routes` and its SHA; base `main` and its SHA; review decision; merge state. Remote state outranks the retained state.
2. **Check the events that T3 Code never wakes on:**
   - checks that started after the last wake;
   - threads resolved without a comment;
   - a merge;
   - base advancement or a BEHIND state;
   - a ready transition by another actor (reconcile `pr-ready` through `issue-workflow` only if a linked ticket's policy selects it);
   - comments by the account that T3 Code reads with.

   If the PR is closed or merged, stop repair work and report that. If it merged and has a linked ticket, run `pr-merged` first.
3. **Collect the complete feedback snapshot from every channel, with full pagination:**
   - inline comments and their replies;
   - formal review bodies;
   - conversation comments;
   - GraphQL `reviewThreads` (`isResolved`, `isOutdated`, IDs);
   - check runs and their annotations;
   - commit statuses;
   - reviewer output in Actions logs.

   Reread threads that were already handled, for edits and new replies. Update the ignored local ledger.
4. **Evaluate the new comment, and any other new item.** Find its current code target, state the claim, and trace it through the current code, contract and callers. Decide one of: Apply, Already fixed, Disproved, Question, Needs decision, or Outside scope.
5. **Act on the decision.**
   - **Apply:**
     - Confirm that the WorkTrunk worktree is on `api/routes` at the PR head SHA. Use host checkout ownership, `worktrunk`, or gh-stack's `--print-path` form to find the layer.
     - Make the smallest fix, with a regression test. Run the narrowest test, the build and a smoke check through `verify`. Commit through `commit`.
     - Publish through the stack owner, `stacked-pr`, not with a plain `git push`. gh-stack tracks `api/routes`, so a plain push would switch the writer. No upper layer exists, so there is no cascade rebase.
     - Run `pr`'s identity and pre-write checks. Refetch the remote heads, push with `gh stack push`, then confirm the remote tip and the stack view.
     - Reread the remote head and invalidate earlier CI and readiness evidence. Rewrite the whole body through `pr` Update, with no stack map because no chain exists yet.
     - Reply in the thread, worded through `comment-style`. Cite the commit only after you confirm that the published head contains it. Then resolve the thread.
   - **Disproved, or a question answered without a change:** reply with the evidence, worded through `comment-style`. Leave the thread open.
   - **Outside scope:** create one tracking ticket through `issue-workflow` Publish. Reply with the ticket link, then resolve the thread.
   - **Needs decision:** do not reply. Tell the user what must be confirmed and by whom. Continue the independent work. This turn ends for the user, so call `unwatch_pull_request` before you end it.
6. **Readiness.** After a push, the new head's checks are pending, so the PR stays a draft on this wake. Mark it ready only when all three conditions hold:
   - no push happened;
   - all CI for the current head passed;
   - every thread has its disposition.

   Then recheck the state, run `gh pr ready https://github.com/acme/web/pull/2501`, confirm that `isDraft` is false, and start the post-ready observation phase.
7. **Watch hand-back.**
   - Return this layer's pass to the `stacked-pr` owner: head and base, result, and the pending watch action "keep the existing watch".
   - The watch on #2501 is still active, so reuse it. Do not re-arm it after a push or a reply.
   - No other layer exists, so the owner has no unwatched layer to arm in a batch.
   - End the turn while waiting.
   - Do not merge. `acme` is an organization, so the personal-repository merge policy does not apply. Drive waits for a current formal approval or a merge.

### `gh stack` commands

These run only on the Apply path:

- `gh stack --version` records the installed version. Do not upgrade: v0.3.0 is the newest release, and it is past the three-day cooldown.
- `gh stack view --help` and `gh stack push --help` give the current non-interactive flags.
- The JSON view form from that help (for example `gh stack view --json`) confirms that `api/routes` is the only tracked layer and needs no rebase.
- After the refetch, `gh stack push --remote origin`. It is atomic by default from v0.3.0.
- Run the JSON view again to verify the push.

Do not run `submit`, `rebase`, `link`, `sync` or `merge`. Native membership stays pending until `stacked-pr` adds the second layer. The other decision paths run no `gh stack` commands.

### Reported or asked

- **If the wake changed a decision or remote state, report:**
  - the PR URL and current head SHA;
  - the comment's disposition: applied with its commit, replied, linked to a ticket, or waiting for confirmation from a named person;
  - the verification commands and their results;
  - the current checks (pending for a new head) and the remaining items;
  - that stack membership is still pending, with `stacked-pr` as owner;
  - the status `waiting` on the existing watch;
  - coverage gaps: the event types in step 2 and edited comments, which may not trigger a wake.
- **On the Needs decision path:** ask the question, name who must answer it, and give a recommendation. Unwatch first.
- **If nothing changed:** end the turn without a message.

## Case H: "Create a PR for my branch hotfix/rounding against release/1.2"

### Skills loaded, in order

1. `pr/SKILL.md`, in Create mode.
2. `pr/references/publication.md`, the GitHub account section, before the first `gh` call.
3. `pr/references/review-gate.md`.
4. `pr/references/claims.md`, then `pr/references/review-packet.md`, for the title and body.
5. The rest of `pr/references/publication.md`, before the push and the create, and for the result check.
6. `pr/references/continuation.md`, then `pr-followup/SKILL.md` in Drive scope, with `feedback.md`, `github-collection.md` and `ci-and-observation.md` (its T3 Code subsection arms the watch).
7. Invoked only when needed, not read here:
   - `issue-workflow` Inspect, only if the branch or commit names a ticket;
   - `commit`, only for uncommitted work that the PR includes (none here: the branch has one commit);
   - `review-code-changes`, only if the existing report fails the gate's reuse rule.

`stacked-pr` is not loaded. The base `release/1.2` is the head of open PR #50 by `release-manager` (base `main`), but this is not a stack request:

- The user asked for one PR against an explicit base and never mentioned stacks.
- `release/1.2` is the release branch that the hotfix targets. It is not a lower layer of the user's own work.
- A native stack, through `gh stack submit` after adopting `release/1.2`, would link another author's PR #50 into a stack. The hotfix could then land only after #50, bottom-up. Both effects mutate another person's PR outside this request.

`pr` therefore creates an ordinary PR with the verified explicit base.

### Steps and the PR-creating command

1. **Recheck that no PR exists for the branch.** `gh pr list --repo acme/web --state all --head hotfix/rounding --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft` returns nothing.
2. **Verify the base.** `git fetch origin release/1.2` runs over SSH. Record the base SHA and the head SHA.
3. **Pass the review gate.** Reuse the validated report, which has no findings, if both conditions hold:
   - its Scope names the exact `<merge-base>..<head>` SHAs against the verified `origin/release/1.2`;
   - its recorded profile matches the gate: a fresh Codex context, the newest Sol model, and `xhigh` effort.

   If either does not hold, rerun the review in a `delegate_task` child with that profile.
4. **Compose the title and body.** Use the repository rules, the base templates and recent merged PRs. Add one merge-care line: the fix reaches `main` through #50 only if it merges into `release/1.2` before #50 merges. Write the body to an ignored temporary file and measure it against the length budget.
5. **Publish.**
   - Under the actor binding, `gh api user --jq .login` must print the actor.
   - Push with `git push -u origin HEAD:refs/heads/hotfix/rounding` over the SSH remote, then confirm the remote tip.
   - Recheck that no PR exists, then create the PR:

```text
GH_TOKEN="$(gh auth token --hostname github.com --user <actor> || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "<title>" --body-file <ignored-tmp>/pr-body.md
```

6. **Verify and continue.**
   - Run `gh pr view <new-url> --json url,headRefName,headRefOid,headRepository,baseRefName,title,body,isDraft` to verify the result.
   - Register the PR with T3 Code.
   - Follow the continuation into `pr-followup` Drive: take the final snapshot, call `watch_pull_request`, then end the turn.

### `gh stack` commands

None.

### Reported or asked

- **Report:**
  - `created`, with the URL;
  - the head `hotfix/rounding@<sha>` and the base `release/1.2@<sha>`;
  - the draft state;
  - the body length against its budget;
  - the review gate result: the reused report's path and profile, with zero findings;
  - the commands that ran and their results;
  - that Drive is armed, with the status `waiting`.
- **Also report:** `release/1.2` is the head of https://github.com/acme/web/pull/50, which `release-manager` opened against `main`. The new PR is an ordinary PR, not part of a stack, and #50 was not changed. The merge-order note from step 4 also appears in the body.
- **Ask:** nothing. Stacking with #50 would be a separate `stacked-pr` request that involves #50's owner.

## Files read (sha256)

| File | sha256 |
| --- | --- |
| probes/arm-2-gh.md | f662e403fae3adda16285d6ee321c0d4f7eb618135353400d7e18c0a45995432 |
| arms/arm-2/pr-followup/SKILL.md | a61c0704f1b5343a18c1bbbea729f76166c52f4a0b5aa26cd9b54dc375d13531 |
| arms/arm-2/pr-followup/references/ci-and-observation.md | 0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c |
| arms/arm-2/pr-followup/references/feedback.md | c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd |
| arms/arm-2/pr-followup/references/github-collection.md | 38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400 |
| arms/arm-2/pr/SKILL.md | 5ba92f094b67fa2f928b9c181bdc26adfa68c5fbe74e16de7a8fe127100a009f |
| arms/arm-2/pr/references/publication.md | e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f |
| arms/arm-2/pr/references/review-gate.md | 67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d |
| arms/arm-2/pr/references/continuation.md | 471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c |
| arms/arm-2/pr/references/claims.md | ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887 |
| arms/arm-2/pr/references/review-packet.md | 7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3 |
| arms/arm-2/stacked-pr/SKILL.md | 2e675d9a813fffc7dee5e8e8e917c275db9204fe1fe7613aa52eac0dbc00e51d |
| arms/arm-2/stacked-pr/references/cli-workflow.md | 903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710 |
| arms/arm-2/stacked-pr/references/cli-create.md | e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5 |
| arms/arm-2/stacked-pr/references/cli-maintain.md | 0eaecaabad806aaa60a65ddb68572b829a6ebf6504cddc75532c4e6930cf2f83 |
| arms/arm-2/stacked-pr/references/stack-design.md | 4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296 |
| arms/arm-2/stacked-pr/references/troubleshooting.md | d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc |

All paths are relative to `<scratch>/`. I read `cli-create.md`, `stack-design.md` and `troubleshooting.md` while I evaluated the stack route for Case H, which I then rejected. `cli-create.md` also confirms the rule from Case G that a single submitted layer has pending membership.

Deviation: to find the reference files, I ran `ls -R` on the `pr`, `pr-followup` and `stacked-pr` skill directories. The probe allows only reads and `shasum`. I made no other commands, edits, GitHub calls or network calls, and wrote no file other than this answer.
