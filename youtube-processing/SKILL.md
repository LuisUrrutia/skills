---
name: youtube-processing
description: Process YouTube URLs into Obsidian-ready notes by extracting canonical video IDs, handling transcript download/reuse, downloading the video thumbnail, generating bilingual (EN/ES) summaries, and organizing files under Personal/Youtube with frontmatter compatibility. Use when the user shares one or more YouTube links and wants structured transcript plus summary notes.
---

# YouTube Video Processing System

Vault root for this workflow:

- Prefer `$HOME`-based paths.
- Linux default: `$HOME/obsidian/Personal`
- Current macOS setup example: `$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal`

Convert a YouTube link into a structured note set: `transcript.md`, English
summary, Spanish summary, and local thumbnail image, all stored in an
Obsidian-compatible folder with stable metadata and filtering tags.

Follow this exact processing order and do not reorder steps.

## Workflow

1. Video ID extraction
2. Duplicate check
3. Transcript handling
4. Thumbnail attachment
5. Summary creation
6. Folder and file organization
7. Base compatibility update

## 1) Video ID Extraction

- Parse `video_id` from URL.
  - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ` -> `dQw4w9WgXcQ`
- Use `video_id` as canonical identity for duplicate detection.

## 2) Duplicate Check

- Search existing notes under `./Youtube/**/*.md`:
  - `rg 'video_id:\s*"?{video_id}"?' ./Youtube -g '*.md'`
- If a match exists, locate whether `transcript.md` already exists in that
  video folder.
- If transcript exists, ask user exactly:
  - Override transcript and reprocess everything, or
  - Reuse existing transcript and regenerate summaries only.
- If no match exists, continue with transcript download.

## 3) Transcript Handling

- Use `yt-dlp` MCP for subtitle/transcript retrieval.
- Language priority:
  1. English subtitles first
  2. Spanish subtitles fallback

Transcript rules:

- Save transcript exactly as returned (no rewriting).
- Filename must be exactly `transcript.md`.
- Include YAML frontmatter with at least:
  - `video_id`
  - `channel`
  - `original_video`

Also extract metadata for summaries:

- Title
- Channel
- Duration
- Upload date

## 4) Thumbnail Attachment

- Create `attachments/` inside the video folder if missing.
- Download and save a local thumbnail in `attachments/`.
- Preferred filename pattern: `{safe_video_id}.jpg`.
- Build `safe_video_id` from `video_id` by replacing filesystem-invalid
  characters (`:` `/` `\\` `*` `?` `"` `<` `>` `|`) with `-`.
- Try thumbnail URLs in this order until one succeeds:
  1. `https://img.youtube.com/vi/{video_id}/maxresdefault.jpg`
  2. `https://img.youtube.com/vi/{video_id}/hqdefault.jpg`
  3. `https://img.youtube.com/vi/{video_id}/mqdefault.jpg`
  4. `https://img.youtube.com/vi/{video_id}/default.jpg`
- Keep the thumbnail local (do not hotlink remote YouTube image URLs in notes).

## 5) Summary Creation

- If reusing existing transcript, read `transcript.md` from existing folder.
- Create bilingual summaries (English and Spanish) from transcript content.
- Translation constraints:
  - Do not use external translation tools.
  - Translate directly with context awareness.
  - Preserve technical terms, proper nouns, and code examples.

## 6) Folder and File Organization

### Main Topic Rules

- Set `main_topic` as first non-system tag.
- Exclude `youtube`, `en`, `es`.
- Normalize `main_topic` to lowercase slug.
- Replace `/` with `-` (example: `ai/agents` -> `ai-agents`).

### Folder Structure

- `./Youtube/{main_topic}/{video_folder_title}/`

### Title and Filename Rules

- Derive concise title from `Brief Summary`.
- Generate English title for English summary filename.
- Generate equivalent Spanish title for Spanish summary filename.
- Use natural-language filenames (with spaces), not dash-separated slugs.
  - Example: `Como uso Claude Code 50 consejos practicos.md` (correct)
  - Not: `como-uso-claude-code-50-consejos-practicos.md`
- Required files in each folder:
  - `{english_title}.md`
  - `{spanish_title}.md`
  - `transcript.md`
  - `attachments/{safe_video_id}.jpg`

## 7) Base Compatibility Update

In English summary frontmatter only:

- Add `spanish_file: "{spanish_filename}.md"`

Compatibility constraints:

- `spanish_file` must exactly match the Spanish filename.
- Keep transcript filename fixed as `transcript.md`.
- Keep thumbnail path fixed as `attachments/{safe_video_id}.jpg`.
- Do not include `en` or `es` in tags.
- Use `language: "en"` and `language: "es"` in frontmatter.

## Summary Template

```markdown
---
original_video: "{Video URL}"
channel: "{Channel Name}"
duration: "{Duration}"
upload_date: {YYYY-MM-DD}
video_id: "{Video ID}"
thumbnail_file: "attachments/{safe_video_id}.jpg"
category: "{Main Category}"
language: "en"
spanish_file: "{Spanish filename}.md"
tags:
  - youtube
  - {programming-language}
  - {tool}
  - {topic-specific}
  - {framework}
---

![Video Thumbnail](attachments/{safe_video_id}.jpg)

## Brief Summary
{One concise paragraph overview}

## Key Points
- {Important point 1}
- {Important point 2}

## Comprehensive Summary

### {Descriptive Section Title 1}
{Detailed explanation of what is being taught in this section}
```

## Comprehensive Summary Requirements

- Prioritize educational value for future study.
- Use descriptive section titles naming concepts or skills.
- Explain methods, techniques, and key insights.
- Keep key points to maximum 15 bullets.

## System Configuration

- Write markdown files directly to filesystem first.
- If direct write fails, fallback to Obsidian MCP functions.
- Report download or processing failures clearly.

## Final QA Checklist

- Video folder exists at expected path.
- Transcript exists as `transcript.md` (or explicit reuse path used).
- Thumbnail exists as `attachments/{safe_video_id}.jpg`.
- English and Spanish summary files exist with title-based names.
- English summary includes exact `spanish_file`.
- Required frontmatter fields are present in both summaries.
- `thumbnail_file` is present and equals `attachments/{safe_video_id}.jpg`.
- All tags are in English.
- Tags exclude `en` and `es`.
- At least 5 relevant tags are present.
- `upload_date` is formatted as `YYYY-MM-DD`.
- Brief summary, key points, and comprehensive summary are complete.
- Comprehensive summary uses clear, learning-oriented section titles.
- Markdown has no broken links or missing resources.
