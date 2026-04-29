---
name: obsidian-tasks
description: Use when creating, reviewing, or debugging Obsidian Tasks plugin task lines, query blocks, recurring tasks, dates, priorities, dependencies, presets, global filters, or custom statuses.
---

# Obsidian Tasks

## Overview

Tasks manages Markdown checkbox tasks across a vault with dates, recurrence, priorities, dependencies, custom statuses, presets, and editable query results. Preserve task-line syntax because query interactions edit source Markdown.

## Task Syntax

```md
- [ ] Write proposal #task 📅 2026-05-01 🔼
- [ ] Weekly review #task 🔁 every Friday 📅 2026-05-01
- [ ] Draft spec #task 🆔 draft-spec
- [ ] Implement spec #task ⛔ draft-spec
- [x] Send invoice #task ✅ 2026-04-24
```

- Use fixed `YYYY-MM-DD` dates.
- Date markers: created `➕`, scheduled `⏳`, start `🛫`, due `📅`, done `✅`, cancelled `❌`.
- Priority markers: lowest `⏬`, low `🔽`, medium `🔼`, high `⏫`, highest `🔺`.
- Dependencies use IDs/blockers, commonly `🆔 id` and `⛔ id`.

## Query Examples

```tasks
not done
due before tomorrow
group by filename
sort by due
limit 100
```

```tasks
not done
path includes Projects
group by folder
sort by priority
sort by due
limit 100
```

## Storage And Settings

- Plugin config: `.obsidian/plugins/obsidian-tasks-plugin/data.json`.
- Important settings: global query/filter, task format, created/done/cancelled date automation, recurrence behavior, presets, and custom statuses.
- Query results can update source task lines when users toggle or edit tasks.

## Safety Rules

- Keep metadata on the same task line.
- Preserve indentation, IDs, dependency markers, recurrence, dates, and priority when editing.
- Use `limit` on broad query blocks.
- Choose one task format per vault; avoid mixing emoji and Dataview task formats without a reason.
- Avoid function-based filters, sorts, and groups in shared templates unless reviewed.

## Common Mistakes

- Writing natural-language dates like `tomorrow` in source task lines instead of fixed dates.
- Duplicating tasks manually instead of querying source tasks.
- Creating broad vault-wide dashboards without filters or limits.
- Breaking recurrence syntax when completing or editing recurring tasks.
- Removing IDs used by dependencies or Task Board.
