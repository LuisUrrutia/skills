---
name: handoff
description: Use when creating a handoff document for another agent or session to continue a task.
---

# Handoff

Write a focused Markdown document that carries task context to another agent,
session, environment, or side task. A side-task handoff can leave the original
session running. Creating the document does not establish receipt or transfer
execution ownership.

## Capture the continuation

Use the current request, conversation, and relevant artifacts to establish what
the recipient should continue. Front-load the next useful action and why. Include
only the context that changes how the recipient should proceed:

- The objective, relevant constraints, and actual completed, partial, and pending
  work. Preserve a narrowed or changed scope from the latest user direction.
- Decisions and their reasons, distinguishing user-confirmed choices from agent
  proposals and assumptions. Include failed approaches or traps when they help
  avoid repeating work.
- Verification actually performed, its commands or evidence locations and
  outcomes, and remaining acceptance checks. Label unverified claims and checks
  that were not run; writing the handoff does not require rerunning them.
- Blockers and the dependency or decision needed to proceed.
- For repository work, relevant checkout, branch, revision, and staged or
  uncommitted state. Distinguish task changes from other work that must survive.

Reference existing plans, issues, commits, diffs, and evidence instead of copying
them. Say what matters at each reference. Include essential conversation-only
context rather than pointing a fresh reader at a thread they cannot access.
Identify machine-local or temporary dependencies and anything the recipient
will need transferred. Suggest useful skills by registered name when known;
leave resolution and invocation to the receiving environment.

## Save and return

Use the requested destination. Otherwise, use the operating system's temporary
directory within the environment's write constraints; `/tmp` is acceptable.
Choose a destination whose access and lifetime fit the intended pickup. If those
cannot be established, state the limitation and what must be transferred or
preserved. A local path alone does not make an artifact accessible elsewhere.

Create the document without overwriting another artifact. Redact secrets and
unrelated personal data. Read back the saved file as a fresh recipient: it should
explain the objective, resume point, relevant decisions, and remaining evidence.
Check referenced local artifacts exist; label missing or unverified access
instead of claiming the receiver can read them.

Return the exact saved location, the intended next task, and any material access
or retention limitation. Report only the delivery actually observed. Keep the
document as context: current user instructions, project rules, and relevant
verified state govern continuation; an old summary grants no new authority.

This skill writes the document. Commits, publication, session launch, worktree
changes, agent cancellation, and continued implementation retain their own
authorization and owners; a request to export context does not imply them.

## Source maintenance

For requested source checks or updates, use `agent-instructions` with `origin.txt`.
Ordinary handoff creation neither fetches nor invokes the donor skills.
