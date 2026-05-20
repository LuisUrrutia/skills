# Article Processing Reference

## Vault Path

- Write only under the Personal Obsidian vault.
- Prefer `$HOME`-based paths.
- Linux default: `$HOME/obsidian/Personal`
- macOS example:
  `$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal`
- If the Personal vault cannot be found, ask the user for its location.
- Store outputs relative to the vault root:
  `./Articles/{main_topic}/{english_article_title}/`

## Source Identity And Duplicate Check

- Resolve the source identity URL before generating the UUID.
- Prefer the page's canonical URL when confidently available.
- Canonical sources include `link[rel="canonical"]` and stable metadata.
- If canonical metadata is missing or ambiguous, use the user-provided URL.
- Strip tracking parameters only when they cannot change article identity.
- Never use a Freedium mirror URL as the source identity.
- If the user-provided URL differs from source identity, keep `original_url`.
- Generate UUIDv5 from the source identity URL:
  `npx uuid v5 "<source_identity_url>" URL`
- Use the same UUID in English and Spanish notes.
- Treat the UUID as the canonical identity for dedupe.
- Search existing notes before content extraction:
  `rg 'uuid:\s*"?{generated_uuid}"?' ./Articles -g '*.md'`
- Match quoted and unquoted UUID values.
- If a match exists, stop and report the existing note path.

## Extraction Rules

- Use browser extraction first through the `agent-browser` skill.
- Extract the source page directly unless Medium blocks access.
- Detect Medium paywall or access indicators, including:
  - `Create an account to read`
  - `author made this story available to`
- Use Freedium only when Medium content is blocked or incomplete:
  `https://freedium-mirror.cfd/{original_url}`
- Do not use Freedium as the default for non-Medium URLs.
- Do not replace `source` with the Freedium URL in frontmatter.
- If browser extraction and valid Medium fallback fail, ask for pasted content.

## Site Extraction Hints

- Medium via Freedium:
  - Content: `document.querySelector("body > div.container > div")`
  - Title: `document.querySelector("h1")`
  - Author/date block:
    `document.querySelector("body > div.container > div > div:nth-child(2)")`
- Medium direct:
  - Content: first `<article>` element
- Dev.to:
  - Detect by `dev.to` domain or `meta[name="application-name"] == "dev.to"`
  - Content: `document.querySelector("#article-body")`
  - Title: `meta[property="og:title"]`
  - Author fields: `#article-show-container` data attributes
  - Date: `#main-title time`
- Other article sites:
  - Use the extracted main article body.
  - Ignore navigation, ads, comments, sidebars, footers, and widgets.

## Content And Language Rules

- Focus on the core article body.
- Keep enough source structure to preserve the argument and evidence.
- Add study summaries, key points, and section headings without inventing claims.
- Preserve technical terms, names, links, and code examples.
- If the source is English, create an English note and Spanish translation.
- If the source is Spanish, create a Spanish note and English translation.
- If the source is another language, create only English and Spanish notes.
- Translate directly with context awareness.
- Do not create an original-language note for non-English, non-Spanish sources.
- Write each note's study layer and preserved body in that note's language.

## Image Rules

- Include all meaningful images that belong to article content.
- Treat diagrams, screenshots, charts, code images, and inline examples as meaningful.
- Exclude nav images, ads, avatars, previews, tracking pixels, logos, and widgets.
- Detect article images from `<img>`, `<picture>`, `srcset`, CSS, and SVG.
- Choose the highest-quality article image source available.
- Build the complete article image list before downloading.
- Download images to temporary `tmp_images/` first.
- Try download tools in this order: `aria2c`, `wget`, `curl`.
- Retry failed images with the next tool.
- Move successful files to:
  `./Articles/{main_topic}/{english_article_title}/attachments/`
- Use short contextual English filenames.
- Force `.jpg` for JPEG images, never `.jpeg`.
- Keep appropriate non-JPEG extensions, such as `.png`, `.webp`, and `.svg`.
- Use local image links only:
  `![Alt text](attachments/{image_name}.{extension})`
- Do not hotlink remote article images in notes.

## Folder, Filename, And Tag Rules

### Main Topic

- Set `main_topic` as the first non-system tag.
- Exclude `article`, `en`, and `es` when choosing `main_topic`.
- Normalize `main_topic` to a lowercase slug.
- Replace `/` with `-`, such as `git/worktree` becoming `git-worktree`.

### Folder Structure

- Article folder: `./Articles/{main_topic}/{english_article_title}/`
- English note:
  `./Articles/{main_topic}/{english_article_title}/{english_article_title}.md`
- Spanish note:
  `./Articles/{main_topic}/{english_article_title}/{spanish_article_title}.md`
- Attachments: `./Articles/{main_topic}/{english_article_title}/attachments/`

### Filenames

- Use natural-language filenames with spaces.
- Preserve title text as much as practical.
- Do not use dash-separated slug filenames for notes.
- Replace invalid macOS filename characters:
  - `:` with `-`
  - `/` and `\` with `-`
  - `*` with `-`
  - `?` with nothing
  - `"` with `'`
  - `<` and `>` with `()`
  - `|` with `-`

### Tags

- Include at least 5 relevant tags.
- Write all tags in English.
- Include `article`.
- Use nested tags for specific concepts, such as `git/worktree` or `react/hooks`.
- Do not duplicate a parent tag when a nested tag already covers it.
- Do not include `en` or `es` tags.

## Output Contract

- Create two markdown notes per article, one English and one Spanish.
- Each note must include a faithful article body plus a study layer.
- Put the study layer before the preserved article body.
- Translate the preserved article body for the translated-language note.
- Use the same UUID in both notes.
- Use `language: "en"` for the English note.
- Use `language: "es"` for the Spanish note.
- Add `spanish_file: "{spanish_filename}.md"` to the English note.
- Omit `spanish_file` from the Spanish note.
- Make `spanish_file` exactly match the Spanish filename.
- Preserve spaces, capitalization, accents if present, and `.md`.
- Keep image links local and relative to the note folder.
- Keep attachments inside `attachments/`.
- Remove `tmp_images/` after moving successful downloads.
