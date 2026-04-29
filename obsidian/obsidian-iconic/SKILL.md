---
name: obsidian-iconic
description: Use when configuring, reviewing, or debugging Obsidian Iconic icons, colors, file rules, folder rules, tab icons, tag icons, property icons, ribbon icons, or icon rulebooks.
---

# Obsidian Iconic

## Overview

Iconic customizes icons and colors for Obsidian UI elements and can automate file/folder icons with rulebooks. Icons are visual cues, not durable workflow state.

## Capabilities

- Customize tabs, files, folders, bookmarks, tags, properties, ribbon commands, and app/window buttons.
- Use Lucide icons and emojis.
- Apply optional colors.
- Create file and folder rules based on name, filename, extension, path, tags, properties, headings, links, embeds, created/modified dates, and system clock.
- Rules have priority order and can visually override manual icons.

## Storage And Settings

- Plugin config: `.obsidian/plugins/iconic/data.json`.
- Iconic can create rotating backups such as `data.json.backup1`.
- Settings include icon maps and `fileRules` / `folderRules`.

## Safe Workflow

1. Prefer rules over one-off icon edits for shared conventions.
2. Use paths, tags, and properties as rule targets.
3. Document icon meanings when they imply workflow cues.
4. Avoid relying on emoji rendering consistency across devices.
5. Avoid using Iconic and Iconize for the same UI areas because visual conflicts are expected.

## Common Mistakes

- Treating icons/colors as source-of-truth metadata.
- Creating fragile path rules before folder names are stable.
- Editing `data.json` directly instead of using UI/rulebook.
- Forgetting higher-priority rules override lower-priority or manual icons visually.
