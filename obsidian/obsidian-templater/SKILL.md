---
name: obsidian-templater
description: Use when creating, reviewing, or debugging Obsidian Templater templates, tp.* syntax, folder templates, file templates, startup templates, user scripts, or system-command templates.
---

# Obsidian Templater

## Overview

Templater expands Markdown templates with `tp.*` functions, JavaScript execution blocks, user scripts, and optional system commands. Treat executable templates as code.

## Core Syntax

- Inline output: `<% tp.date.now("YYYY-MM-DD") %>`.
- JavaScript execution: `<%* const name = await tp.system.prompt("Name"); tR += name; %>`.
- File helpers: `tp.file.title`, `tp.file.rename()`, `tp.file.move()`, `tp.file.creation_date()`.
- Date helpers: `tp.date.now(format, offset)`, `tp.date.tomorrow()`, `tp.date.weekday()`.
- Frontmatter: `tp.frontmatter["field"]`.
- Prompts: `tp.system.prompt()`, `tp.system.suggester()`.
- User scripts: `tp.user.<scriptName>(args)`.

## Storage And Settings

- Plugin config: `.obsidian/plugins/templater-obsidian/data.json`.
- Important settings: templates folder, trigger-on-new-file, folder templates, file-regex templates, startup templates, user scripts folder, system commands, command timeout.
- Templates are Markdown files in the configured template folder.
- User scripts are JavaScript files in the configured scripts folder.

## Safe Workflow

1. Prefer simple interpolation for dates, titles, aliases, and static metadata.
2. Use `<%* %>` only for prompts, branching, calculations, or file operations.
3. Review scripts before enabling folder templates, startup templates, or system commands.
4. Avoid templates that rename, move, or delete files unless explicitly requested.
5. Keep system commands disabled unless there is a reviewed need.

## Examples

```md
---
type: meeting
created: <% tp.date.now("YYYY-MM-DD") %>
status: draft
---

# <% tp.file.title %>

## Notes
```

```md
<%*
const vendor = await tp.system.prompt("Vendor")
const amount = await tp.system.prompt("Amount")
tR += `vendor: ${vendor}\namount: ${amount}`
%>
```

## Common Mistakes

- Using JavaScript blocks for simple static templates.
- Enabling startup templates without treating them as automation.
- Creating system-command templates without explicit approval.
- Forgetting `tR +=` inside `<%* %>` when output is needed.
- Making folder templates too broad, causing imports or copied files to trigger unexpected automation.
