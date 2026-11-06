# Dry-run probe output: Codex, baseline

- Host: Codex delegate, gpt-6.1-sol, reasoningEffort high, read-only
- Runtime: baseline arm (f2150614), rendered probe sha256 a08ce8cd... (cases A-F) and f662e403... (cases G-H)
- Probe: stacked-pr-probes/probe-entry-points.md
- Limit: a plan of actions; no tool executed and no GitHub write.

## Cases A-F (verbatim)

Provider: OpenAI; model: gpt-6.1-sol; reasoning effort: high.

This is a dry run. No Git, GitHub, network, implementation, review, or watch operation below was executed. The probe hash matches the supplied value.

All hypothetical gh commands use the verified actor's binding:
`GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh …`
Here `actor` is the verified login from the setup; its actual name was not supplied. Titles and body-file paths below are prepared, evidence-backed inputs, not invented PR content. Git transport stays on SSH.

The fixture establishes that v0.3.0 is installed and eligible under the default three-day cooldown, Git is sufficiently recent, and native stacks are enabled. No extension installation or upgrade is needed. The skills still require live subcommand help before mutation. This dry run prohibits that lookup, so I identify commands whose argument forms remain dependent on help rather than inventing flags.

A. Load `stack-worktree` for the project worktree workflow, then `stacked-pr` for topology and submission. Select its CLI route, loading `cli-workflow.md`, `cli-create.md`, `stack-design.md` and `troubleshooting.md` for existing-branch adoption and linked worktrees. Load `worktrunk` and `references/switch.md` before worktree operations. Load `pr` for each Review gate, later Draft-only presentation, and `pr-followup` for Drive.

The plan is `main <- ci/carry-approval <- storybook/anchored-clock`. The first concern already has a commit; preserve and adopt that tip. The second concern must be implemented and verified before its PR exists. WorkTrunk owns worktree lifecycle; gh-stack owns stack tracking, ancestry changes, pushing and submission. The project's plain-create examples do not replace the native submission procedure selected by stacked-pr.

First inspect worktrees with `wt list`. Adopt the existing bottom branch with the current gh-stack init/adopt form from live help. Create the upper worktree with:

```sh
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
```

Continue in the returned directory, implement the upper concern, invoke `commit` at atomic boundaries, and adopt/add that existing branch to the shared catalog. Do not invent init/add positional syntax: the supplied files explicitly delegate that syntax to live help. Verify both original ownership and parent ancestry, checks, and absence of a rebase need.

Invoke pr Review gate bottom-up: bottom against main, upper against ci/carry-approval. Invoke `review-code-changes` as directed by the gate: a fresh Codex context on the newest available Sol model, explicitly xhigh. Resolve findings and restack through the stack owner before reviewing the upper layer. Apply any supplied cap against each immediate base; none is specified here. The existing CI commit does not itself require editing workflows; invoke `github-actions` if workflow changes become necessary. No stack-aware-CI route is justified merely by the bottom layer containing CI code.

After both layers pass, the PR-creating operation for BOTH layers is:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh stack submit --auto --remote origin
```

Run with stdout not attached to a terminal. Confirm requested draft handling in live help; omit `--open` because it also readies existing drafts. Neither layer is opened with `gh pr create`. One submit after both layers are ready avoids presenting a single PR as an established native stack. If deliberately submitting the bottom first, the same submit operation creates it, but native membership remains pending until the second PR exists.

For each newly created PR invoke pr Draft-only, then apply its verified title/body with actor-bound `gh pr edit <exact-url> --title <title> --body-file <file>`. Native bodies carry no stack map. Verify actual heads, immediate bases, draft states and membership through the documented GitHub stack endpoint; local JSON and PR bases alone are insufficient. Report both URLs, revisions and stack number, or partial publication and the exact blocker.

Follow-up: run a Drive pass on every layer before waiting. Each pass returns to stacked-pr; it does not nest a watch or stop the other layer's first pass. The owner completes authorized repairs, refreshes affected passes, then batches watches for all waiting layers. As a test sub-agent I would return pending watch actions to the parent and arm none. In this organization repository, green CI does not authorize a merge: Drive stops on verified current formal approval or merge; merging requires separate applicable authorization. A default draft does not mean keep-draft.

B. Entry order: the caller's already-loaded stack-worktree, then pr, then stacked-pr when pr resolves the explicitly dependent topology. Load the same CLI/adoption references as A; worktrunk is already relevant to the linked checkout.

Pass the verified bottom-layer facts to stacked-pr: branch ci/carry-approval, head 0e5c9c4, base main at 2105bea, no PR, upper layer planned. Preserve that tip, check ancestry, and let stacked-pr adopt it. There is no reason to ask whether the user wants ordinary dependent PRs: none was requested.

pr does not independently push and open an ordinary PR with `gh pr create`. Its result at this boundary is a handoff to the stack submission owner. If the owner submits the currently available single layer after its Review gate, the PR-creating command is the actor-bound `gh stack submit --auto --remote origin` above; report native membership pending until layer 2 exists. Alternatively build layer 2 and submit both as in A. pr later supplies Draft-only copy and verified publication metadata to the owner.

C. Entry order: worktrunk and its switch reference, then stacked-pr for the dependent PR request, then pr for Review gate and Draft-only, then pr-followup for continuation. Load CLI creation, design and troubleshooting/adoption references. The project stack-worktree skill also applies to stacked worktree setup; it does not acquire stack mutation ownership.

After `wt list` and preserving the parent state:

```sh
wt switch --create storybook/anchored-clock --base ci/carry-approval --format=json
```

Use the returned path. Worktree creation alone produces no new change or PR. Implement, commit and verify the requested upper concern; if its requirements are unavailable, report that prerequisite instead of manufacturing a change.

Adopt the bottom and upper branches into gh-stack in order, retaining tips and reusing https://github.com/acme/web/pull/2488. This request includes creating/submitting the stack, so conversion is within the requested operation. After the upper Review gate, actor-bound `gh stack submit --auto --remote origin` creates the upper PR and links the two PRs. It must not create a duplicate bottom PR or use plain pr Create for the upper layer. Preserve the existing bottom PR's stage and body, except removing any stack map. Compose the new upper body through pr Draft-only. Verify remote membership, bases and draft states, then run the coordinated Drive passes. Report reused bottom URL, new upper URL, stack number, revisions and pending work.

D. Entry order: pr-followup, then stacked-pr BEFORE independent per-layer mutations or watches. Load its CLI route, troubleshooting/adoption and maintenance references; load cli-create for the adoption procedure. Inspect native membership explicitly: the known ordinary PR bases do not establish a native stack.

The first decision is a conversion question, before adoption: “These two PRs are ordinary dependent PRs. Convert them into a native GitHub stack before continuing Drive, or keep them as an ordinary dependent chain?”

This question is required by stacked-pr/references/cli-workflow.md: for an operation other than create/submit on existing unstacked PRs, “ask before adoption whether to convert it, because sync links two or more open PRs into a native stack.” Earlier stack intent does not erase that operation-specific instruction. Do not silently sync, submit, or call `gh stack link`.

On consent, adopt ci/carry-approval then storybook/anchored-clock without changing their tips, and use the current non-interactive `gh stack sync` form from live help, including `--remote origin` where accepted. It links the existing PRs; no new PR-creating command is needed. Keep both drafts and remove stack maps. Before Drive passes continue, require one mutation owner, verified ancestry and direct bases, unchanged intended heads, matching local tracking, and a fresh remote read proving both PRs share one native stack in the intended order. Report any mismatch as blocked.

If conversion is declined, that is explicit selection of the manual route. Load manual-chain.md, retain the ordinary PRs, verify their ancestry/bases and accurate maps, and continue Drive under stacked-pr's single ownership. Do not require native membership on that route. Run every layer's pass before coordinated waiting, under the same draft-readiness and organization-repository limits as A.

E. Entry order: pr, its publication/review-gate/claims/review-packet references, then pr-followup after verified creation. No stacked-pr, stack-worktree or gh-stack operation is needed. Accept the supplied exact-range review report after checking that it satisfies the required profile, full coverage and current revision; otherwise the gate is not yet satisfied.

After the exact-PR recheck, destination verification, necessary explicit branch push and prepared title/body, create the default draft with:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh pr create --repo acme/web --base main --head fix/null-total --draft --title "$title" --body-file "$body_file"
```

Read back and verify the result, register its URL with the host, report the review gate and validation, and continue Drive unless create-only was requested. No invented title, validation or URL is justified by this fixture.

F. Entry order: the already-running stacked-pr manual route (manual-chain.md, manual-create.md and stack-design.md), then pr Create and its publication/review references. Reuse the qualifying exact-range review report. The user explicitly selected ordinary dependent PRs, so pr returns publication to that owner rather than restarting native routing.

After exact-head discovery confirms no matching open PR and the already-pushed head is verified:

```sh
GH_TOKEN="$(gh auth token --hostname github.com --user "$actor" || echo none)" gh pr create --repo acme/web --base stack/01-schema --head stack/02-api --draft --title "$title" --body-file "$body_file"
```

No `gh stack` mutation runs. The body carries the ordinary chain's bottom-to-top map with this PR marked; refresh the other open member's map after the new URL is known. pr verifies the created remote PR and returns `created`, exact URL, head/base SHAs, draft state, title/body budget, review report/profile/dispositions, actual validation and remaining work to stacked-pr. Continuation returns to the authorized owner, which coordinates all Drive passes and pending watches rather than starting a competing loop.

Files read and SHA-256:

The paths below are relative to:
`<scratch>/arms/arm-2/`
except the three explicitly absolute paths. The two local rule files were required by the supplied AGENTS.md. No other scratchpad files were read.

```text
8d16938aa89dbb3d3d10ad4c0e8e3cd889ee49cb5c98e5c71be959ebad256bd0  <personal rules file>
91dbbe6b14981106b6d7a5bc6f46e8f93f064274a4662d33c91ba5bbd971593f  <personal rules file>
a08ce8cd01d8f16caf4687bf110171e94a7d72d5a6c8c8602e8c3f775c79c9cc  <scratch>/probes/arm-2.md
c17d76795825d3dcb233e01014473f30b7953cf94f93ed77a1a3075b655af7f2  stack-worktree/SKILL.md
2e675d9a813fffc7dee5e8e8e917c275db9204fe1fe7613aa52eac0dbc00e51d  stacked-pr/SKILL.md
5ba92f094b67fa2f928b9c181bdc26adfa68c5fbe74e16de7a8fe127100a009f  pr/SKILL.md
a61c0704f1b5343a18c1bbbea729f76166c52f4a0b5aa26cd9b54dc375d13531  pr-followup/SKILL.md
aba8d9fd202de9144b8ef0a7f945c8db487aeac53c3aaf7ad1341013a0e5bf94  worktrunk/SKILL.md
903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710  stacked-pr/references/cli-workflow.md
a94d75dc3e23c3f41aafc7e6775f7b86380bd11dc9d06e6e7f1293e92621b8a2  worktrunk/references/switch.md
e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5  stacked-pr/references/cli-create.md
d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc  stacked-pr/references/troubleshooting.md
4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296  stacked-pr/references/stack-design.md
e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f  pr/references/publication.md
67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d  pr/references/review-gate.md
471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c  pr/references/continuation.md
132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7  stacked-pr/references/manual-chain.md
0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c  pr-followup/references/ci-and-observation.md
ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887  pr/references/claims.md
7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3  pr/references/review-packet.md
8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b  stacked-pr/references/api-workflow.md
0eaecaabad806aaa60a65ddb68572b829a6ebf6504cddc75532c4e6930cf2f83  stacked-pr/references/cli-maintain.md
bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0  stacked-pr/references/manual-create.md
c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd  pr-followup/references/feedback.md
38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400  pr-followup/references/github-collection.md
4bd552ace395c347f3605a8919524ede74d202e22ec0178d25e498052bba6ca8  pr/references/visual-evidence.md
f11316f98a0db6277ddb9f3781ce1ee4cbfdb1b5201fea4fb9079c2e770a3b8b  pr/references/attachments.md
```


## Cases G-H (verbatim)

Provider: OpenAI; model: gpt-6.1-sol; reasoning effort: high.

This is a dry-run answer. No GitHub, network, stack, publication, or watch command was executed. Only the requested answer file was created.

G. Watch wake for the planned bottom layer

Skills, in operational order: pr-followup (resume Drive), stacked-pr (retain stack ownership and select the CLI route), worktrunk (worktree boundaries), and pr (publication/Update when needed). Invoke commit, verification/debug support, comment-style, and issue-workflow only at their applicable boundaries; their files were not loaded.

1. Restore the original Drive start time, ledger, authority, watch state, and retained stack ownership. Refresh https://github.com/acme/web/pull/2501 from GitHub: exact head/base repositories, refs and SHAs, open/closed/merged state, draft state, checks and review state. Reconcile an externally observed ready event if applicable; check for merge before continuing repair.
2. Return stack coordination to stacked-pr before any ancestry or publication mutation. Its planned-stack ownership survives the bottom layer targeting main and its native membership being pending. Neither fact makes this an ordinary standalone PR. Select the CLI route from the supplied extension listing: v0.3.0 is eligible under the default cooldown, Git 2.50 and shared worktrees are supported. No install or upgrade is needed. Refresh local tracking and remote membership; PR head/base fields alone cannot establish membership.
3. Collect all feedback channels, including the new published review comment, edited replies, resolved/outdated threads, formal review bodies, conversation comments, check summaries/annotations, status contexts, and reviewer output in successful as well as failed CI jobs. Paginate fully. Re-read current PR metadata after collection. Inaccessible evidence stays unknown.
4. Evaluate the comment against current code and requirements. Apply a supported in-scope improvement; investigate uncertainty; ask immediately only for a consequential unresolved decision. Continue independent work. A notification alone does not establish that a repair is needed.
5. For a repair, keep stacked-pr as the sole mutation owner. Verify the changed behavior, build and broader smoke path; invoke commit for an atomic change. Use the CLI maintenance route for any needed upward cascade and safe publication, preserving tips and unrelated changes. Do not use a standalone rebase or direct Git push to bypass gh-stack tracking. Refresh the complete PR description through pr Update from the verified published diff. Re-read the thread, invoke comment-style, reply with published evidence, and resolve only as its disposition permits. Outside-scope findings require their tracking ticket; confirmation-dependent threads stay open.
6. Reassess the draft readiness gates from a fresh snapshot. The current draft state is not a keep-draft instruction. Mark ready only after every required gate is established, then perform fresh post-ready collection, including newly triggered checks and reviewers. acme/web is an organization repository, so the personal-repository automatic merge policy does not apply; do not merge without the required separate authority.
7. Return this layer's current head/base, disposition, checks and pending watch action to the stack owner. It completes any other in-scope layer passes and mutations before waiting. Reuse active watches; batch activation of all unwatched waiting layers through the owner. On a user-facing blocker, question, completion, or a handback required by uncovered events, unwatch before returning. Otherwise yield to the existing host watch without polling. Preserve the original Drive timing.

PR creation: none on this wake. Do not create the planned second layer merely because this layer woke.

gh stack commands: no unconditional mutating command is justified by the notification. In live execution, establish the installed contract with gh stack --version and command help, then use the help-confirmed JSON inspection form and remote stack reads. If repair requires it, the owner uses the help-confirmed cascading rebase and safe push forms with origin wherever --remote is accepted. Do not blindly run gh stack sync or gh stack submit merely to eliminate the expected pending membership.

Report the new comment's actual disposition and any repair/publication/readiness change, current revision/check/review state, and remaining prerequisites. Continue reporting native membership as pending until the second layer exists; do not claim a verified native stack yet. The retained planned-stack authorization does not need a new conversion question. If the wake changes neither a decision nor remote state, yield without a status message or PR comment.

H. Create hotfix/rounding against release/1.2

Skills, in operational order: pr (Create and identity/base resolution), stacked-pr (dependent topology and submission ownership), worktrunk (worktree boundaries), then pr for the per-layer review gate and Draft-only presentation, and pr-followup Drive after verified submission.

Handoff instead of a standalone PR-creating command:

“stacked-pr: handle creation of hotfix/rounding against the verified release/1.2 base in acme/web, origin over SSH. Existing https://github.com/acme/web/pull/50 is release/1.2 -> main and belongs to release-manager. No hotfix PR exists. Preserve that existing PR's commits, base and draft/review stage, and unrelated work. Establish tracking/ownership and ancestry before adopting anything. Use the CLI route with installed gh-stack v0.3.0. Reuse the supplied validated review report if its exact range and required review profile match; no findings need repair. Create the missing upper PR through the selected stack route, verify actual native membership, and continue follow-up under one mutation owner.”

The pr skill explicitly routes dependent-branch topology to stacked-pr. The supplied base is the head of an open PR, so the candidate chain is main <- release/1.2 <- hotfix/rounding. These loaded rules provide no exception merely because the lower PR has another author or the user omitted the word “stack.” Do not silently choose main as the hotfix base.

The CLI owner inspects tracking and ancestry, preserves existing tips, and uses the help-confirmed init/adopt form if needed. On that route, gh stack submit creates the missing PR; gh pr create is not the creation command. Its currently documented non-interactive form is gh stack submit --auto, with stdout not attached to a terminal and origin supplied wherever live help supports --remote. Confirm the actual draft-state flags in live help before executing. Default the new PR to draft. Do not use --open to inadvertently ready the existing PR.

Before submit, ensure every active tracked layer is in scope. If another active layer would also be published, ask before submitting. A different PR author alone does not justify rewriting or broadening that PR's work. If ownership or intended scope cannot be established, stop that mutation and ask the precise ownership/scope question.

After submit, use pr Draft-only for the new PR's title/body and apply the metadata with gh pr edit; change a reused PR only as authorized, including removal of a stack map. Read the actual remote stack endpoint to verify membership; successful submit, local tracking and PR bases are insufficient. Report created versus reused PRs, actual head/base/draft state, native membership, review evidence and remaining gates. Do not invent a new PR number or stack number. Continue Drive unless the user requests create-only; no such limit is supplied here.

Read manifest

Actual skill-file read order across this dry run: pr-followup, pr, stacked-pr, worktrunk. The per-case sequences above describe execution/handoff order. No stack-worktree or github-actions skill was loaded: neither worktree creation/cleanup nor workflow changes are requested. Other named support skills are described, not read, as the probe requires.

Paths below are relative to:
<scratch>/arms/arm-2

SHA256  File
a61c0704f1b5343a18c1bbbea729f76166c52f4a0b5aa26cd9b54dc375d13531  pr-followup/SKILL.md
5ba92f094b67fa2f928b9c181bdc26adfa68c5fbe74e16de7a8fe127100a009f  pr/SKILL.md
2e675d9a813fffc7dee5e8e8e917c275db9204fe1fe7613aa52eac0dbc00e51d  stacked-pr/SKILL.md
aba8d9fd202de9144b8ef0a7f945c8db487aeac53c3aaf7ad1341013a0e5bf94  worktrunk/SKILL.md
0eacadb3574de2e4364fc4ecd1c38d9053cb4df7570e7a30e3aa8158b4c7174c  pr-followup/references/ci-and-observation.md
c66b96fa26ca085ed17224b6619d705a4b5b7e3e7f7da4c9de60b80d730ff7dd  pr-followup/references/feedback.md
38a5d0e3f8758a335cfe03f5a8e43b4f2338a2276646f379d97fe9920a49b400  pr-followup/references/github-collection.md
903880ed1226a5024a64920d93e21fdd4fbbd04b8e4d3a79d26ea097142cd710  stacked-pr/references/cli-workflow.md
0eaecaabad806aaa60a65ddb68572b829a6ebf6504cddc75532c4e6930cf2f83  stacked-pr/references/cli-maintain.md
e6bad738c61bbc347347f8d1b3fec779b2ac2e7b001403ca8a91501561d4dcc5  stacked-pr/references/cli-create.md
d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc  stacked-pr/references/troubleshooting.md
4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296  stacked-pr/references/stack-design.md
e2e564257673c1e018a7134a8a2c28585545f6865ef202c2b6f1b8c8902ce25f  pr/references/publication.md
67196719b0ca16fc136cae2288ae48b36e239f0c42ac38c75a756153dd69b06d  pr/references/review-gate.md
ab57710eb4e310080eac414838a781b352ba7c422f59610f00cda0d87bab2887  pr/references/claims.md
7cf33764d92709d6c8a7f368ae1820c094eb8eb167e22f424922b481274114b3  pr/references/review-packet.md
471f98dd541f2801045e3b8705eda458b741e2a3c135fa27fc24c4a965cf316c  pr/references/continuation.md

Additional files read (absolute paths):
8d16938aa89dbb3d3d10ad4c0e8e3cd889ee49cb5c98e5c71be959ebad256bd0  <personal rules file>
91dbbe6b14981106b6d7a5bc6f46e8f93f064274a4662d33c91ba5bbd971593f  <personal rules file>
f662e403fae3adda16285d6ee321c0d4f7eb618135353400d7e18c0a45995432  <scratch>/probes/arm-2-gh.md

