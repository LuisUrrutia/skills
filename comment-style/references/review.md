# PR replies and review comments

Read this for a reply to review feedback or a new inline finding. Use the supplied
review decision and evidence; `pr-followup` owns investigating and repairing
feedback on your own PR, `pr-review-followup` owns settling the threads of a review
you gave, and `review-code-changes` owns an audit when those tasks are requested.
A request to word an established finding does not start a fresh whole-PR review.

When the caller requires findings in an unfamiliar code language to become
questions, frame the technical finding as a plain question, whether it appears
in a new comment or a reply. Keep status updates and direct answers in their
natural form unless the caller asks otherwise. This changes the framing, not the
supported concern, certainty of the evidence, or assigned severity. Do not infer
that preference from the code language alone.

## Reply to the actual point

Read enough of the thread to avoid repeating an answered question. When a
published fix does what the reviewer asked or suggested, the whole reply is
`Fixed in <commit>.`, translated only for a thread in another language. The
reviewer already knows the problem, and the commit shows the change. Add a short
sentence in the same form only for one of these:

- a deviation from the suggestion, or a choice among offered options when you
  took one other than the reviewer's first or its reason could change their view;
- a partial fix or a scope that differs from the request;
- a declined or deferred item, with its concrete reason;
- the answer to a question the fix does not settle.

State only that difference, reason, or answer. Never restate what the reviewer
said, including their diagnosis or suggestion, and never narrate the
implementation, its tests, or other additions; the commit shows them. Without a
fix, give the answer or the concrete reason for disagreeing, then stop.

Distinguish proposed, changed locally, checked, published, and deployed. Say
"fixed" only when the evidence supports the implied scope. Do not invent a test
result, publication, agreement, or promise. When revising an earlier incorrect
answer, give the correction and its deciding fact without a defensive preamble.

If supplied facts do not settle a technical claim, inspect the relevant code or
report the missing evidence. Ask a genuine question when the answer is outside
accessible evidence; keep an unverified premise out of the question.

## Word a new finding

Use the caller's review conventions and severity, or the repository's documented
conventions when the caller supplies none. Otherwise mark optional advice
with `suggestion:` and minor rule violations with `nit:`; a concrete defect, a
change your own work depends on or a genuine question starts with its point. Do
not downgrade a supported defect to a nit. Skip isolated taste objections; a
documented rule or repeated inconsistency can justify a minor comment.

Start with the observable problem, a genuine question, or an established
straightforward change. Omit formulaic politeness such as an opening "please".
Keep the tone respectful through factual, direct wording.

Build each finding around one connected idea. When a request needs a reason,
weave its condition and consequence into the same thought with links such as
"because", "since", "if" or "when". Prefer that connection over a detached
explanation or a standalone instruction tacked onto the end. Avoid using a
semicolon to join the request and its explanation. Split sentences when that
improves readability, keeping their causal connection explicit. Preserve necessary
conditions without forcing the same structure on every comment.

In a new finding, describe what a commit changed rather than inserting its hash,
unless revision evidence is needed; a reply about your own fix cites the hash as
that evidence.

The review workflow owns which findings to post, their locations, deduplication,
and resolution. For an authorized inline reply, use its existing thread. Keep
new findings separate from replies; this wording skill does not fan a message
out to other sites or resolve a discussion.

## Say enough to find the problem

A new finding, or a reply that raises or argues a technical point, goes to an
author who knows the code and can investigate with an agent. Give what goes
wrong, the input, state or user that triggers it, the rule or ticket that makes
it required, and the ask or question in one or two short sentences, usually
under 40 words. Leave out how you established it, such as call chains, the code
path that lets it through, configuration flags, defaults and ticket history, and
extra examples, side observations and caveats the author will meet while
fixing; give them when the author asks or disputes the point. Name at most
one fix, preferably an existing pattern; do not join alternative fixes with
"or". Fixing it here or tracking it in a ticket remains one ask.

When the PR works without a change your own work depends on, the comment is a
request, not a finding: usually one sentence with the ask and the work that
depends on it, such as a link to your PR. Leave out why that work needs it; the
author can ask.
