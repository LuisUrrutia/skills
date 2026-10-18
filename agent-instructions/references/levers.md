# Levers

Read this before writing or reviewing a pointer, a step or its completion
criterion, or where material sits, and before tightening or rewording existing
text. [The entrypoint's](../SKILL.md) Negation and Pruning sections apply here
too.

## Context pointers

A **context pointer** is a reference held in the agent's context that names some
out-of-context material and encodes the condition for reaching it. A skill's
description is one; a line in `AGENTS.md` naming a doc is the same object. The
pointer's _wording_, not its target, decides when the agent reaches the material,
and how reliably. A must-have target behind a weakly worded pointer is a variance
bug: sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches**
that should trigger reaching it (a branch is a distinct case the document
handles, so different runs take different paths through it). A pointer with no
condition, such as a bare "see references", names no branch. Every word of an
always-loaded pointer costs on every turn, so it earns even harder pruning than
the body:

- **Front-load the leading word**: the pointer is where it does its triggering
  work.
- **One trigger per branch.** Synonyms that rename a single branch are one branch
  written twice; collapse them and keep only genuinely distinct branches.
- **Cut identity the body already carries.** A pointer that summarizes the
  procedure becomes a shortcut: the agent follows the summary and skips the body.
  State when to reach the material, not how it works.

A pointer to another skill names it by its registered name, with the condition
that selects it and, when the pointer sends it work rather than reaching its
reference, the inputs it hands over and the completion evidence it returns;
never a file inside it, by path or by a description such as "its PR review
reference". That skill's entrypoint decides what it loads, and its procedure
stays in that skill. Use a resource its entrypoint documents for callers, such
as a validator, only through that documented contract. Links within the current
skill may address its own resources.

## The two loads

Every document and pointer you add spends one of two budgets:

- **Context load** is the cost of always-loaded material on the agent's window:
  an `AGENTS.md` line, a skill description, anything sitting in context every
  turn, spending tokens and attention whether or not it fires.
- **Cognitive load** is the cost on the human: which documents exist and when to
  reach for each. The human is the index. Not a cost to minimize: it is the price
  of human agency; spend it where human judgment matters, remove it where it does
  not.

Material reached only through a pointer escapes context load at the price of the
pointer's own line; material with no pointer at all rides entirely on cognitive
load.

## Information hierarchy

A document is built from two content types: **steps** (the ordered actions the
agent performs) and **reference** (definitions, rules, facts consulted on
demand). The two mix freely: all steps (a recipe), all reference (a review's
rules), or both, as this skill does. The core decision is where each piece sits
on the **information hierarchy**, a ladder ranked by how immediately the agent
needs the material:

1. **In-file step** is the primary tier: what the agent does, in order.
2. **In-file reference** is consulted on demand. Often a legitimately flat
   peer-set (every rule of a review on one rung), which is a fine arrangement,
   not a smell.
3. **Disclosed reference** is pushed out into a separate file, reached by a
   context pointer, loaded only when the pointer fires. Spans a sibling file in
   the same folder through fully external reference that lives anywhere and any
   document can point at.

Push too little down and the top bloats; push too much and you hide material the
agent actually needs. That tension is the whole decision.

**Progressive disclosure** is the move down the ladder (out of the main file and
behind a pointer) so the top stays legible. Not primarily a token optimization:
it is how the hierarchy is protected. Branching is the cleanest disclosure test:
inline what every branch needs, and push behind a pointer what only some
branches reach. A reference that every branch must read discloses nothing. When
a document has steps, in-file reference that should be disclosed buries them and
turns attending to them into a coin-flip: a variance lever, not just a
legibility one.

**Co-location** is the within-file companion: where the ladder decides _how far
down_ a piece sits, co-location decides _what sits beside it_ once there. Keep a
concept's definition, rules, and caveats under one heading rather than
scattered, so reading one part brings its neighbors with it. The test: the
document should read like documentation written for the agent. Grouped material
reads that way; scattered material does not. (Distinct from duplication: that
repeats one meaning in two places; scattering fragments one meaning across many.)

**Sprawl** is the failure mode here: a document simply too long, even when every
line is live and unique. Attention thins across the excess, and every extra line
is one more to keep relevant. The cure is the ladder: disclose reference behind
pointers, and split by branch or sequence so each path carries only what it
needs.

## Steps and completion criteria

Every step ends on a **completion criterion**, the condition that tells the agent
the work is done. Two properties make it a lever:

- **Clarity**: can the agent tell done from not-done? A vague bound
  ("understanding reached") invites **premature completion**: ending the step
  before it is genuinely done, attention slipping to _being done_. The visible
  steps still ahead (the **post-completion steps**) supply the pull; the
  criterion's clarity is the resistance. Defend in order: **sharpen the bound
  first** (local and cheap); only if it is irreducibly fuzzy _and_ you observe the
  rush, hide the later steps by splitting the sequence. Hiding only works across
  a real context boundary (a hand-off or a subagent dispatch; an inline call
  leaves the later steps in context and clears nothing).
- **Demand**: how much it requires. "Every modified model accounted for" forces
  thorough work where "produce a change list" does not. Demand drives
  **legwork** (the digging the agent does within the work, latent in the wording
  rather than written as its own step), and it is not step-bound: "every rule
  applied" binds a body of flat reference just as "every step done" binds a
  sequence, which is how an all-reference document still carries an
  exhaustiveness bar.

The strongest criteria are both checkable and exhaustive.

Match each step's freedom to its fragility. Keep a fixed sequence, or code, where
an operation is fragile or the order protects an invariant, such as an identity
check before a remote write; give work with several valid paths an outcome and
decision criteria instead of a ritual. A loop needs a progress signal, an end
condition and a response to a recurring blocker.

Name the next actor at every boundary. A phase loaded into the same conversation
is not a hand-off: an instruction there to "return to the caller" can only end
the turn, so state the next action where the same agent continues. Keep the real
boundaries as they are: a child agent's return, a user decision, and a pause
that the host resumes later.

## When to split

Splitting one document into two spends one of the two loads, so split only when
the cut earns it:

- **By sequence**: split a run of steps where the post-completion steps tempt the
  agent to rush the one in front of it. Keeping them out of view drives more
  legwork on the current task. Beware the reverse: merging sequences exposes each
  step's later steps to what follows, inviting premature completion.
- **By invocation**, skill-specific: see
  [skill-mechanics.md](skill-mechanics.md#splitting-by-invocation).

## Leading words

A **leading word** is a compact concept already living in the model's pretraining
that the agent thinks with while running the document (_lesson_, _fog of war_,
_tracer bullets_). Repeated as a token, never as a sentence, it accumulates a
distributed definition and anchors a whole region of behavior in the fewest
tokens, by recruiting priors the model already holds. Use only a word familiar in
its ordinary sense or as a standard term of the domain: a coined word recruits no
priors and costs its definition in tokens. Where the document narrows the word's
sense, define it once, and keep the same word wherever the concept recurs.

A leading word names a behavior; it never replaces the condition, obligation,
quantity or exception that governs it. "Run a _tight_ loop" still needs the
condition that selects the loop and the criterion that ends it.

It anchors twice. In the body, _execution_: the agent reaches for the same
behavior every time the word appears, and inside flat reference it focuses
attention on a class of thing to look for. In a pointer, _invocation_: when the
same word lives in your prompts, your docs, and your codebase, the agent links
that shared language to the material and reaches it more reliably.

Hunt for opportunities to refactor with leading words: a triad spelled out at
three sites, a pointer spending a sentence to gesture at one idea. Each is a
passage that can collapse into a single token:

- "fast, deterministic, low-overhead" → _tight_ (a _tight_ loop).
- "a loop you believe in" → _red_, when failing on the bug is the belief the
  author meant: a fuzzy gate becomes a binary observable state (the loop goes
  _red_ on the bug, or it doesn't). When the meaning is unclear, ask first.

You win twice: fewer tokens, and a sharper hook for the agent to hang its
thinking on. Assume every document carries restatements that a leading word can
retire, and look for them. A word too weak to beat the default is a no-op
([Pruning](../SKILL.md#pruning)), and steering by prohibition is its own failure
([Negation](../SKILL.md#negation)).
