# Skill mechanics

## Host metadata

These skills support Claude Code and Codex. `name` and a precise `description`
are shared; other metadata is host-specific. Inspect the installed format and,
when insufficient, current primary documentation. Keep adapters separate and
preserve supported metadata: acceptance by one host does not establish portability.

For Codex's `agents/openai.yaml`, use the host creator as
[packaging](packaging.md#host-tools-and-dependencies) directs. Generators may replace
the file; preserve unrelated policy and dependencies.

## Invocation

- **Model-invoked:** an always-loaded description enables automatic discovery,
  explicit human invocation and access from other skills. Shared reference can
  have one home in such a skill.
- **User-invoked:** replace trigger lists with a short capability summary. Report that
  agents and other skills cannot invoke it; the human remembers when to use it.

Verify each host's control rather than copying between hosts:

| Host | Explicit-only control |
| --- | --- |
| Claude Code | `disable-model-invocation: true` in frontmatter |
| Codex | `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; explicit `$name` still invokes it |

Preserve existing policy. New skills stay model-invoked unless the user chooses
otherwise. If a skill is only used manually, propose the context/discoverability
tradeoff; invocation policy is separate from permission to act.

Reference shared by two user-invoked skills belongs in a reachable model-invoked
reference skill, not either unreachable skill or a file lost when packages are
copied.

## Description

Apply [pointer rules](levers.md#context-pointers): the shortest clear statement of
the action and distinguishing context that select this skill. Name the capability,
not its subtasks. Keep procedures, examples, inventory, tools and feature lists
in the body or references. Retain qualifiers only to resolve demonstrated
selection ambiguity.

Rewrite from intended requests and near misses; preserve activation scope. Read
the description beside neighboring descriptions, checking competing claims and
naming each owner's distinct task and handoff without advertising the collection.

## Splitting by invocation

Split when a distinct leading word used in actual prompts warrants independent
invocation, or another skill must reach the capability. Otherwise extend the
existing owner or add a conditional reference; a competing skill spends context
without adding ownership.

## Router skills

When remembering user-invoked skills becomes burdensome, a user-invoked router
can list when to use each. It can suggest them, not invoke them for the human.
