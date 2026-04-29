---
name: obsidian-makemd
description: Use when working with Obsidian MAKE.md / make.md spaces, Navigator, context databases, views, formulas, actions, labels, stickers, hidden files, folder ordering, or .space-managed vault structures.
---

# Obsidian MAKE.md

## Overview

MAKE.md adds an app-like workspace layer over Obsidian. Treat its Spaces, context databases, views, formulas, actions, and `.space` files as plugin-managed state unless the user explicitly asks for config-level changes.

## Capability Map

- **Navigator:** Focuses, search, hidden items, pinning, and drag ordering inside MAKE.md's sidebar.
- **Spaces:** Folders, tags, vault root, and built-ins become customizable spaces with their own views.
- **Context databases:** Space-scoped tables with schemas, rows, saved views, filters, sorts, formulas, relations, aggregates, table/list/board/calendar layouts.
- **Space Views:** Custom dashboards built from note blocks, list views, dividers, images, buttons, labels, stickers, ratings, toggles, and progress.
- **Labels:** Stickers, colors, aliases, and covers for files/spaces.
- **Formulas:** Calculated fields and path/list/date helpers such as `spaceItems`, `spaces`, `sort`, `filter`, `map`, and `findIndex`.
- **Actions:** Buttons and commands that can open links or run commands; treat as executable automation.

## Storage Model

- Plugin settings: `.obsidian/plugins/make-md/data.json`.
- Default plugin config folder: `.space`.
- Root vault space files: `.space/context.mdb`, `.space/views.mdb`, `.space/commands.mdb`, `.space/def.json`.
- Folder space files: `<folder>/.space/context.mdb`, `<folder>/.space/views.mdb`, `<folder>/.space/commands.mdb`, `<folder>/.space/def.json`.
- Tag spaces use the configured spaces folder plus `.space` files.
- `context.mdb` stores context schemas/tables; `views.mdb` stores frames/views; `commands.mdb` stores actions.
- Hidden/default ignored internals include `.space`, `.mdb`, `_assets`, and `_blocks`.

## Ordering Guidance

MAKE.md supports custom ordering inside its own Navigator/Spaces. Default space sort is `rank`, and drag/drop reorder writes row order into the context table. This is not the same as native Obsidian File Explorer sorting.

- Use MAKE.md Navigator when the user wants a curated ordered workspace with clean folder names.
- Use Iconic for native file/folder icons if the user wants Obsidian File Explorer icons.
- Use a dedicated sorting plugin, such as Custom File Explorer Sorting, if the user specifically needs native File Explorer manual order.
- Do not rename folders with numeric prefixes unless the user explicitly prefers filesystem-level order.

## AI-Safe Workflow

1. Classify the requested change as note content, metadata, context schema, view, formula, action, label, or plugin setting.
2. Edit normal Markdown/frontmatter only when fields and conventions are clear.
3. Prefer MAKE.md UI/plugin workflows for context databases, views, formulas, and actions.
4. Before touching `.space`, `.mdb`, `commands.mdb`, `views.mdb`, or plugin `data.json`, explain the risk and ask for confirmation.
5. Avoid bulk edits in iCloud-shared vaults; MAKE.md maintains indexes and context rows that can desync during sync conflicts.

## Practical Patterns

- Use Spaces as dashboards for folders, tags, projects, topics, research areas, or operating views.
- Use context fields for durable metadata such as `status`, `owner`, `priority`, `due`, `area`, `source`, `review_date`, and `next_action`.
- Use Space Views to show pinned notes, context list views, buttons, status widgets, and progress.
- For multi-column Markdown dashboards, prefer small Markdown subnotes rendered as Space View `flow` frames instead of large inline `text` frames; this preserves Markdown rendering and keeps content editable as normal notes.
- Keep dashboard rows to two columns on desktop unless the user explicitly wants dense layouts. When editing MAKE view state directly, account for row gaps in width math, e.g. two columns with a `44px` gap need widths like `calc(50% - 22px)`, not plain `50%`.
- Use labels/stickers/colors for navigation cues, not as the only source of truth.
- Use formulas for calculated values like days until due date, risk score, progress, age since review, or totals.
- Use actions only for low-risk navigation or command shortcuts; avoid actions that run scripts or mutate many files.

## Shared Vault Guidance

- Use clean folder names and MAKE.md Navigator rank/order for preferred display order.
- Assign one owner for structural changes to Spaces, views, formulas, and actions.
- Do not have multiple users edit the same Space View or context database at the same time.
- Back up the vault before changing `.space`, `.mdb`, view schemas, or action definitions.
- Prefer append-only notes and stable frontmatter fields to reduce sync conflict risk.

## Context Schema Examples

- Project tracker: `status`, `owner`, `priority`, `due`, `next_action`, `risk`, `progress`.
- CRM/contact tracker: `type`, `organization`, `role`, `relationship`, `last_contact`, `next_follow_up`, `owner`.
- Research tracker: `topic`, `source`, `status`, `confidence`, `last_checked`, `url`, `summary`.
- Expense tracker: `date`, `vendor`, `category`, `amount`, `currency`, `amount_usd`, `paid_by`, `receipt`.
- Decision tracker: `decision`, `date`, `owner`, `status`, `rationale`, `follow_up`.

## Formula And Action Guardrails

- Good formulas: days until due date, progress percentage, risk score, USD reference totals, review age.
- Avoid formulas that encode business-critical decisions without a plain-language note explaining the rule.
- Safe actions: open dashboard, open template, open external URL, navigate to a Space.
- Review-required actions: create notes, move files, modify properties, run Obsidian commands that change vault state.
- Avoid actions that execute scripts, use `new Function`-style arbitrary code, or mutate many files.

## Visual Layer Guidance

| Need | Use |
|---|---|
| MAKE.md Navigator/Space visual labels | MAKE.md stickers, colors, aliases, covers |
| Native Obsidian File Explorer icons | Iconic folder/file rules |
| Semantic workflow state | Frontmatter properties, tags, and Tasks |
| Pretty dashboards | MAKE.md Space Views plus Dataview/Tasks where appropriate |

## Common Mistakes

- Assuming MAKE.md sorts the native File Explorer. It orders MAKE.md Navigator/Spaces; native sorting needs Obsidian or a sorting plugin.
- Editing `.mdb` files by hand. They are plugin data, not Markdown source.
- Treating stickers/colors as durable metadata. Store state in properties and use labels only for presentation.
- Storing Markdown-heavy dashboard cards in MAKE `text` frames when `flow` frames pointing at normal notes would render and sync more predictably.
- Setting two `50%` columns plus a row gap, which can wrap cards into one column. Subtract half the gap from each column width or use the MAKE.md UI to adjust layout.
- Creating script/actions automation in a shared vault without review.
- Changing property names used by context databases without checking formulas, views, and templates.
