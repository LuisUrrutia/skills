---
name: youtube-processing
description: Process YouTube URLs into Obsidian-ready study notes with transcript reuse, local thumbnails, bilingual EN/ES summaries, and Personal/Youtube frontmatter compatibility. Use when the user shares one or more YouTube links and wants structured transcript plus summary notes saved to Obsidian.
---

# YouTube Processing

Convert YouTube videos into a complete Obsidian note set under the Personal vault: `transcript.md`, English summary, Spanish summary, and a local thumbnail.

## Scope And Output

- Use only for YouTube video URLs; do not use for articles, podcasts, generic webpages, or non-YouTube videos.
- Write only under the Personal Obsidian vault. Prefer `$HOME`-based paths: Linux `$HOME/obsidian/Personal`; macOS `$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal`.
- Ask for the vault path if the Personal vault cannot be found.
- Store outputs at `./Youtube/{main_topic}/{video_folder_title}/`.
- Required files: English summary, Spanish summary, `transcript.md`, and `attachments/{safe_video_id}.jpg`.

## Ordered Workflow

Follow this order exactly:

1. Extract canonical `video_id` from the URL.
2. Search `./Youtube/**/*.md` for an existing matching `video_id`.
3. Decide whether to reuse or refresh any existing `transcript.md`.
4. Download or read `transcript.md`.
5. Extract title, channel, duration, and upload date.
6. Download the best available thumbnail to local `attachments/`.
7. Choose `main_topic`, folder title, filenames, and English tags.
8. Create English and Spanish summary notes.
9. Verify folder structure, frontmatter, tags, local links, and Base compatibility.

## Identity And Duplicate Rules

- Parse `video_id` from common URL forms, including `watch?v=`, `youtu.be/`, and Shorts URLs.
- Treat `video_id` as the canonical identity.
- Search before downloading anything: `rg 'video_id:\s*"?{video_id}"?' ./Youtube -g '*.md'`.
- Match quoted and unquoted `video_id` values.
- If a matching video folder has `transcript.md`, ask exactly one question with these choices:
  - Override transcript and reprocess everything.
  - Reuse existing transcript and regenerate summaries only.
- If a matching summary exists but no transcript exists, download the transcript and reuse the existing folder when practical.

## Transcript And Thumbnail Rules

- Use `yt-dlp` or available YouTube transcript MCP/tooling for subtitle retrieval.
- If `$HOME/youtube_cookies.txt` exists, pass it to `yt-dlp` as `--cookies "$HOME/youtube_cookies.txt"`.
- Prefer English subtitles when available; otherwise prefer the video's original-language subtitles before any translated subtitle track.
- Save transcript text exactly as returned; do not rewrite, summarize, or translate it.
- Filename must be exactly `transcript.md`.
- Include transcript frontmatter with at least `video_id`, `channel`, and `original_video`.
- Save one thumbnail as `attachments/{safe_video_id}.jpg`.
- Build `safe_video_id` by replacing invalid filename characters (`:` `/` `\\` `*` `?` `"` `<` `>` `|`) with `-`.
- Try thumbnail URLs in order: `maxresdefault.jpg`, `hqdefault.jpg`, `mqdefault.jpg`, `default.jpg`.
- Use only local thumbnail links in notes; never hotlink YouTube image URLs.

## Folder, Filename, And Tag Rules

- Choose `main_topic` from the first meaningful non-system tag.
- Exclude `youtube`, `en`, and `es` when choosing `main_topic`.
- Normalize `main_topic` to a lowercase slug and replace `/` with `-`, such as `ai/agents` becoming `ai-agents`.
- Derive concise natural-language filenames from each summary's `Brief Summary`.
- Use spaces in filenames; do not use dash-separated slug filenames.
- Replace invalid macOS filename characters safely.
- Include at least five relevant English tags, including `youtube`.
- Do not include `en` or `es` tags.

## Summary Contract

- Create exactly two summary notes per video, one English and one Spanish.
- Use `language: "en"` for the English note and `language: "es"` for the Spanish note.
- Add `spanish_file: "{spanish_filename}.md"` to the English note only.
- Make `spanish_file` exactly match the Spanish filename, including spaces, capitalization, accents if present, and `.md`.
- Keep `thumbnail_file` exactly `attachments/{safe_video_id}.jpg`.
- Translate directly with context awareness; do not use external translation tools.
- If the transcript is not English or Spanish, translate summaries into English, Spanish, or both as needed while keeping the transcript unchanged.
- Preserve technical terms, proper nouns, links, and code examples.
- Do not invent claims, examples, or conclusions not supported by the transcript.

Each summary must include frontmatter for `original_video`, `channel`, `duration`, `upload_date`, `video_id`, `thumbnail_file`, `category`, `language`, and `tags`. The English note also includes `spanish_file`.

Each summary body must include the local thumbnail image, `## Brief Summary`, `## Key Points`, and `## Comprehensive Summary` with concept-focused section titles. Prioritize educational value for future study and keep key points to 15 bullets or fewer.

## Completion Standard

Before reporting completion, verify: folder and required files exist; required frontmatter is present; `upload_date` uses `YYYY-MM-DD` when available; `thumbnail_file` and all thumbnail links are local; English `spanish_file` exactly matches the Spanish filename; Spanish note omits `spanish_file`; tags are English, include `youtube`, exclude `en` and `es`, and include at least five relevant tags; transcript is faithful; summaries are complete, language-specific, and transcript-grounded; duplicate detection happened before download; existing transcript flow asked whether to override or reuse; failures are reported clearly.
