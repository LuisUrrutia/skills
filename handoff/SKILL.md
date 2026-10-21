---
name: handoff
description: Use when writing a handoff document so another agent or session can continue a task.
---

# Handoff

Write a compact handoff document summarizing the current conversation and work
state so a fresh agent can continue: in another session, host or directory,
through a colleague, or on a parallel side task while this session continues.

Write and save only the document. Launching or seeding sessions, pausing, agent
cancellation, commits, publication, worktree changes and continuation retain their
owners and authorization. Saving proves neither receipt nor ownership transfer.

## Choose what travels

Focus on what the request or caller says the next session will do; otherwise on
continuing the current task. Keep only relevant context a fresh agent cannot
infer from accessible material. Include conversation-only context: the recipient
cannot open this conversation.

Reference existing artifacts by path or URL with what to read; do not copy
their contents, including checklists.
Use repository-relative paths for repository files; label absolute paths
as machine-local.

## Write the document

Open with the next action and why; the rest supports it. Record checkable facts
with their basis; label inferences and unverified beliefs:

- Objective, scope and completion criteria as the user last directed.
- Done, partial and not started work, with dependencies.
- Each decision labeled user-confirmed, agent-proposed or assumed, with reasons;
  keep unapproved distinct from rejected.
- Each check with command and observed outcome, including historical results,
  or not run. No rerun required.
- Blockers and what clears them; approaches likely to be retried and why abandoned.
- For repository work, branch, revision, staged and uncommitted changes,
  separating task changes from other work to preserve.

Separate output requirements from tool permissions. Use `agent-instructions` for
continuation guidance: next action, initial reads and user-set execution limits.
If absent from the skill catalog, write without it. Handoff documents never
trigger its two-model review, even for guidance aimed at another agent: a handoff
request is not instruction authoring.

Include a "Suggested skills" section naming, by registered name, skills the next
agent should use; the receiving environment resolves and invokes them.

Redact any sensitive information, such as API keys, passwords, and unrelated
personal data.

## Save and report

Use the destination named by the user's request, including one forwarded by a
caller; a caller-chosen location is not user-named. Otherwise save to the temporary
directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), not the
current workspace or repository. Create a new file; overwrite only when the
request names it for update.

Even if temporary storage cannot serve pickup on another machine or container, or
after cleanup, save there. Create no bundles, patches, archives or other copies
of the work, even temporarily. Leave any preservation destination to the user.

Check each referenced local file exists; label missing ones. After all edits,
including verification fixes, read the whole saved file into context as a fresh
agent: confirm the next action, why, and what to avoid where limits or abandoned
approaches exist.

Reply with:

- Exact saved path; next task in one line.
- Any access or retention limits and their cause, not only preservation advice.
- When pickup is limited, exactly what to copy or fetch: the document and each
  unreachable local file, including required Git state (branch, commits, staged
  task changes).
