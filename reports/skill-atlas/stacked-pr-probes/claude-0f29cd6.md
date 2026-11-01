# Dry-run probe: Claude Code host

- Host: Claude Code general-purpose subagent, model claude-opus-5-5, default effort, read-only.
- Runtime: `git archive 0f29cd6 stacked-pr` at /tmp/stacked-pr-head; manifest sha256 f0246d6299cf7dd2edd44d1c69ebd3a93e38138fb589792b9d876f4b08df4c1c.
- Probe: stacked-pr-probes/probe-0f29cd6.md.
- Limit: a plan of actions; no tool executed and no GitHub write.

## Output (verbatim)

A. "Sincroniza mi cadena con main"
- Route: CLI. Deciding observation: `gh extension list` shows gh-stack installed; the user did not ask for ordinary PRs.
- Untracked PRs do not decide the route. Under cli-workflow.md, sync is an "other operation" -> report the missing stack and ask before adoption, because sync links the two open PRs into a native stack.
- Writes before the question: none beyond read-only setup (git status --short --branch, git remote -v, git --version, gh auth status, gh extension list, gh release list -R github/gh-stack ..., branch/PR inspection). No adoption, no `gh stack init`, no fetch/rebase.
- PRs created: none.
- Question: "Tus PRs `model` y `api` son PRs dependientes normales y no forman un stack nativo. Si sincronizo con gh-stack, primero los adopto y la sincronización los vincula como stack nativo en GitHub. ¿Quieres convertirlos en stack nativo, o prefieres dejarlos como PRs normales y que los sincronice con Git?"

B. User answers "No, déjalos como PRs normales"
- Route: Manual. Deciding observation: the declined conversion is the user's choice of ordinary dependent PRs; gh-stack never tracked the chain, so no migration is needed.
- Plan (manual-maintain.md "Restack onto a moved trunk"): record current branch, dirty paths, model/api tips and PR bases; fetch origin; replay the whole chain from the top onto origin/main so model moves with its commits (e.g. rebase with --update-refs from api); a branch checked out in another WorkTrunk worktree is replayed there explicitly; push both refs in one `git push --atomic` with per-branch `--force-with-lease` to origin; verify both contain the new trunk, PR bases stay model->main and api->model, each layer's diff is unchanged, remote refs equal the verified local tips; check each PR body carries an accurate bottom-to-top stack map and update it if not.
- PRs created: none.

C. User answers "Sí, conviértelo en stack nativo"
- Route: CLI, adoption first.
- Plan: confirm installed v0.3.0 is the eligible tag (`gh stack --version`), read --help for every planned command; record current branch, dirty paths and tips; adopt per cli-create.md "Build or adopt" and troubleshooting.md "Adopt existing branches or PRs": verify model is an ancestor of api, then `gh stack init` with model and api bottom-to-top, keeping both tips; adoption complete when the stack view lists both in order with unchanged tips; sync per cli-maintain.md: fetch origin, compare local and remote order, run `gh stack sync --remote origin` in its non-interactive form (on divergence, troubleshooting's divergence branch); remove any stack map from both PR bodies with `gh pr edit`; verify local and GitHub order, heads, bases and trunk agree, and the stack endpoint places both PRs in one native stack.
- PRs created: none (both reused).

D. Submit reports stacked PRs not enabled, confirmed by the endpoint
- Route: CLI until the failure. Submit's message alone does not count; the documented not-enabled 404 from GET repos/luisurrutia/demo/stacks confirms GitHub's report, so native stacks are unavailable: blocker.
- Decline any offer to create regular PRs; no `gh pr create`.
- PRs created: none; `gh stack submit --auto` was the only PR-creating command and it failed.
- Report: the blocker with both observations, the two layers built and tracked locally with branches and tips, and an offer of ordinary dependent PRs; if accepted, the manual route takes over after the tracked chain moves through troubleshooting.md "Move a tracked chain to manual".

E. gh-stack absent, "Haz un stacked PR con estos 2 cambios locales"
- Route: CLI. Deciding observation: `gh extension list` lacks github/gh-stack; nothing prohibits installation.
- Install: `gh extension install github/gh-stack --pin v0.3.0`, confirm with `gh stack --version`.
- Then: plan layers (stack-design.md); build with `gh stack init` and the add-layer command, staging explicit paths; `pr` Review gate per layer bottom-up (Check cap if a cap applies); create PRs with `gh stack submit --auto` with stdout not attached to a terminal; titles/bodies via `pr` Draft-only plus `gh pr edit`, no stack map; verify both PRs in one native stack through the stack endpoint; continue into pr-followup Drive. Never `gh pr create`.

Files read (sha256):
- probe.md 0cce718f51d71b0d27ad7aa79635ba4b4a1f05028511cd4aef59b3f998e55682
- SKILL.md 1ba9fa5e832881643f33647518779aab36cdfb2265db56929dd9031c6016337a
- references/cli-workflow.md 5f711c9123179a933aaa852b410110261507648acf9b168fb6248479ee7ffef9
- references/cli-maintain.md 0eaecaabad806aaa60a65ddb68572b829a6ebf6504cddc75532c4e6930cf2f83
- references/cli-create.md adac600b1e8a8fe96e17f6c46f0f5753305e433c13ba1922031844afa6bd91bc
- references/troubleshooting.md d5df2b59d9fa2b84c4f1f148efb747df6629bfadc60c01a4c074dfc3ec9871fc
- references/manual-chain.md 132b331d5d0dc4fb4cd86cc38ae3eb11a77522152f5dd7cc2ee9e1d4d62abcc7
- references/manual-maintain.md 589e866b688c4808a2e5cd36bf4beba8fee4d6f50a7144b4ff2b25d890d18d69
- references/api-workflow.md 8a4c9e3a6be27df717d1e04713d23b3c3a8976efd39fce4baa24dee655d3ea6b
- references/stack-design.md 4dc656cb108938648912629f46146c3d3fa5f3a8683a89a243c6c1e6a3456296
- references/manual-create.md bb4ee7c5372683a1c1f92227b3a86986c9532d0e0525e063d3f7a900112731a0
