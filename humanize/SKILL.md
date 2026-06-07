---
name: humanize
description: Remove AI-writing tells while preserving meaning, facts, citations, and the author's voice. Use when the user asks to humanize text, de-AI writing, make prose sound less robotic or less like ChatGPT, review prose for AI patterns, rewrite drafts in a natural voice, or edit a file so it reads like a specific person wrote it.
---

# Humanize

Make text sound like a real person wrote it. Do not dumb it down, inflate it, or swap one kind of fake voice for another.

## Quick start

1. Read the full text before editing.
2. Identify clusters of AI tells, not isolated false positives.
3. Rewrite the affected passages while preserving meaning, facts, names, numbers, citations, and useful structure. In rewrite mode, confirmed AI tells are output constraints: do not recreate them in cleaner prose.
4. Match the author's voice. If the user provides a writing sample, mirror its rhythm, vocabulary, punctuation habits, and level of formality.
5. Read the result aloud. If it sounds like a press release, chatbot reply, SEO article, or polished committee memo, revise again.

## Modes

- `rewrite`: return the humanized text. This is the default.
- `review`: flag passages that sound AI-written, explain the pattern, and suggest fixes without rewriting everything.
- `edit`: when the user gives a file path and asks for in-place changes, read the file, make targeted edits, and preserve unrelated content.

Ask one brief question only when voice, audience, or format would materially change the rewrite. If the user says "just make it human," use a clear, direct voice and proceed.

For comprehensive AI-pattern detection, audits, or disputed false positives, use [REFERENCE.md](REFERENCE.md). It covers language, grammar, structure, formatting, chatbot residue, context contamination, academic, social, density, rhythm, multilingual, emerging artifacts, and false-positive guardrails.

## Core workflow

### 1. Calibrate voice

- Preserve the register the context needs: academic, technical, casual, professional, warm, blunt, or personal.
- Add personality only when the content supports it. Blog posts, essays, LinkedIn posts, and emails can have opinions and texture. Reference docs, legal text, academic prose, and API docs should stay plain and precise.
- Keep the author's intelligence level. Human does not mean simplistic.

### 2. Find pattern clusters

Treat stacked signals as one strong finding. Do not pad the review by listing the same phrase under five labels.

Common AI tells:

- Significance inflation: "pivotal," "testament," "plays a crucial role," "reflects broader trends."
- Promotional language: "vibrant," "renowned," "breathtaking," "seamless," "groundbreaking."
- AI vocabulary clusters: "delve," "tapestry," "landscape," "realm," "robust," "leverage," "underscore," "foster," "comprehensive."
- Superficial `-ing` clauses: "highlighting," "showcasing," "underscoring," "reflecting," "ensuring."
- Vague authority: "experts say," "industry reports," "some critics argue" without a named source.
- Formulaic structure: repeated section shapes, neat takeaway endings, forced "challenges and future prospects" sections.
- Grammar tics: copula avoidance (`serves as`, `boasts`, `features` where `is` or `has` is clearer), negative parallelism, false "from X to Y" ranges, synonym cycling.
- Style tells: metronomic sentence length, too many em dashes, bolded inline headers, emoji decoration, title-case headings in plain prose, overformatted lists.
- Chatbot residue: "Great question," "I hope this helps," "Let me know," cutoff disclaimers, reasoning-chain artifacts, placeholder text, leaked citation markup, AI-tool UTM parameters.
- Low information density: sentences that restate the previous sentence without adding facts, examples, stakes, or useful nuance.

Do not over-flag normal human choices. One em dash, one transition word, title case under a style guide, or formal vocabulary in academic writing is not enough. Look for density and interaction. Formal, academic, technical, multilingual, and house-style prose is not automatically AI-written. This false-positive guardrail protects source text; it does not permit adding those tells in rewrite mode.

### 3. Rewrite with substance

- Replace puffery with concrete facts.
- Use simple verbs when they are clearer: `is`, `has`, `does`, `uses`, `shows`.
- Name the source or cut the vague claim.
- Break forced triads. Keep the natural number of items.
- Repeat the clearest noun when repetition helps. Do not synonym-cycle.
- Vary rhythm with short, medium, and longer sentences. Let some paragraphs stop without a tidy moral.
- Treat confirmed AI tells as rewrite bans for generated wording. Do not recreate dash-heavy phrasing, decorative formatting, chatbot transitions, forced section shapes, synonym cycling, or other patterns you just diagnosed.
- Do not introduce em dashes unless preserving quoted/source text or matching a provided writing sample, house style, or explicit user preference. When a dashy or over-polished sentence needs repair, reconnect the ideas with sentence craft: subordinate clauses, conjunctions, commas, colons, semicolons when natural, reordered clauses, or paragraph flow. Do not fix em dashes by chopping every connection into isolated period-separated sentences.
- Use contractions, first person, asides, humor, or sharper opinions only when they fit the audience and source voice.
- Keep citations, code blocks, data, technical terms, and quoted text intact unless the user asks otherwise.

## Output

For rewrites, return the revised text first. Add a short `Changes` section only when useful or requested.

For reviews, use this compact format:

```md
### AI-writing tells

| Passage | Pattern | Suggested fix |
|-|-|-|
| "..." | Significance inflation + vague authority | Replace with a specific source or delete the claim. |
```

For file edits, summarize the files changed and the validation performed.

## Final checklist

- Meaning, facts, numbers, citations, and constraints are preserved.
- The rewrite fits the requested audience and format.
- Pattern clusters are fixed without flattening legitimate human voice.
- The text has sentence-length variation and concrete details.
- Confirmed AI tells are absent from generated wording, including unnecessary em dash characters (`—`).
- Idea connections still flow; punctuation cleanup did not create choppy period-stacked prose.
- Chatbot framing, filler, generic conclusions, and unsupported claims are gone.
- The result passes the read-aloud test.
