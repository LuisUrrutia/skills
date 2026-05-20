# Article Processing Templates

## Frontmatter Template

Use this frontmatter shape for the English note. Use the same required fields
for the Spanish note, but omit `spanish_file` from the Spanish note.

Omit `original_url` when it matches `source`.

```markdown
---
uuid: "{uuid_v5_from_source_identity_url}"
source: "{source_identity_url}"
original_url: "{user_provided_url_when_different_from_source}"
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

## Note Body Template

Use this body order for both English and Spanish notes:

```markdown
![{Primary image alt text}](attachments/{image_name}.{extension})

## Brief Summary

{One concise paragraph explaining the article's core idea.}

## Key Points

- {Important point 1}
- {Important point 2}
- {Important point 3}

## Study Notes

### {Concept-focused section title}

{Explain the idea, method, or argument in learning-oriented language while
staying faithful to the source.}

## Preserved Article Body

{Cleaned article body with source headings, links, images, code examples, and
important structure preserved.}
```

## Body Rules

- Keep the study layer concise and useful for later retrieval.
- Preserve the article body's argument, evidence, and technical details.
- Do not invent claims, examples, or conclusions not supported by the source.
- If no primary image exists, omit the opening image line.
