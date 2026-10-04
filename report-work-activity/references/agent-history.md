# Agent conversations

Read when collecting coding or general agent sessions. Prefer host thread/history
tools within their advertised project/account scope. Otherwise discover supported
local stores or explicitly supplied exports from runtime configuration and help.
An optional installed `chat-history` skill can own retrieval; the reporting and
Luna extraction contract stays here. Do not install it implicitly.

Enumerate candidate sessions cheaply, then select messages by their timestamps,
including sessions created before the requested period. Session creation, last
modification and directory date are discovery hints, not final filters. Preserve
full session and message IDs or exact file/line/database locators. Mark absent
timestamps unknown; context outside the window must not enter its metrics.

Use read-only database access and bounded decoded reads of supported record
shapes. Verify the schema instead of guessing SQL. If a source is unsupported,
record it rather than exporting the whole store. Matthew Blode's `chat-history`
source documents canonical Codex records, Claude JSONL, indexed Cursor reads and
explicit exports; its implementation is not bundled or promised by this skill.
The old `daily-meeting-update` OpenCode helper is retired from this workflow:
it selects session creation time and reads unbounded later messages.

Give the Luna worker selected metadata and bounded message/tool-result excerpts.
It returns a short summary of request, work, observed result and remaining
actions, with deciding locators. Exclude system/developer directives, hidden
reasoning, credentials and irrelevant personal text. Distinguish human messages,
injected handoffs, parent dispatches, proposals, failed attempts and successful
tool results. Keep later corrections that change a completion claim.

Deduplicate mirrored messages, selected export branches, resumed sessions and
child/parent summaries by stable identities or explicit lineage. Child results
can establish work but are not additional copies of the parent's accomplishment.
Exclude this report's own collection/synthesis turns. If the current conversation
also contains earlier substantive work, include only that work rather than
dropping the whole session. Do not infer attendance, duration, deployment or
personal authorship from an agent saying "done".

Retain a minimal digest and supporting excerpts in the report bundle. Native
locators alone are insufficient for offline follow-up if the host may later be
unavailable. Refresh only named missing or contradictory context.
