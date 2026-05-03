---
name: daily-meeting-update
description: Summarize recent development activity
---

# Daily Meeting Update

Generate a concise standup update from recent development activity. Use `$ARGUMENTS` as the reporting window, automatically pull available GitHub, local git, Jira, Atlassian, and OpenCode context, interview the user for missing intent and nuance, then produce a meeting-ready Markdown update.

Tool data is context, not the source of truth. Do not ask before extracting available GitHub/Git, Jira/Atlassian, or OpenCode activity. If `~/Projects` does not exist, ask where the user clones repositories. Write the final standup to `daily-DATE.md`, where `DATE` is the report date in `YYYY-MM-DD` format.

## Context

Repository: !`git remote get-url origin 2>/dev/null | sed -E 's#(git@github.com:|https://github.com/)([^.]+)(\.git)?#https://github.com/\2#' || echo "No repository"`
User: !`gh api user --jq .login 2>/dev/null || git config user.name 2>/dev/null || echo "Unknown user"`

---

## Phase 1: Resolve Window And Detect Integrations

### Step 1: Resolve The Time Window

Treat `$ARGUMENTS` as the time window, for example `yesterday`, `2026-05-01`, `last 3 days`, or `since 9am`. If `$ARGUMENTS` is empty, use a stored timestamp or config if one exists, then fall back to `yesterday`.

If the window is ambiguous but still usable, state the assumption in `Blockers / Notes`. Ask a follow-up only when the ambiguity would materially change the report.

### Step 2: Silent Detection

Check available integrations silently. Suppress errors unless the user explicitly asks what happened.

| Integration | Detection |
|-------------|-----------|
| Git | `git rev-parse --is-inside-work-tree` succeeds |
| GitHub CLI | `gh auth status` succeeds |
| Atlassian CLI | `acli jira auth status` succeeds or `acli` exists |
| Atlassian MCP | Atlassian MCP tools are available; prefer over Atlassian CLI |
| OpenCode History | `test -f ~/.local/share/opencode/opencode.db` |

Use the current directory only as context. For local commits, default to scanning repositories under `~/Projects`. If `~/Projects` does not exist, ask the user where they clone their repositories.

If `gh` is not installed or authenticated, continue with local git and any other approved sources. Add a safety note that GitHub activity is unavailable.

### Step 3: Identify User And Local Scan Root

Identify the GitHub login with `gh api user --jq .login` when possible. Fall back to local git author data if GitHub is unavailable.

Use `~/Projects` as the default local repository scan root. If it does not exist, ask one precise question: `Where do you clone your repositories?` Use the current repository only as extra context or when the user explicitly requests current-directory-only scanning.

---

## Phase 2: Pull Activity

### GitHub PRs And Reviews

When GitHub CLI is available, collect recent work with global PR search by default. Do not scope to the current repository unless the user explicitly asks to narrow the search.

Collect:

- User-authored PRs updated or created in the selected window
- PRs merged by or owned by the user
- Reviews completed by the user
- Comments, mentions, or review requests involving the user on others' PRs

Use global searches such as:

```bash
gh search prs --author @me --created ">=YYYY-MM-DD"
gh search prs --author @me --updated ">=YYYY-MM-DD"
gh search prs --reviewed-by @me --updated ">=YYYY-MM-DD"
gh search prs --commenter @me --updated ">=YYYY-MM-DD"
gh search prs --mentions @me --updated ">=YYYY-MM-DD"
```

Use `gh pr list` only when intentionally working inside a specific repository or when the user narrows the search:

```bash
gh pr list --author @me --search "created:>=YYYY-MM-DD OR updated:>=YYYY-MM-DD" --json number,title,state,url,updatedAt,createdAt
```

Add `--repo OWNER/REPO` only when the user explicitly asks to limit GitHub activity to a repository.

Inspect details only when needed for a readable summary. Prefer PR URLs returned by global search because PR numbers alone are repository-relative:

```bash
gh pr view PR_URL --comments --json number,title,state,url,author,reviews,comments,latestReviews
gh api repos/OWNER/REPO/pulls/PR_NUMBER/reviews
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments
gh api repos/OWNER/REPO/issues/PR_NUMBER/comments
```

### Local Git

Collect local branch commits across repositories, not just the current working directory. Use `~/Projects` as the default clone root. If `~/Projects` does not exist, ask the user where they clone all repos.

From the selected root, discover git repositories with `fd` when available:

```bash
fd '^\.git$' --hidden --no-ignore
```

If `fd` is unavailable, use `find`:

```bash
find . -name .git
```

For each repository found, enter the repository folder or run the equivalent with `git -C`. Collect branch and commit context with read-only commands:

```bash
git branch --show-current
git log --all --since="WINDOW" --author="USER" --format="%h%x09%ad%x09%d%x09%s" --date=short
git for-each-ref --format="%(refname:short)" refs/heads
```

Group results by repository and branch when practical. If author matching is unreliable, report the assumption and summarize only commits that appear attributable to the user.

### Jira / Atlassian

When Atlassian MCP or Atlassian CLI is available, collect tickets assigned to the user or updated in the selected window. Prefer Atlassian MCP over Atlassian CLI because the Rovo MCP server can search and fetch Jira data in real time through the user's existing Atlassian Cloud permissions. Capture ticket key, title, status, assignee, URL, and meaningful recent activity. Do not dump full ticket histories.

#### Atlassian MCP Preferred Path

If Atlassian MCP tools are available, use them before `acli`:

- Search Jira issues assigned to the current user and updated in the selected window.
- Fetch details for relevant issues only when needed for a readable summary: key, title, status, assignee, updated time, URL, latest comments or activity, and linked PRs/pages when available.
- Use Confluence, Compass, Bitbucket, JSM, and Teamwork Graph tools only when they add relevant standup context.
- Respect MCP tool results as permission-scoped data; do not ask the user to authenticate unless the MCP client reports that authorization is required.

MCP tools and resources to know:

- Shared platform: `atlassianUserInfo` gets the current Atlassian user, and `getAccessibleAtlassianResources` lists accessible cloud sites and `cloudId` values.
- Jira read/search: `searchJiraIssuesUsingJql` searches work items with JQL; `getJiraIssue` fetches an issue by key or ID; `getJiraIssueRemoteIssueLinks` lists linked remote resources; `getTransitionsForJiraIssue`, `getVisibleJiraProjects`, and `lookupJiraAccountId` help resolve project/user/workflow context.
- Rovo search/fetch: `searchAtlassian` searches Jira and Confluence with natural language; `fetchAtlassian` fetches Jira or Confluence content by Atlassian Resource Identifier (ARI). Use these when the user references a vague issue/page title instead of a key or URL.
- Teamwork Graph: `getTeamworkGraphContext` retrieves relationships around Atlassian entities, including linked PRs, repos, deployments, services, builds, Jira issues, Confluence pages, Compass components, people, teams, meetings, and external docs; `getTeamworkGraphObject` fetches objects returned by that context query. Use this to explain cross-product work, linked PRs, or release context.
- Confluence: `searchConfluenceUsingCql`, `getConfluencePage`, page descendant/comment tools, and space/page listing tools can add spec, release-note, or planning-page context.
- Jira Service Management: `getJsmOpsAlerts`, `getJsmOpsScheduleInfo`, and `getJsmOpsTeamInfo` are API-token-only and useful only for on-call, incident, or ops standups.

If MCP is unavailable, unauthorized, admin-blocked, or returns no Jira tools, fall back to Atlassian CLI (`acli`) for Jira-only activity; note that `acli` will not cover Confluence or Compass context.

#### Atlassian CLI Fallback

For Atlassian CLI, use `acli jira auth status` to detect an authenticated Jira account. If login is required and the user asked to configure it, use OAuth with `acli jira auth login --web`; API-token login is also supported through `acli jira auth login --site "mysite.atlassian.net" --email "user@atlassian.com" --token < token.txt`.

Use `acli jira workitem search` with JQL for standup collection. ACLI uses `workitem`, not `issue`:

```bash
acli jira auth status
acli jira workitem search --jql 'assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC' --fields 'key,summary,status,assignee,updated' --json --paginate
acli jira workitem search --jql 'updated >= "-1d" AND statusCategory != Done ORDER BY updated DESC' --fields 'key,summary,status,assignee,updated' --json --paginate
acli jira workitem search --jql '(assignee = currentUser() OR updated >= "-1d") AND statusCategory != Done ORDER BY updated DESC' --fields 'key,summary,status,assignee,updated' --json --paginate
acli jira workitem search --filter FILTER_ID --fields 'key,summary,status,assignee,updated' --json --paginate
```

Quote JQL relative dates such as `"-1d"` in standup queries. Use `--filter FILTER_ID` when the team already has a saved Jira filter for daily work.

Fetch issue details only when needed for the summary:

```bash
acli jira workitem view KEY-123 --fields "key,summary,status,assignee,description,comment" --json
```

Use `--json` for structured parsing, `--csv` when tabular output is easier, `--fields` to limit output, `--limit` for bounded searches, `--paginate` when the requested window may include many work items, and `--filter` for saved Jira filters. Prefer JQL over ad hoc filters because ACLI's documented work-item search path is JQL-based.

### OpenCode History

Run the bundled digest script automatically when the OpenCode database exists. Refer to the script from this skill bundle, not from an installation-specific absolute path. Depending on the host agent, use its native bundled-file reference such as `@scripts/opencode_digest.py`, or resolve `scripts/opencode_digest.py` relative to this `SKILL.md` file.

```bash
python3 scripts/opencode_digest.py --format json
```

By default, the digest scans all OpenCode projects in the local database. Only pass `--project` when the user explicitly wants one project:

```bash
python3 scripts/opencode_digest.py --project ~/my-app --format json
```

If the user asks for today's sessions:

```bash
python3 scripts/opencode_digest.py --date today --format json
```

Use the digest output as context. Filter out obviously irrelevant or personal sessions from the summary, and let the user correct or exclude noisy items during the interview.

If the digest script fails, skip OpenCode history and add a safety note. Common non-blocking causes: Python is unavailable, the OpenCode database is missing, there are no sessions for the target date, or the database cannot be read.

Store pulled data as interview context. Do not generate the update yet unless the user explicitly asked for an automatic summary with no interview.

---

## Phase 3: Interview With Context

Ask all four standup questions before generating the update unless the user explicitly asks for a no-interview summary. Stop after asking the interview questions and wait for the user's answers; do not infer answers from tool data alone. Use pulled data as context prompts, not as final wording.

### 1. Yesterday / Since Last Update

If data was pulled, summarize the useful bits first:

```text
Here is what I found so far:
- Merged PR #120: fix login timeout
- Opened PR #125: add OAuth flow
- Reviewed PR #123
- Jira PROJ-456 moved to In Progress
- OpenCode: researched payment providers

What else did you work on yesterday or since the last update?
```

If no data was pulled:

```text
What did you work on yesterday or since the last update?
```

If the answer is vague, ask one short follow-up, such as:

- What changed or shipped?
- Was that completed, still in progress, or blocked?
- Which project, PR, or ticket was that for?

### 2. Today / Next

Ask:

```text
What will you work on today?
```

If active PRs, branches, or Jira tickets were pulled, include them as prompts:

```text
I see these active items:
- PR #125: add OAuth flow
- branch oauth-staging has recent commits
- PROJ-456: Fix payment bug (In Progress)

Are any of these part of today's plan?
```

### 3. Blockers

Ask:

```text
Any blockers or impediments?

1. No blockers
2. Yes, I have blockers
```

If yes, ask for the blocker details and who or what is needed to unblock it.

### 4. Topics For Discussion

Ask:

```text
Any topic you want to bring up at the end of the daily?

1. No topics
2. Yes, I have a topic
```

Examples of useful topics:

- Technical decision that needs input
- Alignment with another team
- Question about priority or scope
- Announcement or context the team should know

---

## Phase 5: Generate Update

Resolve the report date from the selected window and write the final update to `daily-DATE.md`, where `DATE` is `YYYY-MM-DD`. For example, a report for May 3, 2026 must be written to `daily-2026-05-03.md`.

Combine interview answers and selected tool data into concise Markdown:

```markdown
# Standup

Window: [resolved time window]

## Yesterday / Since Last Update
- [Completed work, merged PRs, meaningful commits, selected sessions, or ticket progress]

## Today / Next
- [Likely next work based on user input, active PRs, branches, and tickets]

## PRs I Own
- [PR number, title, state, link]

## Activity On Others' PRs
- [Review/comment/mention summary]

## Local Branch Commits
- [repo] [branch]: [commit summary]

## Jira / Tickets
- [Ticket key, title, status, relevant progress]

## Blockers / Notes
- [Only real blockers, missing auth, missing repo scan root, empty results, or assumptions]
```

Keep the update under 15 bullets unless the user asks for a fuller report. Rewrite raw tool output into human-readable outcomes. Include PR or ticket identifiers only with enough context to be useful.

Omit empty sections unless they carry an important safety note. Keep `Blockers / Notes` when there are blockers, missing integrations, missing local repo scan root, no repositories found, missing timestamp/config, empty results, or assumptions.

---

## Quick Reference

| Phase | Action | Tooling |
|-------|--------|---------|
| Resolve | Interpret `$ARGUMENTS` as the time window | Conversation, shell date parsing as needed |
| Detect | Check git, gh, jira, Atlassian MCP, OpenCode history | Bash, shell commands, MCP availability |
| Collect | Auto-collect available sources; ask only for missing repo root | `gh`, `fd`/`find`, git, jira, Atlassian MCP, `opencode_digest.py` |
| Pull | Fetch available context | global `gh search prs`, `fd`/`find`, read-only git, Atlassian MCP first, acli fallback, `opencode_digest.py` |
| Interview | Ask yesterday/today/blockers/topics | Direct conversation |
| Generate | Write concise Markdown to `daily-DATE.md` | File output plus final summary |

---

## Reporting Rules

- Favor outcomes and blockers over raw logs.
- Separate owned PRs from activity on others' PRs.
- Separate local-only git findings from GitHub findings.
- Treat empty results as a valid finding; do not invent activity.
- If GitHub is unavailable, say the summary is based on local git and any other approved sources.
- If `~/Projects` does not exist and no alternate root is provided, say local branch commits are unavailable until the user provides a repo root.
- If Atlassian MCP is unavailable, use `acli` when available. If both Jira sources are unavailable, add a short safety note. If OpenCode history is unavailable, add a short safety note.
- Do not include secrets, private tokens, raw environment values, or irrelevant personal activity.

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Assuming the current directory is the only project | Development work often spans multiple local repositories and OpenCode projects | Scan `~/Projects` or the provided clone root and digest all OpenCode projects by default; narrow only when requested |
| Treating tool data as the final update | Tools capture activity, not intent or nuance | Interview first, then summarize |
| Including every session, commit, PR, comment, or ticket | Standups need signal, not a transcript | Summarize outcomes and let the user select relevant items |
| Asking for data after the interview | Context is most useful before interview prompts | Pull available data before the interview |
| Including raw commit messages | They are often cryptic or noisy | Rewrite into outcomes |

---

## Never

- Never assume integrations are configured.
- Never skip blockers or discussion topics unless the user explicitly asks for a no-interview summary.
- Never include obviously personal or irrelevant sessions in the final summary; let the user correct noisy OpenCode history during the interview.
- Never generate more than 15 bullets by default.
- Never include ticket or PR numbers without a title or short explanation.
- Never require GitHub access to produce a local-only summary.
- Never fail the whole update because one integration is missing.
- Never claim reviews, merges, blockers, or next steps that were not supported by collected data or user input.
