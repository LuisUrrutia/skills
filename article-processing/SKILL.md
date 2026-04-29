---
name: article-processing
description: Process web article URLs into Obsidian-ready bilingual notes (EN/ES) with UUID-based deduplication, metadata frontmatter, local attachments, and Articles.base compatibility. Use when the user shares one or more article links and wants structured notes saved under Articles.
---

# Skill: article-processing

Convert article links into structured notes under the current vault layout.

Vault root for this workflow:

- Prefer `$HOME`-based paths.
- Linux default: `$HOME/obsidian/Personal`
- Current macOS setup example: `$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal`

Store outputs in:

- `./Articles/{main_topic}/{english_article_title}/`

Follow this exact processing order and do not reorder steps.

## Workflow

1. UUID generation
2. Duplicate check
3. Content extraction
4. Content analysis
5. Image download
6. Obsidian content creation
7. Base compatibility update
8. Cleanup

## 1) UUID Generation

- Generate UUIDv5 from article URL:
  - `npx uuid v5 "<article_url>" URL`
- Use the same UUID for English and Spanish notes.
- Treat UUID as canonical identity for deduplication.

## 2) Duplicate Check

- Search existing notes under `./Articles/**/*.md`:
  - `rg 'uuid:\s*"?{generated_uuid}"?' ./Articles -g '*.md'`
- Match both quoted and unquoted UUID values.
- If a match exists, stop and report the existing note path.

## 3) Content Extraction

Primary method:

- Use `agent-browser` skill to open and extract article content.
- Detect Medium paywall indicators such as:
  - `Create an account to read`
  - `author made this story available to`
- If paywall is detected, use Freedium mirror:
  - `https://freedium-mirror.cfd/<original_url>`

Fallback:

- If browser extraction fails, ask user for pasted article content.

## 4) Content Analysis

Detect source type and focus only on core article content:

- Medium via Freedium:
  - Content: `document.querySelector("body > div.container > div")`
  - Title: `document.querySelector("h1")`
  - Author/date block: `document.querySelector("body > div.container > div > div:nth-child(2)")`
- Medium direct:
  - Content: first `<article>` element
- Dev.to:
  - Detect by `dev.to` domain or `meta[name="application-name"] == "dev.to"`
  - Content: `document.querySelector("#article-body")`
  - Title: `meta[property="og:title"]`
  - Author fields from `#article-show-container` data attributes
  - Date from `#main-title time`
- Other sites:
  - Use extracted main article body.

Image analysis scope:

- Include only images that belong to article content.
- Ignore nav, ads, social widgets, and unrelated media.
- Handle `<img>`, `<picture>` (choose highest-quality source), CSS backgrounds, SVG references.
- Build a complete list of article images before downloading.

## 5) Image Download

Download order:

- Try `aria2c`, then `wget`, then `curl`.
- Download to temporary `tmp_images/` first.
- Retry failed images with the next tool.
- Move successful files to:
  - `./Articles/{main_topic}/{english_article_title}/attachments/`

Renaming rules:

- Use short contextual English names.
- Force `.jpg` extension for JPEG images (never `.jpeg`).
- Keep other extensions when appropriate (`.png`, `.webp`, `.svg`).

Reference rule:

- Use local links only:
  - `![Alt text](attachments/{image_name}.jpg)`

## 6) Obsidian Content Creation

### Main Topic Rules

- Set `main_topic` as the first non-system tag.
- Exclude `article`, `en`, `es`.
- Normalize to lowercase slug.
- Replace `/` with `-` (example: `git/worktree` -> `git-worktree`).

### Folder and File Structure

- Article folder:
  - `./Articles/{main_topic}/{english_article_title}/`
- English note:
  - `./Articles/{main_topic}/{english_article_title}/{english_article_title}.md`
- Spanish note:
  - `./Articles/{main_topic}/{english_article_title}/{spanish_article_title}.md`
- Attachments:
  - `./Articles/{main_topic}/{english_article_title}/attachments/`

### Language Rules

- If source is English: create English + Spanish notes.
- If source is Spanish: create Spanish + English notes.
- If source is another language: create only English + Spanish notes (do not keep original-language note).

### Filename Rules

- Preserve title text as much as possible.
- Use natural-language filenames (with spaces), not dash-separated slugs.
  - Example: `Como uso Claude Code 50 consejos practicos.md` (correct)
  - Not: `como-uso-claude-code-50-consejos-practicos.md`
- Replace invalid macOS filename chars:
  - `:` -> `-`
  - `/` and `\\` -> `-`
  - `*` -> `-`
  - `?` -> ``
  - `"` -> `'`
  - `<` and `>` -> `()`
  - `|` -> `-`

## 7) Base Compatibility Update

`Articles/Articles.base` depends on this:

- English note must include:
  - `spanish_file: "{spanish_filename}.md"`
- `spanish_file` must exactly match the Spanish filename.
- Keep `language: "en"` / `language: "es"` in frontmatter.
- Do not include `en` or `es` in tags.

## 8) Cleanup

- Remove temporary `tmp_images/` after files are moved.
- Verify files, links, frontmatter, and attachments are complete.

## Frontmatter Template

```markdown
---
uuid: "{uuid_v5_from_url}"
source: "{original_url}"
author: "{author_name}"
published: {YYYY-MM-DD}
category: "{main_category}"
language: "en"
spanish_file: "{spanish_filename}.md"
tags:
  - article
  - {language_or_tool}
  - {framework}
  - {broad_topic}
  - {nested_topic/subtopic}
---
```

Tag constraints:

- Minimum 5 relevant tags.
- All tags in English.
- Use nested tags for specific concepts (`git/worktree`, `react/hooks`).
- Do not duplicate parent tag when nested tag exists.

## QA Checklist

- Folder exists in `./Articles/{main_topic}/{english_article_title}/`.
- English and Spanish notes exist and share the same UUID.
- English note includes exact `spanish_file`.
- Frontmatter includes required fields.
- `published` is `YYYY-MM-DD`.
- Attachments exist under local `attachments/` folder.
- All in-content image links point to local attachments.
- At least 5 relevant English tags are present.
- Tags do not include `en` or `es`.
- `tmp_images/` is removed.
