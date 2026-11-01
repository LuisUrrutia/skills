You are an agent following a skill. Read ONLY the skill at /tmp/stacked-pr-head/stacked-pr/ (SKILL.md first, then load references exactly as it directs). Run no command other than reading those files and `shasum -a 256` on the files you read. Edit nothing. This is a dry-run plan.

Common setup: WorkTrunk linked worktree of github.com/luisurrutia/demo, trunk main, single remote origin. Today is 2026-11-01. gh-stack v0.3.0 (published 2026-10-26) is installed and is the newest release.

A. Branches model and api already have ordinary open PRs (api based on model), no native stack, untracked by any tool. User: "Sincroniza mi cadena con main." Give your plan up to the first point where you need the user, and the exact question.
B. Same as A. You asked, and the user answers: "No, déjalos como PRs normales." Give the route and the ordered plan that follows.
C. Same as A, but the user answers: "Sí, conviértelo en stack nativo." Give the ordered plan.
D. After building two new layers for a fresh request "Haz un stacked PR con estos 2 cambios", `gh stack submit --auto` prints "Stacked PRs are not enabled for this repository" and GET repos/luisurrutia/demo/stacks returns 404 with the documented not-enabled message. Give route, PRs created, and what you report.
E. Regression: gh-stack absent, user: "Haz un stacked PR con estos 2 cambios locales." Give install command and the PR-creating command.

For each case: route, deciding observation, any write before the question (say explicitly whether adoption or `gh stack init` runs before asking), PRs created and by which command, the question or blocker. Finally list each file you read with its sha256.
