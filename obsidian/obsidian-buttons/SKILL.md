---
name: obsidian-buttons
description: Use when creating, reviewing, or debugging Obsidian Buttons plugin button codeblocks, Button Maker output, inline buttons, command buttons, chain/swap buttons, button mutations, styling arguments, Templater-enabled buttons, or Buttons used to trigger Commander macros and other Command Palette commands.
---

# Obsidian Buttons

## Overview

Buttons renders Markdown `button` codeblocks and inline button references into clickable Obsidian actions. Use this skill to author safe, valid button blocks and to connect Buttons with Commander macros by targeting Command Palette command names.

## Safe Workflow

1. Confirm the requested button behavior and whether it mutates notes, creates files, runs macros, opens links, or calls Templater.
2. Prefer command buttons for existing Obsidian/plugin commands and Commander macros.
3. Use exact Command Palette display names in `action`; Buttons source resolves commands by `command.name` case-insensitively, not by command ID.
4. Keep destructive or broad automation behind explicit approval. Treat Buttons, Commander macros, Templater code, URI links, and chain buttons as executable automation.
5. Prefer small visible buttons in normal notes or a dedicated button library note. Use inline buttons only after creating a source block with a stable `^button-id`.
6. Test risky buttons manually in Obsidian or create them in a scratch note before placing them on shared dashboards.

## Commander Macro Buttons

Create a Buttons command button that runs the Commander macro command exactly as it appears in Obsidian's Command Palette:

````markdown
```button
name Crear gasto
type command
action Commander: Crear gasto
color green
```
^button-crear-gasto
````

If the macro does not run, verify the visible command name in the Command Palette or with Obsidian developer tooling. Do not substitute Commander internal IDs unless the command palette name is unavailable and the plugin code has been inspected.

## Common Button Pattern

Every normal button is a fenced codeblock followed by a block ID:

````markdown
```button
name Button label
type command
action Toggle pin
```
^button-example
````

Inline buttons reference an existing block ID with backticks:

```markdown
Run it here: `button-example`
```

For full syntax, button types, mutation arguments, styling, and troubleshooting, read `references/buttons-syntax.md`.

## Button Type Selection

Use `type command` for Commander macros, core commands, and plugin commands.
Use `type link` for URLs and Obsidian URIs.
Use `type append text`, `prepend text`, `cursor text`, `line(N) text`, or `note(title, open) text` for direct text insertion or note creation.
Use corresponding `template` types for Core Templates or Templater template files.
Use `type chain` only when multiple actions must run in sequence.
Use `type swap` only for inline multi-state controls.

## Gotchas

Command actions require command display names. Chain `actions` must be valid JSON. Inline button references must include the `button-` prefix; mutation references like `remove [id1,id2]`, `swap [id1,id2]`, and `id parent` use only the ID suffix. Templater expressions require `templater true` and do not work reliably inside inline swap targets.
