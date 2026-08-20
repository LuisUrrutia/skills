# Rewrite fidelity

`SKILL.md` owns the workflow. Use the rules below to build the meaning contract and run the fidelity pass for a rewrite or file edit, or to compare versions for semantic drift during review.

## Operating rule

Humanization is recomposition, not summarization. Preserve the information, not the source's shape: keep every unique substantive claim and qualification unless the user authorizes cuts, but merge, split, or reorder material when the original structure carries no meaning of its own. Let the piece's purpose determine emphasis: compress repetition and routine connective material, and expand only by unpacking information already present. You may replace unsupported promotional wrappers when the resulting passage retains the author's material point, stance, context, and support. When it is unclear whether evaluative language carries a real claim, preserve or recast it rather than silently deleting it.

If the source is visibly truncated, rewrite only the complete material and ask for the missing passage when it affects the result. Treat the continuation as unavailable rather than completing it from context.

Surface polish fails when it changes what a careful reader would conclude.

## Meaning contract

Track these parts of each claim:

- **Actors and actions:** who does what to whom, including agency hidden by passive voice.
- **Facts and mechanisms:** names, numbers, technical details, examples, and how something works.
- **Certainty and attribution:** fact, possibility, probability, opinion, allegation, estimate, or reported claim, plus who holds that view.
- **Scope:** quantifiers and limits such as "some," "most," "all," "only," "at least," and the population or time period they govern.
- **Polarity, conditions, and exceptions:** negation, prerequisites, caveats, and cases where the claim does not apply.
- **Causality and sequence:** cause, correlation, order, timing, and dependencies.
- **Intent and stance:** what the author asserts, requests, criticizes, explains, implies, or deliberately leaves open.
- **Support mapping:** which quotation, example, citation, footnote, or link supports which claim.
- **Structural meaning:** ordering, numbering, headings, code fences, and other formatting that carries priority, procedure, hierarchy, or legal effect.

A shorter sentence fails when it turns uncertainty into fact, expands a limited claim, converts opinion into consensus, invents causality, replaces a mechanism with a conclusion, shifts agency, detaches a citation, or drops a condition that changes when the claim is true.

## Claim-by-claim fidelity pass

After the reader pass, compare source and rewrite in this order:

1. Identify each unique source claim and its actor, action, object, truth-changing modifiers, and supporting material.
2. Locate its home in the rewrite. Several repeated source sentences may map to one rewritten sentence, but no unique claim may disappear by accident.
3. Confirm that the rewrite makes the same assertion with the same certainty, scope, polarity, conditions, causality, sequence, attribution, and intent.
4. Confirm that quotations remain exact, citations remain attached to the claims they support, and examples have not become general evidence.
5. Remove any new fact, measurement, example, interpretation, or precision that the source or user did not supply.
6. Preserve genuine ambiguity when the source is ambiguous. Ask the user only when resolving it would materially change the text.

The pass is complete when every unique source claim maps to a faithful rewritten claim and every rewritten claim maps back to supplied material.

## Functional-word tests

### Adverbs

Judge an adverb by the information it carries:

1. When it adds vague force to a weak verb or adjective, remove it or choose a precise verb that preserves the claim.
2. When it expresses measurable magnitude and the source gives the measurement, use that measurement. "Loads quickly" may become "loads in 300 ms" only when 300 ms is supplied.
3. When a precise verb carries the same action and manner, prefer it. "Spoke softly" may become "whispered" only when the source supports whispering; the words are not interchangeable in every context.
4. When it changes frequency, intent, scope, timing, exclusivity, or another truth condition, preserve it or recast the same information. "Occasionally," "accidentally," and "only" often belong to the claim.

Remove the adverb as a test. If the proposition changes, the rewrite must carry that information somewhere.

### Plain words

Use plain wording as a tie-breaker between expressions that make the same claim:

1. Prefer a common word over a formal synonym when meaning and tone remain equal: "use" over "utilize," "to" over "in order to," and "if it fails" over "in the event that it fails."
2. Prefer a direct verb over a noun phrase when the actor and action remain the same: "check" over "perform a check" and "configure" over "carry out the configuration."
3. Recheck actor, certainty, scope, causality, technical precision, and tone after simplifying.
4. Keep exact domain terms such as "encryption," "latency," and "authentication." Broader substitutes such as "protection," "slowness," or "access" are less accurate, not simpler.
5. Define an unfamiliar technical term when the audience needs help instead of replacing it with a different concept.

**Example:**

- Source: "The function enables callers to retrieve the data."
- Faithful: "The function lets callers retrieve the data."
- Drift: "The function retrieves the data." This changes the function from enabling the operation to performing it.

## Drift examples

| Source | Meaning drift | Faithful rewrite |
| --- | --- | --- |
| "The change could reduce latency." | "The change reduces latency." | "The change may reduce latency." |
| "Some users find the new menu confusing." | "The new menu confuses users." | "Some users find the new menu confusing." |
| "The app encrypts files before uploading them." | "The app uploads files securely." | "The app encrypts each file before upload." |
| "The process fails occasionally." | "The process fails." | "The process sometimes fails." |
| "The user accidentally deleted the file." | "The user deleted the file." | "The file was deleted by mistake." |
| "The parser only accepts JSON files." | "The parser accepts JSON files." | "The parser accepts only JSON files." |
| "Lee said the launch was delayed." | "The launch was delayed." | "Lee said the launch was delayed." |
| "Errors rose after the migration." | "The migration caused more errors." | "Errors increased after the migration." |
