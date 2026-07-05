# PR Skill Verification

## Baseline

Snapshot: `baseline-old-skill.md`

Observed gaps from reading the old skill against the eval prompts:

- The old skill has strong draft and git safety gates.
- The old skill mentions skimmability, validation, and risks, but the fallback body model omits explicit `Approach`, `Review guide`, and `AI assistance` slots.
- The old skill does not strongly frame PR content as a reviewer decision packet or proof pack.
- The old skill says to run the PR title/body through `humanize`, but does not encode the concrete readability rules from `WHAT_MAKES_IT_EASY_TO_READ.md`.

## Post-edit checks

Completed below.

## Targeted `SKILL.md` edit checks

- Added PR-as-decision-packet framing.
- Added fallback support for `Approach`, `Review guide`, and conditional `AI assistance`.
- Added validation as proof-pack guidance with exact commands/checks and explicit gaps.
- Added readability guidance from the research note.
- Rechecked draft enforcement terms remain present.

## Experimental `SKILL2.md` checks

- Created standalone alternative rewrite.
- Preserved draft-only creation and draft verification.
- Organized workflow around repository state, PR boundary, metadata conventions, review packet, decision gate, execution, and output.
- Included readability and AI assistance guidance.
