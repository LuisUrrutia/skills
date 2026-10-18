# MISSION.md Format

`MISSION.md` lives at the workspace root. It captures who is learning and the _reason_ they are learning this topic. Every teaching decision (what to teach next, which resources to surface, which exercises to design) should trace back to this document.

## Template

```md
# Mission: {Topic}

Learner: {The person this workspace belongs to}
Status: {confirmed | provisional}

## Why
{1-3 sentences. The concrete real-world goal the learner is chasing. What changes in their life or work when they have this skill? Avoid abstract framings like "to understand X"; push for the underlying outcome.}

## Success looks like
- {A specific, observable thing the learner will be able to do}
- {Another specific thing}
- {…}

## Constraints
- {Time available, deadline, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of scope
- {Adjacent topics the learner explicitly does not want to chase right now, protecting the zone of proximal development}
```

## Rules

- **One mission and one learner per workspace.** If the learner wants to learn two unrelated things, that is two workspaces. Another person learning the same topic gets their own workspace.
- **Concrete over abstract.** "Run a half marathon by October" beats "get fitter." "Ship a Rust CLI to my team" beats "learn Rust."
- **Push back on vagueness.** If the learner cannot articulate why, ask before writing anything, as the Mission section of [SKILL.md](./SKILL.md) describes. A bad mission is worse than no mission.
- **Mark what you assumed.** When the learner declines questions, asks for a file or lesson now, or nobody can answer, write the mission with `Status: provisional` and mark each assumed line `(assumed)`. Confirm or correct those lines as evidence arrives, then set `Status: confirmed`.
- **Revise when reality shifts.** Missions change. When the learner's goal moves, update this file after they confirm the change: don't leave a stale mission steering future sessions.
- **Keep it short.** If `MISSION.md` runs past a screen, it has stopped being a compass and started being a plan. The plan belongs in `ROADMAP.md`, prior knowledge in learning records, and the learner's language and preferences in `NOTES.md`.
