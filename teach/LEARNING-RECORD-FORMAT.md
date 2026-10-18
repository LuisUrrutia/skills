# Learning Record Format

Learning records live in `./learning-records/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the directory lazily: only when the first record is written.

They are the teaching equivalent of ADRs: they capture non-obvious lessons, key insights, and stated prior knowledge that will steer future sessions. Together with `ROADMAP.md`, they decide what to teach next.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for future sessions.}
```

That is the whole format. A learning record can be a single paragraph. The value is recording _that_ this is now known and _why_ it changes what to teach next, not in filling out sections.

## Evidence

A record that claims the learner can do something names its evidence level and how it was shown:

- **Reported**: the learner states prior knowledge or experience. Record the depth they claim.
- **Supported**: the learner succeeded with hints, examples or corrections.
- **Independent**: the learner did an unseen or changed task without help, such as passing a checkpoint.
- **Retained**: the learner did it again without help in a later session, in a changed context.

Write the level and the task as an `Evidence` line, for example `Evidence: independent, predicted the output of an unseen buffered-channel program (lesson 0004)`. Do not turn evidence into scores, percentages or mastery claims.

## Optional sections

Only include these when they add genuine value. Most records won't need them.

- **Status** frontmatter (`active | superseded by LR-NNNN`): useful when an earlier understanding turns out to be wrong and is replaced.
- **Objective**: the `ROADMAP.md` objective IDs the record supports, such as `O3`.
- **Implications**: what this unlocks or rules out for future sessions. Worth recording when non-obvious.

## Numbering

Scan `./learning-records/` for the highest existing number and increment by one.

## When to write a learning record

Write one when any of these is true:

1. **The learner demonstrated genuine understanding of something non-trivial**: not just exposure, but evidence they can use the concept correctly. This sets a new floor for what to teach next.
2. **The learner disclosed prior knowledge**: "I already know X." Record it so future sessions don't re-teach it. Also record the _depth_ claimed.
3. **A misconception was corrected**: the learner previously believed something wrong and now sees why. These are high-value: they predict future stumbling blocks for related topics.
4. **The mission shifted in response to learning**: the learner discovered they cared about something different than they thought. Cross-link to [[MISSION.md]] and update it.

### What does _not_ qualify

- Material that was merely covered. Coverage is not learning. Wait for evidence.
- Practice the learner declined. Understanding stays unmeasured; nothing was learned or disproved.
- Anything already captured tersely in [[GLOSSARY.md]] as a term definition. Don't duplicate.
- Session-by-session activity logs. Learning records are not a journal: they are decision-grade insights.

## Supersession

When a later record contradicts an earlier one (the learner's understanding deepened or corrected), mark the old record `Status: superseded by LR-NNNN` rather than deleting it. The history of how understanding evolved is itself useful signal.
