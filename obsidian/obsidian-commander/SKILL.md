---
name: obsidian-commander
description: Use when configuring, reviewing, or debugging Obsidian Commander commands, macros, ribbon buttons, status bar items, page header buttons, file menu items, mobile toolbar, or hidden commands.
---

# Obsidian Commander

## Overview

Commander places Obsidian commands in UI surfaces and can create macros with command and delay steps. Treat macros and startup macros as executable automation.

## Capabilities

- Add commands to ribbon, status bar, page header, file explorer, editor menu, file menu, and mobile toolbar.
- Rename commands and override icons.
- Hide selected ribbon/status/UI commands.
- Create macros from command steps and delays.
- Use device-specific visibility modes.

## Storage And Settings

- Plugin config: `.obsidian/plugins/cmdr/data.json`.
- Settings include command arrays per UI surface, macros, hidden entries, spacing, and advanced toolbar config.

## Safe Workflow

1. Keep shared command surfaces small and obvious.
2. Prefer navigation and note-creation shortcuts over mutating workflows.
3. Use device-specific visibility for desktop/mobile differences.
4. Review every macro step before enabling.
5. Avoid startup macros unless the user explicitly approves them.

## Common Mistakes

- Hiding recovery-critical commands or UI affordances.
- Creating macros that run AI, delete/move files, publish, export, sync, or change settings without approval.
- Overloading the UI with too many buttons.
- Forgetting command IDs can change when plugins are removed or renamed.
