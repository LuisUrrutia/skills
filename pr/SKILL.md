---
name: pr
description: Create or update Pull Requests / PRs, draft PR copy, or push branches for review.
---

# Pull request

Create or update one GitHub pull request: safe `gh` operations, and a body a reviewer can act on.

This skill owns the push, the PR, its title, body, template conventions, and initial state. Land the commits with the `commit` skill first. When the branch is stacked (`gh stack view --json` succeeds, the resolved base is another feature branch, or the user asks for a stack), `stacked-pr` owns branch order, base resolution, submit, rebase, and merge sequence.

## Modes

- **Create**: no open PR for this branch. Open one in the user's preferred initial state, defaulting to draft.
- **Update**: an open PR exists. Audit its body against the diff, then show the URL and the proposed edits and ask before changing title, body, or metadata.
- **Draft-only**: the user wants copy, a state read, or metadata suggestions. Deliver them and stop, with no push, create, or edit.

Terminal states are `created`, `updated`, `draft-only`, `blocked`, and `refused`. Reaching one ends the turn. Further edits, labels, reviewers, issue comments, or cleanup wait for a new instruction.

## Claims

Everything the PR asserts is a **claim**, and every claim ships verified. What counts as a source: `git`, `gh`, the tracker, the code. What does not: the existing PR body, a prior assistant or bot summary, the branch name, and your own inference from the diff.

Verify before you write it:

- **What the PR delivers.** A scaffold behind a flag is not the shipped capability. Read what the code does end to end.
- **Who it affects.** Read the actual gate (permission check, flag reader, route guard) rather than inferring an audience from the feature's name. When the audience is broad or awkward to name, phrase it role-neutrally.
- **Numbers.** Cite a measurement you took. With no honest figure, carry the weight in the verb (`cut`, `unblock`, `start`, `stop`); a hand-waved figure is worse than none.
- **Work items.** Check each ticket's assignee and status before writing that the PR covers it. Claim the PR's own ticket and the ones assigned to the author; the rest are a possible draft that stays open for its owner.
- **Closing the ticket.** List the issue's explicit asks, check each against the diff, and name the ones the branch leaves unimplemented or half-done. That gap is invisible in the diff and it decides whether the ticket can close on this PR alone.
- **The existing body, in update mode.** A body written mid-branch rots as commits land: a caveat that was true at the first push ("hidden for everyone", "no endpoint exists", "not wired yet") may have been implemented three commits later while the body still swears otherwise. Name every stale claim when you present the proposed edits.

## Guardrails

### Initial state

A new PR opens as a draft by default. A user preference for ready PRs overrides that default. Accept the preference from the current request or user-specific instructions available in context; repository conventions, existing PRs, and prior assistant or bot summaries do not establish it. The preference chooses only a new PR's initial state; changing an existing PR's state still requires explicit approval.

For one PR, use the command matching the resolved state:

- Draft default: `gh pr create --draft --base <base> --head <branch> --title <title> --body-file <file>`
- Ready preference: `gh pr create --base <base> --head <branch> --title <title> --body-file <file>`

Inspect the command string before running it: `--draft` is present for the draft default and absent for a ready preference. Rebuild a mismatched command before execution. For a stack, pass the resolved state to `stacked-pr`, which owns the submit command.

Verify right after creation with `gh pr view <url-or-branch> --json isDraft,url`. The result must match the resolved state. Correct one mismatch with `gh pr ready --undo <url-or-branch>` for the draft default or `gh pr ready <url-or-branch>` for a ready preference, then verify again. Still mismatched: report the URL and stop, with no metadata edits or other PR actions.

Forbidden creation paths are `--web`, `-w`, `--editor`, `-e`, `--recover`, `--draft=false`, and any interactive flow. Omit `--draft` for a ready PR.

### Stop and ask

Proceed unasked on low-risk creation work: pushing a branch that has no upstream, creating a PR in the resolved initial state on the default base, and filling title and body from commits, diff, and template.

Everything else waits for the user:

- Not a git repository, `gh` missing, or `gh` not authenticated.
- The branch is `main` or `master`, unless the user wants a PR from it.
- No commit or diff against the chosen base.
- Staged, unstaged, or untracked changes in the worktree. PRs ship committed work.
- Secret-looking paths or content: `.env*`, keys, certificates, tokens, credentials, databases.
- A diff too broad for one review: unrelated concerns, mixed refactor and behavior change, generated noise, large binaries, lockfiles, or anything outside the requested boundary. Recommend a split instead.
- The branch is behind its upstream or has diverged.
- The operation needs a rebase, force-push, non-default base, reviewers, labels, milestone, or assignees.

Approval is per-operation and explicit: rebase, force-push, base change, reviewers, labels, changing an existing PR's state, and close or reopen each need their own.

## Workflow

### 1. Resolve repository state

- `git status --short --branch`, `git branch --show-current`, `git remote -v`.
- `git rev-parse --abbrev-ref --symbolic-full-name @{u}` for the upstream; failure means there is none.
- `gh pr view --json url,state,title,baseRefName,isDraft` for an existing PR. Not-found means create mode; auth, network, and permission failures are blockers.
- `gh repo view --json defaultBranchRef` when the default branch matters.
- Resolve the base in this order: the user's request, the existing PR's base, the upstream tracking branch, GitHub's default branch, then `main` or `master`.
- Resolve a new PR's state under [Initial state](#initial-state).
- Any PR, branch, base, or upstream that came from the user or earlier context gets verified with `gh pr view`, `git rev-parse --verify`, or `git ls-remote`. Unverifiable means unknown: resolve from repository state instead.

Done when repository, branch, remotes, upstream, existing PR, mode, base, and new-PR state are all known.

### 2. Inspect the PR boundary

- `git log --oneline --decorate <base>..HEAD`: read every commit, not just the last one.
- `git diff --stat <base>...HEAD`, then `git diff <base>...HEAD`: read the whole diff. Summaries skip binary and generated artifacts; risky files still get flagged.
- Confirm one coherent purpose and a reviewable size. When that fails, stop with a split recommendation.
- Run the [Claims](#claims) checks that read the branch: what it delivers, who it affects, the issue's asks, and in update mode the existing body.

Done when every commit and changed file is accounted for, the boundary is coherent and committed, and no claim in an existing body contradicts the diff.

### 3. Discover metadata conventions

Read all three sources before drafting a word.

**The written rules.** Read the repo's own pull-request section first: `CONTRIBUTING.md`, and the PR or workflow section of `AGENTS.md` / `CLAUDE.md`. Requirements no template carries live here — a ticket link in the description, a title format, a merge strategy, a review bar — and they outrank this skill's defaults wherever the two disagree. `grep -in "pull request" CONTRIBUTING.md AGENTS.md CLAUDE.md` finds the section when no heading names it.

**The template.** Search the resolved base and current tree in the repository root, `docs/`, `.github/`, and any `PULL_REQUEST_TEMPLATE/` directory under them for `pull_request_template.md` or `PULL_REQUEST_TEMPLATE.md`. A single template file on the base is the established shape to follow. A template added or changed by the current branch is part of the change, not evidence of repository convention. With several in a `PULL_REQUEST_TEMPLATE/` directory, pick the base template whose filename matches the change type, and ask once when that is ambiguous; a user saying `template=<filename>` has already picked.

**Recent merged PRs.** Run `gh pr list --state merged --limit 10 --json number,title,url,body` and read at least three bodies, template or no template. The template gives the skeleton; merged PRs show how this repo fills it: how deep each section runs, whether bullets are bold-led, which optional sections real authors keep, the house tone, and the title convention. Copy the dominant pattern, and when patterns conflict follow the newest PRs closest to this change type.

A lookup failure in an authenticated GitHub repo stops the run: report the exact command failure rather than inventing a style.

Done when the written rules, the selected template and whether it exists on the resolved base (or its proven absence), and the dominant convention are all established, and every requirement the written rules impose is on a list you check before finalizing.

### 4. Write the review packet

The body is a **review packet**: what changed, why it matters, and where the risk sits, in the fewest lines a reviewer can act on. The reviewer already has the diff.

Before drafting, answer one question: what will the reviewer understand differently after reading this? That answer is the organizing principle for every choice below.

#### Which sections exist

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

#### Verification

Run the repo's checks before finalizing (tests, coverage, lint, typecheck, formatter). When the template or dominant convention includes `Validation`, fill it with exact evidence. Otherwise, report the evidence in the `Validation:` line of the output block and add no reviewer-facing verification section unless the user asks for one.

#### What each section carries

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

#### Opening: the problem, then the solution

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

Hold the problem to about two sentences and cut any that restates the same pain in other words. Then give the solution its own sentence, next to that paragraph rather than folded into it. Both halves are mandatory: a problem with no solution beside it leaves the reviewer to reverse-engineer from the diff what the change does about it, which is the whole thing they came to judge. The tracker links the ticket for you, so the body carries no ticket or epic key the title already has, unless the written rules from step 3 ask for one; those win.

```
BEFORE  Ordering equipment today means one of two things: picking it inside a 195-field
        merchant application, or filing a Zendesk ticket. There's no self-service path, so
        partners chase it over phone and email. MMS-611 pulls equipment ordering out of the
        application flow and into Flute.

AFTER   Ordering equipment today happens inside a 195-field merchant application, or
        through a Zendesk ticket. There's no self-service path.
```

What the BEFORE loses is the ticket key and the restatement, not the solution. The AFTER is the problem half only, and the sentence naming what the change does follows it.

Every PR answers why it exists, a 20-line fix as much as a feature: a bug report, an incident, a wrong code path, a prerequisite for work that follows. Establish it from the user's request, the linked ticket or incident, the conversation, or written project context. Branch names, commit messages, existing PR bodies, and prior summaries are discovery hints, not sources; verify their suggestions against that context. When none of it establishes the motivation, ask the user what was broken, missing, or slow before this; whether it unblocks other work; or whether a specific incident, request, or decision led here. A confidently wrong problem statement sends the reviewer hunting a bug that never existed, so motivation is never inferred from the diff. Read the strategy or product doc when the issue names one: issue "Problem" fields are written for people who already have the context, and mislead without it.

#### Title

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
2. **Verified claims only.** Audience and numbers come from [Claims](#claims), not from the feature's name.
3. **Plain and short.** Prefer a plain word to internal jargon (`entry points`, `wire up`, `refactor`), short enough to read unwrapped in a PR list.

Rules 1 and 3 pull against each other; resolve toward accuracy. When the honest framing is a judgment call, offer the user two or three variants with the tradeoff each makes and let them choose: title framing is cheap to ask about and expensive to get wrong in a PR list.

#### Before you finalize

Reread the first sentence against the symptom test, and walk the step 3 written rules one by one against the finished body and title. Both fail silently: a diagnosis-first opening and a missing house requirement each read fine on their own.

Hold paragraphs to two to four lines. A longer block gets skipped whole, and a run of one-line fragments reads as fragments. Write in the active voice: `X overrides Y`, never `Y is overridden by X`.

Name a thing before referring to it, and repeat the noun rather than reach for a pronoun pointing several clauses back. A body written with the code open reads as a chain of undefined referents to everyone else.

Run the copy through the `humanize` skill when it is available, keeping the result direct and short rather than polished filler.

Punctuation: a colon where one clause introduces or explains the next, a period where it does not, in the title and in every bullet label. Step 6 greps for the slips.

Close a GitHub issue with `Fixes #<issue-number>` as the last line of the body. Co-author trailers and authorship footers stay out of the title and body.

### 5. Decide or ask once

- No PR yet and only low-risk work needed: proceed. Push the branch if it needs it, then create the PR in the resolved initial state.
- A PR already exists: show its URL, the stale claims found in step 2, and the proposed title and body, then ask before editing.
- A risky decision is needed: present mode, branch, base, initial state, push or rebase needs, reviewers, labels, and the exact title and body.
- Ambiguous input: ask one concise question with concrete options, recommended default first.

Put every risky decision in that single turn, and hold execution until each one is answered.

### 6. Execute approved actions

- Push with `git push -u origin <branch>` when the branch has no upstream and the push is low-risk.
- Write the body to a temporary file and pass `--body-file`. Inline `--body` mangles backticks, lists, code fences, and shell syntax.
- Grep the final title and body file for `—`, `–`, curly quotes (`“ ” ‘ ’`), and a sentence opening on `This PR` or `This change`, and fix every hit. Drafting slips past these, and one command catches them.
- Create with the sanctioned command from [Initial state](#initial-state), then verify `isDraft` matches the resolved state.
- Update with `gh pr edit <url-or-branch> --title <title> --body-file <file>` plus only the approved metadata flags.
- On a failed command, report the exact command, the concise failure, and the next decision. Retrying with broader permissions or destructive git actions is off the table.
- Once the create or update is verified and reported, stop.

## Output

Return exactly one terminal state. For a completed PR:

```markdown
Status: created|updated
PR: <url>
Branch: <branch>
Base: <base>
Mode: created|updated
Draft: yes|no
Metadata: reviewers/labels/milestone/assignees changed, or none
Validation: commands run and their results, or not run with reason
Risk check: no unrelated or secret-looking changes found, or the flagged items
```

For blocked work, use `Status`, `Blocker`, `Exact Command`, `Exact Error`, `Decision Needed`, and `Proposed PR Metadata` when it exists. Every run ends with either the PR URL or the exact blocker.
