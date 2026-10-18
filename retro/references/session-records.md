# Session records

Read this when the retrospective targets a past session, or when the current
session's early turns are no longer in context. These layouts were observed in
Claude Code and Codex on 2026-10-18. Hosts change them: before relying on a
layout, list its directory and read the first lines of one record, and report a
layout that no longer matches. A host configured with another home directory,
through `CLAUDE_CONFIG_DIR` or `CODEX_HOME`, keeps its records there.

## Stay inside the project

Identify the project before opening any record: its root, its worktree paths
(`git worktree list`) and its remote URL. Open only records whose working
directory or repository matches. Other projects' records are never a fallback,
even when nothing matches.

Apps that drive these agents, such as T3 Code, leave the records in the agent's
own location below.

## Claude Code

- Records live under `~/.claude/projects/`, one directory per working directory.
  The directory name is the absolute path with `/` and `.` replaced by `-`:
  `/Users/me/.t3/app` becomes `-Users-me--t3-app`. Each worktree path has its own
  directory.
- Each session is `<session-id>.jsonl`. Subagent sessions are in
  `<session-id>/subagents/agent-*.jsonl`.
- Each line is one JSON event. Conversation events (`user`, `assistant`,
  `attachment`) carry `cwd`, `sessionId` and `gitBranch`; bookkeeping events,
  which often open the file, carry only `sessionId`.
- A user message is a `"type": "user"` event whose `message.content` is a string
  or a list of `text` blocks. A list of `tool_result` blocks is a tool result.

## Codex

- Records live in `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<id>.jsonl`,
  stored by date, not by project, so filter them before reading.
- The first line has `"type": "session_meta"`. Its `payload.cwd` and
  `payload.git.repository_url` identify the project. Read only that line from
  each candidate, with `jq` or another JSON reader, and open a rollout fully
  only after it matches:

  ```sh
  for f in ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl; do
    head -n 1 "$f" | jq -r --arg f "$f" '[$f, .payload.cwd, .payload.git.repository_url // "", .payload.git.branch // ""] | @tsv'
  done
  ```

- Messages are `"type": "response_item"` lines with `payload.role`. Codex injects
  instruction files and environment context as early `user` messages, which open
  with the instruction file's heading or a tag such as `<environment_context>`;
  the user's request is the first `user` message that is neither. `developer`
  messages are injected instructions.
- `~/.codex/session_index.jsonl` maps session IDs to thread names.

## Pick the session

Match the session the user described (date, branch or task) by its opening
request. For the current session, take this project's record that is still being
written, the most recently modified one, and confirm it by its latest turns before
reading its early ones. If no record matches, or the record is not accessible, say
so and ask the user for the record or a digest; the report states what a digest
cannot show.

Records are large and hold private details and secrets. Extract the user's
messages, failed tool calls and corrections instead of loading whole files, and
quote only what a finding needs.
