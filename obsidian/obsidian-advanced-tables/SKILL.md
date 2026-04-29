---
name: obsidian-advanced-tables
description: Use when creating, editing, reviewing, or debugging Obsidian Markdown tables with the Advanced Tables plugin, including table formatting, Tab/Enter navigation, alignment, row/column operations, sorting, CSV export, toolbar commands, settings, and TBLFM formulas.
---

# Obsidian Advanced Tables

## Overview

Advanced Tables adds command-driven editing, formatting, navigation, sorting, and formulas to standard Markdown tables in Obsidian. Use plugin-specific source facts instead of guessing spreadsheet behavior or command names.

## Safe Workflow

1. Determine whether the task is plain Markdown table authoring, Advanced Tables command use, formula authoring, or plugin configuration.
2. Preserve Markdown compatibility: avoid nonstandard table syntax except Advanced Tables formula comments immediately following a table.
3. For formulas, use exact `<!-- TBLFM: ... -->` syntax and verify functions/operators from `references/advanced-tables-reference.md`.
4. Treat row/column deletion, sorting, transpose, and formula evaluation as mutating actions. Ask before applying them broadly across important notes.
5. For mobile use, do not rely on physical `Tab`/`Enter`; recommend command palette, mobile toolbar commands, or the Advanced Tables toolbar.

## Quick Reference

| Need | Use |
|---|---|
| Create/fix a Markdown table | Standard Markdown table plus Advanced Tables format command |
| Navigate cells | `Tab`, `Shift+Tab`, `Enter`, or commands when enabled |
| Align a column | `Left align column`, `Center align column`, `Right align column` |
| Add/remove/move data | Row/column insert, delete, move, transpose commands |
| Sort data | Put cursor in target column, then sort ascending/descending |
| Calculate totals | Formula comment directly below table, then evaluate formulas |
| Export | Open Advanced Tables toolbar, use CSV export |

Read `references/advanced-tables-reference.md` for exact command names, settings, formula syntax, and examples.

## Strong Example

````markdown
| Item            | Qty | Unit | Total |
| --------------- | --: | ---: | ----: |
| Notebook        |   2 | 3.50 |  7.00 |
| Pen             |   5 | 1.20 |  6.00 |
| **Grand Total** |     |      | 13.00 |
<!-- TBLFM: $>=($2*$3);%.2f -->
<!-- TBLFM: @>$>=sum(@I..@-1);%.2f -->
````

This keeps the table plain Markdown, right-aligns numeric columns, calculates each row total from quantity and unit price, then calculates the final total. Formula evaluation is explicit; it does not auto-recalculate while editing.

## Common Mistakes

Do not invent Excel-style syntax like `=SUM(A1:A3)`. Advanced Tables uses org-mode-like `TBLFM` comments, row references with `@`, and column references with `$`.

Do not use `TBFM` even though older comments/tests mention it; the parser grammar requires `TBLFM`.

Do not place blank lines between a table and its formula comments. Formula lines are collected only while they are contiguous HTML comments immediately after the table.

Do not assume `Tab` and `Enter` navigation works on mobile or in every editing mode. The plugin provides commands and a toolbar fallback.

Do not edit plugin `data.json` directly unless the user explicitly asks for plugin configuration edits; most Advanced Tables work belongs in Markdown notes or Obsidian settings.
