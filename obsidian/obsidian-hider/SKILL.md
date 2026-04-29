---
name: obsidian-hider
description: Use when configuring, reviewing, or debugging Obsidian Hider UI visibility settings, hidden tabs, status bar, vault name, scrollbars, sidebar buttons, search counts, instructions, or properties.
---

# Obsidian Hider

## Overview

Hider hides Obsidian UI elements by toggling body classes and CSS. It does not manage note content; its main risk is making Obsidian harder to use or recover.

## Capabilities

- Hide tab bar, status bar, vault/profile name, scrollbars, sidebar buttons, tooltips, file explorer buttons, search suggestions/counts, prompt instructions, and properties in Reading view.
- Provides commands to toggle tab bar and status bar.

## Storage And Settings

- Plugin config: `.obsidian/plugins/obsidian-hider/data.json`.
- Settings are mostly boolean toggles.
- CSS works through classes such as `hider-status`, `hider-tabs`, and related body classes.

## Safety Rules

- Avoid hiding settings/profile/vault switcher affordances in shared or beginner vaults.
- Document alternate hotkeys if hiding visible controls.
- Keep file explorer buttons visible when users need create/rename/move workflows.
- Do not treat hidden UI as access control; it is visual only.

## Common Mistakes

- Making Obsidian appear broken by hiding core navigation.
- Hiding search counts or suggestions when search interpretation matters.
- Assuming Hider changes data or permissions.
