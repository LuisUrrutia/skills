# PR replies and review comments

Read this for a reply to review feedback or a new inline finding. Use the supplied
review decision and evidence; `pr-followup` owns investigating and repairing
feedback, and `review-code-changes` owns an audit when those tasks are requested.
A request to word an established finding does not start a fresh whole-PR review.

When the caller requires findings in an unfamiliar code language to become
questions, frame the technical finding as a plain question, whether it appears
in a new comment or a reply. Keep status updates and direct answers in their
natural form unless the caller asks otherwise. This changes the framing, not the
supported concern, certainty of the evidence, or assigned severity. Do not infer
that preference from the code language alone.

## Reply to the actual point

Read enough of the thread to avoid repeating an answered question. State what
changed, the answer, or the concrete reason for disagreeing, then stop. Keep only
the evidence the reviewer needs to assess that response.

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
with `suggestion:` and minor rule violations with `nit:`; a concrete defect or
genuine question starts with its point. Do not downgrade a supported defect to a
nit. Skip isolated taste objections; a documented rule or repeated inconsistency
can justify a minor comment.

Start with the observable problem, a genuine question, or an established
straightforward change. Omit formulaic politeness such as an opening "please".
Keep the tone respectful through factual, direct wording.

One finding gets one point, not necessarily one sentence. Use short sentences
for the problem, consequence and any requested change when each needs space. Avoid
joining a request to its explanation with a semicolon. Split the sentences or
connect them naturally with "if", "when" or "because". Preserve the causal
sequence and necessary conditions without imposing the same structure on every
comment.

Preserve exact identifiers and reachable example values when they are necessary;
shorten the explanation, not its evidence. Point to an existing pattern when that
helps the author act. Describe what a commit changed rather than inserting its
hash, unless revision evidence is needed.

The review workflow owns which findings to post, their locations, deduplication,
and resolution. For an authorized inline reply, use its existing thread. Keep
new findings separate from replies; this wording skill does not fan a message
out to other sites or resolve a discussion.
