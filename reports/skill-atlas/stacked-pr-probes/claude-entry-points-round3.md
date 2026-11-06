# Dry-run probe output: Claude Code, round 3

- Host: Claude Code general-purpose subagent, claude-opus-5-5, default effort, read-only
- Runtime: round-3 candidate arm, runtime manifest sha256 193d0f97546222fe6dce6b123757192c15543590f336fe14570c3a26313b938f, rendered probe sha256 23e95b58...
- Probe: stacked-pr-probes/probe-entry-points.md, round 3
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases F, H, I, J, K (verbatim)

Model: Claude Opus 5.5 (claude-opus-5-5)

# arm-4 dry-run answers

Conventions used below:

- `BIND` is the actor binding `GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)"`. It prefixes every `gh` command, reads included (pr/references/publication.md, "GitHub account"). The PR-creating commands are written out in full.
- `<title>` and `<body-file>` are composed at run time from the repository's conventions and the diff. The body file is an ignored temporary file (publication.md, "Create or update metadata").
- Skills named in the files but not loaded here (review-code-changes, pr-followup, commit, issue-workflow, comment-style, communicate-clearly, task-breakdown) are invoked, not read.

---

## F. stacked-pr (manual route) invokes pr Create for `stack/02-api` on `stack/01-schema`

**Skills loaded, in order**

1. stacked-pr `SKILL.md`. Routing ran `gh extension list` (`gh stack github/gh-stack v0.3.0`). Manual route chosen because the user explicitly asked for ordinary dependent PRs.
2. stacked-pr `references/manual-chain.md`
3. stacked-pr `references/manual-create.md`, with `references/stack-design.md` loaded by its "Plan and build" step. troubleshooting.md is not needed: no adoption rewrite and no oversized branch.
4. pr `SKILL.md`
5. pr `references/publication.md#github-account`
6. pr `references/review-gate.md`
7. pr `references/claims.md`
8. pr `references/review-packet.md`
9. pr `references/publication.md` (rest of the file)
10. pr `references/continuation.md`

**What pr does**

- **Mode.** Create. The stack-layer redirect does not apply: "Unless `stacked-pr` invoked this Create". stacked-pr is the caller, so pr does not invoke it again.
- **Identity.** Run `BIND gh api user --jq .login`. It must print `dev` before the first write.
- **Scope**
  - Read the branch, status, remotes, upstream and HEAD. The push destination is `origin` = `acme/web` over SSH.
  - Exact PR lookup: `BIND gh pr list --repo acme/web --state all --head stack/02-api --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`. It returns no match with head repository `acme/web`. A match would be reused, not duplicated.
  - Base: run `git fetch origin stack/01-schema` and verify the fetched ref.
  - Open PRs headed by the base: `BIND gh pr list --repo acme/web --state open --head stack/01-schema --json number,url,author,headRepository,headRepositoryOwner`. This returns #40, which is the parent layer. No redirect, because stacked-pr is already the caller.
  - Record the exact base and head SHAs.
  - The branch is already pushed. Confirm with `git ls-remote origin refs/heads/stack/02-api` that the remote tip equals local HEAD. No push is needed.
- **Review gate.** Reuse the supplied validated report. Its scope names the exact `<merge-base>..<head>` that will be published, and it has no findings. Reuse is valid only when its recorded profile is the gate's profile (fresh Codex context, newest Sol model, `xhigh`). Nothing needs a disposition, and no repeat review runs.
- **Compose**
  - Read the repository instructions, `CONTRIBUTING.md`, the PR templates on `stack/01-schema`, and recent merged non-bot PRs (titles, and up to ten body lengths for the budget).
  - Inspect every commit in `stack/01-schema..stack/02-api` and the full three-dot diff.
  - Write the title and body under review-packet.md and claims.md.
  - Because this is the manual route, the body carries the bottom-to-top map that manual-create.md requires, with the current PR marked. For example: `Stack: #40 (stack/01-schema) → **this PR** (stack/02-api)`.
  - Measure the body with `wc -m` against the length budget.
- **Create.** Recheck the exact PR, head, base and remote tip immediately before creating, then run:

```
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "<title>" --body-file <body-file>
```

  It is a draft because the user stated no preference for ready.
- **Verify.** Run `BIND gh pr view <new-url> --json url,headRefName,headRefOid,headRepository,baseRefName,title,body,isDraft` and confirm that every field is as intended. Register the PR with the host.
- **Continuation**
  - No ticket is involved, so issue-workflow is not invoked.
  - stacked-pr's "Follow up layers" owns follow-up for new layers. pr therefore returns to that authorized loop and does not nest its own pr-followup loop.
  - The pr-followup Drive pass for this layer runs under stacked-pr. It returns its pending watch action to stacked-pr and does not arm a watch itself.

**`gh stack` / `wt` commands:** none. On the manual route, `gh extension list` ran only for routing.

**What pr returns to stacked-pr**

- **Status:** `created`.
- **PR:** the new PR URL. Head `stack/02-api@<head-sha>`, base `stack/01-schema@<base-sha>`, draft = true.
- **Body:** its length against the budget, with the reason for any overrun. The detail comment URL, or none.
- **Validation:** the commands that actually ran on this head, with their results. Missing checks are named.
- **Review gate:** the reused report's path and its recorded provider, model and effort. Zero findings, so no dispositions. This is labeled as reused, earlier evidence, separate from the commands run in this execution.
- **Commands:** every executed command with its result.
- **Remaining work for stacked-pr:**
  - Write the same map into #40's body, marking #40.
  - Verify the chain from fresh GitHub reads.
  - Run the layer's Drive pass.
- **Coordination left out of the body:** #40 merges first.
- **Passed back to stacked-pr:** the verified actor `dev`, the revision SHAs and the publication state.

**Asked:** nothing.

---

## H. "Create a PR for my branch hotfix/rounding against release/1.2" (#50 is by another author)

**Skills loaded, in order**

1. pr `SKILL.md`
2. pr `references/publication.md#github-account`
3. pr `references/review-gate.md`
4. pr `references/claims.md`
5. pr `references/review-packet.md`
6. pr `references/publication.md`
7. pr `references/continuation.md`
8. Then invoke pr-followup in Drive mode (not read).

Not loaded: stacked-pr, because there is no stack signal, and worktrunk, because there is no checkout switch.

**What pr does**

- **Exact PR:** `BIND gh pr list --repo acme/web --state all --head hotfix/rounding --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft` returns none.
- **Base:** run `git fetch origin release/1.2` and verify the ref. Then run `BIND gh pr list --repo acme/web --state open --head release/1.2 --json number,url,author,headRepository,headRepositoryOwner`. It returns #50 by `release-manager`, with head repository `acme/web`.
- **Stack-layer test (pr Create):**
  - The request does not place the PR in a stack.
  - The base is the head of an open PR, but `release-manager` is not `dev`, so it is not "another open PR by the same author".
  - Nothing shows that another PR will build on this one.
  - Result: this is not a stack layer, and pr keeps the Create itself.
- **Review gate:** reuse the validated exact-range report, which has no findings (same profile condition as in F).
- **Compose:** title and body per claims.md and review-packet.md, with no stack map.
- **Publish:**
  - If origin lacks the local tip, run `git push -u origin HEAD:refs/heads/hotfix/rounding`, then confirm with `git ls-remote origin refs/heads/hotfix/rounding`.
  - Run `BIND gh api user --jq .login`. It must print `dev`.
  - Recheck the exact PR, then create it:

```
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "<title>" --body-file <body-file>
```

- **Verify:** `BIND gh pr view <new-url> --json ...` (same fields as F). Register the PR with the host.
- **Continuation:** no ticket. Continue into pr-followup Drive and pass the URL, head and base SHAs, draft state, validation and pending work. No `keep-draft` is passed, because the user gave no such instruction.

**`gh stack` / `wt` commands:** none.

**Reported:** `created`, with the standard return fields listed in F. The user also gets a context note that is not in the body: `release/1.2` is the head of #50 (into `main`, by `release-manager`), and it was not treated as a stack parent.

**Asked:** nothing.

---

## I. "Create a PR for my branch feature/api-routes against feature/data-model" (#12 is yours)

**Skills loaded, in order**

1. pr `SKILL.md`
2. pr `references/publication.md#github-account`
3. The stack layer is detected, so pr invokes stacked-pr `SKILL.md`.
4. stacked-pr `references/cli-workflow.md`
5. stacked-pr `references/cli-create.md`
6. stacked-pr `references/stack-design.md`
7. stacked-pr `references/troubleshooting.md`, because existing PR #12 must be adopted.
8. pr in Review gate mode, which uses `references/review-gate.md`. It invokes review-code-changes in a Codex child (not read).
9. pr in Draft-only mode for the new PR's copy (`references/claims.md`, `references/review-packet.md`).
10. stacked-pr `references/api-workflow.md`, for the documented stack-list read endpoint.
11. Then invoke pr-followup in Drive mode (not read).

stack-worktree is not loaded, because no worktree operation was requested.

**What pr does, up to the handoff**

1. **Mode:** Create, requested by the user. Bind the actor. Read the branch, status, remotes, upstream and HEAD. The push destination is `origin` = `acme/web`.
2. **Exact PR:** `BIND gh pr list --repo acme/web --state all --head feature/api-routes --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft` returns none.
3. **Base:**
   - Run `git fetch origin feature/data-model` and verify the ref.
   - Run `BIND gh pr list --repo acme/web --state open --head feature/data-model --json number,url,author,headRepository,headRepositoryOwner`. It returns #12: author `dev`, head repository `acme/web`, so it is kept.
   - The base is the head branch of another open PR by the same author, so this PR is a stack layer.
4. **Handoff:** before the review gate, pr invokes stacked-pr with the request and returns stacked-pr's result as `handed-off`. pr runs no `gh pr create` and no review gate of its own.

**What stacked-pr does**

- **Routing**
  - The request is neither CI/automation nor REST-owned.
  - `BIND gh extension list` prints `gh stack  github/gh-stack  v0.3.0`.
  - The user did not ask for ordinary dependent PRs, so the CLI route is selected.
  - Recorded: the operation (create a layer above #12), the route, the deciding observation (the extension listing), repository `acme/web`, trunk `main`, push remote `origin` and principal `dev`. Before any mutation, also record the current branch, dirty paths (none) and the tips of both branches.
- **Live contract (cli-workflow.md)**
  - Run `git status --short --branch`, `git remote -v`, `git --version` (2.50), `BIND gh auth status` and `BIND gh extension list`.
  - Run `BIND gh release list -R github/gh-stack --exclude-pre-releases --json tagName,publishedAt`. The newest release, v0.3.0 (2026-10-26), is 11 days old, past the default 3-day cooldown. It is the eligible release and is already installed, so nothing is installed or upgraded.
  - Run `BIND gh stack --version` and record the result.
  - Git 2.50 meets the 2.36 minimum, and v0.3.0 meets the v0.2.0 minimum for a stack that spans worktrees. WorkTrunk worktrees are not another branch manager.
  - Read `gh stack init --help`, `gh stack view --help` and `gh stack submit --help` to get the non-interactive forms. Pass `--remote origin` to every command that accepts it.
- **Inspect**
  - The JSON stack view shows no local stack. This is recorded as observed state.
  - Check #12's remote stack membership through the API read endpoint documented at https://docs.github.com/en/rest/pulls/stacks.
  - If #12 is already the top of a native stack, append only above that verified top.
- **Plan (stack-design.md):** `main <- feature/data-model (#12) <- feature/api-routes (new)`. Verify ancestry with `git merge-base --is-ancestor feature/data-model feature/api-routes`.
- **Adopt (troubleshooting.md, "Adopt existing branches or PRs")**
  - The branches are local and gh-stack owns them, so use the init/adopt form, with branches ordered bottom-to-top:
    `BIND gh stack init <adopt form from live help> feature/data-model feature/api-routes`
  - Confirm with the JSON stack view that both branches are listed in order and that their tips are unchanged.
- **Review gate**
  - Invoke pr in Review gate mode for `feature/api-routes` against its immediate PR base `feature/data-model`.
  - No report exists, so review-code-changes runs in a fresh Codex context on the newest Sol model with `xhigh` effort. In T3 Code this is a `delegate_task` child. Elsewhere it is `codex exec -m <newest Sol model> -c model_reasoning_effort="xhigh"`, run on `<merge-base>..<feature/api-routes head>`.
  - Dispose of every finding before submitting: fixes go through commit, followed by a repeat review.
  - #12 is not gated, because it is not a new layer.
- **Create (the only PR-creating command)**

```
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh stack submit --auto --remote origin | cat
```

  - Add the flag for the draft state that `gh stack submit --help` documents. The new PR defaults to draft.
  - Do not pass `--open`, because it would also mark #12 ready.
  - stdout is piped so that it is not a terminal.
  - Submit reuses #12 and creates the `feature/api-routes` PR inside one native stack.
- **If submit says stacks are unavailable**
  - As `dev`, read the stack-list endpoint and `acme/web` itself.
  - The stacks are unavailable only if the stack-list endpoint returns 404 while the repository read succeeds. In that case, report a blocker and offer ordinary dependent PRs.
  - For any other failure, retry once if it is transient; otherwise report a blocker. Decline any offer to create regular PRs.
- **Copy**
  - pr Draft-only composes the new PR's title and body, with no stack map. Apply them with `BIND gh pr edit <new-url> --title "<title>" --body-file <body-file>`.
  - Edit #12 only to remove a stack map, if it has one. Keep #12's draft or ready stage.
- **Verify**
  - Read the stack endpoint again. It must show #12 and the new PR in one native stack, in bottom-to-top order.
  - Run a fresh `gh pr view` for both PRs and check head, base, title, body (no map) and draft state.
  - If the stack is missing or split, rerun submit once. If membership is still wrong, report a blocker.
- **Follow up:** run the pr-followup Drive pass for the new layer. In T3 Code, arm its watch in one batched host invocation.

**`wt` commands:** none.

**Reported:** pr returns `handed-off` with stacked-pr's result:

- The created PR URL, plus head and base SHAs and draft state.
- Reused #12.
- The native stack number.
- The review gate report and its profile.
- The executed commands.
- The Drive or watch status.

**Asked:** nothing on the expected path. A question comes up only for a blocker, an unrelated tracked layer that submit would publish, or a review item that needs the user's decision.

---

## J. "Create a PR for my branch hotfix/rounding against release/1.2" (#61 is yours, but from a fork)

**Skills loaded, in order:** the same as H. pr `SKILL.md`, then `publication.md#github-account`, `review-gate.md`, `claims.md`, `review-packet.md`, `publication.md` and `continuation.md`, then invoke pr-followup in Drive mode. stacked-pr is not loaded.

**What pr does**

- **Exact PR:** the lookup for `hotfix/rounding` in `acme/web` returns none.
- **Base:**
  - Run `git fetch origin release/1.2`. This verifies `acme/web`'s own `release/1.2`, not the fork's.
  - Run `BIND gh pr list --repo acme/web --state open --head release/1.2 --json number,url,author,headRepository,headRepositoryOwner`. It returns #61, whose head repository is `dev/web`.
  - pr keeps only results "whose head repository is the target", so #61 is discarded. `--head` matches the branch name only, which is why the fork PR appears in the results.
  - No same-repository open PR is headed by `release/1.2`, and nothing else signals a stack. pr keeps the Create.
- **Review gate:** reuse the validated exact-range report, which has no findings.
- **Compose:** per claims.md and review-packet.md, with no stack map.
- **Publish:** push if needed with `git push -u origin HEAD:refs/heads/hotfix/rounding`, check with `BIND gh api user --jq .login`, then:

```
GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "<title>" --body-file <body-file>
```

  The head is the plain branch name, with no `owner:` prefix, because the branch lives in `acme/web` itself.
- **Verify, register and continue:** as in H, continuing into pr-followup Drive.

**`gh stack` / `wt` commands:** none.

**Reported:** `created`, with the standard fields. A context note says that #61 is the fork's `dev/web:release/1.2` and is unrelated to the base.

**Asked:** nothing.

---

## K. "Create a worktree for a new branch docs/typo off main so I can fix a typo"

**Skills loaded, in order**

1. worktrunk `SKILL.md`
2. worktrunk `references/switch.md`. The agent's shell cannot keep directory changes, so the destination path must come from structured output.

Not loaded:

- stack-worktree: this is not a stacked-PR workflow, and its own text says that for one isolated branch you use plain `wt switch --create`.
- stacked-pr: no dependent branch.
- pr: no PR was requested.

**Exact command, run inside the repository**

```
wt switch --create docs/typo --format=json
```

- `main` is the default branch, and new branches use the default branch as their base. `--base main` would therefore be redundant.
- If the installed version rejects `--format`, check `wt switch --help`.
- Take the worktree path from the JSON result and set it as the working directory for each later command.

**Reported:** the branch `docs/typo`, its base `main` at the recorded SHA, and the new worktree path.

**Conditions**

- If a project hook needs approval in the non-interactive shell, report it and use worktrunk's `references/project-config.md`. Do not add `--no-hooks` without authorization.
- If `wt` is unavailable, report a blocker. Never fall back to `git worktree`.
- If the repository has no `.config/wt.toml`, suggest creating it (global rule).

No PR and no commit are made at this step.

**Asked:** nothing.

---

## Files read (sha256)

| File | sha256 |
| --- | --- |
| probes/arm-4.md | 23e95b58fa070b1df2e3c8f6647e8103cde9a34268ac6daf3914cfc73cb9d74c |
| arms/arm-4/pr/SKILL.md | 868ab12421531652a4418e6f27378316c8ca591e6bf83d9788257580e67ae60d |
| arms/arm-4/pr/references/publication.md | e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f |
| arms/arm-4/pr/references/review-gate.md | 67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d |
| arms/arm-4/pr/references/claims.md | ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887 |
| arms/arm-4/pr/references/review-packet.md | 7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3 |
| arms/arm-4/pr/references/continuation.md | 471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c |
| arms/arm-4/stacked-pr/SKILL.md | 1613cb23ba546cf43ffba2185e2ea2018c110180c28f71231e836b5081695297 |
| arms/arm-4/stacked-pr/references/manual-chain.md | 132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7 |
| arms/arm-4/stacked-pr/references/manual-create.md | bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0 |
| arms/arm-4/stacked-pr/references/cli-workflow.md | 903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710 |
| arms/arm-4/stacked-pr/references/cli-create.md | e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5 |
| arms/arm-4/stacked-pr/references/stack-design.md | 4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296 |
| arms/arm-4/stacked-pr/references/troubleshooting.md | d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc |
| arms/arm-4/stacked-pr/references/api-workflow.md | 8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b |
| arms/arm-4/stack-worktree/SKILL.md | c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2 |
| arms/arm-4/worktrunk/SKILL.md | 517081b22ef7a82fb63571fdbfba028fc4a0fac233a0649c6141357a3db09592 |
| arms/arm-4/worktrunk/references/switch.md | a94d75dc3e23c3f41aafc7e6775f7b86380bd11dc9d06e6e7f1293e92621b8a2 |

The `arms/arm-4/` paths are relative to . stack-worktree/SKILL.md was read to decide whether it applies to I and K. It is not loaded in either case.

Paths are relative to <scratch>.

## Case L (pr-followup eval 3), same runtime, rendered probe sha256 d35919dd...

Model: Claude Opus 5.5 (claude-opus-5-5)

# Case L: direct `pr-followup` Drive of draft PR https://github.com/acme/web/pull/77

## Skills loaded (in order)

1. `pr-followup` (`<root>/pr-followup/SKILL.md`). This is the only skill loaded at the start. I read its references at the boundaries where the skill names them:
   - `references/feedback.md` and the file it includes, `references/github-collection.md`, for the feedback collection.
   - `references/ci-and-observation.md` for the failing lint job, for base maintenance, and before I arm the host watch.

Other skills load later and only when their boundary arrives (pr-followup: "Load support only at the boundary that needs it"):
- `worktrunk`: only if the current linked worktree is not already on `fix/null-total` at the PR head SHA. It does the checkout (for example `wt switch fix/null-total`).
- `debug`: only if the lint failure has an uncertain cause.
- `github-actions`: only if the repair must change workflow YAML.
- `verify`: for the execution evidence (narrowest check, the lint command itself, build, broader smoke).
- `commit`: at the atomic boundary of the fix.
- `pr`: for publication. It does the actor binding for `dev`, the SSH and exact-destination checks, the lease push, the post-write checks and the full rewrite of the PR body from the published diff. I also use its identity checks again before `gh pr ready`.
- `comment-style`: only before I write a reviewer reply, if collection finds review threads.
- `issue-workflow`: only if a linked ticket exists and its policy selects `pr-ready` (at the ready transition), or a thread falls outside this PR and needs a tracking ticket.

Not loaded:
- `stacked-pr` and `stack-worktree`. Drive does not cover a stack or a dependent chain here: no open PR uses `fix/null-total` as its base, the base `main` heads no other PR, and the user never mentioned stacks. pr-followup invokes `stacked-pr` only "when Feedback or Drive covers a stack or dependent chain". Base updates for this ordinary PR use rebase under the standing policy ("route a stack to `stacked-pr`" does not apply).
- `pr-review-followup`. I use it only if the state check shows that `dev` reviewed the PR and did not author it.

## `gh stack` commands and `stacked-pr` invocation

None. I run no `gh stack` command and do not invoke `stacked-pr`. The installed `gh stack` v0.3.0 extension and the repository's stacked-PR setting do not matter here, because the PR is not part of a stack or chain. With no retained task state, I still record "ordinary PR, not a stack" in the new ledger.

## What I do first, in order

1. **Set the scope to Drive.** "Drive ... until approval" is an explicit babysitting request. Nothing in it says read-only, keep-draft or merge, and it sets no time limit, so no elapsed-time cutoff applies.
   - The stopping condition is a current formal APPROVED review that is valid for the current head under the repository's policy. Green checks or a bot's success comment do not count.
   - `acme/web` is an organization repository, so the Luis Urrutia personal-repository merge policy does not apply. I confirm this from the owner type in the metadata. I never merge and never enable auto-merge.
   - A draft PR is not a review stopper. Drive covers the ready transition after the readiness gates pass.

2. **Establish the exact PR state** (reads only), using `github-collection.md`, which starts with the metadata:
   - PR URL, target repo `acme/web`, head repo/ref/SHA (`fix/null-total`), base ref/SHA (`main`).
   - Open/closed state, `isDraft` (true), review decision, merge state and mergeability.
   - Repository merge requirements: required checks and required approvals.
   - The PR author, compared with the verified actor `dev`. If `dev` is a reviewer and not the author, I switch to `pr-review-followup`.
   - Any linked ticket.
   - Confirmation that the PR is not closed or merged, because repair work stops on a closed target.
   - Confirmation of the non-stack topology: no open PR has base `fix/null-total`.
   - Because it is a draft, I do not reconcile `pr-ready` yet.

3. **Start the ledger in ignored task storage.** No task state is retained, so I record the Drive start time (it sets the watch cadence and stays the same across wakes and pushes), the PR identity, head/base, the topology decision and the authorized actions.

4. **Register the PR with the host** if the host supports it and the PR is not registered yet (on T3 Code, `link_pull_request`). This is a host action, not a GitHub write. I do not arm the watch yet.

5. **Match the local checkout to the PR head before any edit.** I check that this WorkTrunk-managed linked worktree is on `fix/null-total` at the exact head SHA, and I preserve unrelated work and the index state. If it is on another branch or SHA, I load `worktrunk` for the switch. I never use raw `git worktree`.

6. **Collect every feedback channel, with full pagination** (`feedback.md` and `github-collection.md`):
   - Inline comments with replies.
   - Formal reviews.
   - Conversation comments.
   - GraphQL `reviewThreads`, with independent cursors for the threads and for the comments in each thread. Resolved and outdated threads stay in the collection.
   - Check runs for the head SHA, with their output summaries.
   - Annotations, including those on successful runs.
   - Commit statuses.
   - Actions runs and job logs, including reviewer output in green jobs.

   I record each item with its source ID and version. I skip PENDING reviews. Any inaccessible channel is a coverage gap, not an empty inbox.

7. **Investigate the failing lint job at the same time** (`ci-and-observation.md`):
   - I identify the required, optional and pending checks for the actual head.
   - I read the failing job's command, error and log (`gh run view <run-id> --repo acme/web --log`) and the source it points to.
   - I classify the failure as a product defect, a workflow configuration problem, an environment problem or flaky behavior. A lint failure is normally deterministic, so I do not rerun it. I disable nothing and weaken no rule.
   - I load `debug` only if the cause is uncertain, and `github-actions` only if the workflow itself must change.

Every review thread then gets a disposition. If the cause is clear, the next part of the loop is:
- Make the smallest root-cause fix.
- Verify it with `verify` and the project checks: the lint command, a narrow test, the build and a smoke path.
- Commit with `commit`.
- Publish with `pr`, push with lease and update the whole PR body.
- Take a fresh snapshot for the new head.
- When CI is fully green and all feedback is settled, run `gh pr ready` after the `pr` identity checks and verify `isDraft=false`.
- Take a fresh post-ready snapshot, which covers workflows and reviewers that the ready state triggers.
- Arm the host watch (on T3 Code, `watch_pull_request`) right after the final snapshot and end the turn.

Drive keeps waiting until a verified current approval. Then I stop the watch and report: the PR URL, the head, the commits, the exact verification commands and their results, the current checks, any remaining items, and the state (`complete for requested scope`, `waiting` or `blocked`).

## Files read (sha256)

- `probes/arm-4-l.md`: d35919dde23ddf7667097571b6d448f34c77a5ca4ba5db420ec11c43266dd9e4
- `arms/arm-4/pr-followup/SKILL.md`: 9d7b8f0615d20e6be2f42564a672ed1aa178c1dfdd0b550b6e9fb59a3dd85b6c
- `arms/arm-4/pr-followup/references/feedback.md`: c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd
- `arms/arm-4/pr-followup/references/github-collection.md`: 38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400
- `arms/arm-4/pr-followup/references/ci-and-observation.md`: 0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c

I also ran `ls -R` on the skills root to list its files, which goes beyond the probe's "`shasum` only" command rule. It read no file contents.
