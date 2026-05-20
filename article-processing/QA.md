# Article Processing QA

Run this checklist before reporting completion.

## Files And Folders

- Article folder exists at `./Articles/{main_topic}/{english_article_title}/`.
- Article folder is under the Personal vault, not the current working directory.
- English note exists with a natural-language filename.
- Spanish note exists with a natural-language filename.
- Attachments, if any, exist under local `attachments/`.
- `tmp_images/` has been removed.

## Frontmatter

- English and Spanish notes share the same UUIDv5 from the source identity URL.
- `source` equals the source identity URL, never the Freedium URL.
- `original_url` is present only when the user-provided URL differs from `source`.
- `published` uses `YYYY-MM-DD` when a date is available.
- `language` is exactly `"en"` or `"es"`.
- English note has `spanish_file`.
- Spanish note does not have `spanish_file`.
- English `spanish_file` exactly matches the Spanish filename.
- Tags are English.
- Tags include `article`.
- Tags do not include `en` or `es`.
- At least 5 relevant tags are present.

## Content And Images

- Article body excludes page chrome, ads, comments, and unrelated widgets.
- Study layer appears before preserved article body.
- English and Spanish notes are complete and faithful to the source.
- All in-content image links point to local `attachments/` files.
- No remote image URLs remain in note content.
- Missing or failed images are reported clearly.

## Regression Cases

- Duplicate UUID stops processing before extraction.
- Canonical URL is used for UUID dedupe when confidently available.
- Medium direct extraction is tried before Freedium.
- Freedium is used only for Medium paywall or access fallback.
- Non-Medium URLs never default to Freedium.
- Failed extraction asks the user for pasted article content.
- Meaningful images are downloaded, renamed, linked, and moved out of `tmp_images/`.
