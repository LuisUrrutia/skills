# Comment and test sweep

The parent runs this sweep beside the maintainability sweep. It repeats two
supplement checks so that their results do not depend on one engine noticing
them. Start each check from the production and test paths the diff adds or
changes, follow it into unchanged files where it names them, and record its
census in the ledger: each member with its outcome, or `none` when nothing
applies.

- **Comments.** Census each comment, doc comment, XML summary and docstring the
  diff adds or changes, each existing one on a member the diff changes, and the
  summary of each interface, base type or contract a changed member implements,
  test-class and test-method summaries included. Check each against the head's
  behavior, as the supplement's comment rule does; check those the diff adds or
  changes also against the repository's comment rules, such as those on listing
  callers, stamps or diff history. A comment that fails a check is a candidate.
- **Test level.** For each filter, rule or result-changing branch the production
  diff adds or changes, find the test that fails without it, as the supplement's
  census does, and record its level and the runtime it runs on, such as a mock,
  an in-memory provider or the real database. A member pinned only below the
  level that the standard governing its path requires, under that standard's own
  exceptions, is a candidate; a sibling member's test on the required runtime, or
  the file's existing lower-level pattern, does not count as that test. A PR body
  coverage
  claim the tests do not support is evidence for that candidate, recorded in
  Review basis.

Each supported item becomes a candidate that the protocol judges.
