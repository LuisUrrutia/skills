You are an agent following a skill. Read ONLY the skill at /tmp/stacked-pr-cr/stacked-pr/ (SKILL.md first, then references as it directs). Run no command except reading those files and `shasum -a 256` on them. Edit nothing. Dry run.

Setup: WorkTrunk linked worktree of github.com/luisurrutia/demo, trunk main, remote origin. Today 2026-11-01. Releases: v0.3.0 (2026-10-26), v0.2.1 (2026-10-09).
1. User: "Haz un stacked PR con estos 2 cambios." gh-stack v0.3.0 installed. After building, `gh stack submit --auto` prints "Stacked PRs are not enabled for this repository". GET repos/luisurrutia/demo/stacks returns 404 "Not Found"; GET repos/luisurrutia/demo succeeds.
2. Same, but GET repos/luisurrutia/demo also returns 404.
3. gh-stack v0.2.1 installed; user asks to add a layer to an existing native stack. `gh extension install github/gh-stack --pin v0.3.0` fails after removal with "could not connect to api.github.com".
4. User asks "¿Cómo está mi stack?"; gh-stack v0.2.1 installed.
For each: route, deciding observation, exact commands for install/upgrade/rollback, what version you record, PRs created, and what you report. Then list files read with sha256.
