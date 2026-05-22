# People Memory Reference

Use these rules after `SKILL.md` triggers. Keep writes small, factual, and useful.

## Vault And Scope

- Default vault root is the user's Obsidian Personal vault.
- Store people profiles in `06 - People/` under that vault.
- Use `Assets/Templates/t.people.md` as the source convention for new profiles.
- `People.base` currently exists, but do not treat it as authoritative if it filters `file.inFolder("People")`. Use `06 - People/` unless the user says otherwise.
- Do not edit `.omo/` runtime state.
- Do not add scripts unless the user asks for them.

## Mention Detection

Trigger on any person mention:

- Full name, such as `Aleksandr Pasevin`.
- Alias or nickname, such as `Alek`.
- Contextual reference, such as `my manager`, `my cousin`, `the founder I met last week`, or `the person from yesterday`.
- Explicit create or update requests for person data.

## Matching Rules

Search `06 - People/**/*.md` before writing. Match against:

- Filename.
- `aliases` frontmatter.
- Name fields if present, such as `name` or `full_name`.
- Existing notes, where-met details, role, company, and last conversation when context matters.

Normalize names by trimming spaces and comparing case-insensitively. Treat punctuation and repeated spaces as weak differences, not different people.

## Confidence Rules

Use these confidence bands:

- `1.00`: exact full name or filename match.
- `0.90`: exact alias or nickname match.
- `0.80`: strong contextual match with one clear candidate.
- `0.70`: fuzzy name match with a minor typo or spacing difference.
- `0.55`: contextual inference only.

Update without asking only when there is exactly one confident match at `0.80` or higher and no close competitor. If the top two candidates are close, ask the disambiguation question from `TEMPLATES.md`.

## Contextual Reference Rules

Contextual references can update a profile only when they resolve to exactly one confident match. If there is no confident match, ask who the person is. If there are multiple plausible matches, ask the user to choose.

Once the user clarifies a contextual person, create or update a real profile. Do not store lasting memory under a placeholder such as `my manager.md`.

## Creation Rules

Create a profile only after you have:

- Full name.
- One context clue, such as where the user met them, relationship to the user, role, event, project, or why they matter.

Company is optional. Do not require company for creation.

Use a natural filename: `{Full Name}.md`. If the user gives only a nickname or contextual reference, ask for the full name and one context clue before creating the file.

## Write Gate Rules

Write only when there is new useful relationship memory. Useful memory includes:

- Contact or identity fields.
- How the user knows the person.
- Relationship context, preferences, commitments, follow-ups, or personal details that may help future conversations.
- Corrections to existing profile data.

Do not write when the mention is incidental, already recorded, vague, or unresolved. In that case, report no write.

## Safe Update Rules

Read the matched file before changing it. Preserve the existing structure as much as possible.

Append new relationship memory to `# Notes`. Preserve `# Conversations` and `# Next Check-ins` exactly unless the user asks to update them or the current exchange clearly belongs there. Add or update `## Last conversation` only when it is useful for the profile, not as a universal requirement. Update `last_contact` to `[[YYYY-MM-DD]]` when a meaningful interaction or explicit update happened.

For list fields such as `aliases` and `tags`, merge new values and dedupe case-insensitively while keeping preferred capitalization.

For empty identity or contact fields, save explicitly provided values. This includes phone and email. If `email`, `phone`, `linkedin`, or `company` already has a value, ask before overwriting it. Treat these as identity or contact fields that need confirmation before replacement.

Preserve optional frontmatter keys such as `twitter`, `github`, `website`, and `instagram`. Keep any unknown frontmatter keys intact.

For other single-value fields, such as `role` and `where_met`, update only when the user clearly provides a correction or new value. If the replacement would conflict with existing profile data, ask unless the user explicitly framed it as a correction.

## Conflict Rules

Ask before overwriting existing `email`, `phone`, `linkedin`, or `company`. Use the conflict question from `TEMPLATES.md` or a similarly direct question.

If the user confirms a replacement, update the field and add a short note that records the change date and prior value. Do not erase older notes that mention the previous context.

If new information conflicts with historical notes, preserve the history and add the new dated note. Relationships change. The profile should show that change instead of pretending the older state never existed.

## Preservation Rules

Never delete existing notes, aliases, tags, image embeds, Dataview blocks, links, or custom sections unless the user specifically asks. Always preserve `# Conversations` and `# Next Check-ins` if present. Keep unknown frontmatter keys intact.

If required sections are missing, add only what is needed for the current write:

- Frontmatter if the file has none.
- `# Notes` for durable relationship memory.
- `## Last conversation` only when useful for recent conversation context.

Do not reorder a mature profile just to match the template. Preserve the user's formatting where it remains valid.
