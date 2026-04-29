# Meta Bind Buttons Reference

## Source Facts

Reviewed from `https://github.com/mProjectsCode/obsidian-meta-bind-plugin`, manifest version `1.4.8`, docs at `https://www.moritzjung.dev/obsidian-meta-bind-plugin-docs/`, and source files under `packages/core/src/config/ButtonConfig.ts` and `packages/core/src/fields/button/actions/`.

Button codeblocks use Markdown language `meta-bind-button` and YAML content.

## Button Config

Required fields:

- `label`: text shown on the button.
- `style`: one of `default`, `primary`, `destructive`, `plain`.

Optional fields:

- `icon`: Lucide icon name.
- `class`: CSS classes separated by spaces.
- `cssStyle`: inline CSS style string.
- `backgroundImage`: vault image path.
- `tooltip`: hover text.
- `id`: ID for inline `BUTTON[id]` references.
- `hidden`: hide source button when using inline references.
- `action`: one button action.
- `actions`: list of button actions.

`action` and `actions` are mutually exclusive.

## Actions

Command:

```yaml
action:
  type: command
  command: app:toggle-pin
```

The `command` value is an Obsidian command ID. The source executes `app.commands.executeCommandById(id)`. Use Meta Bind's `Select and copy command id` command or inspect `app.commands.listCommands()` when uncertain.

Templater create note:

```yaml
actions:
  - type: templaterCreateNote
    templateFile: "Recursos/Plantillas/Nuevo gasto.md"
    folderPath: "Finanzas/Gastos"
    fileName: "Nuevo gasto"
    openNote: true
    openIfAlreadyExists: false
```

Fields:

- `templateFile`: vault-relative template path, required.
- `folderPath`: optional vault-relative destination folder.
- `fileName`: optional new note name.
- `openNote`: optional boolean.
- `openIfAlreadyExists`: optional boolean, requires `fileName` to be useful.

Run Templater file:

```yaml
actions:
  - type: runTemplaterFile
    templateFile: "Recursos/Plantillas/Acción.md"
```

This evaluates the Templater file against the current note.

Open:

```yaml
action:
  type: open
  link: "Finanzas/Gastos/Gastos.md"
  newTab: true
```

Other mutating actions include `createNote`, `insertIntoNote`, `replaceInNote`, `replaceSelf`, `regexpReplaceInNote`, and `updateMetadata`. Use them only after confirming target file context and mutation scope.

JavaScript actions include `js` and `inlineJS`; treat both as executable code requiring explicit approval.

## Inline Buttons And Groups

Inline buttons use backticks and reference button IDs:

```markdown
`BUTTON[nuevo-gasto]`
```

Multiple IDs render a group:

```markdown
`BUTTON[nuevo-gasto, nueva-reunion]`
```

The source button must be defined in the same note or in Meta Bind Button Templates:

````markdown
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

## Buttons Plugin Migration Notes

Buttons plugin fields are not valid Meta Bind fields.

| Buttons plugin | Meta Bind |
|---|---|
| `name` | `label` |
| `color green` | `style: primary` or custom `class` |
| `type command` + `action <display name>` | `type: command` + `command: <command id>` |
| Templater create command display name | Prefer `templaterCreateNote` with `templateFile` |
| `^button-id` block ID | `id: button-id` plus inline `BUTTON[button-id]` if needed |

Do not paste a Command Palette display name into Meta Bind's `command` field.
