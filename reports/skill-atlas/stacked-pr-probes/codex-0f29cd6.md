# Dry-run probe: Codex host

- Host: T3 Code delegate, Codex gpt-6.1-sol, reasoningEffort high, read-only.
- Runtime: `git archive 0f29cd6 stacked-pr` at /tmp/stacked-pr-head; manifest sha256 f0246d6299cf7dd2edd44d1c69ebd3a93e38138fb589792b9d876f4b08df4c1c.
- Probe: stacked-pr-probes/probe-0f29cd6.md.
- Limit: a plan of actions; no tool executed and no GitHub write.

## Output (verbatim, formatting condensed)

A
- Route: CLI, pending conversion approval.
- Deciding observation: github/gh-stack v0.3.0 is installed; WorkTrunk does not own stack tracking. The existing ordinary PRs are untracked and have no native stack.
- Plan: Inspect repository, authentication, versions, branch tips, ancestry, PR bases, and remote membership through reads. Record main, origin, and main <- model <- api. Stop before adoption.
- Writes before question: None. Neither adoption nor `gh stack init` runs.
- PRs created: None.
- Exact question: "Los PRs de `model` y `api` todavía no forman un stack nativo. Sincronizarlos con `gh-stack` los vinculará en uno. ¿Quieres convertirlos en un stack nativo o mantenerlos como PRs normales?"
- This pause follows cli-workflow.md: "ask before adoption whether to convert it".

B
- Route: Manual.
- Deciding observation: The user explicitly chooses ordinary dependent PRs.
- Writes before question: None; no adoption or `gh stack init`. No ownership migration is necessary because the chain was never tracked.
- Ordered plan: 1. Inspect ancestry, PR bases, dirty paths, worktree ownership, and local/remote tips; preserve the original commits. 2. Fetch origin through SSH. 3. Replay the entire chain from its top onto updated main, moving intermediate refs with their commits. Explicitly replay branches in their owning worktrees when necessary. 4. Verify model contains updated main, api contains updated model, and each incremental diff remains correct; run applicable checks. 5. Push affected refs atomically with explicit leases against the recorded remote tips. 6. Verify remote heads and PR bases (model -> main, api -> model); ensure both ordinary PR bodies carry accurate chain maps.
- PRs created: None; reuse both existing PRs.
- Question/blocker: None under the supplied facts.

C
- Route: CLI.
- Deciding observation: The user explicitly authorizes native conversion.
- Writes before question: None. Adoption and `gh stack init` occur only after that answer.
- Ordered plan: 1. Complete the CLI contract checks and read live help for every planned command; v0.3.0 already satisfies the cooldown. 2. Record dirty paths, branch/worktree ownership, original tips, PR bases, and intended remote objects; preserve existing commits. 3. Adopt model, then api, through the supported `gh stack init` operation. Verify JSON order and unchanged tips. Adoption does not perform the requested restacking. 4. Fetch origin, compare local and remote work, then run the supported non-interactive `gh stack sync` form. Pass `--remote origin` wherever supported. 5. Resolve any conflicts through the CLI recovery workflow; stop for a source decision if local and remote chains contain different work. 6. Verify updated ancestry, heads, bases, trunk agreement, checks, and preservation of unrelated state. 7. Verify the documented stack endpoint places both existing PRs in one native stack, in order. Remove their old chain maps and preserve their review stages.
- PRs created: None expected; sync links the two existing open PRs.
- Question/blocker: None further under the supplied facts.

D
- Route: CLI, blocked; offer manual conversion without taking it automatically.
- Deciding observation: The failed submit is confirmed by the stack endpoint's documented not-enabled response. A generic submit error alone would not establish this.
- Writes before question: Local layer creation and tracking have already occurred, and submit was attempted. Do not migrate ownership before the user chooses.
- PRs created: No fallback PRs. Decline any regular-PR offer; never run `gh pr create`. The supplied failure does not prove whether submit partially created PRs: inspect PR reads and report any actual PRs as created by `gh stack submit --auto`, without claiming native membership.
- Report: Native stacks are unavailable for luisurrutia/demo; native publication is blocked. Report preserved local layers and any observed PR URLs.
- Exact question: "El repositorio no tiene habilitados los stacks nativos. ¿Quieres publicar los dos cambios como PRs normales dependientes?"
- If accepted, migrate the tracked chain through troubleshooting before any manual Git write.

E
- Route: CLI.
- Deciding observation: Native-stack creation was requested, and installation is neither prohibited nor reported as failed. Absence of the extension does not select manual.
- Writes before question: No question is required. Install, initialize tracking, and build the two verified layers.
- Install command: `gh extension install github/gh-stack --pin v0.3.0`
- PR-creating command, with stdout not attached to a terminal: `gh stack submit --auto`. Add `--remote origin` if live submit help supports it. Confirm the installed version, read live command help, and complete each layer's review gate and any applicable cap check before publication.
- PRs created: Two missing layer PRs and their native stack, through submit only. Apply titles/bodies afterward, verify server membership, and perform the required follow-up passes.
- Question/blocker: None assumed. Installation failure or confirmed repository unavailability becomes a blocker; neither authorizes automatic manual publication.

Files read (sha256):
- probe.md 0cce718f51d71b0d27ad7aa79635ba4b4a1f05028511cd4aef59b3f998e55682
- SKILL.md 1ba9fa5e832881643f33647518779aab36cdfb2265db56929dd9031c6016337a
- references/cli-workflow.md 5f711c9123179a933aaa852b410110261507648acf9b168fb6248479ee7ffef9
- references/manual-chain.md 132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7
- references/cli-maintain.md 0eaecaabad806aaa60a65ddb68572b829a6ebf6504cddc75532c4e6930cf2f83
- references/manual-maintain.md 589e866b688c4808a2e5cd36bf4beba8fee4d6f50a7144b4ff2b25d890d18d69
- references/cli-create.md adac600b1e8a8fe96e17f6c46f0f5753305e433c13ba1922031844afa6bd91bc
- references/stack-design.md 4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296
- references/troubleshooting.md d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc
- references/api-workflow.md 8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b
