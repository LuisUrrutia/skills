---
name: explain-decisions
description: Use when reconstructing the reasons behind existing code or design decisions.
---

# Explain decisions

Explain what evidence establishes about a decision's origin, constraints, and
tradeoffs. Use this skill directly; no coordinator or upstream skill is required.

## Locate the decision

Identify the code, choice, and period the question concerns. Read enough of the
implementation, callers, configuration, and nearby tests to check the premise.
Treat a reason suggested by the user as a hypothesis. Use available context to
resolve a vague target; ask only if different interpretations change the inquiry.

Separate the original reason, later reasons for keeping the design, and its
present technical effect. These may differ. Current behavior and ownership belong
to explain-code; diagnosing an observed failure belongs to debug. Preserve combined
requests without silently taking on repairs, a general audit, or guided teaching.

## Follow relevant evidence

Start with the closest useful records: explanatory comments, decision documents,
history, and linked discussions. When Git history is available, read
[references/git-history.md](references/git-history.md) to distinguish introduction,
later edits, and missing history. Code alone is not a record of author intent;
test code records expected behavior, not why it was chosen or whether it passes.

Follow concrete leads into PRs, tickets, documents, or team conversations using
available read tools. Read the relevant discussion and outcome, not just a title
or search snippet. Match the component, revision, and time period. For a guard,
retry, or threshold, look for a linked incident or measurement when the evidence
suggests that origin; the code's defensive shape alone does not establish one.

Choose sources to resolve the question or distinguish live explanations. Expand
when a link, contradiction, or missing decision context warrants it. There is no
mandatory sweep of every connector and no required agent roster. Investigate
directly; delegation is optional only when the host and task authorize it.

Track which records and queries support the answer. Distinguish a search with no
relevant results from unavailable evidence and sources outside the chosen scope.
An inaccessible linked discussion remains unknown. Continue independent leads,
but do not claim its contents or infer that no rationale exists anywhere.

Keep source, tests, configuration, and external state unchanged. Do not contact
authors or publish findings unless requested. A requested explanatory artifact
may be written at its agreed destination; ordinary investigation creates no
permanent records or teaching infrastructure.

## Weigh the record

Keep confidence attached to each substantive claim:

- **Recorded reason:** a source explicitly states the motivation. Attribute it
  to that record and time; a stated goal does not prove that the change achieved
  it, that everyone agreed, or that it still applies.
- **Supported inference:** explain which observations support the interpretation
  and the step that connects them. Several indirect signals remain an inference;
  copies of one statement are not independent corroboration.
- **Unknown or competing explanations:** name the missing evidence. Include a
  hypothesis only when it helps answer the question or choose the next search;
  plausible engineering benefits are not substitutes for historical evidence.

Compare conflicting records by date, scope, and relation to the implemented
decision. Resolve a superseded proposal when the record supports that reading;
otherwise preserve the contradiction with both sources. Neither the latest edit
nor a tidy narrative automatically wins. A later recollection is evidence of
that person's account, with its timing preserved.

Keep historical motivation separate from present validity. Current documentation
or measurements can establish today's constraints, not what an author knew then.
A metric change after a release alone proves neither causation nor the reason
for choosing an exact value. Before advising removal, check the current contract
and consumers; a retired original constraint alone does not make code redundant.
Ground advice about a replacement in the actual caller contract, including return
types and asynchronous behavior. A changed mechanism need not change that public
contract.

## Answer and stop

Lead with the answer at the requested depth and within the requested length.
Prioritize the conclusion and deciding evidence over retelling every search.
Put source locations, commit IDs,
or source URLs beside the claims they support. Use a short timeline or comparison
only when it clarifies a changed decision or competing account. Do not impose a
fixed report, confidence score, diagram, or list of empty source categories.

End the search when the question is supported and material contrary evidence is
accounted for, or when remaining leads are exhausted, inaccessible, or outside
the authorized scope. State any unanswered part, the relevant search limits, and
the specific evidence that could resolve it. Unknown is a valid result.

If this investigation prepares a requested change, carry forward evidenced
constraints and unresolved risks as planning inputs. Distinguish current
requirements from obsolete historical constraints. Recommendations remain advice;
this skill does not start implementation or delivery.

## Source maintenance

When asked to check or update this skill from its sources, read
[references/upstream-updates.md](references/upstream-updates.md). Ordinary
investigation does not fetch skill sources or require another skill.
