# Modal Form Reference

## Source Facts

Reviewed from `https://github.com/danielo515/obsidian-modal-form`, installed manifest version `1.64.4`, docs at `https://danielorodriguez.com/obsidian-modal-form/`, and source files under `src/API.ts`, `src/core/FormBuilder.ts`, `src/core/FormResult.ts`, `src/core/input/InputDefinitionSchema.ts`, and file input models.

Plugin ID: `modalforms`.

API access:

```javascript
const modalForm = app.plugins.plugins.modalforms.api;
```

Main API methods:

- `openForm(formNameOrDefinition, options?)`
- `namedForm(name, options?)`
- `limitedForm(name, limitOptions, formOptions?)`
- `builder(name, title?)`

## FormBuilder Methods

Core:

- `modalForm.builder(name, title?)`
- `.build()`

Fields:

- `.text({ name, label, description, required })`
- `.number({ name, label, description, required })`
- `.date({ name, label, description, required })`
- `.time({ name, label, description, required })`
- `.datetime({ name, label, description, required })`
- `.textarea({ name, label, description, required })`
- `.toggle({ name, label, description, required })`
- `.email({ name, label, description, required })`
- `.tel({ name, label, description, required })`
- `.note({ name, label, folder })`
- `.folder({ name, label, parentFolder })`
- `.slider({ name, label, min, max })`
- `.tag({ name, label, exclude })`
- `.select({ name, label, options })`
- `.dataview({ name, label, query })`
- `.multiselect({ name, label, options })`
- `.document_block({ name, label, body })`
- `.markdown_block({ name, label, body })`
- `.image({ name, label, filenameTemplate, saveLocation })`
- `.file({ name, label, folder, allowedExtensions })`

## Form Options

Pass defaults with `values`:

```javascript
await modalForm.openForm(form, { values: { date: "2026-04-26" } });
```

## Dataview Query Fields

Dataview fields evaluate a JavaScript expression with `dv`, `pages`, and `form` in scope. Return an array of values.

Examples:

```javascript
dv.pages('"Finanzas/Monedas"').file.name
dv.pages('"Finanzas/Categorías de gasto"').file.name
dv.pages('"Finanzas/Proveedores"').file.name
dv.pages().where(p => p.currency_code).currency_code.distinct()
```

For dependent fields:

```javascript
dv.pages('"Projects"').where(p => !form.area || p.area == form.area).file.name
```

## Result Handling

`openForm` returns `FormResult`.

Useful methods:

- `result.getData()` returns a shallow copy of raw form data.
- `result.asFrontmatterString({ pick, omit })` returns YAML without `---` delimiters.
- `result.asDataviewProperties({ pick, omit })` returns Dataview inline fields.
- `result.get(key)` returns a raw-ish value or empty string.
- `result.getValue(key)` returns a `ResultValue` wrapper for safe rendering.

The result has `status: "ok" | "cancelled"` in source. Check cancellation before writing files.

## File Uploads

File inputs save the selected browser file with its original filename into `input.folder` using `app.vault.createBinary`. The returned value is a `FileProxy` exposing:

- `.path`
- `.name`
- `.basename`
- `.extension`
- `.toString()` returning path

Example:

```javascript
const data = result.getData();
const receiptPath = data.receipt?.path || "";
const receiptLink = receiptPath ? `[[${receiptPath}]]` : "";
```

The file service creates the destination folder if missing, but it does not automatically deduplicate filenames. Consider filename collision behavior before relying on file uploads in high-volume workflows.
