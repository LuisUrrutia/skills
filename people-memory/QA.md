# People Memory QA

Run these checks before reporting a write.

## Manual Checks

- Confirm the target file is under `06 - People/` in the Obsidian Personal vault.
- Confirm `.omo/` runtime state was not read for memory content and was not edited.
- Confirm no scripts were added.
- Confirm no unrelated files were touched.
- Confirm the write gate passed because there was new useful relationship memory or an explicit create or update request.
- Confirm ambiguous names were not written without user clarification.
- Confirm contextual references updated only when there was exactly one confident match.
- Confirm unknown contextual references asked who the person is.
- Confirm any clarified contextual person became a real profile, not a placeholder profile.
- Confirm new profile creation had a full name plus one context clue.
- Confirm company was not required for profile creation.

## Profile Checks

- Frontmatter remains valid YAML.
- Existing unknown frontmatter keys were preserved.
- Optional frontmatter keys such as `twitter`, `github`, `website`, and `instagram` were preserved.
- Existing image embeds were preserved.
- Existing Dataview blocks were preserved.
- Existing notes and conversation history were preserved.
- Existing `# Conversations` was preserved unless explicitly updated.
- Existing `# Next Check-ins` was preserved unless explicitly updated.
- `aliases` and `tags` were merged without case-insensitive duplicates.
- `last_contact` uses `[[YYYY-MM-DD]]` when updated.
- `# Notes` contains only useful durable memory.
- `## Last conversation` was added or updated only when useful, and was otherwise left absent or unchanged.

## Contact And Identity Checks

- Explicitly provided phone or email was saved when the field was empty.
- Existing `email`, `phone`, `linkedin`, or `company` was not overwritten without asking first.
- Confirmed overwrites were recorded with a short dated note.
- Conflicting historical context was preserved rather than deleted.

## Response Checks

- If a file changed, response includes the mini diff.
- If no file changed, response says no write was made.
- If clarification is needed, response asks one direct question and stops.
- Response does not expose unrelated profile contents.
