# Review packet

Use this reference when the requested deliverable includes a PR title or body. The reviewer already has the diff, so the packet carries what changed, why it matters, and where the risk sits in the fewest lines a reviewer can act on.

Before drafting, answer one question: what will the reviewer understand differently after reading this? That answer organizes every choice below.

## Which sections exist

**With a template, its headings are the complete set.** Optional and commented-out sections stay out unless the user asks for them, and a heading the template does not define never appears. Content with no home does not earn one: fold it into the nearest section, or cut it.

- Scope limits, follow-ups, and what deliberately did not change go in the changes section.
- Load-bearing gotchas, deliberate deviations from the design, and links to the strategy doc, designs, or build doc go in the reviewer-context section.

Tick a template checklist item when the diff proves it; leave the rest unticked.

**With no template and no sectioned convention** — the repo has no template file and the merged PRs are unstructured prose — use this fallback structure:

```markdown
## Why is this being done?
<!-- The problem, incident, user need, or prerequisite. What was broken, missing, or slow before this. -->

## What changed
<!-- The change at altitude: what someone can now do that they could not. No types, no symbol names, no file tour. Drop this heading when the why above already answers it. -->

## Out of scope
<!-- What a reader would expect to find here and will not, and why. Drop this heading when there is nothing. -->

## Reviewer knowledge check
<!-- Links and context tied to this PR: ticket, spec, design, decision record, sibling PR. Drop this heading when the reviewer needs no context beyond the diff. -->
```

The comments are the filling guide: write under each, then strip them from the posted body. `Why is this being done?` always appears and carries both halves: the problem, then what the change does about it. Scale the content to the change, so a 20-line fix earns one line rather than a paragraph.

The other three headings are conditional:

- `What changed` earns its heading only when the change resists the one or two sentences the why gives it: several independent strands, or a shape that needs a list to follow. A single coherent change already explained up there needs no second section restating it.
- `Out of scope` earns its heading when something a reader would expect is deliberately absent: a field left for a later ticket, a sibling bug left alone, a follow-up the change sets up but does not do. Bound it to what they would expect, or it grows into a list of everything the PR is not.
- `Reviewer knowledge check` earns its heading when a reviewer needs a link or non-obvious warning before judging the diff.

With nothing to put under a conditional heading, drop the heading rather than write "nothing".

`What changed` stays at altitude. The reviewer reads the code for the types, the new functions, and the state a component holds, so naming those spends the section's space on what they already have:

```
TOO LOW   Created component X with state A for the flow launched when the user clicks Y.
ALTITUDE  Adds the multi-step flow so a user can create an order.
```

When present, `Reviewer knowledge check` carries what equips the reviewer and nothing else: links strictly tied to this PR, and a warning where the code reads wrong at first pass. What fails there:

- An open question the author never answered. "Worth a decision before this ships" is the author's call, and a reviewer reading code cannot close it. Decide it, or take it to the ticket.
- A link nobody will open, or one that documents the area rather than this change.
- Anything the code's own comments already explain, since the reviewer reads those.
- A handoff note for whoever consumes the change later, and any reassurance that an untouched area still works.

The section is often one or two items. Padding it to look thorough buries the one that mattered.

## Verification

Run the repo's checks before finalizing (tests, coverage, lint, typecheck, formatter). When the template or dominant convention includes `Validation`, fill it with exact evidence. Otherwise, report the evidence in the `Validation:` line of the [output block](../SKILL.md#output) and add no reviewer-facing verification section unless the user asks for one.

## What each section carries

When a template names its own sections, these are the common ones it draws from:

- `Summary`: one or two sentences with the net change and why it matters, conclusion first.
- `Why this change`: one short paragraph naming the problem, incident, user need, or engineering reason, when the summary and linked issue leave it unclear.
- `Approach`: the design choices, rejected alternatives, or tradeoffs a reviewer cannot infer from the code. Skip it when there was no real decision.
- `Changes`: three to five bullets grouped by behavior, surface, or reviewer concern.
- `Validation`: the exact commands, manual QA, screenshots, security scans, or performance checks that ran, or `Validation: not run` with the reason.
- `Risks and impact`: real user, data, security, performance, compatibility, migration, dependency, rollout, or rollback concerns. `Low risk` is filler unless the house convention wants it.
- `Review guide`: where to start, the risky areas, the mechanical changes to skim, and the feedback wanted. When the template has a reviewer-context section, fill it with what a reviewer needs before judging the change: the strategy or product doc, designs, prototypes, flow diagrams, each labeled with the question it answers. Harvest them from the linked issue and its parent epic instead of asking the author.
- `AI assistance`: when AI did substantial work or the user mentions it, state what it touched, what the human reviewed or rewrote, and what verification backs it.

Cut anything that would not change what the reviewer does: duplicate facts, implementation diaries, and inventories the diff already lists with their types, whether of files, columns, fields, or flags. Name a mechanism only where the reason behind it is invisible in the code. A short body a reviewer finishes beats a complete one they skim.

Cutting stops at one floor: the reviewer can predict the diff's shape from the body before opening it. Surprise at which surfaces the change touches means the cut went past an inventory and took a surface that needed naming. Name every surface once, in a clause, and let the diff carry the contents.

## Opening: the problem, then the solution

Open with the problem in the words of the person who asked for it, from their prompt, the linked issue, or the incident report. Then say what the change does about it. A reviewer should know what was wrong before reading one implementation detail.

```
BAD   Removed implicit workspace carry-over from every "new thread" entry point
      (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads
      inherit only the project from context; branch, worktree, and env mode always
      come from the configured defaults. Deleted buildContextualThreadOptions,
      startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

GOOD  My "new worktree" default was ignored when starting new threads on existing
      worktrees. Super unintuitive. Now your preferences always apply.
```

The bad version is accurate and useless: an inventory of call sites and deleted symbols that never says what broke or why anyone cared. The good version names the pain first, in the reporter's voice, and resolves it in one clause. Symbol names and touched surfaces go further down, or nowhere.

Open on the **symptom**, not the **diagnosis**. The symptom is what the person hit: something they could not do, or something that behaved wrong. The diagnosis is what you found when you went looking — the column, the constraint, the missing type, the call site — and it belongs in the details. An opening can be a genuine problem statement and still be the wrong one, told from inside the system:

```
BAD   The session store keyed entries by user id alone, so a second login overwrote the
      first and the cleanup job could not tell the two apart.

GOOD  Signing in on your phone logs you out on your laptop.
```

Test the first sentence: could the person who asked have said it? They say what they cannot do. The names of the parts you changed are your words, not theirs, so a first sentence built out of them is diagnosis and the symptom is still missing.

Hold the problem to about two sentences and cut any that restates the same pain in other words. Then give the solution its own sentence, next to that paragraph rather than folded into it. Both halves are mandatory: a problem with no solution beside it leaves the reviewer to reverse-engineer from the diff what the change does about it, which is the whole thing they came to judge. The tracker links the ticket for you, so the body carries no ticket or epic key the title already has, unless the written rules collected in step 3 ask for one; those win.

```
BEFORE  Ordering equipment today means one of two things: picking it inside a 195-field
        merchant application, or filing a Zendesk ticket. There's no self-service path, so
        partners chase it over phone and email. MMS-611 pulls equipment ordering out of the
        application flow and into Flute.

AFTER   Ordering equipment today happens inside a 195-field merchant application, or
        through a Zendesk ticket. There's no self-service path.
```

What the BEFORE loses is the ticket key and the restatement, not the solution. The AFTER is the problem half only, and the sentence naming what the change does follows it.

Every PR answers why it exists, a 20-line fix as much as a feature: a bug report, an incident, a wrong code path, a prerequisite for work that follows. Establish it from evidence allowed for `Motivation and problem` in the [Claims matrix](../SKILL.md#claims). When none of it establishes the motivation, ask the user what was broken, missing, or slow before this; whether it unblocks other work; or whether a specific incident, request, or decision led here. A confidently wrong problem statement sends the reviewer hunting a bug that never existed, so motivation is never inferred from the diff. Read the strategy or product doc when the issue names one: issue "Problem" fields are written for people who already have the context, and mislead without it.

## Title

Match the merged-PR style when there is one (ticket prefix, casing, length). Otherwise use `type(scope): summary`, dropping the scope when none is useful.

Within that shape the title names **the outcome, not the mechanism**. A reviewer scanning a PR list should learn why the change matters without opening it.

```
BAD   perf(server): negotiate permessage-deflate on the websocket
GOOD  perf(server): cut websocket frame size by 70%+ with gzipping
```

A worked example, where the first two attempts each failed a different way:

```
BAD   [MMS-1230] Equipment request entry points behind a feature flag
BAD   [MMS-1230] Request equipment for a merchant without leaving the portal
GOOD  [MMS-1230] Start equipment ordering: Request button behind a feature flag
```

The first names the mechanism, and "entry points" is internal jargon nobody outside the ticket uses. The second states a real outcome, which is why it tempts: it reads well, the way a product person would write it. It is still wrong, because the modal behind that button was a placeholder, so merging it let nobody request equipment. The third trades polish for the scope the PR actually shipped.

Rules, in priority order when they collide:

1. **Never oversell.** A first slice, a scaffold, or an entry point behind a flag is the start of the work: title it that way (`Start X: …`, `First slice of X: …`). The test is whether someone who merged it expecting that outcome would feel cheated. A scope caveat earns its place in the title only when dropping it would promise a capability the PR does not deliver; when the title is honest without it and the body's opening already draws the boundary, keep the title clean.
2. **Verified claims only.** Audience and numbers come from the [Claims matrix](../SKILL.md#claims), not from the feature's name.
3. **Plain and short.** Prefer a plain word to internal jargon (`entry points`, `wire up`, `refactor`), short enough to read unwrapped in a PR list.

Rules 1 and 3 pull against each other; resolve toward accuracy. When the honest framing is a judgment call, offer the user two or three variants with the tradeoff each makes and let them choose: title framing is cheap to ask about and expensive to get wrong in a PR list.

## Before you finalize

Reread the first sentence against the symptom test, and walk the written rules collected in step 3 one by one against the finished body and title. Both fail silently: a diagnosis-first opening and a missing house requirement each read fine on their own.

Hold paragraphs to two to four lines. A longer block gets skipped whole, and a run of one-line fragments reads as fragments. Write in the active voice: `X overrides Y`, never `Y is overridden by X`.

Name a thing before referring to it, and repeat the noun rather than reach for a pronoun pointing several clauses back. A body written with the code open reads as a chain of undefined referents to everyone else.

Punctuation: a colon where one clause introduces or explains the next, a period where it does not, in the title and in every bullet label. The execution step greps for the slips.

Close a GitHub issue with `Fixes #<issue-number>` as the last line of the body. Co-author trailers and authorship footers stay out of the title and body.
