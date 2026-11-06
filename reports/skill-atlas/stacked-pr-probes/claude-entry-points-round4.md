# Dry-run probe output: Claude Code, round 4

- Host: Claude Code general-purpose subagent, claude-opus-5-5, default effort, read-only
- Runtime: round-4 candidate arm, runtime manifest sha256 0d4a5d41e97079a9339ccf831f3944cec6cefe45166ea6de6e257c7c2afe7918, rendered probe sha256 a773e038...
- Probe: stacked-pr-probes/probe-entry-points.md, round 4
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases F, H, I, J (verbatim)

Model: Claude Opus 5.5 (claude-opus-5-5)

# Dry-run answers for arm-5 (cases F, H, I, J)

Skills root: arms/arm-5

Conventions for all cases:

- The actor is `dev`. Every `gh` command carries the binding from `pr/references/publication.md#github-account`, reads and rate-limit checks included. I write the binding in full on the commands the probe asks for. The binding is `GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)"`.
- Before the first GitHub write, `gh api user --jq .login` under the binding must print `dev`. The setup says it does.
- The target is on github.com, so `gh api` calls take no `--hostname`.
- The default is a draft PR (`pr/SKILL.md`, Create: "Default to draft unless the user prefers ready"). No case states a ready preference.
- `<title>` and the body file are placeholders. The title follows the repository convention, which I read from written rules, merged PRs and base commit subjects. The body is written to an ignored temporary file. The diff content is not given, so the dry run cannot fix them.
- No case sets a review-size cap, so Check cap does not run. No case names a ticket, so `issue-workflow` runs only if the branch, commits or body turn out to reference one.

---

## Case F: manual route, `pr` Create for `stack/02-api` on `stack/01-schema` (#40)

### Skills loaded (in order)

1. `stacked-pr/SKILL.md`, the caller. Routing ran `gh extension list`, which shows `github/gh-stack v0.3.0`. The user explicitly asked for ordinary dependent PRs, so routing selected **Manual**.
2. `stacked-pr/references/manual-chain.md`
3. `stacked-pr/references/manual-create.md`
4. `stacked-pr/references/stack-design.md`. Plan and build directs it. The layer is already built and pushed, so it only confirms the bottom-to-top plan `main <- stack/01-schema <- stack/02-api`.
5. `pr/SKILL.md`, in Create mode, invoked by `stacked-pr`.
6. `pr/references/publication.md`, GitHub account section, before the first `gh` command.
7. `pr/references/review-gate.md`
8. `pr/references/claims.md`
9. `pr/references/review-packet.md`
10. `pr/references/publication.md`, the remaining sections, before the mutation.
11. `pr/references/continuation.md`

`attachments.md` and `visual-evidence.md` are loaded only if the diff has a visible UI change or needs a visual. The case does not say so.

If the session loaded `stack-worktree` next to `stacked-pr`, it adds no step here. No worktree is created. The selected route owns PR creation and bodies, so its "Stacked on #N" line yields to the manual route's bottom-to-top map.

### What `pr` does

1. **Operation.** The request is Create. The base `stack/01-schema` is the head of open PR #40, which makes this a stack layer. `stacked-pr` invoked this Create, so `pr` does not invoke it again ("Unless `stacked-pr` invoked this Create...").
2. **Identity and scope.** `git status --short --branch`, `git remote -v`, the upstream, and `git rev-parse HEAD`. The push destination is `origin`, which is `acme/web` over SSH. The target is `acme/web`.
3. **Exact PR.**
   `GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr list --repo acme/web --state all --head stack/02-api --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`
   I match both the branch and the head repository `acme/web`. The setup has no existing PR for this branch.
4. **Base.** `git fetch origin stack/01-schema`, then verify the ref identity. The base is not the default branch, so `pr` runs the base lookup. **Exact lookup command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:stack/01-schema -f state=open --jq '.[] | select(.head.repo.full_name == "acme/web") | {number, author: .user.login, head: .head.ref, head_repo: .head.repo.full_name, base: .base.ref}'
   ```

   The expected result is #40. A failed or incomplete lookup would block Create. #40 confirms the parent that `stacked-pr` declared.
5. **Revision.** Record the base and head SHAs. Inspect `git log stack/01-schema..stack/02-api` and `git diff stack/01-schema...stack/02-api`.
6. **Review gate.** The validated `review-code-changes` report's Scope covers the exact `<merge-base>..<head>`, so I reuse it. The condition is that its recorded profile matches the gate profile: a fresh Codex context, newest Sol model, `xhigh`. Otherwise the review runs again on that profile. The report has no findings and no open questions, so nothing is fixed and no repeat review runs.
7. **Compose.** Read the repository instructions, `CONTRIBUTING.md`, templates on the base, recent non-bot merged PRs (the `gh pr list --state merged ...` query from `pr/SKILL.md`), and `git log --no-merges --format=%s -20 origin/stack/01-schema`. The body follows the review packet. It also carries the manual route's bottom-to-top map with this PR marked, for example `Stack: #40 (stack/01-schema) -> **this PR** (stack/02-api)`. The map is required because GitHub shows no chain for a manual chain. The body is measured with `wc -m` against the length budget.
8. **Publish.** The branch is already pushed, so there is no push. I check that `git ls-remote origin refs/heads/stack/02-api` equals local HEAD. I run `gh api user --jq .login`, which must print `dev`, and recheck the exact PR immediately before creating.
9. **PR-creating command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "<title>" --body-file "<ignored-temp-dir>/stack-02-api-body.md"
   ```

10. **Verify.** `gh pr view <url> --json url,headRefName,headRepository,headRefOid,baseRefName,title,body,isDraft`. I compare the head, base, title, body and draft state, then register the PR with the host and check the thread links.
11. **Continuation.** No ticket, so there is no `issue-workflow` call. Next is the `pr-followup` Drive pass for this layer. `stacked-pr` "Follow up layers" applies, so the pass returns its head/base, result and pending watch action to `stacked-pr`, the single stack mutation owner, and arms no watch. This follows `pr`'s "Return to an already authorized loop instead of nesting another".

### What `pr` returns (to `stacked-pr`)

- Status `created`.
- The new PR URL and number.
- Head `stack/02-api@<sha>` in `acme/web` and base `stack/01-schema@<sha>`, which heads #40.
- Draft state `true`, verified by a fresh read.
- Body length in characters against the budget, with the reason for any overrun. The budget is the second-longest recent merged body but at least 1,000 characters, or 2,500 when fewer than three bodies were measured. There is no detail comment unless the budget needs one.
- Validation tied to the current head.
- The review gate result: the reused report's path and profile, its scope `<merge-base>..<head>`, 0 findings and 0 open questions.
- The executed commands and their results: exact-PR lookup empty, base lookup returned #40, remote tip verified, create, verify.
- The Drive pass result and its pending watch action.
- Remaining work for `stacked-pr`. Put the same map, with #40 marked, in #40's body (`manual-create.md`: "Put the same bottom-to-top map in every body"), confirm every layer through fresh reads, then arm the layer watches as "Follow up layers" directs.
- The verified identity (`dev`), revision and publication state.

`gh stack` commands: none. The manual route does not use them. `wt` commands: none. Nothing is asked.

---

## Case H: `hotfix/rounding` against `release/1.2`, base heads #50 by `release-manager`

### Skills loaded (in order)

1. `pr/SKILL.md` (Create)
2. `pr/references/publication.md`, GitHub account section
3. `pr/references/review-gate.md`
4. `pr/references/claims.md`
5. `pr/references/review-packet.md`
6. `pr/references/publication.md`, publish, create and verify
7. `pr/references/continuation.md`

`stacked-pr` is not loaded and `stack-worktree` is not loaded.

### What `pr` does

1. **Exact PR:** `gh pr list --repo acme/web --state all --head hotfix/rounding --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`, under the binding, returns none.
2. **Base:** `git fetch origin release/1.2` and verify the ref. The base is not the default branch. **Exact lookup command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:release/1.2 -f state=open --jq '.[] | select(.head.repo.full_name == "acme/web") | {number, author: .user.login, head: .head.ref, head_repo: .head.repo.full_name, base: .base.ref}'
   ```

   The result is #50: author `release-manager`, head `release/1.2` in `acme/web`, base `main`.
3. **Stack-layer test.** `pr` sends a layer to `stacked-pr` only under three conditions:
   - the request or caller places the PR in a stack;
   - its base is the head branch of another open PR **by the same author**;
   - another PR will build on it.

   None holds. #50's author is `release-manager`, not `dev`, the user never mentions stacks, and nothing builds on this PR. So this is an ordinary Create with no handoff.
4. **Review gate.** The validated report covers the exact range with no findings, so I reuse it. The profile condition from case F applies. There is nothing to fix.
5. **Compose.** Same steps as case F, without a stack map.
6. **Publish.** `git push -u origin HEAD:refs/heads/hotfix/rounding` runs if the remote branch is missing or behind. The push goes over the SSH `origin`. Then I confirm `git ls-remote origin refs/heads/hotfix/rounding`. I run `gh api user --jq .login`, which prints `dev`, and recheck the exact PR.
7. **PR-creating command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "<title>" --body-file "<ignored-temp-dir>/hotfix-rounding-body.md"
   ```

8. **Verify and continue.** Verify with `gh pr view`, then register with the host. The continuation goes into `pr-followup` Drive, which arms the host watch. The user did not ask for create-only. There is no keep-draft instruction.

### Reported or asked

I report `created` with the URL, head/base, draft state, body length against the budget, the review gate result and the commands. I also tell the user one coordination point and leave it out of the body. `release/1.2` is the head of `release-manager`'s open #50 (`release/1.2 -> main`), so this hotfix reaches `main` through #50. Because #50 has a different author, the PR is not a stack layer and gets no native stack or map. Nothing is asked.

`gh stack` commands: none. `wt` commands: none.

---

## Case I: `feature/api-routes` against `feature/data-model`, base heads #12 by `dev`

### Skills loaded (in order)

1. `pr/SKILL.md` (Create)
2. `pr/references/publication.md`, GitHub account section, before the first `gh` command
3. Handoff: `stacked-pr/SKILL.md`
4. `stack-worktree/SKILL.md`. It is the project skill that covers stacks, and the `stacked-pr` description pairs the two. Only its worktree setup is kept.
5. `stacked-pr/references/cli-workflow.md`
6. `stacked-pr/references/cli-create.md`
7. `stacked-pr/references/stack-design.md`
8. `stacked-pr/references/troubleshooting.md`: the adoption and worktrees sections, because PR #12 already exists.
9. `stacked-pr/references/api-workflow.md`: the stack-list endpoint, for the post-submit read.
10. `pr` again, called by `stacked-pr`, in Review gate mode (`review-gate.md`) and in Draft-only mode (`claims.md`, `review-packet.md`).
11. `pr-followup` Drive.

### What `pr` does, up to the handoff

1. **Identity and scope.** Bind `gh` to `dev`. Run `git status --short --branch`, `git remote -v`, and read the upstream and HEAD. The target and push destination are `acme/web` over the SSH `origin`.
2. **Exact PR:** `gh pr list --repo acme/web --state all --head feature/api-routes --json number,url,state,headRefName,headRepository,headRepositoryOwner,baseRefName,isDraft`, under the binding, returns none.
3. **Base:** `git fetch origin feature/data-model` and verify the ref. **Exact lookup command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:feature/data-model -f state=open --jq '.[] | select(.head.repo.full_name == "acme/web") | {number, author: .user.login, head: .head.ref, head_repo: .head.repo.full_name, base: .base.ref}'
   ```

   The result is #12: author `dev`, head `feature/data-model` in `acme/web`, base `main`.
4. **Classification.** The base is the head branch of another open PR by the same author, so this is a stack layer and belongs to `stacked-pr`. `stacked-pr` did not invoke this Create. So `pr` invokes `stacked-pr` with the request **before the review gate**. `pr` passes the request, `acme/web`, trunk `main`, the SSH `origin`, actor `dev`, the parent #12 and both branch tips.
5. **Handoff, and what `pr` does not do.** No review gate in Create mode, no title or body, no push, and **no `gh pr create`**. `gh pr create` would open an ordinary PR outside GitHub's native stack. `pr` returns `handed-off` together with `stacked-pr`'s result. If `stacked-pr` were unavailable, it would report `blocked` instead.

### After the handoff (`stacked-pr`, for completeness)

- **Route.** The task is neither automation nor REST-owned. `gh extension list` shows `github/gh-stack v0.3.0`, and the user did not ask for ordinary PRs. So the route is **CLI**. Recorded observation: the extension listing.
- **`stack-worktree`.** I keep its worktree setup, and it needs none: the branch exists in the current WorkTrunk worktree and all work is committed. Its `gh pr create --base feature/data-model`, `git push -u origin` and "Stacked on #12" line do not apply, because the CLI route owns PR creation, pushes and bodies. A native stack carries no map. `wt list` is the only `wt` command, a read-only check of where `feature/data-model` is checked out.
- **Live contract.**
  - `git status --short --branch`, `git remote -v`, `git --version` (2.50, at least 2.36) and `gh auth status`.
  - `gh extension list`, then `gh release list -R github/gh-stack --exclude-pre-releases --json tagName,publishedAt`. v0.3.0 was published 2026-10-26, which is 11 days ago. That is past the default three-day cooldown, so v0.3.0 is the eligible release and is already installed. There is no upgrade.
  - `gh stack --version`, and `gh stack <init|view|submit> --help` to get the non-interactive forms. Pass `--remote origin` where a command accepts it.
- **Inspect and adopt.**
  - The JSON stack view (`gh stack view --json`, per live help) is expected to show no local stack.
  - Plan from `stack-design.md`: `main <- feature/data-model (#12) <- feature/api-routes`.
  - Check ancestry with `git merge-base --is-ancestor feature/data-model feature/api-routes` and record both tips.
  - Adopt with the current `gh stack init` adopt form, bottom to top. Linked WorkTrunk worktrees are not another branch manager. If `feature/data-model` is checked out in another worktree, the `--print-path` form finds it. v0.3.0 supports stacks that span worktrees.
- **Review gate.** `pr` runs in Review gate mode for `feature/api-routes` against `feature/data-model`. This case supplies no report, so a fresh Codex child (in T3 Code, `delegate_task`) runs `review-code-changes` on the newest Sol model at `xhigh`. Fixes go through `commit`, followed by a repeat review.
- **PR-creating command (by `stacked-pr`, not `pr`).** `gh stack submit --auto --remote origin`, with flags confirmed from live help and stdout not a TTY. I add no `--open`, so #12's stage is kept. Submit reuses #12, creates the `feature/api-routes` PR as a draft, and links both into one native stack.
- **After submit.**
  - `pr` runs in Draft-only mode for the new PR. I apply its result with `gh pr edit <new-url> --title "<title>" --body-file <file>`, without a map. #12 changes only to remove any map it has.
  - I read the documented stack-list endpoint (https://docs.github.com/en/rest/pulls/stacks) to prove the order #12 then the new PR. If membership is missing or split, I rerun submit once.
  - I report the created PR, the reused #12 and the stack number. A Drive pass runs for the new layer, and its watch is armed in T3 Code's batched invocation.
- **Asked.** Nothing, unless the review finds something that needs a user decision.

---

## Case J: `hotfix/rounding` against `release/1.2`, branch name matches only fork PR #61

### Skills loaded (in order)

Same as case H: `pr/SKILL.md`, then `publication.md` (GitHub account), `review-gate.md`, `claims.md`, `review-packet.md`, `publication.md` (publish, create and verify), `continuation.md`. `stacked-pr` is not loaded and `stack-worktree` is not loaded.

### What `pr` does

1. **Exact PR:** `gh pr list --repo acme/web --state all --head hotfix/rounding --json ...` returns none.
2. **Base:** `git fetch origin release/1.2` and verify `acme/web`'s own `release/1.2`. **Exact lookup command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh api -X GET repos/acme/web/pulls --paginate -f head=acme:release/1.2 -f state=open --jq '.[] | select(.head.repo.full_name == "acme/web") | {number, author: .user.login, head: .head.ref, head_repo: .head.repo.full_name, base: .base.ref}'
   ```

   The result is a successful empty list. The `head` filter is owner-qualified, so GitHub does not return #61, whose head is `dev:release/1.2`. Even if #61 came back, `head.repo.full_name` is `dev/web`, not `acme/web`, so the filter would drop it. A successful empty result is "no PR is headed by the base". It is not an unknown, so Create is not blocked.
3. **Stack-layer test.** `acme/web:release/1.2` heads no open PR. #61 shares only the branch name, it is a different branch in the fork, and its author being `dev` does not matter. The request does not mention a stack. So this is an ordinary Create with no handoff. A branch-name-only `gh pr list --head release/1.2` would surface #61 and route this PR to `stacked-pr` by mistake, so I do not use it for this test.
4. **Review gate.** The validated report covers the exact range with no findings, so I reuse it, under the same profile condition.
5. **Publish.** `git push -u origin HEAD:refs/heads/hotfix/rounding` if the remote branch is missing or behind, then `git ls-remote origin refs/heads/hotfix/rounding`. I run `gh api user --jq .login`, which prints `dev`, and recheck the exact PR.
6. **PR-creating command:**

   ```sh
   GH_TOKEN="$(gh auth token --hostname github.com --user dev || echo none)" gh pr create --repo acme/web --base release/1.2 --head hotfix/rounding --draft --title "<title>" --body-file "<ignored-temp-dir>/hotfix-rounding-body.md"
   ```

   The head is a plain `hotfix/rounding` because head and target are the same repository, `acme/web`.
7. **Verify and continue.** Verify, register with the host, then continue into `pr-followup` Drive.

### Reported or asked

I report `created` with the URL, head/base, draft state, body length against the budget, the review gate result and the commands. A note for the user: fork PR #61 (`dev/web:release/1.2 -> main`) has the same branch name but is not this PR's base, and no stack was created. Nothing is asked.

`gh stack` commands: none. `wt` commands: none.

---

## Files read, with sha256

| File | sha256 |
| --- | --- |
| probes/arm-5.md | a773e038ddd8a320520cadd252a91b957d591b68a8f3f4b52f7e326a7b7bbdee |
| <root>/pr/SKILL.md | f8d840bfc87aae6c8b540d40f6ce2fd1026fe0972c9b2e463fa7c09b62ff94db |
| <root>/pr/references/publication.md | e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f |
| <root>/pr/references/review-gate.md | 67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d |
| <root>/pr/references/claims.md | ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887 |
| <root>/pr/references/review-packet.md | 7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3 |
| <root>/pr/references/continuation.md | 471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c |
| <root>/stacked-pr/SKILL.md | 1613cb23ba546cf43ffba2185e2ea2018c110180c28f71231e836b5081695297 |
| <root>/stacked-pr/references/manual-chain.md | 132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7 |
| <root>/stacked-pr/references/manual-create.md | bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0 |
| <root>/stacked-pr/references/stack-design.md | 4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296 |
| <root>/stacked-pr/references/cli-workflow.md | 903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710 |
| <root>/stacked-pr/references/cli-create.md | e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5 |
| <root>/stacked-pr/references/troubleshooting.md | d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc |
| <root>/stacked-pr/references/api-workflow.md | 8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b |
| <root>/stack-worktree/SKILL.md | c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2 |

`<root>` is arms/arm-5. I did not read `pr-followup`, `commit`, `review-code-changes`, `issue-workflow`, `attachments.md`, `visual-evidence.md` or the other route files. The commands above are planned, not run. The only commands run were `shasum -a 256` on the files listed here.

Paths are relative to <scratch>.
