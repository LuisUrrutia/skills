---
name: obsidian-editing-toolbar
description: Use when configuring, reviewing, or debugging Obsidian Editing Toolbar commands, toolbar layouts, custom commands, format brush, mobile toolbar, import/export, or AI editing features.
---

# Obsidian Editing Toolbar

## Overview

Editing Toolbar adds a rich editor toolbar with Markdown/HTML formatting commands, toolbar positions, command groups, custom commands, format brush, import/export, mobile layouts, and optional AI editing features.

## Capabilities

- Toolbar modes: top, following selection, fixed, and mobile.
- Built-in Markdown and some HTML formatting commands.
- Custom commands and submenus.
- Format brush for reapplying formatting.
- Import/export of toolbar configuration.
- Optional AI features for completion, rewrite, summarization, translation, and content generation.

## Storage And Settings

- Plugin config: `.obsidian/plugins/editing-toolbar/data.json`.
- Settings include command arrays, custom commands, toolbar appearance, mobile commands, format brush state, and AI settings.
- API keys/secrets may use Obsidian secret storage where supported; legacy configs can still contain sensitive values.

## Safety Rules

- Leave AI features disabled unless the user explicitly approves provider, data sharing, and scope.
- Do not share or commit `data.json` if it contains API keys or legacy custom model settings.
- Prefer portable Markdown commands over HTML insertion unless the vault accepts HTML.
- Export/import command subsets rather than overwriting all personal toolbar preferences.
- Treat selected text and current-file context as potentially sent to external AI providers when AI is enabled.

## Common Mistakes

- Enabling AI features without consent.
- Inserting HTML alignment/formatting into a Markdown-portability-focused vault.
- Overwriting another user's toolbar layout in a shared config.
- Forgetting mobile and desktop toolbar needs can differ.
