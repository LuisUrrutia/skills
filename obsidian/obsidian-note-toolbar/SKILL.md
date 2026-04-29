---
name: obsidian-note-toolbar
description: Use when configuring, reviewing, or debugging Obsidian Note Toolbar toolbars, folder mappings, notetoolbar properties, toolbar callouts, commands, links, menus, scripts, variables, or mobile toolbar behavior.
---

# Obsidian Note Toolbar

## Overview

Note Toolbar adds context-aware toolbars to notes using commands, file/folder links, URIs, menus, variables, callouts, and optional script items. Script items are executable automation.

## Capabilities

- Show toolbars by `notetoolbar` property, folder mapping, default toolbar, selected text, mobile navigation, new tab launchpad, or embedded toolbar callout.
- Toolbar items can run commands, open files/folders/URIs, open menus, or run Dataview/Templater/JS Engine/JavaScript scripts.
- Variables can use note titles and properties in labels, tooltips, and URIs.

## Storage And Settings

- Plugin config: `.obsidian/plugins/note-toolbar/data.json`.
- Important settings include `toolbars`, `folderMappings`, `rules`, `toolbarProp`, `scriptingEnabled`, `defaultToolbar`, and `textToolbar`.

## Safe Workflow

1. Prefer folder mappings for broad behavior and `notetoolbar: <name>` for per-note overrides.
2. Keep toolbar names stable because notes may reference them in frontmatter.
3. Use toolbar items for navigation and safe commands by default.
4. Do not enable or generate script items without explicit review.
5. Avoid direct `data.json` edits unless the user requested plugin-level config changes.

## Common Mistakes

- Renaming toolbars without updating note properties.
- Enabling scripting for convenience without reviewing scripts.
- Embedding toolbar callouts everywhere instead of using mappings/properties.
- Overwriting personal toolbar preferences in a shared vault.
