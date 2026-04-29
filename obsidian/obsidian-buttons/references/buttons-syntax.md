# Buttons Syntax Reference

## Source Facts

Reviewed from `https://github.com/shabegom/buttons`, manifest version `0.9.13`, README last updated `2025-08-02`, and `src/` implementation.

Commands registered by the plugin:

- `Button Maker`
- `Insert Inline Button`

Command buttons call `app.commands.listCommands()`, find by `command.name.toUpperCase() === action.toUpperCase().trim()`, then execute that command ID. The `action` line must be the Command Palette display name.

## Base Format

````markdown
```button
name Label
type command
action Toggle pin
```
^button-example
````

The block ID must be directly below the codeblock and start with `^button-`. Use descriptive IDs such as `^button-nuevo-gasto`.

## Recognized Arguments

Core arguments:

- `name <label>`
- `type <button type>`
- `action <command, URL, text, template name, or expression>`
- `id <parent-id>` for inheritance
- `swap [id1,id2]`
- `remove true` or `remove [id1,id2]`
- `replace [start,end]`, `replace [+1,+3]`, `replace [-2,-1]`, or `replace [cursor]`
- `templater true`
- `color blue|green|red|yellow|purple`
- `customColor <css-color>`
- `customTextColor <css-color>`
- `class <css-class>`
- `folder <folder path>`
- `prompt true`
- `width <number>` in em units
- `height <number>` in em units
- `align left|center|right top|middle|bottom`
- `actions [...]` for chain buttons
- `hidden true` to avoid rendering a source block

`name` supports multi-line Markdown with `{}` or `[]` delimiters:

````markdown
```button
name {
**Crear gasto**
Adjuntar comprobante
}
type command
action Commander: Crear gasto
width 18
height 4
align center middle
```
^button-crear-gasto
````

`action` supports multi-line content for text and copy buttons. It continues until another recognized argument starts at the beginning of a non-empty line.

## Command Buttons

Use for Obsidian core commands, plugin commands, and Commander macros:

````markdown
```button
name Nueva tarea
type command
action Commander: Nueva tarea
color blue
```
^button-nueva-tarea
````

Troubleshooting:

- If nothing happens, verify the command name as shown in Command Palette.
- Buttons does not resolve command IDs from `action`.
- Command lookup is case-insensitive but otherwise name-based.

## Link Buttons

````markdown
```button
name Abrir Vault
type link
action obsidian://open?vault=CiviNova&file=Vault
```
^button-abrir-vault
````

Use for URLs, Obsidian URIs, and x-callback URLs. Treat external URIs as executable links and ask before adding sensitive data.

## Text Buttons

Supported type forms:

- `append text`
- `prepend text`
- `cursor text`
- `line(1) text`
- `line(+1) text`
- `line(-2) text`
- `note(Title, tab) text`

Open methods for note creation: `vsplit`, `hsplit`, `split`, `tab`, `same`, `false`.

````markdown
```button
name Agregar seguimiento
type append text
action ## Seguimiento
- [ ] Próxima acción
```
^button-agregar-seguimiento
````

Use `folder <path>` with `note(...) text` when the new note must be created under a specific folder.

## Template Buttons

Supported type forms mirror text buttons:

- `append template`
- `prepend template`
- `cursor template`
- `line(1) template`
- `line(+1) template`
- `line(-2) template`
- `note(Title, tab) template`

````markdown
```button
name Nuevo gasto
type note(<% tp.date.now("YYYY-MM-DD") %> Gasto, tab) template
action Nuevo gasto
folder Finanzas/Gastos
templater true
```
^button-nuevo-gasto
````

Template lookup searches enabled Core Templates and Templater folders. If both contain the same template name, the source code prefers Templater.

## Chain Buttons

Use valid JSON in `actions`. Each object needs `type` and `action`; action objects can also include other fields such as `folder`.

````markdown
```button
name Flujo gasto
type chain
actions [
  {"type": "command", "action": "Commander: Abrir Finanzas"},
  {"type": "command", "action": "Commander: Nuevo gasto"}
]
```
^button-flujo-gasto
````

Notes:

- Actions execute top to bottom.
- If one action fails, later actions still attempt to run.
- Chain supports command, copy, link, template, calculate, text, and nested chain actions.
- Put `templater true` on the chain to process Templater expressions in action, type, and folder fields.

## Swap And Inline Buttons

Create source buttons with IDs, then create a swap button and insert it inline.

````markdown
```button
name Iniciar
type command
action Commander: Iniciar foco
```
^button-foco-iniciar

```button
name Detener
type command
action Commander: Detener foco
```
^button-foco-detener

```button
name Foco
type swap
swap [foco-iniciar,foco-detener]
```
^button-foco

`button-foco`
````

Inline references use backticks and require the full `button-` prefix. Swap buttons only work as inline buttons.

## Mutations

Remove the clicked button:

```markdown
remove true
```

Remove other buttons by ID suffix:

```markdown
remove [draft,review,approve]
```

Replace absolute lines:

```markdown
replace [1,3]
```

Replace relative lines near the button:

```markdown
replace [+1,+3]
```

Remove the line where the cursor was when clicked:

```markdown
replace [cursor]
```

Prefer relative replacement for reusable templates and dashboards.

## Styling

Built-in colors: `blue`, `green`, `red`, `yellow`, `purple`.

Layout arguments:

```markdown
width 18
height 4
align center middle
```

Use `class <css-class>` for custom snippets. Use Style Settings for global Buttons appearance when available.

## Templater

Add `templater true` when `name`, `type`, `action`, or `folder` contains `<% ... %>` that should be evaluated on click.

````markdown
```button
name Registrar hora
type append text
action Hora: <% tp.date.now("HH:mm") %>
templater true
```
^button-registrar-hora
````

Templater expressions are processed on click and restored for future use. Avoid using Templater in inline swap target buttons unless manually tested; source warns it is not reliable there.

## Review Checklist

- Does every button have a unique `^button-id`?
- For command buttons, does `action` match Command Palette text?
- For Commander macros, has the macro command been verified and reviewed for side effects?
- For chains, is `actions` valid JSON?
- For text/template mutations, are `replace` and `remove` scoped narrowly?
- For generated notes, is `folder` correct and is duplicate-file behavior acceptable?
- For Templater, is `templater true` present only when needed?
