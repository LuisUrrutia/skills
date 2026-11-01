# Create or submit a native CLI stack

Use this branch only for the requested creation operation, or for the adoption that another
mutation on this route needs first. The CLI route's live-contract checks are preconditions.

## Plan

Load [stack-design.md](stack-design.md). State the layers bottom-to-top, with one concern and one
owner for every incremental change; files may evolve across layers. For an oversized branch,
existing PRs, layers checked out in other worktrees, or another branch manager, load
[troubleshooting.md](troubleshooting.md) before rewriting or adopting anything.

Planning is complete when every incremental change has one owner, every dependency points toward the
trunk, and the verification command for each layer is known.

## Build or adopt

Read live help for the current create/adopt and add-layer commands. Create the bottom layer from the
intended trunk, verify it, then create each upper layer from the one below. Stage explicit paths or
hunks so unrelated changes stay outside the stack. Multiple commits may share a layer when they
serve its single concern.

For adoption, preserve existing tips and verify ancestry before writing local stack metadata.

Build or adoption is complete when the CLI's JSON view shows the planned order, each adjacent parent
is an ancestor of its child, every incremental change and commit belongs to one concern,
layer checks pass, and no branch needs a rebase. Stop here when the request is local-only. When
adoption only prepares another operation, it is complete under the criterion in
[cli-workflow.md](cli-workflow.md), and that operation handles any rebase the branches need.

## Submit

`gh stack submit` creates the missing PRs and the native stack in one operation. Opening layer PRs
with `gh pr create` or the `pr` skill's Create mode yields ordinary PRs outside any stack, so on
this route only submit creates them. Read live help for the current non-interactive submit form
(currently `--auto`, run with stdout not attached to a terminal) and how it represents the requested
draft state. Its `--open` flag also marks existing PRs ready for review; when existing drafts must
stay drafts, submit without it and mark only the intended new PRs ready with `gh pr ready`.

Non-interactive submit acts on every active layer of the current stack. When a tracked active layer
is outside the request, ask before submitting instead of publishing a subset another way.

Submit reports stacked PRs as unavailable after any failed stack lookup, including authentication,
rate-limit and network errors. Before treating it as GitHub's unavailability report, read the
documented stack endpoint from [api-workflow.md](api-workflow.md#establish-the-live-contract): only
its documented not-enabled response counts, and SKILL.md then decides the route. Any other failure
keeps the CLI route; retry a transient one once, otherwise report a blocker. Decline any offer to
create regular PRs.

Then invoke `pr` in Draft-only mode for each PR that submit created and apply its title and body,
without a stack map, with `gh pr edit`. Change a reused PR only to remove a stack map, unless the
request changes it. Preserve the stage of existing PRs unless the request changes it.

Read the documented stack endpoint again: submit can exit successfully even when linking the stack
failed. When the read shows a missing or split stack, classify the stderr and rerun submit once; if
membership is still wrong, report a blocker with the PR URLs, and never report them as a stack. A
native stack needs at least two PRs, so a single submitted layer is reported with its membership
pending until a second layer exists.

Submission is complete when a fresh GitHub read proves that every requested PR has the intended
head, base, title, body without a stack map, and draft state, and the stack endpoint places every
requested PR in one native stack in bottom-to-top order, or a single layer is reported as pending. The JSON stack view and PR bases alone do
not prove that membership. Report created and reused PR identifiers and the stack number, then
continue as Scope and safety in the root `SKILL.md` directs.
