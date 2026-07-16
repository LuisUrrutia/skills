---
name: humanize
description: Humanize prose through natural-voice rewriting, AI-pattern review, and in-place file editing. Use when the user wants text rewritten in a more human voice, asks whether writing sounds AI-generated, or gives a file path and asks for humanizing edits while preserving meaning, facts, citations, and author voice.
---

# Humanize

Make text sound like a real person wrote it. Don't dumb it down, inflate it, or swap one kind of fake voice for another.

## Modes

- `rewrite`: Return the humanized text first. Add a short `Changes` section only when useful or requested.
- `review`: Return findings only. Use the review table under [Output contracts](#output-contracts), and don't rewrite the full piece unless the user asks.
- `edit`: Modify the requested file in place. Preserve unrelated content, then report changed files and validation performed.

Ask one brief question only when voice, audience, or format would materially change the result. If the user says "just make it human," use a clear, direct voice and proceed.

## Primary workflow

### 1. Read and lock constraints

- Read the full text before editing or judging it.
- Identify nonnegotiables: meaning, facts, names, numbers, citations, code, quotes, domain terms, format, audience, and user constraints.
- If the user provides a writing sample, note its rhythm, vocabulary, punctuation habits, and level of formality.

Done when you can state what must survive unchanged and what voice the result should match.

### 2. Diagnose clusters

- Identify clusters of AI tells, not isolated false positives.
- Treat stacked patterns as one strong finding. Don't pad a review by listing the same phrase under five labels.
- Use [REFERENCE.md](REFERENCE.md) for comprehensive audits, disputed false positives, or pattern families beyond the obvious.

Done when every major edit or review finding is tied to a cluster, and normal human choices are not flagged on their own.

### 3. Rewrite with voice and substance

- Preserve the register the context needs: academic, technical, casual, professional, warm, blunt, or personal.
- Add personality only when the content supports it. Blog posts, essays, LinkedIn posts, and emails can have opinions and texture. Reference docs, legal text, academic prose, and API docs should stay plain and precise.
- Replace puffery with concrete facts, vague authority with named sources, and filler with useful content.
- Keep the author's intelligence level. Human does not mean simplistic.
- Keep citations, code blocks, data, technical terms, quoted text, and constraints intact unless the user asks otherwise.

Done when the text says the same thing more naturally, with facts and author voice stronger than polish.

### 4. Enforce rewrite constraints

- Confirmed AI tells become constraints on generated wording. Don't recreate dash-heavy phrasing, decorative formatting, chatbot transitions, forced section shapes, synonym cycling, vague authority, or other diagnosed patterns.
- Don't introduce em dashes unless preserving quoted or source text, matching a provided writing sample or house style, or following an explicit user preference.
- Use straight ASCII quotes (`"`) and apostrophes (`'`) in generated wording unless preserving quoted or source text, matching a provided writing sample or house style, or following an explicit user preference.
- Preserve legitimate formal, academic, technical, multilingual, and house-style choices. The goal is natural voice, not flattening.

Done when the generated text avoids every confirmed tell while keeping protected source choices intact.

### 5. Read aloud and revise

- Read the result as if it were going to be published under the author's name.
- Revise again if it sounds like a press release, chatbot reply, SEO article, polished committee memo, or a mechanical anti-AI filter.

Done when the prose sounds publishable for the stated audience and still means what the source meant.

## Output contracts

For `rewrite`, return the revised text first. If useful or requested, add:

```md
### Changes

- Replaced generic claims with concrete details.
- Cut chatbot framing and repeated structure.
```

For `review`, use this compact format:

```md
### AI-writing tells

| Passage | Pattern | Suggested fix |
|-|-|-|
| "..." | Significance inflation + vague authority | Replace with a specific source or delete the claim. |
```

For `edit`, use this compact format:

```md
Changed: `path/to/file.md`
Validation: Re-read the edited passage and checked protected facts, citations, and constraints.
```

## Completion gate

Pass only when all gates are true. If any gate fails, revise again before answering.

- Meaning, facts, names, numbers, citations, constraints, and protected wording are preserved.
- The result matches the requested audience, format, and author voice.
- Pattern clusters are fixed without flattening legitimate human choices.
- Confirmed AI tells are absent from generated wording.
- Em dashes were not introduced except for quoted/source text, writing samples, house style, or explicit user preference.
- Straight ASCII quotes and apostrophes are used in generated wording except for quoted/source text, writing samples, house style, or explicit user preference.
- The prose has concrete detail, natural rhythm, and no chatbot framing, filler, generic conclusions, or unsupported claims.
- The read-aloud test passes.
