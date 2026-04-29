---
name: obsidian-callout-manager
description: Use when creating, reviewing, or debugging Obsidian callout types, Callout Manager custom callouts, callout colors, icons, theme/snippet detection, callout IDs, or callout rendering conventions.
---

# Obsidian Callout Manager

## Overview

Callout Manager discovers, creates, and customizes Obsidian callout types, icons, and colors from Obsidian defaults, themes, snippets, and custom settings.

## Markdown Syntax

```md
> [!info] Title
> Body text.

> [!warning]
> Important caveat.
```

## Capabilities

- Browse available callouts.
- Customize colors and icons.
- Create custom callout IDs.
- Detect callouts from Obsidian, themes, and snippets.
- Expose an API for other plugins.

## Storage And Settings

- Plugin config: `.obsidian/plugins/callout-manager/data.json`.
- Settings include custom callouts, per-callout settings, detection flags, and complex theme/light/dark conditions.

## Safety Rules

- Prefer standard Obsidian callout IDs unless a shared custom vocabulary is needed.
- Do not invent custom callout IDs casually in shared notes.
- Keep callout IDs readable even without the plugin.
- Avoid relying on theme-only callouts unless the theme/snippet is part of the vault setup.
- Do not use callouts for structured data that belongs in frontmatter, tables, or tasks.

## Common Mistakes

- Creating many near-duplicate callout types.
- Encoding workflow state only through callout color/icon.
- Editing complex `data.json` appearance conditions directly without testing.
