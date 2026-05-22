---
name: people-memory
description: Maintains Obsidian Personal vault People profiles in `06 - People/` as persistent relationship memory during conversation. Use when any person is mentioned by full name, aliases, nicknames, or contextual references, or when the user asks to create or update a person profile.
---

# People Memory

## Purpose

Keep useful relationship memory in Obsidian People profiles without writing noise. This skill is a concise entry point, with detailed matching, prompts, and QA kept in the companion docs.

## Quick Start

1. Trigger on any person mention, including full names, aliases, nicknames, and contextual references such as `my manager`, `my cousin`, or `the founder I met last week`.
2. Load [REFERENCE.md](REFERENCE.md) before matching or updating.
3. Search existing profiles under `06 - People/` by filename, aliases, known names, and relevant context.
4. Decide whether the write gate passes before editing.
5. Use `Assets/Templates/t.people.md` as the source template convention for new profiles.
6. Load [QA.md](QA.md) before reporting completion after any write.

## Core Workflow

1. Detect the person mention or explicit create/update request.
2. Match the person using [REFERENCE.md](REFERENCE.md), including confidence and contextual reference rules.
3. If creation or a prompt is needed, use [TEMPLATES.md](TEMPLATES.md) for the exact profile shape and question wording.
4. Write only when allowed by the write gate.
5. Preserve existing profile structure and fields while making the smallest useful change.
6. Run the QA checklist before responding.

## Write Gate

Triggering is broad. Writing is narrow.

Write only when one of these is true:

- The user explicitly asks to create or update a person profile.
- The conversation adds new useful relationship memory, such as identity, contact details, role, company, alias, where-met context, preferences, commitments, follow-ups, or meaningful conversation notes.

Do not write when:

- The person is only mentioned in passing.
- The fact is already present in the matched profile.
- The information is vague, unresolved, or not useful as durable relationship memory.

## Ask Instead Of Writing

Ask one direct clarification question, then stop, when:

- A name, alias, or nickname matches multiple plausible profiles.
- A contextual reference does not resolve to exactly one confident person.
- Creation is requested but the full name or one context clue is missing.
- The update would overwrite an existing `email`, `phone`, `linkedin`, or `company` value.

## Output Contract

Return exactly one of these modes:

1. Mini diff after write: name the profile path and summarize only the fields or notes changed.
2. No-write response: say no write was made and give the short reason.
3. One clarification question and stop: ask only what is needed to proceed.

Do not expose unrelated profile contents.

Do not read `.omo/` runtime state for memory content, and do not edit `.omo/`.

## References

- Load [REFERENCE.md](REFERENCE.md) before matching, creating, or updating any profile.
- Load [TEMPLATES.md](TEMPLATES.md) when you need exact prompts, profile shape, or output wording.
- Load [QA.md](QA.md) before reporting completion after a write.
