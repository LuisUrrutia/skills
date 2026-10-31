# Review gate

Run the gate after [identity and scope](../SKILL.md#establish-identity-and-scope)
and any [size check](../SKILL.md#check-the-review-size-cap), before composing
claims, so the title and body describe the final head.

Commit included work through `commit`, then obtain a validated
`review-code-changes` report whose Scope names the exact `<merge-base>..<head>`
SHAs to publish. Reuse a supplied or earlier report with that scope from the
review profile below; otherwise run the review. Skip the gate only on the user's
explicit instruction. If `review-code-changes` is unavailable, report the gate as
blocked.

Run every review of the gate, repeat reviews included, in a fresh Codex context
on the newest Sol model the host's catalog offers, with reasoning effort set
explicitly to `xhigh`. In T3 Code, use a `delegate_task` child with that target;
elsewhere, run `codex exec -m <model> -c model_reasoning_effort="xhigh"`, not
`codex exec review`, whose own formatter drops the canonical report. The child
runs `review-code-changes` on the declared scope, edits no product files and
returns its validated report path. Record the actual provider, model and effort
with the report. If that profile is unavailable or limited, report the gate as
blocked and ask the user; substitute another model only on their direction.

A `partial` or `unreadable` Coverage entry leaves the review unfinished: resolve
the limit, or ask the user whether to proceed.

Before pushing or creating, dispose of every finding and open question:

- Fix each `required` finding and each `optional` one within the change's
  purpose: code through `commit`, title or body remedies while composing.
- Record the code evidence that disproves a finding instead of changing code.
- Report an `optional` suggestion outside the change's purpose, or aimed at later
  changes, as a follow-up.
- Answer an open question with its needed evidence; a resulting defect becomes a
  finding.
- Ask the user when an item needs their decision or its remedy lands outside this
  repository; creation waits for the answer.

After fixes, rerun affected checks and a repeat review of the new head, passing
the previous report and each disposition with its evidence. Proceed when a review
of the exact head leaves nothing to fix. If a repeat review keeps a finding that
the last fix or disproof did not change, or a third review still leaves something
to fix, stop and ask the user.

Return the final report path and its review profile, or the user's skip, with
each item's disposition.
