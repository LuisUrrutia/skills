# Dry-run probe after the CodeRabbit fixes: Claude Code host

- Host: Claude Code general-purpose subagent, claude-opus-5-5, default effort, read-only.
- Runtime: working tree after the CodeRabbit fixes, copied to /tmp/stacked-pr-cr; manifest sha256 a28dbf638da46d4f2ef033e854be78bfdc1788a77ef42829b919026e84ccd7cb. Files read: SKILL.md 2e675d9a..., cli-workflow.md 903880ed..., cli-create.md e6bad738..., troubleshooting.md d5df2b59..., api-workflow.md 8a4c9e3a..., stack-design.md 4dc656cb....
- Probe: probe-coderabbit.md. Limit: a plan of actions; no tool executed and no GitHub write.

## Output (condensed)

1. Stack list 404 with a readable repository: CLI route; this pair alone counts as GitHub's unavailability report. No install. Records v0.3.0. Declines regular PRs; reports the blocker citing submit and both reads and offers ordinary dependent PRs only (no API route); a tracked chain moves to manual through troubleshooting.md if accepted.
2. Repository read also 404: stays CLI; not counted as unavailability (wrong repository or no access). No retry. Blocker names the failure and points to `gh auth status` and repository access, without claiming stacks are unavailable.
3. v0.2.1, upgrade fails offline: records v0.2.1; `cp -R ~/.local/share/gh/extensions/gh-stack <scratch>`; `gh extension remove gh-stack`; `gh extension install github/gh-stack --pin v0.3.0` (one retry); never `--force`; restores the copy and confirms `gh stack --version` = v0.2.1, which it records; continues on v0.2.1 (>= v0.2.0 for worktrees); the new layer PR only via `gh stack submit --auto --remote origin`, or a network blocker without claiming unavailability.
4. Read-only status on v0.2.1: no install or upgrade; records v0.2.1; inspects through the JSON view, `gh pr view` and the REST stack read without writing tracking; notes that v0.3.0 is available.
