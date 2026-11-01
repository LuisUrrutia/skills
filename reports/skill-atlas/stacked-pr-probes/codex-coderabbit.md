# Dry-run probe after the CodeRabbit fixes: Codex host

- Host: T3 Code delegate, Codex gpt-6.1-sol, reasoningEffort high, read-only.
- Runtime: /tmp/stacked-pr-cr, manifest sha256 a28dbf638da46d4f2ef033e854be78bfdc1788a77ef42829b919026e84ccd7cb (same tree as commit 6f0f86d's stacked-pr/). Files read: SKILL.md 2e675d9a..., cli-workflow.md 903880ed..., cli-create.md e6bad738..., stack-design.md 4dc656cb..., troubleshooting.md d5df2b59..., api-workflow.md 8a4c9e3a....
- Probe: probe-coderabbit.md. Limit: a plan of actions; no tool executed and no GitHub write.

## Output (condensed)

1. Stack list 404 with a readable repository: CLI route, blocked by confirmed unavailability; no install; records v0.3.0; inspects any PRs the failed submit created without claiming a stack; offers ordinary dependent PRs without switching; migrates tracking first if the user chooses manual.
2. Repository read also 404: CLI stays; access blocker; reports both reads and submit stderr; does not claim stacks are disabled or switch to manual or API.
3. v0.2.1, upgrade fails offline: `gh stack --version`; `cp -R "$HOME/.local/share/gh/extensions/gh-stack" <scratch backup>`; `gh extension remove gh-stack`; `gh extension install github/gh-stack --pin v0.3.0` with one retry; restores the copy and confirms `gh stack --version`; `--pin v0.2.1` only without a backup; records the verified version, stops if none is confirmed; new layer only via `gh stack submit`, never `gh pr create`.
4. Read-only status on v0.2.1: no install or upgrade; records v0.2.1 and reports v0.3.0; JSON view and read endpoints only, no tracking writes.
