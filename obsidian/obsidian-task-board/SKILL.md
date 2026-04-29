---
name: obsidian-task-board
description: Use when configuring, reviewing, or debugging Obsidian Task Board boards, vault scans, task cache, task editing, task archiving, board filters, custom statuses, Tasks plugin integration, or Map View.
---

# Obsidian Task Board

## Overview

Task Board scans Markdown tasks and displays/edit them in centralized board views. Board actions update source Markdown files, so preserve task syntax and IDs.

## Capabilities

- Scan Markdown tasks across the vault.
- Display boards with filters, columns, custom statuses, and task modals.
- Add, edit, complete, delete, and archive tasks while updating source files.
- Support Tasks plugin-compatible task formats and metadata.
- Integrate with Tasks plugin statuses, QuickAdd, Daily Notes, Reminder, and other workflow plugins.
- Map View exists, but localStorage-backed state makes it riskier for shared workflows.

## Storage And Settings

- Plugin config: `.obsidian/plugins/task-board/data.json`.
- Task cache defaults to `.obsidian/plugins/task-board/tasks.json` unless configured otherwise.
- May use files such as task-board data, archived tasks, and a predefined task note depending on settings.
- Map View state uses localStorage keys for node positions, sizes, viewport, and file stack.

## Safe Workflow

1. Add and edit canonical tasks in Markdown when possible; let Task Board rescan/cache.
2. Preserve task status, dates, priority, IDs, dependencies, indentation, and metadata markers.
3. Use scan filters to exclude archives, templates, attachments, generated folders, and private areas.
4. Do not edit cache files directly.
5. Avoid Map View for shared canonical planning until localStorage limitations are acceptable.

## Common Mistakes

- Bulk rewriting task lines and dropping IDs/metadata.
- Treating `tasks.json` as source of truth.
- Scanning the entire vault without exclusions in large vaults.
- Depending on Map View state across devices/users.
