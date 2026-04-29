---
name: obsidian-dataview
description: Use when creating, reviewing, or debugging Obsidian Dataview DQL, DataviewJS, inline fields, metadata dashboards, task queries, table views, list views, or calendar views.
---

# Obsidian Dataview

## Overview

Dataview renders live views from Markdown metadata, frontmatter, inline fields, links, tags, lists, and tasks. Prefer DQL for maintainable dashboards; treat DataviewJS as executable code.

## Query Types

- `TABLE`: tabular metadata views.
- `LIST`: page or value lists.
- `TASK`: task queries from Markdown files.
- `CALENDAR`: date-based page views.
- Inline DQL: `` `= this.file.name` ``.
- DataviewJS: `dataviewjs` blocks using `dv.*` APIs.

## Metadata Patterns

```yaml
---
type: project
status: active
owner: Alex
due: 2026-05-01
tags:
  - project
---
```

```md
Owner:: Alex
[status:: active]
(review_date:: 2026-05-01)
```

## Examples

```dataview
TABLE status, owner, due, file.mtime AS "Updated"
FROM "Projects"
WHERE status != "archived"
SORT due ASC
```

```dataview
TASK
FROM "Meetings"
WHERE !completed
GROUP BY file.link
```

## Storage And Settings

- Plugin config: `.obsidian/plugins/dataview/data.json`.
- Cache/index data uses IndexedDB/localforage, not Markdown source files.
- Important toggles include DataviewJS, inline JS, inline DQL, render settings, and refresh behavior.

## Safety Rules

- Scope broad queries with `FROM "Folder"` or tags.
- Prefer frontmatter with stable lowercase field names for shared dashboards.
- Prefer DQL over DataviewJS unless logic cannot be expressed in DQL.
- Do not enable or write DataviewJS casually; JavaScript can access Obsidian APIs and modify files.
- Do not rely on query output as canonical data; store source data in notes.
