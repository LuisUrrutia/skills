---
name: humanize
description: Use whenever producing, refining, or reviewing written content, including requests to humanize it or remove AI-sounding patterns.
---

# Humanize

Recompose prose so it reads as one coherent piece written by a person. Preserve the writer's meaning, intelligence, and register. Optimize for effortless comprehension, then for brevity.

## Choose the mode

- `rewrite`: Return revised prose. The source may be pasted or supplied through context.
- `review`: Diagnose why prose feels generated, generic, or unnatural. Assess the writing, not whether a person or model authored it.
- `edit`: Modify the requested file in place while preserving unrelated content.

Ask one brief question only when voice, audience, or format would materially change the result. When the user says only "make it human," infer the register from the source and proceed in a clear, direct voice.

## Workflow

### 1. Lock the meaning contract

- Read the complete target before judging or rewriting it. For a scoped file edit, also read enough surrounding material to understand its role and local style.
- For `rewrite` and `edit`, read [FIDELITY.md](FIDELITY.md) before drafting and build the meaning contract it defines. For `review`, read it when evaluating semantic drift between versions.
- Protect names, numbers, citations, code, quotations, domain terms, formatting requirements, and user constraints.
- Treat secondhand text as protected: preserve watched phrases inside quotations, titles, proper names, and examples where the phrase is discussed rather than used.
- Treat a supplied writing sample as the authority for rhythm, vocabulary, formality, and punctuation choices not fixed by this skill.

Complete this step when the protected claims, exclusions, constraints, and target voice are explicit enough to compare against a rewrite.

### 2. Find the throughline and clusters

- State what the reader should understand, feel, or do after reading the piece. Infer this purpose from the source when it is unstated.
- Trace the route to that purpose across the whole text. Mark repetition, misplaced support, missing links, unsupported claims, and sections that preserve an outline rather than advance the thought.
- Diagnose interacting pattern clusters. A single fashionable word, punctuation mark, or tidy sentence is weak evidence; density and repetition across families are useful evidence.
- Route into [REFERENCE.md](REFERENCE.md): for `review`, read the complete catalog and its false-positive guardrails; for `rewrite` or `edit`, use its route map to load the sections that match observed clusters. Read the complete catalog for a piece-wide audit or a disputed case.
- Describe observable effects on the prose. Style alone cannot establish whether a human or a model wrote it.

Complete this step when the purpose, route, and material clusters are accounted for without turning ordinary author choices into findings.

### 3. Recompose from the throughline

- Rewrite from the intended route instead of polishing the source line by line. Cut repetition, combine related ideas, move support beside its claim, and reorder material when the meaning contract permits it.
- Prefer familiar, direct language when it carries the same meaning, precision, and tone. Keep technical or specialized wording when a simpler term would blur a distinction.
- Use the shortest formulation that preserves the full claim and remains easy to understand on the first read. Keep transitions that reveal a useful relationship.
- Build cause, contrast, sequence, condition, and consequence into the syntax. Choose sentence boundaries from changes in actor, stage, focus, or cognitive load rather than a target length.
- Match the context's register. Personal and persuasive writing can carry opinion and texture; reference, legal, academic, and technical prose should remain controlled and precise.
- Use only facts, examples, measurements, and sources already present or supplied by the user. Concrete writing comes from exposing supported detail, not inventing it.

Complete this step when the text reaches its point by the clearest economical route and every unique substantive claim still has a faithful home.

### 4. Tune voice, cohesion, and surface style

- Read the draft continuously. Make referents unmistakable, vary rhythm where the thought calls for it, and keep deliberate repetition used for precision, emphasis, or cadence.
- Repair mechanical synonym cycling, repeated paragraph templates, separately polished fragments, and choppy period-stacked prose through structure rather than cosmetic word swaps.
- Turn every diagnosed cluster into a constraint on the new wording, then rescan the revised passage for the same cluster and for new patterns introduced by the rewrite.
- Let punctuation express the relationship between ideas. A colon should introduce what precedes it; an em dash should serve the author's voice rather than act as an all-purpose connector. Use straight ASCII quotation marks (`"`) and apostrophes (`'`) in all generated or edited prose, including plain text and Markdown. Convert curly quotation marks and apostrophes unless exact character preservation is required for code, identifiers, filenames, or protected text. Match a writing sample and house style for other punctuation.
- Keep headings, lists, tables, callouts, and emphasis that help the intended reader; remove formatting that merely makes the prose look processed.

Complete this step when the draft reads as a continuous thought, its variation feels purposeful, and no repair has flattened the author's legitimate style.

### 5. Run two verification passes

1. **Reader pass:** Read the draft without consulting the source. Repair unclear logic, missing connections, vague referents, awkward cadence, and sentences that require backtracking.
2. **Fidelity pass:** Compare it with the source claim by claim using the meaning contract. Restore anything weakened, strengthened, generalized, narrowed, reassigned, or erased. Remove anything newly invented.

Repeat both passes after any substantive repair. Complete when the reader pass is natural and the fidelity pass finds no semantic drift.

## Deliver the selected mode

For `rewrite`, put the revised text first without chatbot framing. Add a brief `### Changes` section only when the user requests it or when material restructuring needs explanation.

For `review`, keep findings proportional to the evidence:

```md
### Writing-pattern review

Overall concern: Low | Medium | High

| Passage | Cluster and effect | Suggested repair |
| --- | --- | --- |
| "..." | Significance padding weakens a concrete claim. | State the supported result directly. |

This rating describes the prose, not who or what wrote it.
```

For `edit`, report the actual paths and checks performed:

```md
Changed: `path/to/file.md`
Validation: Checked the rewrite against the meaning contract, local style, and diagnosed clusters.
```

## Completion gate

Finish only when every gate passes:

- **Fidelity:** The claim-by-claim pass in `FIDELITY.md` succeeds; protected material remains intact and no specificity was invented.
- **Voice:** Audience, format, register, dialect, and author choices survive without mechanical imitation.
- **Purpose:** The throughline is clear, support sits where the reader needs it, and source order remains only when it serves the piece.
- **Economy and cohesion:** Every remaining sentence adds content or a useful connection; referents are clear; repetition and variation are purposeful.
- **Naturalness:** Diagnosed clusters are absent from generated wording, punctuation and formatting serve the prose, and the reader pass sounds publishable under the author's name.
- **Contract:** The response follows the selected mode and includes no unnecessary preamble or process residue.
