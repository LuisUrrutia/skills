---
name: agent-instructions
description: Use when writing or reviewing AI agent instructions or skills. Excludes following instructions and factual updates that leave guidance unchanged.
---

# Agent instructions

Write and review what an agent consumes as instructions: a skill, a persistent
instruction file such as `AGENTS.md` or `CLAUDE.md`, an agent prompt or brief, and
a document one of them points to. The packaging differs; the writing does not: the
same levers make each one predictable, since the agent takes the same _process_
every run rather than producing the same output. A request can define a new
capability; prior use or repetition is not a prerequisite.

Reading or following instructions does not start this skill, and a factual update
qualifies only when it changes agent guidance or instruction loading. `handoff`
owns handoff documents; this skill covers the continuation guidance inside them.
Implementation plans, tickets and human-facing documentation keep their own
owners even when an agent reads them.

When a skill request draws on completed work or conversation history, start with
`workflow-to-skill` to extract the contract, even if the user names no authoring
skill. `create-project-instructions` owns investigating a project's code and
knowledge sources for its instruction contract. Write directly from either
skill's evidence handoff, or from a fully supplied capability, without sending it
back through discovery. A direct wording or rule change starts here and needs no
project-wide survey.

`skill-maintenance` owns each skill's `origin.toml` record and its checks and
updates from recorded sources or installed dependencies; send those requests
there. An update hands the text it incorporates to this skill for writing and
evaluation. Ordinary writing never starts an upstream check.

Load the branch the target needs:

- **Skill:** read [references/skill-mechanics.md](references/skill-mechanics.md)
  for host metadata, invocation, the description, splitting, router skills and
  the skill's record, and [references/packaging.md](references/packaging.md)
  before creating a package, adding or moving its files or helpers, or
  validating it.
- **Persistent instruction file:** read
  [references/instruction-files.md](references/instruction-files.md) to find the
  canonical source and the scope where the rule belongs.
- **Standardizing a capability or adopting an external skill:** read
  [references/reuse.md](references/reuse.md) before writing an implementation.
- **Agent prompt or referenced guide:** this file suffices; keep its caller's
  inputs, output contract and loading condition.

## Establish meaning and scope

Read the complete target and enough surrounding instructions, imports, references
and repository context to know its authority and callers. From the user's current
request, establish:

- What the agent should do differently, and which existing meaning must survive.
- Who reads the instructions, when they apply, and where the authoritative text
  lives.
- Conditions, exceptions, permissions and the evidence of completion.
- Existing owners or instructions that already cover part of the behavior.
- Which statements are observed behavior, approved policy, team preference or a
  proposed change, and what establishes their authority and scope.

Make type, quantity, depth and completion evidence explicit where they separate
plausible requests. "Create tests" leaves open the behavior or risk, the test
level, the scope, whether to write or also run them, and how much coverage
suffices; available tooling does not choose the objective. Resolve schemas,
rounding, rules for discarding records and similar domain decisions from an
authoritative contract, and tell the future agent where that contract lives and
when to ask. An invented default labeled as an assumption still gets used.

Where guidance overlaps, such as donor drafts, an adapter and its source, or two
skills, compare trigger, owner, action, completion evidence and authority:
similar prose can hide a read-only review beside an automatic repair. Resolve a
conflict from established authority, scope or an explicit user decision, then
keep the governing rule or state distinct conditions. Popularity does not justify
replacing a local rule; check changes to invocation, approvals, testing, tools
and external writes with extra care.

Use accessible evidence before asking. When the objective, or the meaning needed
to express it, stays uncertain, ask the user: state the plausible interpretations
and how each changes the result. Pause the drafting or execution that depends on
the answer, and continue only work that no answer could invalidate. Ask only what
the user has not settled. Routine wording choices that keep the same intent need
no question, and precise-sounding wording never stands in for a requirement the
user did not give.

A review-only request returns findings and proposed corrections with evidence and
leaves the source unchanged. Any other request edits within its scope, sized to
it: a one-line change stays one line and needs no new skill, evaluation suite or
interview about repeated work.

Done when the intended behavior can be stated without contradiction, invented
rules, or an open question that the wording depends on.

## Write

Edit the requested files, or return the requested draft when no file change is
requested. Apply every section from [Context pointers](#context-pointers) through
[Pruning](#pruning) to each changed line; when the change answers an observed
failure, start from [Fix an observed failure](#fix-an-observed-failure). Examples
and source documents are evidence for the rewrite, not operations to run while
authoring.

Done when each changed line passes every section and sits in the scope the
request established.

## Get both model perspectives

When the user explicitly asks for instruction creation, editing or review within
this skill's scope, alone or inside a larger task, get independent reviews from
both profiles before finalizing the instructions or the review findings:

| Provider | Model | Reasoning effort |
| --- | --- | --- |
| Codex | Astra | xhigh |
| Claude | Fable | xhigh |

These do not start the pair:

- Instruction work that an agent takes on by its own decision within a larger
  task.
- An agent's review of its own changes, inline or through a subagent, even when
  the user requested those changes, unless the user asks for that review. A
  user-requested edit still keeps the pair it requires.
- A handoff document. Writing, updating or reviewing one never starts the pair,
  even when this skill supplies its continuation guidance.

The agent that receives the user's request runs the pair, unless it delegates the
work with a brief that relays that request and assigns the pair to the delegate;
every such brief states who runs the pair. An agent working from another agent's
brief runs the pair only when that brief both relays the user's request and
assigns the pair to it. A quoted user request alone does not assign it.

Before requesting either review, read
[references/model-pair.md](references/model-pair.md) for runner resolution, the
briefs, rate limits and other failures, and reconciliation.

The pair is complete when at least one profile completed every review round,
each profile not skipped for a rate or usage limit reviewed the instructions in
their final meaning (for a review-only request, the unchanged target; a later
edit that keeps the reviewed meaning needs no new round), and each material
finding is adopted or rejected with a reason. Until then, keep the result
provisional and report the exact blocker.

## Verify the change

Compare the revision with the intended meaning: actors, actions, scope,
conditions, exceptions, obligation, quantity, authority and completion evidence.
Check that pointers and imports resolve and that unrelated content survives.

For substantive behavior changes, new or combined skills, routing changes,
incorporated upstream changes or observed failures, read
[references/evaluation.md](references/evaluation.md) and run the behavioral
checks it calls for. A narrow wording correction needs only this fidelity check.
Use host validators only for the formats they validate. The pair's reviews
assess the text; they are not behavioral evidence.

Done when the requested result passes its applicable checks and each claim the
report makes has its evidence or is labeled as not tested. A required check that
fails or cannot run leaves the result unfinished, and the report says so.

## Report

Report the changed instructions and their scope, the checks actually run with
their results, and any unresolved limitation. Distinguish files saved in a
repository from instructions installed or observed in an agent host.

When this agent ran the pair or assigned it to a delegate, report each profile's
actual provider, model and effort, its run, rate-limit skip or blocker, and how
each material finding was reconciled. Otherwise, state that this agent did not
run the pair.

For a skill, report whether its record changed or that its repository keeps
none.

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
branches reach. When a document has steps, in-file reference that should be
disclosed buries them and turns attending to them into a coin-flip: a variance
lever, not just a legibility one.

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
  [references/skill-mechanics.md](references/skill-mechanics.md#splitting-by-invocation).

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
retire, and look for them.

**Negation** is the failure mode beside this lever: steering by prohibition
drags the forbidden behavior into context and makes it _more_ available, not
less. _Don't think of an elephant_, and the elephant is all there is; the
negation is a weak modifier the strongly activated concept overruns, so the ban
half-reads as an instruction to do the thing. Prompt the **positive**: state the
target behavior ("write one-line comments") so the banned one is never spoken. A
blanket prohibition also carries **harmful precision**: wrong on one plausible
task in ten, it is still obeyed on that task. A prohibition earns its place only
as a hard guardrail you cannot phrase positively: safety, data loss, a format
contract, or a shortcut that agents were observed to take under pressure after
understanding the rule. Even then, name the observed shortcut rather than a
hypothetical one, and pair the prohibition with the positive target so attention
lands on what to do.

## Pruning

- Keep each meaning in a **single source of truth**: one authoritative place, so
  changing the behavior is a one-place edit. **Duplication** (the same meaning in
  more than one place) costs maintenance and tokens, and inflates a meaning's
  prominence on the ladder past its real rank. (The accidental inverse of a
  leading word, which repeats a token on purpose, never the meaning.)
- The **environment** is a source of truth too (`package.json` scripts, config
  files, the directory layout, `--help` output), and a document that restates it
  is a **cache**: a copy of a lookup, earning its load only when the lookup is
  expensive. Cache what the agent cannot find by looking: the unwritten
  convention, the reason behind a choice, the gotcha no config confesses. Leave
  the one-file, one-command lookups to the environment, where they cannot go
  stale.
- Check every line for **relevance**: does it still bear on what the document
  does? A line loses relevance by never bearing on the task (mere exposition, or
  a branch that should be disclosed) or by going stale as the behavior or world
  it describes changes. Shorter documents are easier to keep relevant. Without a
  pruning discipline the default fate is **sediment**: stale layers that settle
  because adding feels safe and removing feels risky, until you must core down
  through them to find what is still live. So new guidance goes into its existing
  home: revise, combine or replace the passages it touches, and rewrite the
  section when coherence needs it. Add separate text only for a distinct decision
  with no home.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by
  default pays load to say nothing. The test (does it change behavior versus the
  default?) is model-relative, not reader-relative: two people disagreeing about
  a no-op disagree about the default, and settle it by running the document, not
  by debate. When a sentence fails, delete the whole sentence rather than trim
  words from it. The test also grades leading words: a word too weak to beat the
  default (_be thorough_ when the agent is already thorough-ish) is a no-op, and
  the fix is a stronger word (_relentless_), not a different technique.
- Grade a line by what it supplies before cutting it. Generic competence the
  model already has is a no-op. Host behavior belongs in that host's adapter.
  Team policy and preferences stay, in one home, even when they differ from the
  model's default; code and tests show behavior without establishing intended
  policy. An operational contract or an observed failure keeps the minimum that
  holds it. A volatile fact points to its current source.
- Pruning keeps **force**. Compression keeps actors, actions, scope, conditions,
  exceptions, obligation strength, quantity, authority and completion evidence:
  "prefer" stays "prefer", "create" does not become "run", a suggestion does not
  become a universal rule, a read does not become a write, and an attempted
  check does not become a successful one. Before deleting a rule as enforced
  elsewhere, inspect the actual configuration, execution path and coverage;
  brevity, a donor's score or a model's apparent knowledge cannot establish
  redundancy. Keep rare consequential constraints.

## Fix an observed failure

Name the failure mode first, then fix that. Inspect the output and the action
trace before adding a rule, and check loading evidence: an instruction the agent
never read needs a pointer or placement fix, not stronger wording. When loading
is unobserved, report that limit while correcting the defects visible in the
text.

| Observed failure | Lever |
| --- | --- |
| Material never reached | Sharpen the pointer; inline the material only if sharpening fails. |
| Wrong structure or order | State the required parts in the order the reader needs them. |
| Missing required element | Give it a slot in the existing output structure. |
| Rule applied in the wrong circumstances | State the observable condition and action for each branch. |
| Step ended before its work was done | Sharpen its completion criterion; split the sequence only across a real context boundary. |
| Authorized work stopped at a phase boundary | Trace the next actor and continuation path, then state the next action where the same agent continues. |
| Understood rule bypassed under pressure | Name the observed shortcut in a guardrail paired with the positive target, and test it under that pressure. |
| A line changed nothing | Delete the whole sentence, or replace a weak word with a stronger one. |

Keep material exceptions as explicit conditions, and counter only observed
workarounds. A pause is not itself a failure; repair the observed transition
without widening authorization or making required work optional.
