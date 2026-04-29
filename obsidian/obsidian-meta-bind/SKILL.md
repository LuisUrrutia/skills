---
name: obsidian-meta-bind
description: Use when creating, reviewing, or debugging Obsidian Meta Bind input fields, view fields, button codeblocks, inline buttons, button groups, button actions, command actions, Templater note creation actions, metadata-bound controls, or Meta Bind plugin configuration.
---

# Obsidian Meta Bind

## Overview

Meta Bind renders interactive Markdown controls in Obsidian: input fields, view fields, and YAML-configured buttons. Treat Meta Bind buttons and field updates as executable or mutating automation, especially when they run commands, Templater, JavaScript, or metadata updates.

## Safe Workflow

1. Identify whether the control reads metadata, updates metadata, opens links, creates files, runs Templater, runs commands, or executes JavaScript.
2. Prefer normal Markdown `meta-bind-button` codeblocks for visible buttons; use inline `BUTTON[id]` only when the source button is defined in the same note or in Meta Bind Button Templates.
3. For command buttons, use Obsidian command IDs, not Command Palette display names. Use the `Meta Bind: Select and copy command id` command when available.
4. For Templater note creation, prefer `type: templaterCreateNote` with an explicit vault-relative `templateFile` over a command action when the goal is to create a note from a known template.
5. Keep destructive actions, broad metadata updates, JavaScript, and note rewrites behind explicit approval.
6. Test risky buttons in a scratch note before placing them on dashboards or shared notes.

## Common Button Patterns

Visible command button:

````markdown
```meta-bind-button
label: Toggle pin
style: default
  type: command
  command: app:toggle-pin
```
````

Templater note creation button:

````markdown
```meta-bind-button
label: Nuevo gasto
style: primary
actions:
  - type: templaterCreateNote
    templateFile: "Recursos/Plantillas/Nuevo gasto.md"
    openNote: true
```
````

Inline button using a hidden source button in the same note:

````markdown
`BUTTON[nuevo-gasto]`

```meta-bind-button
label: Nuevo gasto
style: primary
id: nuevo-gasto
hidden: true
actions:
  - type: templaterCreateNote
    templateFile: "Recursos/Plantillas/Nuevo gasto.md"
    openNote: true
```
````

## Button Type Selection

- Use `command` for existing Obsidian/plugin commands when you have the command ID.
- Use `templaterCreateNote` to create a new note from a Templater template.
- Use `runTemplaterFile` to run Templater code from a template file against the current note.
- Use `open` for vault links, Obsidian links, and external URLs.
- Use `createNote`, `insertIntoNote`, `replaceInNote`, `replaceSelf`, or `updateMetadata` only after confirming the mutation scope.
- Use `js` or `inlineJS` only when JavaScript execution is explicitly approved.

## Conversion From Buttons Plugin

Buttons plugin command buttons use Command Palette display names in `action`. Meta Bind command buttons use command IDs in `command`. Do not copy `action Templater: Create Nuevo gasto` into a Meta Bind `command` field.

Buttons plugin:

````markdown
```button
name Nuevo gasto
type command
action Templater: Create Nuevo gasto
color green
```
````

Meta Bind equivalent when a template path is known:

````markdown
```meta-bind-button
label: Nuevo gasto
style: primary
actions:
  - type: templaterCreateNote
    templateFile: "Recursos/Plantillas/Nuevo gasto.md"
    openNote: true
```
````

## Gotchas

- `action` and `actions` are mutually exclusive.
- `style` must be `default`, `primary`, `destructive`, or `plain`; Buttons colors such as `green`, `yellow`, `blue`, and `purple` do not map directly unless custom CSS classes are added.
- `command` action values must be command IDs; Meta Bind source calls `app.commands.executeCommandById(id)`.
- Inline `BUTTON[id]` references require an `id` on a button codeblock in the same note, unless using plugin-level Button Templates.
- `templaterCreateNote.templateFile` is vault-relative and must include the `.md` extension.
- Mutating actions depend on the file context where the button is rendered. Be cautious inside embedded notes, callouts, dashboards, and plugin-rendered views.

For full source-backed syntax and action reference, read `references/meta-bind-buttons.md`.
