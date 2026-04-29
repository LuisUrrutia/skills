---
name: obsidian-style-settings
description: Use when creating, reviewing, or debugging Obsidian Style Settings CSS blocks, snippet controls, theme variables, class toggles, color settings, sliders, selects, or style-setting IDs.
---

# Obsidian Style Settings

## Overview

Style Settings reads YAML-like `/* @settings */` comments in CSS snippets, themes, and plugins, then exposes UI controls that write CSS variables or body classes.

## Settings Block Example

```css
/* @settings
name: Vault Tweaks
id: vault-tweaks
settings:
  - id: accent-color
    title: Accent color
    type: variable-color
    format: hex
    default: '#007AFF'
  - id: compact-mode
    title: Compact mode
    type: class-toggle
    addCommand: true
*/
```

## Common Control Types

- `variable-color`: color CSS variables.
- `variable-number`: numeric CSS variables.
- `variable-text`: text/string variables.
- `class-toggle`: toggles classes on `body`.
- `class-select`: selects one class from a list.
- headings and info blocks for organization.

## Storage And Settings

- Plugin config: `.obsidian/plugins/obsidian-style-settings/data.json`.
- Settings are keyed by section and setting IDs, often like `sectionId@@settingId`.
- CSS is discovered from enabled snippets, themes, and plugin styles.

## Safety Rules

- Keep `id` values stable; changing IDs loses existing user choices.
- Use globally unique IDs to avoid collisions.
- Prefer variables and class toggles over rewriting large CSS blocks.
- Do not use Style Settings as data storage; it is presentation configuration.
- Avoid unsafe CSS generated from untrusted user strings.

## Common Mistakes

- Renaming setting IDs after users configured them.
- Creating duplicate IDs across snippets/themes.
- Encoding semantic workflow state only as CSS classes.
- Adding too many controls instead of a small useful surface.
