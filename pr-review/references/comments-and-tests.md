# Comment and test sweep

The parent runs this sweep beside the maintainability sweep. It repeats two
supplement checks so that their results do not depend on one engine noticing
them. Run each check over the production and test paths the diff adds or
changes, and record its census in the ledger: each member with its outcome, or
`none` when nothing applies.

- **Comments.** Census each comment, doc comment, XML summary and docstring that
  the diff adds or changes, that describes a changed member or the code around
  it, or that documents an interface, base type or contract a changed member
  implements. Test-class and test-method summaries count. Check each against the
  head's behavior, as the supplement's comment rule does, and against the
  repository's comment rules, such as those on listing callers, stamps or diff
  history. A comment that fails either check is a candidate.
- **Test level.** For each filter, rule or result-changing branch the production
  diff adds or changes, find the test that fails without it, as the supplement's
  census does, and record its level and the runtime it runs on, such as a mock,
  an in-memory provider or the real database. A member pinned only below the
  level the repository's testing standard requires for it, or a PR body claim
  about coverage that the tests do not support, is a candidate.

Each supported item becomes a candidate that the protocol judges.
