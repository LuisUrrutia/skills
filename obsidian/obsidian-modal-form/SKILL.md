---
name: obsidian-modal-form
description: Use when creating, reviewing, or debugging Obsidian Modal Forms plugin forms, FormBuilder API usage, modal form JavaScript integrations, Templater or QuickAdd form captures, Dataview-backed form fields, file or image upload fields, form templates, registered form commands, and modal form plugin configuration.
---

# Obsidian Modal Form

## Overview

Modal Forms defines structured Obsidian input forms that can be opened from JavaScript contexts such as Templater, QuickAdd, and DataviewJS. Treat forms that create notes, upload files, run templates, or write metadata as executable automation.

## Safe Workflow

1. Confirm whether the form should be a named plugin form saved in settings or a self-contained form built in code.
2. Prefer self-contained FormBuilder forms when the behavior, validation, and note creation logic should remain testable with the script that uses it.
3. Prefer named forms when the user wants to manage fields/templates from the Modal Forms UI.
4. Avoid editing `.obsidian/plugins/modalforms/data.json` unless explicitly approved; inspect the local schema first and make the smallest reversible change.
5. Use `app.plugins.plugins.modalforms.api` from JavaScript contexts.
6. Validate returned values before writing files or metadata.
7. Treat Dataview query fields as dynamic code-like expressions; keep queries scoped and resilient to missing form values.

## API Pattern

Open a named form:

```javascript
const modalForm = app.plugins.plugins.modalforms.api;
const result = await modalForm.openForm("example-form");
const data = result.getData();
```

Build a self-contained form:

```javascript
const modalForm = app.plugins.plugins.modalforms.api;
const form = modalForm.builder("expense-form", "Nuevo gasto")
  .text({ name: "vendor", label: "Proveedor", required: true })
  .date({ name: "date", label: "Fecha", required: true })
  .number({ name: "amount", label: "Importe", required: true })
  .dataview({ name: "currency", label: "Moneda", query: 'dv.pages("Finanzas/Monedas").file.name' })
  .file({ name: "receipt", label: "Recibo", folder: "Finanzas/Gastos/Adjuntos", allowedExtensions: ["pdf", "png", "jpg", "jpeg", "webp"] })
  .build();
const result = await modalForm.openForm(form, { values: { date: "2026-04-26" } });
```

## Field Selection

- Use `text`, `textarea`, `number`, `date`, `time`, `datetime`, `toggle`, `email`, and `tel` for basic values.
- Use `select` for fixed values.
- Use `dataview` for suggestions from vault metadata or catalog notes.
- Use `note` or `folder` for picking existing notes or folders.
- Use `file` for arbitrary file uploads. The plugin saves the file to `input.folder` and returns a `FileProxy` with `.path`, `.name`, `.basename`, and `.extension`.
- Use `image` for image uploads that need filename templates and image-specific save settings.

## Dataview Fields

Dataview form fields run sandboxed Dataview expressions and must return an array. If the expression does not start with `return`, Modal Forms prefixes `return` internally.

Good examples:

```javascript
dv.pages('"Finanzas/Monedas"').file.name
dv.pages('"Finanzas/Categorías de gasto"').file.name
dv.pages('"Finanzas/Proveedores"').file.name
dv.pages().where(p => p.currency_code).currency_code.distinct()
```

For dependent queries, use the `form` variable defensively:

```javascript
dv.pages('"Projects"').where(p => !form.status || p.status == form.status).file.name
```

## Results

Use `result.getData()` when processing values in JavaScript. Use `result.getValue(key)` or property accessors in templates when rendering values safely.

File uploads return a FileProxy-like object:

```javascript
const data = result.getData();
const receiptPath = data.receipt?.path || "";
```

## Commands And Templates

Named forms can have templates and registered commands:

- `Modal Forms: Insert template: [Form Name]`
- `Modal Forms: Create note from template: [Form Name]`

Use plugin-managed commands only when the form template is saved in Modal Forms settings. For custom validation, FX lookup, file naming, or multi-step note creation, call the API from a Templater user script instead.

## Common Mistakes

- Confusing Modal Forms plugin ID `modalforms` with other folder names.
- Editing `data.json` before checking whether a self-contained builder form is safer.
- Assuming Dataview fields accept DQL strings like `TABLE`; they expect JavaScript expressions using `dv`.
- Forgetting Dataview query fields must return arrays.
- Treating uploaded file results as plain strings instead of reading `.path` from FileProxy.
- Using `allowedExtensions` with leading dots inconsistently. Local examples use `pdf`; docs show `.pdf`. Verify in the installed plugin if filtering matters.
- Writing notes after cancelled forms; check `result.status` or required values before continuing.
