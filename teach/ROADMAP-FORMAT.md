# ROADMAP.md Format

`ROADMAP.md` lives at the workspace root. It is the route from what the learner can already do to the success items in [[MISSION.md]]: ordered objectives, the checkpoint that shows each one, and the evidence behind each status. It is an index. Lesson content belongs in lessons, and the reasons behind a status belong in learning records.

## Template

```md
# Roadmap: {Topic}

Reaches: {The "Success looks like" items from MISSION.md that this roadmap covers}
Pace: {The learner's stated time or deadline, or "not stated: stages without dates"}

## Stage 1: {Name}

Milestone: {A real application of this stage, tied to a success item, with its feedback criteria}

| ID | The learner can | Needs | Checkpoint | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| O1 | {Observable capability: explain, predict, do, evaluate} | none | {An unseen or changed task done without help, and what a pass looks like} | open | |
| O2 | {...} | O1 | {...} | supported | LR-0004 |

## Stage 2: {Name}

...

## Deferred

- O9 {Objective}: {Why it was deferred, and what would bring it back}
```

## Status values

- `open`: no evidence yet.
- `reported`: the learner states prior knowledge, recorded with its depth. It satisfies `Needs` until an attempt contradicts it.
- `presented`: a lesson covered the objective; the learner has not attempted it.
- `supported`: the learner succeeded with hints, examples or corrections.
- `met`: the learner passed the checkpoint without help. Cite the learning record.
- `retained`: the learner met it again without help in a later session, in a changed context.

## Rules

- **Observable objectives.** Each objective names something the learner can explain, predict, do or evaluate. "Understand X" is not an objective.
- **Real prerequisites only.** `Needs` lists the objectives without which this one cannot be learned. Order objectives by `Needs`, then by the nearest unmet success item.
- **Status follows evidence.** Change a status only when an attempt, a statement of prior knowledge or a lesson supplies its evidence, and fill `Evidence` with the record or lesson. Coverage alone moves an objective no further than `presented`.
- **Stable IDs.** Give an inserted objective a new ID. Move a dropped objective, or one skipped without a statement of prior knowledge, to `Deferred` with its reason instead of deleting it.
- **Pace from the learner.** The `Pace` line takes the learner's stated time or deadline. Without one, stages carry no dates; add dates only when the learner gave a deadline or schedule, and never invent a weekly commitment.
- **Scope that does not fit.** When the objectives do not fit the stated time, move the lowest-priority ones to `Deferred`, state the tradeoff, and confirm it with the learner. Never promise mastery by a date.
- **Revise in place.** The file shows the current route; the learning records keep the history.
