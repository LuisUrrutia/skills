# People Memory Templates

Use these templates exactly when they fit. Keep responses short.

## New Person Template

Use this shape for new profiles in `06 - People/`, following the vault-native convention from `Assets/Templates/t.people.md`.

````markdown
---
created: "[[{YYYY-MM-DD}]]"
aliases: []
tags: []
company:
role:
where_met: "{Context clue}"
last_contact: "[[{YYYY-MM-DD}]]"
phone:
email:
linkedin:
---

# Notes

___

- {YYYY-MM-DD}: {Initial useful relationship memory.}

```dataview
TABLE without ID
rows.file.link as "Files", rows.topic as "Topic", Date
FROM "Journal"
WHERE contains(people, link("{Full Name}")) OR contains(file.outlinks, link("{Full Name}"))
SORT dateformat(file.ctime, "yyyy-MM-dd") ASC
GROUP BY dateformat(file.ctime, "yyyy-MM") AS Date
```
````

## Optional Last Conversation Snippet

Add this only when the latest exchange is useful as a current summary.

```markdown
## Last conversation

- {YYYY-MM-DD}: {Brief note about the conversation or update.}
```

## Preserve Existing Profile Areas

Do not remove or rewrite these sections when updating an existing profile:

- `# Conversations`
- `# Next Check-ins`

## Disambiguation Question

```text
Which person do you mean?

1. {Full Name} ({short context})
2. {Full Name} ({short context})

Reply with the number or the full name.
```

## Contextual Unknown Question

```text
Who is "{contextual reference}"?

I need their full name and one context clue before I can create or update a People profile.
```

## Creation Data Question

```text
I can create a People profile for {Person}. What is their full name, and what is one context clue I should remember, such as how you know them, where you met, their role, or why they matter?
```

## Existing Field Overwrite Question

```text
{Full Name} already has {field}: {old value}. Should I replace it with {new value}?
```

## Mini-Diff Response

```text
Updated {Full Name}.

- Frontmatter: {field changes, or "no changes"}
- Notes: {new bullet summary, or "no changes"}
- Last conversation: {new entry summary, "not updated", or "not present"}
```

## No-Write Response

```text
No People profile write. This mention did not add new useful relationship memory.
```
