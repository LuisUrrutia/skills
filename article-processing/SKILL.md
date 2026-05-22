---
name: article-processing
description: Process article URLs into hybrid archive/study Obsidian Articles notes with bilingual EN/ES output, UUIDv5 dedupe from the canonical article URL, browser-first extraction, Medium/Freedium paywall fallback, local attachments, and Articles.base-compatible frontmatter. Use when the user shares article links, including Medium or Freedium links, and wants structured notes saved under Articles with English and Spanish files.
---

# Article Processing

Convert article URLs into bilingual hybrid archive/study notes under the
Personal Obsidian vault's Articles layout.

## Scope

Use this skill for one or more web article URLs when the output should be saved
as English and Spanish markdown notes under:

`./Articles/{main_topic}/{english_article_title}/`

Do not use this skill for videos, podcasts, newsletters without article bodies,
or generic webpages with no article content.

## Core Rules

- Write only under the Personal Obsidian vault.
- Ask for the vault path if it cannot be found.
- Preserve compatibility with `Articles/Articles.base`.
- Use the source identity URL for UUIDv5 dedupe.
- Prefer a canonical URL only when confidently available.
- Never use a Freedium mirror URL as the source identity or `source` value.
- Check for duplicates before extracting article content.
- Extract with browser tooling first.
- Use Freedium only for Medium paywall or access fallback.
- Ask for pasted article content if extraction and valid fallbacks fail.
- Create exactly two article notes: one English and one Spanish.
- Preserve the article body and add a concise study layer before it.
- Download meaningful article images locally.
- Link only to local `attachments/` files.
- Remove `tmp_images/` before reporting completion.

## Ordered Workflow

Follow this order exactly:

1. Resolve the source identity URL.
2. Generate UUIDv5 from the source identity URL.
3. Search `./Articles` for an existing note with that UUID.
4. Extract the source article in the browser.
5. Use Freedium only when Medium blocks or truncates the article.
6. Ask for pasted content if extraction still fails.
7. Analyze content, metadata, tags, language, and article images.
8. Download all meaningful article images as local attachments.
9. Create English and Spanish notes with shared UUID and frontmatter.
10. Verify files, links, frontmatter, images, and Base compatibility.
11. Remove `tmp_images/`.

## References

Load these files before doing the corresponding work:

- [REFERENCE.md](REFERENCE.md): detailed processing rules.
- [TEMPLATES.md](TEMPLATES.md): frontmatter and note body templates.
- [QA.md](QA.md): completion checklist and regression cases.

## Completion Standard

Before reporting completion, run [QA.md](QA.md) and confirm:

- English and Spanish notes exist in the correct article folder.
- Both notes share the same UUIDv5 from the source identity URL.
- `source` is never a Freedium URL.
- English `spanish_file` exactly matches the Spanish filename.
- The Spanish note omits `spanish_file`.
- Tags are English, include `article`, exclude `en` and `es`.
- At least five relevant tags are present.
- All article image links point to local `attachments/` files.
- Missing or failed images are reported clearly.
