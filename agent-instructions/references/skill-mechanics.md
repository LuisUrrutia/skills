# Skill mechanics

The skill-specific branch of [the entrypoint](../SKILL.md): what changes when
the document is a skill (host metadata, the invocation choice, the description,
splitting by invocation, router skills, and the skill's record). Everything else
about writing it is the reference in `SKILL.md`; packaging and validation are in
[packaging.md](packaging.md).

## Host metadata

These skills run in Claude Code and Codex. `name` and a precise `description`
are the shared entrypoint; everything else is a host feature. Inspect the
intended host's installed skill format and current primary documentation when
local evidence is insufficient, and keep host-specific adapters apart from the
portable instructions. A frontmatter key is not portable merely because another
agent accepts it. Preserve supported existing metadata rather than rebuilding
the file. When the host supplies a creator
([packaging.md](packaging.md#host-tools-and-dependencies)), edit Codex's
`agents/openai.yaml` through it; a generator may replace the whole file, so keep
unrelated policy and dependency settings.

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill keeps a `description` the agent sees, so the agent
  can fire it autonomously, and other skills can reach it. You can still type its
  name: model-invocation always _includes_ user reach; a description only ever
  adds agent discovery, never removes the human's. The description is the
  skill's top-level context pointer, forced to stay loaded at all times:
  permanent context load in exchange for discoverability. A model-invoked skill
  whose content is all reference is also one home for shared reference: another
  skill can invoke it, so reference needed by several skills lives in one place.
- A **user-invoked** skill takes the description out of the agent's reach: only
  the human naming it can invoke it, and no other skill can. Zero context load,
  but it spends cognitive load: you are the index that must remember it exists.
  The `description` becomes human-facing: a one-line summary, trigger lists
  stripped.

Each host sets the choice with its own control. Verify each control's current
behavior on its host rather than copying one into the other:

| Host | User-invoked control |
| --- | --- |
| Claude Code | `disable-model-invocation: true` in the frontmatter |
| Codex | `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; an explicit `$name` mention still invokes the skill |

Keep an existing skill's invocation policy. A new skill stays model-invoked
unless the user chooses otherwise: changing invocation is a product decision,
separate from permission for a particular action, and skills here reach each
other by registered name. When a skill only ever fires by hand, propose user
invocation with its two-load trade and let the user decide.

Shared reference that two user-invoked skills both need can live in neither: with
both out of the agent's reach, neither can fire the other. It belongs in a
model-invoked reference skill, as above, not in a plain file outside the
packages, which a copied skill folder would lose.

## Description

The description is the skill's top-level context pointer, so the pointer rules in
[the entrypoint](../SKILL.md#context-pointers) apply in full. Make it the shortest
clear answer to when the skill should be used: the requested action and the
distinguishing context, so the name and description select the skill before its
body loads.

Name the capability instead of listing its subtasks. A skill covering inventory,
setup, status and job operations for build agents can say "Use when operating or
maintaining build agents"; the body keeps the subtask list. Procedures, concrete
examples, inventory facts, tool choices, deliverable details and feature lists
also belong in the body or references. Keep a qualifier or exclusion only when a
concrete intended request or a neighboring skill shows the selection ambiguity it
resolves.

For an existing skill, rewrite from its activation contract: check the requests
it should serve and the near misses it should not, rather than keeping every term
of the old description. Brevity must not widen or narrow activation. Read the
description beside its neighbors as one listing, because they are always loaded
together: check pairs that could claim the same request, and name the hand-off
and the distinct task that selects each owner without making every description
advertise the whole collection.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in
[the entrypoint](../SKILL.md#when-to-split)): split off a model-invoked skill when
you have a distinct leading word that should trigger it on its own (a trigger
word you actually use in your prompts), or another skill must reach it. You pay
context load for the new always-loaded description, so that independent reach
has to be worth it. Otherwise extend the existing owner or add a conditional
reference: a second skill with the same responsibility competes for the same
requests.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up
cognitive load is cured by a **router skill**: one user-invoked skill that names
the others and when to reach for each, so the human has one skill to remember
instead of many. It can only hint, never fire them: the agent cannot reach a
user-invoked skill, so nothing but the human can invoke one.

## Records

A repository keeps skill records when the target skill or another skill in it has
an `origin.toml`; skills installed in the host outside that repository do not
count. There, hand each new skill, and each change that adds, removes or alters a
rule, a source idea, a deviation from its base or a dependency, to
`skill-maintenance` with the user's reason; when `skill-maintenance` coordinates
the change, it records the result itself. After headings or files move in a skill
with a record, have `skill-maintenance` check the record. Elsewhere, create a
record only when the user asks.
