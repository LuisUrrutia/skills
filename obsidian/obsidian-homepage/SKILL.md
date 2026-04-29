---
name: obsidian-homepage
description: Use when configuring, reviewing, or debugging Obsidian Homepage startup notes, dashboards, canvases, bases, workspaces, open modes, mobile homepage, Dataview refresh, or startup commands.
---

# Obsidian Homepage

## Overview

Homepage opens a configured note, canvas, base, workspace, graph, random note, periodic note, Journal entry, or nothing on startup and by command. Startup commands are automation and require review.

## Capabilities

- Startup homepage for notes, canvases, bases, workspaces, graph, random note, new note, Daily/Weekly/Monthly/Yearly notes, Journal, or none.
- Open modes such as keeping open notes, replacing last note, or replacing all tabs.
- Optional view mode, pinning, auto-scroll, auto-create missing notes, Dataview refresh, and command execution after opening.
- Separate mobile homepage configuration.

## Storage And Settings

- Plugin config: `.obsidian/plugins/homepage/data.json`.
- Settings are versioned and commonly include `homepages` and `separateMobile`.

## Safe Workflow

1. Prefer a normal Markdown dashboard as the homepage.
2. Use conservative open modes unless the user wants startup to replace tabs.
3. Avoid auto-create unless missing notes should be generated.
4. Treat command-on-open as executable automation.
5. Use separate mobile config when startup needs differ by device.

## Common Mistakes

- Using `replace all open notes` when users expect workspace restoration.
- Adding startup commands that mutate files or settings.
- Making mobile inherit a desktop-heavy dashboard.
- Assuming Dataview refresh solves broken metadata conventions.
