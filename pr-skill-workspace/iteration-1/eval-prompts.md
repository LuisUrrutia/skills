# PR Skill Eval Prompts

## Eval 1: Ordinary feature PR

User prompt: `/pr create a draft PR for this branch`

Expected improved behavior:
- Preserves draft-only creation and safety gates.
- PR body leads with what changed and why.
- Includes validation evidence or explicitly says validation was not run with reason.
- Includes real risks or known gaps without filler.
- Gives a review guide when the diff has meaningful review entry points.

## Eval 2: AI-assisted change

User prompt: `/pr create a draft PR; most of the refactor and tests were generated with AI, but I reviewed them`

Expected improved behavior:
- Preserves draft-only creation and safety gates.
- Includes an AI assistance disclosure when substantial AI help is stated.
- States what AI helped with, what the human reviewed, and what validation was performed.
- Avoids treating AI claims as proof without commands or evidence.

## Eval 3: Broad or risky change

User prompt: `/pr open this; it changes auth, a lockfile, CI, and some generated snapshots`

Expected improved behavior:
- Flags broad/risky boundary before creating a PR when appropriate.
- If drafting metadata, includes risk and impact for auth, lockfile, CI, and generated snapshots.
- Guides reviewers to start with high-risk files and treat generated/mechanical changes separately.
