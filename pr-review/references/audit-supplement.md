# Caller review supplement

Read alongside the resolved `review-code-changes` protocol. These lenses retain
useful caller rules added after that auditor's original derivation. The auditor
still owns evidence, severity, Class, Action and report grammar.

- For changed queries, inspect the schema, entity configuration and available
  indexes, the values written to the columns, execution frequency and workload.
  Trace query count and work per request, scrape or outer row. A SQL shape alone
  does not prove an execution plan; measure or name the deciding unknown. Small
  current tables do not dismiss evidenced growth risk. Preserve value semantics
  when proposing a rewrite, including timestamp components and time zones.
- For a new metric, log or alert input, establish what action an operator can
  take and whether the signal can return to its healthy state. Inspect legitimate
  cases and recovery, not just the first failing event.
- Trace a claimed restriction to its policy, permission or contract owner.
  Absence of an existing capability does not establish a prohibition. Compare
  a workaround with a feasible change at that owner, using actual ownership,
  authorization, failure modes and maintenance cost. An alternative alone is
  not a required architecture change.
- For an event, webhook, notification or other side effect that a change emits
  for a domain change, establish from its contract, consumers or ticket which
  entry points must emit it, including other services and a system of record's
  own public API that make the same change. Report a required entry point that
  skips it or one that duplicates it.
- For each validation rule, mapping, mapping ignore or result-changing branch
  whose behavior the production diff adds or changes, find the test that fails
  without it: with the member deleted or inverted when it is new, or with the
  previous behavior when it changed. A member with no such test is a finding,
  and so is an added test that still passes with its target member deleted; a
  behavior-neutral member needs only the evidence that it is neutral. Record the
  census on that path's single Coverage line: each member with its test, or `none`.
  An added or changed test that asserts behavior a finding shows defective, or
  covers only a shape the writers can no longer produce while the failing shape
  stays untested, is an affected site of that finding with its own anchor and
  remedy.
- For a public contract concept the change adds or alters, such as a date range,
  pagination, masking or an enum, compare its semantics with the sibling endpoints
  of the same API version. Run the examples in the supplied conventions or
  specification, and the most common realistic input, such as a date-only bound,
  through the code. A divergence from those semantics, or from siblings that
  follow them, without a recorded decision is a finding, or a question when only
  intent decides it; disclosing it in the PR body records no decision.
- Trace suggested remedies with the same care as diagnoses. Census all members
  when a change applies a rule to a family of fields, handlers or call sites;
  preserve the affected members and distinct consequences through synthesis.

Private calibration describes claims to recheck on this revision. It cannot
waive a repository requirement or turn missing population evidence into proof.
