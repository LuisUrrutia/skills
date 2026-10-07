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
- Trace suggested remedies with the same care as diagnoses. Census all members
  when a change applies a rule to a family of fields, handlers or call sites;
  preserve the affected members and distinct consequences through synthesis.

Private calibration describes claims to recheck on this revision. It cannot
waive a repository requirement or turn missing population evidence into proof.
