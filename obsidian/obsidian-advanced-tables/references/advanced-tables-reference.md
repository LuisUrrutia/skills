# Advanced Tables Reference

## Source Facts

Reviewed from `https://github.com/tgrosinger/advanced-tables-obsidian`, manifest version `0.22.2`, plus formula engine docs/source in `https://github.com/tgrosinger/md-advanced-tables` package version `3.11.0`.

Plugin ID: `table-editor-obsidian`.

The Obsidian plugin wraps `@tgrosinger/md-advanced-tables`; formula behavior lives in that shared package.

## Commands

Command Palette names registered by the Obsidian plugin:

| Command name | Behavior |
|---|---|
| `Go to next row` | Move to the next table row |
| `Go to next cell` | Move to the next cell |
| `Go to previous cell` | Move to the previous cell |
| `Format table at the cursor` | Format current table |
| `Format all tables in this file` | Format every table in active file |
| `Insert column before current` | Insert column before cursor column |
| `Insert row before current` | Insert row before cursor row |
| `Move cursor out of table` | Escape from the table |
| `Left align column` | Set current column alignment left |
| `Center align column` | Set current column alignment center |
| `Right align column` | Set current column alignment right |
| `Move column left` | Move current column left |
| `Move column right` | Move current column right |
| `Move row up` | Move current row up |
| `Move row down` | Move current row down |
| `Delete column` | Delete current column |
| `Delete row` | Delete current row |
| `Sort rows ascending` | Sort rows by current column ascending |
| `Sort rows descending` | Sort rows by current column descending |
| `Transpose` | Swap table rows/columns |
| `Evaluate table formulas` | Evaluate formula comments for current table |
| `Open table controls toolbar` | Toggle/reveal Advanced Tables toolbar |

Default hotkey: `Mod+Shift+D` opens the table controls toolbar.

Source README lists default table navigation when cursor is in a Markdown table:

| Hotkey | Action |
|---|---|
| `Tab` | Next cell |
| `Shift+Tab` | Previous cell |
| `Enter` | Next row |

Mobile note: physical `Tab` and `Enter` navigation are not available; add Advanced Tables commands to the mobile toolbar or use the plugin toolbar.

## Settings

Default settings from source:

| Setting | Default | Notes |
|---|---:|---|
| `formatType` | `NORMAL` | Normal pads cell widths with spaces |
| `showRibbonIcon` | `true` | Shows sidebar/ribbon icon for toolbar |
| `bindEnter` | `true` | Binds Enter to next row; restart required after setting change |
| `bindTab` | `true` | Binds Tab/Shift+Tab to cell navigation; restart required after setting change |

Settings UI labels:

| Label | Effect |
|---|---|
| `Bind enter to table navigation` | Enter advances to next row when cursor is in table; disable for conflicts with tag/CJK autocomplete |
| `Bind tab to table navigation` | Tab/Shift+Tab move between cells; disable for conflicts with tag/CJK autocomplete |
| `Pad cell width using spaces` | Toggles padded table formatting; source maps off to `FormatType.WEAK` |
| `Show icon in sidebar` | Adds toolbar button to sidebar; reload required |

Avoid editing `.obsidian/plugins/table-editor-obsidian/data.json` manually unless explicitly requested. Prefer Obsidian Settings UI.

## Formatting And Alignment

Advanced Tables preserves normal Markdown alignment markers:

| Marker | Alignment |
|---|---|
| `---` | default/none |
| `:---` | left |
| `---:` | right |
| `:---:` | center |

The formatter can complete missing delimiter rows and missing cells. Normal formatting pads cells to column widths; weak formatting avoids padding.

## Formula Basics

Formulas are HTML comments immediately after the table:

```markdown
| Item | Grams |
| ---- | ----: |
| A    |   110 |
| B    |   748 |
| **Total** |     |
<!-- TBLFM: @>$2=sum(@I..@-1) -->
```

Use `TBLFM`, not `TBFM`. Source comments/tests contain old `TBFM` examples, but the parser grammar is exact: `<!-- TBLFM: ` + formulas + ` -->`.

Important formula rules:

- Formula comments must directly follow the table with no blank line.
- Evaluation is explicit via `Evaluate table formulas` or the formula button in the toolbar.
- Multiple formula comments are allowed and evaluated top to bottom.
- Multiple formulas can be chained in one comment with `::` and are evaluated left to right.

```markdown
<!-- TBLFM: @2=@4::$1=$2 -->
<!-- TBLFM: @5$3=sum(@2) -->
```

## Formula References

Rows use `@`; columns use `$`.

| Reference | Meaning |
|---|---|
| `@1`, `@5` | Absolute row |
| `$1`, `$5` | Absolute column |
| `@<`, `$<` | First row / first column |
| `@>`, `$>` | Last row / last column |
| `@I` | First body row below the header delimiter |
| `@-1`, `@+2` | Relative row from destination/current cell |
| `$-1`, `$+2` | Relative column from destination/current cell |
| `@2$4` | Cell at row 2, column 4 |
| `@2` | Row 2 in the current destination column |
| `$4` | Column 4 in the current destination row |

When both row and column are present, row comes first: `@2$4`, not `$4@2`.

## Formula Ranges

Ranges use two dots:

| Range | Meaning |
|---|---|
| `@I..@-1` | Current column, first body row through previous row |
| `$4..$6` | Columns 4 through 6 in current row context |
| `@2$3..@5$5` | Rectangular cell range |
| `@<..@>` | Whole table context |

Range endpoints must be compatible. `@2..$4` is invalid because it mixes a row endpoint and a column endpoint.

## Functions And Operators

Supported single-parameter functions:

| Function | Meaning |
|---|---|
| `sum(source)` | Sum cells in a range, row, column, or cell context |
| `mean(source)` | Average cells in a range, row, column, or cell context |

Supported algebraic operators: `+`, `-`, `*`, `/`.

Algebraic operations must be wrapped in parentheses:

```markdown
<!-- TBLFM: $3=($1*$2);%.2f -->
```

Do not use Excel-style `=SUM(A1:A3)` syntax.

## Conditionals

Conditionals use `if(predicate, trueSource, falseSource)`.

```markdown
<!-- TBLFM: $>=if($1>3, $1, 3) -->
```

Supported comparison operators: `<`, `>`, `<=`, `>=`, `==`, `!=`.

Comparisons are between cells/sources without ranges; do not compare range-to-range.

## Display Directives

Attach a display directive after the source expression:

| Directive | Output |
|---|---|
| `;%.2f` | Fixed decimal places, e.g. two decimals |
| `;dt` | Datetime |
| `;hm` | Hours and minutes |

Examples:

```markdown
<!-- TBLFM: @>=(@I / @3$4);%.2f -->
<!-- TBLFM: $5=($2 - $1);hm -->
```

Times may be datetimes such as `2023-07-12 10:00`, milliseconds since epoch, durations as `HH:MM`, or milliseconds.

## Strong Examples

Row totals and grand total:

```markdown
| Item            | Qty | Unit | Total |
| --------------- | --: | ---: | ----: |
| Notebook        |   2 | 3.50 |  7.00 |
| Pen             |   5 | 1.20 |  6.00 |
| **Grand Total** |     |      | 13.00 |
<!-- TBLFM: $>=($2*$3);%.2f -->
<!-- TBLFM: @>$>=sum(@I..@-1);%.2f -->
```

Time tracking with omitted starts and total duration:

```markdown
| Task        | Start |   End | Duration |
| ----------- | ----- | -----:| --------:|
| Plan day    | 09:00 | 09:15 |    00:15 |
| Fix Bug     | 09:27 | 11:33 |    02:06 |
| Follow-up   |       | 12:22 |    00:49 |
| **Total**   |       |       |    03:10 |
<!-- TBLFM: $>=($3 - if($2>0, $2, @-1$3));hm -->
<!-- TBLFM: @>$>=sum(@I..@-1);hm -->
```

## Troubleshooting

| Symptom | Check |
|---|---|
| Formula does not evaluate | Cursor is in table or formula line, formula comment is immediately below table, and comment uses exact `TBLFM` syntax |
| Parse error notice | Formula grammar, parenthesized algebra, compatible range endpoints, supported function names |
| Sort targets wrong column | Cursor must be in the column used for sorting |
| Tab/Enter conflicts | Disable `bindTab` or `bindEnter`, restart Obsidian, bind commands manually in Hotkeys |
| Mobile navigation missing | Use mobile toolbar commands or Advanced Tables toolbar |
| Live Preview keybinding conflict | Source avoids WYSIWYG table conflicts; use command palette/toolbar if keybindings do not fire |
| Formula sees wrong rows | Remember `@I` is first body row and `@>` includes the final row |
