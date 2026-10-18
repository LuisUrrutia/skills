---
name: handoff
description: Use when writing a handoff document so another agent or session can continue a task.
---

# Handoff

Write a compact handoff document summarizing the current conversation so a
fresh agent can continue the work. The document records the state of the work
for another agent to pick up: in another session, host, or directory, through a
colleague, or as a side task forked while this session keeps running.

This skill writes and saves the document only. Launching or seeding a session,
pausing, cancelling agents, committing, publishing, changing worktrees, and
continuing the work keep their own owners and authorization. A saved document
proves neither receipt nor a transfer of ownership.

## Choose what travels

Treat the purpose that the request or calling workflow states for the next
session as the document's focus, and tailor the document to it. Without a stated
purpose, the focus is continuing the current task. Keep only what bears on that
focus and that a fresh agent cannot infer from the material it can read; leave
out the rest.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs,
issues, commits, diffs). Reference them by path or URL instead, and say what
matters at each one. Use repository-relative paths for repository files, and
label an absolute path to machine-local state as machine-local. Write
conversation-only context into the document, because the recipient cannot open
this conversation.

## Write the document

Open with the next action and why it is next. The rest of the document supports
that step.

Record the state of the work as facts the recipient can check, each with its
basis:

- The objective and its current scope as the user last directed, so the
  recipient knows what done means.
- What is done, partial, and not started, and what depends on what.
- Each decision as user-confirmed, agent proposal, or assumption, with its reason.
- Each check as observed, with its command and outcome, or as not run. Mark a
  belief the session never verified as unverified; writing the handoff does not
  require rerunning checks.
- Blockers and what would clear them, and abandoned approaches the recipient is
  likely to retry, with why they were abandoned.
- For repository work, the branch, revision, and staged and uncommitted changes,
  keeping the task's changes apart from other work that must survive.

Use `agent-instructions` to write the continuation guidance: the next action,
what to read first, and the limits the user set, such as no commits,
publication, or deployment. When the skill catalog lacks it, write the guidance
without it. Writing a handoff never starts the two-model review that
`agent-instructions` requires, even when the request asks for guidance aimed at
another agent: a handoff request is not a request for instruction authoring.

Include a "Suggested skills" section that names, by registered name, the skills
the next agent should use; the receiving environment resolves and invokes them.

Redact any sensitive information, such as API keys, passwords, and unrelated
personal data.

## Save and report

Save to the destination the user's request names, including when a calling
workflow forwards it; a location a workflow picks on its own is not a named
destination. Otherwise save to the temporary directory of the user's OS
(`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), not the current workspace or
repository. Create a new file; replace an existing one only when the request
names it for update.

When the temporary directory cannot serve the pickup, because the recipient runs
on another machine or container or picks up after the directory may be cleared,
still save there, say so, and list exactly what the recipient must copy or
fetch: the document and each referenced local file it cannot reach. Never create
bundles, patches, archives, or other copies of the work, even temporarily.

Reread the saved file as a fresh agent: it must say what to do next and why, and,
where limits or abandoned approaches exist, what not to do. Check that each
referenced local file exists, and label any that does not.

Reply with the exact saved path, the next task in one line, and any access or
retention limit.
