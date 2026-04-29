---
name: obsidian-omnisearch
description: Use when configuring, reviewing, or debugging Obsidian Omnisearch vault search, in-file search, indexing, excluded folders, OCR/document indexing, HTTP API, search cache, or result behavior.
---

# Obsidian Omnisearch

## Overview

Omnisearch provides fast ranked vault search and in-file search with typo tolerance, exclusions, filters, and optional document/OCR indexing through companion capabilities.

## Capabilities

- Cross-vault search and active-file search.
- Ranked search with typo resistance.
- Phrase search, exclusions, and file-type filters.
- Link insertion from results.
- Optional PDF, Office, image, and unsupported-file indexing when configured with supporting tools.
- Optional local HTTP API for integrations.

## Storage And Settings

- Plugin config: `.obsidian/plugins/omnisearch/data.json`.
- Search index/cache uses IndexedDB, commonly `omnisearch/cache/<appId>`.
- Search history also lives in local browser storage/IndexedDB, not Markdown.

## HTTP API Safety

- Keep HTTP API disabled unless explicitly needed.
- Never expose the host beyond `localhost` without a clear threat model.
- Treat `/search?q=...` as a local integration endpoint, not a public API.
- Avoid CORS/open-host settings in shared or synced vaults.

## Indexing Safety

- Only add plaintext extensions to custom indexed file types.
- Do not rely on OCR/document cache as canonical text.
- Expect search results to differ across devices depending on local cache and installed companion plugins.
- Respect Obsidian excluded files/folders when privacy matters.

## Common Mistakes

- Syncing expectations around an index that is local-only.
- Enabling HTTP API for convenience without checking host/CORS.
- Adding binary extensions to plaintext indexing.
- Treating search results as proof that content does not exist.
