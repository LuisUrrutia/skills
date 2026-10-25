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
  census on that path's single Coverage line: each member with its test and the
  runtime that test runs on, or `none`.
- An added or changed test that asserts behavior a finding shows defective, or
  that covers only a shape the writers can no longer produce while the shape that
  fails stays untested, is an affected site of that finding with its own anchor
  and remedy.
- For a public contract concept the change adds or alters, such as a date range,
  pagination, masking or an enum, compare its semantics with the sibling
  endpoints of the same API version. Run the examples in the supplied
  conventions or specification, and the most common realistic input, such as a
  date-only bound, through the code. When a changed expression or branch serves
  several variants, such as API versions, payment methods or environments,
  compare each variant's result at base and head, including the configuration
  that selects it. A divergence from those semantics, from siblings that follow
  them, or in a variant the PR does not target, without a recorded decision is a
  finding, or a question when only intent decides it; disclosing it in the PR
  body records no decision.
- For an error, loading, disabled or selected state the diff sets in a UI or
  form, including an error set from a server response, trace what clears it. A
  state that outlives its cause, such as an error that stays after the input is
  corrected, is a candidate.
- A comment, doc comment, XML summary or docstring that the diff makes untrue is
  a finding under the standard that governs comments, or optional where none
  does.
- For rendered UI the diff adds or changes, check that repeated controls have
  distinct accessible names or a labelled group, and that focus has a defined
  destination after the diff adds, removes or disables an element, counting
  focus the UI or form library already moves. The repository's accessibility
  target governs; the packet's accessibility reference, when present, supplies
  further checks.
- Trace suggested remedies with the same care as diagnoses. Census all members
  when a change applies a rule to a family of fields, handlers or call sites;
  preserve the affected members and distinct consequences through synthesis.

Private calibration describes claims to recheck on this revision. It cannot
waive a repository requirement or turn missing population evidence into proof.
