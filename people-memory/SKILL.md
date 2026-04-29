---
name: people-memory
description: Maintain Obsidian `People` profiles as persistent relationship memory during any conversation. Use whenever a user mentions a person at any time (full name, alias, nickname, or contextual reference) or asks to update person data; find and match the profile by name/aliases, disambiguate multiple matches, request required details when no match exists, then update requested fields plus `# Notes`, `## Last conversation`, and `last_contact` in the matched file.
---

# Skill: people-memory

Maintain person profiles under the Obsidian Personal vault and keep relationship memory current.

Vault root for this workflow:

- Prefer `$HOME`-based paths.
- Linux default: `$HOME/obsidian/Personal`
- Current macOS setup example: `$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal`

Store person files in:

- `./People/`

Follow this exact processing order and do not reorder steps.

## Workflow

1. Person mention detection
2. Candidate matching with confidence score
3. Disambiguation or profile creation
4. Profile update with safe field rules
5. QA checks and response with mini diff

## 1) Person Mention Detection

- Detect when the user is referring to a person, including short names and nicknames.
- Also trigger when the user explicitly asks to update any field for a person profile (for example role, company, phone, where_met, aliases, or notes).
- Treat these as potential triggers:
  - Full name (`Aleksandr Pasevin`)
  - Alias/nickname (`Alek`)
  - Contextual references (`my manager`, `the founder I met last week`) when a name is still inferable from nearby text.

## 2) Candidate Matching With Confidence Score

- Search `./People/**/*.md` for matches using:
  - filename
  - `aliases` field
  - optional fallback fields if present (`name`, `full_name`)
- Normalize matching by trimming spaces and comparing case-insensitively.
- Score each candidate with this priority:
  - exact full name match: `1.00`
  - exact alias match: `0.90`
  - fuzzy name match (minor typo, spacing variation): `0.70`
  - contextual mention inference only: `0.55`
- Use threshold `0.80` for direct update without clarification.
- If top score is below `0.80`, ask clarifying question before writing.
- If top two scores are within `0.10`, treat as ambiguous and disambiguate.

## 3) Disambiguation or Profile Creation

If exactly one match exists:

- Use it and continue to profile update.
- If the user asked for direct profile edits, read the matched file first and update the requested fields in place.

If multiple matches exist:

- Ask the user exactly in this format:
  - `Are you talking about 1) {Full Name} from {Company} or 2) {Full Name} from {Company}?`
- Include all candidates in a numbered list with full name and company.
- Pause and wait for the user selection before writing.

If no matches exist:

- Ask for required creation inputs:
  - full name
  - where user met this person
  - company
- Create a new file in `./People/` after user reply.
- Use filename: `{Full Name}.md` (natural language filename).

## 4) Profile Update

Update the matched or newly created person file with:

- Relevant details from current conversation:
  - personal info
  - personal data
  - personal history
  - relationship context
  - useful follow-up details
- A dedicated section for conversation recency:
  - `## Last conversation`
  - Include concise date-stamped notes about what was discussed.
- A running notes area:
  - `# Notes`
  - Append new bullets instead of replacing prior context.
- Frontmatter updates aligned with existing People format:
  - `last_contact` as `[[YYYY-MM-DD]]`
  - set/update `role`, `company`, `where_met`, `phone`, `email`, `linkedin` when provided
  - set/update `aliases` when user provides new nicknames
- Direct update requests:
  - when user asks to "update" a person, prioritize requested field changes first
  - keep unchanged fields as-is

### Safe Update Rules Per Field

- Single-value fields (`company`, `role`, `where_met`, `phone`, `email`, `linkedin`):
  - replace value when user explicitly provides a new value
  - leave unchanged when user does not mention that field
- List fields (`aliases`, `tags`):
  - merge new values
  - dedupe case-insensitively while preserving preferred capitalization
- Chronological notes:
  - append new bullet to `# Notes`
  - prepend newest entry to `## Last conversation` with `YYYY-MM-DD`
  - update `last_contact` to `[[YYYY-MM-DD]]`

### Conflict Policy

- If a new value conflicts with existing profile data, prefer newest user-provided value.
- Log the replacement in `# Notes` with this format:
  - `Updated {field} from {old} -> {new} on {YYYY-MM-DD}`
- Do not remove historical notes describing prior context.

### Section Auto-Healing

- Before writing updates, ensure canonical structure exists.
- If missing, create:
  - frontmatter keys: `created`, `aliases`, `tags`, `role`, `where_met`, `phone`, `email`, `linkedin`, `company`, `last_contact`
  - `# Notes`
  - `## Last conversation`
- Preserve existing image embed and existing Dataview block.

Preserve existing content:

- Do not delete prior notes unless clearly obsolete and contradicted by user.
- Keep older conversation history and add the latest at top of `## Last conversation`.
- Preserve existing image embeds and Dataview blocks.

## 5) Response Back to User

After updating, return a no-silent-writes mini diff summary:

- include exactly what changed
- include where it changed (frontmatter key, `# Notes`, `## Last conversation`)
- include brief reason (user-provided update, inferred from latest conversation)

If no file write happened, say so explicitly.

Status outcomes:

- matched profile and updated notes, or
- disambiguation requested, or
- no match and creation data requested.

## QA Checklist

- Target file exists under `./People/`.
- Frontmatter remains valid YAML.
- Canonical frontmatter keys exist.
- `last_contact` is updated to latest conversation date.
- `aliases` has no duplicates (case-insensitive).
- `# Notes` exists and includes new entry when relevant.
- `## Last conversation` exists and newest entry is at top.
- Existing Dataview block is preserved.
- Existing image embed is preserved.

## Suggested Person Template

Use this for new files when no profile exists:

```markdown
---
created: "[[{YYYY-MM-DD}]]"
aliases:
  - "{Alias if any}"
tags: []
role: {Role or empty}
where_met: {Where user met this person}
phone: "{Phone or empty}"
email:
linkedin:
company: "{Company}"
last_contact: "[[{YYYY-MM-DD}]]"
---

![[{image_file_if_exists}| center portrait 256]]

# Notes
- {Initial relevant details}

## Last conversation
- {YYYY-MM-DD}: {What we last talked about}

```dataview
TABLE without ID
rows.file.link as "Files", rows.topic as "Topic", Date
FROM "Journal"
WHERE contains(people, link("{Full Name}")) OR contains(file.outlinks, link("{Full Name}"))
SORT dateformat(file.ctime, "yyyy-MM-dd") ASC
GROUP BY dateformat(file.ctime, "yyyy-MM") AS Date
```
```

If alias is unknown, keep `aliases: []`.
