---
name: obsidian-colored-tags
description: Use when configuring, reviewing, or debugging Obsidian Colored Tags palettes, tag color assignments, nested tag coloring, tag taxonomy, accessibility contrast, or tag-color expectations.
---

# Obsidian Colored Tags

## Overview

Colored Tags automatically colorizes Obsidian tags using palettes, optional per-tag assignments, nested tag blending, and contrast handling. Colors are presentation only, not durable metadata.

## Capabilities

- Auto-color known tags.
- Blend nested tag colors.
- Adjust text contrast for accessibility.
- Use built-in or custom palettes.
- Optional experimental per-tag palette assignments.

## Storage And Settings

- Plugin config: `.obsidian/plugins/colored-tags/data.json`.
- Important settings include `palette`, `mixColors`, `transition`, `accessibility`, `knownTags`, `tagColors`, and version fields.
- Known tags are derived from Obsidian metadata cache and plugin state.

## Safety Rules

- Add tags for semantic meaning, not merely for color.
- Do not assume a specific tag color is stable across updates, themes, or settings.
- Do not edit `knownTags` or `tagColors` directly unless explicitly working on plugin config.
- Describe workflows by tag name, not color.

## Common Mistakes

- Treating color as status or source of truth.
- Creating many near-duplicate tags for visual variations.
- Depending on exact colors in documentation.
