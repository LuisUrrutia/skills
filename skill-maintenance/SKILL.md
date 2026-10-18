---
name: skill-maintenance
description: Use when creating or maintaining a skill's origin.toml to record its goal, sources and design decisions, or when checking or updating a skill from its recorded sources or dependencies.
---

# Skill maintenance

Keep each skill's `origin.toml` true to the skill: what the skill is for, the
decisions that shape it, and the outside material it builds on. The record lets a
later edit or update keep those decisions instead of guessing them.
`agent-instructions` owns writing and evaluating the skill's text; this skill owns
its record and its updates from recorded sources.

Read [references/origin-format.md](references/origin-format.md) before writing a
record. Then choose the task from the request:

- **Record:** a skill is created, or a change adds, removes or alters a rule, an
  adopted idea, a deviation from its base, or a dependency. `agent-instructions`
  hands these changes over; a user can also ask directly.
- **Dependents:** "which skills depend on this one" lists each record whose
  `dependencies` name it, as
  [List dependents](references/origin-format.md#list-dependents) describes.
- **Check:** "check this skill for updates" reports candidate changes from its
  sources and leaves the skill and its record unchanged.
- **Update:** "update this skill from its sources" incorporates compatible changes
  and records the review.

Using a skill never fetches its sources, and none of these tasks creates a
schedule.

## Record decisions

1. Read the skill, its record, and the change with the reason the user gave. A
   skill without a record gets one when the user asks or when its repository
   keeps records, that is, another skill in it has an `origin.toml`; skills
   installed in the host outside that repository do not count. The new record
   states the `approach`, a `goal` that says what the skill produces, for whom
   and what success looks like, and the invariants its text already enforces.
2. Write each decision once, as the entry a future editor needs:
   - A rule the user wants kept, such as a scope boundary, an authority limit or
     a host constraint: an invariant.
   - A correction to the base: a deviation.
   - A concept taken from a source: an idea. A donor behavior left out that a
     later update could propose again: a decline. Material from a source the
     record does not list yet first gets its own source or snapshot entry.
   - A skill or tool it calls or hands work to at runtime: a dependency.
3. Describe the decision, not the edit or how it was reached. A reader who never
   saw the conversation, the source or the diff must understand what the skill
   does and why; state the rule rather than copy the skill's text.
4. Update or remove the entries the change makes false, including `where`
   locations of renamed headings and moved files. Remove an invariant or a
   decline only on the user's decision or when its reason no longer holds.
5. When the change adds, replaces or removes a base deviation, judge whether the
   base [still fits](references/origin-format.md#choose-each-sources-role); when
   it does not, keep the approach, report the evidence and ask the user.
6. When the change alters the skill's name, existence, inputs, outputs or
   authority, list its dependents and report each whose role, decisions or text
   relies on the old contract, for `agent-instructions` to update.

Take commits, hashes and dates from the repository or file, never from memory.
Record only reasons the user stated or the evidence shows, and credit each to its
actual source. An invariant without a known reason leaves `reason` out; a
deviation or decline requires one, so ask the user when neither the request nor
the evidence supplies it. Keep review rounds and trial results out of the record,
and cite evidence from the change itself as
[Write the entries](references/origin-format.md#write-the-entries) describes. The
`goal` changes only on the user's statement, because every later decision is
judged against it. Wording fixes and corrections that keep the meaning need no
entry; Git history keeps them.

## Check or update from sources

Read [references/updates.md](references/updates.md). It covers both modes, the
review range of each source, installed dependencies, and when the review cursor
may advance. A partial run reports what stayed unresolved; it never claims the
skill is fully synchronized.

## Validate the record

After any edit to a record, and after headings or files move in a skill that has
one, run the checker described in
[Check the record](references/origin-format.md#check-the-record). Fix every
diagnostic. Then reread each new or changed entry as a newcomer to the source
and the conversation would.

Finish when the record matches the skill and the checker passes, or report the
diagnostics that remain. Commits and publication follow the active repository
rules and user authorization.
