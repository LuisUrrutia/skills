# Collaboration, mail and meetings

Read the selected source sections. Discover tools at runtime and use the actual
read schemas. A provider can be connected without exposing activity history.
Capture minimal relevant excerpts and native IDs, not whole mailboxes or workspaces.

## Slack and document/design work

For Slack, search authored messages in the period and read relevant thread context
for outcomes, promises, requests and later corrections, including in-range replies
to older parent messages. Keep workspace/channel/
message IDs and permalinks. Distinguish authored text from quotations or bot
reposts. Search visibility, private-channel/DM permissions, retention and page
limits belong in coverage. Follow the connector's access requirements; do not
equate public search with the whole workspace.

For Notion and Confluence, use search to find candidate pages, then read the
relevant content and available version/comment history. Last editor and last
edited time identify only that exposed edit, not every contribution in a month.
Fetch linked action items when they affect attribution or current obligations.
For Figma, discover comments/version/activity capabilities separately from design
inspection. File visibility or the ability to read nodes is not an activity feed.
Without actor-linked changes, describe what is known and retain the gap.

## Gmail and Outlook

Support either or both when read access exists. Enumerate Sent, using the user
identity and aliases, and keep sent timestamps, message IDs and thread context.
Drafts, scheduled-but-unsent messages, received mail, quoted earlier messages and
automated sends do not demonstrate the user's sent work. Shared/delegated mailbox
ownership alone does not prove who sent a message; inspect sender/from semantics.
Incoming mail can evidence a request, but does not count as something the user did.

Gmail API date strings use PST boundaries. Prefer epoch-second queries padded
when necessary, then filter exact event instants against `[start, end)`. Its API
does not expand aliases like the Gmail UI. For Outlook, discover the Sent Items
folder/read surface, filter `sentDateTime`, exclude drafts and follow the complete
`@odata.nextLink` rather than reconstructing pagination. Read bounded surrounding
messages to confirm whether a promise was accepted, fulfilled or cancelled.

## Calendars and Granola

Expand recurring events into occurrences and retain timezone, calendar identity,
occurrence ID, cancellation and RSVP state. Label scheduled/accepted meetings as
such; they do not prove attendance or hours actually spent. Attendance needs
explicit participant evidence, source-backed notes, or user confirmation.

When Granola or another note taker is connected, list meeting metadata, retrieve
selected summaries/notes, and deepen only where necessary. Match calendar and
notes using stable meeting references where available; title/time similarity is
a candidate link. Capture decisions, the user's contribution and owned action
items, not the full transcript. A note accessible to the user may be a shared
meeting they did not attend. An unassigned group action is not their commitment.

Granola access and retention vary by the exposed tool, account and workspace.
Do not hard-code a subscription plan, a fixed history window or a local database
path. Missing Granola, Outlook or PagerDuty tools leave explicit gaps; do not
invent integrations or install them as a side effect of reporting.

## Primary documentation checked during authoring

- https://developers.google.com/workspace/gmail/api/guides/filtering
- https://learn.microsoft.com/en-us/graph/api/user-list-messages?view=graph-rest-1.0
- https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0
- https://developers.notion.com/reference/page
- https://developers.figma.com/docs/rest-api/version-history-endpoints/
- https://help.granola.ai/article/granola-mcp
- https://www.granola.ai/integrations/chatgpt

Granola's help and current integration pages described different sharing scopes
when reviewed; query actual runtime capabilities instead of choosing one as a
universal promise. These links guide verification, not fixed tool names.
