# Levers

## Context pointers

A **context pointer** names out-of-context material and when to read it: a skill
description or a line linking a guide. Its wording controls whether the agent
reaches the target. Sharpen a weak pointer first; inline required material only
if that fails.

- Front-load the leading word that triggers recognition.
- Use one trigger per distinct branch; collapse synonyms for the same branch.
- State when to read, not how to perform the procedure. A summary can become a
  shortcut that lets the agent skip the authoritative body.

Name another skill by its registered name and selecting condition. When handing
it work, specify inputs and completion evidence. Its entrypoint owns internal
routing: never point into its files or sections, even by description. Use an
exposed resource such as a validator only through its documented caller contract.
Links within this skill may address its own resources.

## The two loads

**Context load** spends tokens and attention on always-loaded material.
**Cognitive load** is the human effort of remembering what exists and when to use
it. Spend cognitive load where human judgment matters; remove it elsewhere.
Disclosed material costs its pointer until loaded; unlinked material relies
entirely on the human remembering it.

## Information hierarchy

Place material by how immediately the agent needs it:

1. **In-file steps:** ordered actions.
2. **In-file reference:** definitions, rules and facts consulted as needed. A flat
   set of peer rules is valid.
3. **Disclosed reference:** a separate document behind a conditional pointer.

Documents may use steps, reference or both. Inline what every branch needs;
disclose what only some branches use. Too little disclosure buries the workflow;
too much hides required guidance. A reference every branch reads discloses nothing.

**Co-location** keeps a concept's definition, rules and caveats under one heading.
Scattering fragments a meaning; duplication repeats it. **Sprawl** can persist
even with unique, relevant lines: split by branch or sequence so each path carries
what it needs.

## Steps and completion criteria

End every step with a completion criterion that distinguishes done from not-done
and demands all required work. "Every modified model accounted for" demands more
legwork than "produce a change list"; "every rule applied" can bind flat reference too.

Visible later steps can tempt premature completion. Sharpen the current bound
first. Only when it remains irreducibly fuzzy and rushing is observed, hide later
steps across a real context boundary, such as a handoff or child dispatch; an
inline call clears nothing.

Match freedom to fragility: fixed sequences or code protect order-sensitive
invariants; outcomes and decision criteria suit work with several valid paths.
Loops need progress signals, end conditions and a response to recurring blockers.

Name the next actor at boundaries. A phase in the same conversation continues
with its next action; "return to the caller" can instead end the turn. Preserve
real child returns, user decisions and host-resumed pauses.

## When to split

A split must earn its context or cognitive cost:

- **By sequence:** apply the [completion criterion](#steps-and-completion-criteria)
  conditions; merging sequences exposes later steps again.
- **By invocation:** use [skill mechanics](skill-mechanics.md#splitting-by-invocation).

## Leading words

A **leading word** recruits a familiar concept from the model's training, such as
"lesson" or "red". Repeat the term, not its definition. Use ordinary or established
domain vocabulary; coined terms need explanation and recruit no shared meaning.
Define a narrowed sense once and use it consistently.

The term anchors execution in the body and discovery in pointers shared with the
user's prompts and code. Look for repeated descriptions it can replace, while
preserving the governing condition, obligation, quantity and exception.

For example, "a loop you believe in" becomes "red" only if the intended meaning is
that it fails on the bug. When meaning is unclear, ask; a sharper word cannot
supply a missing requirement.
