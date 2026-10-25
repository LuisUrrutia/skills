# Maintainability sweep

The parent reads this after freezing the packet and runs the sweep while the
workers review, beside the seam sweep. It compares what the diff adds with what
the repository already holds, so a copy does not depend on a worker's structure
lens to surface. Run each check over the production and test paths the diff adds
or changes, and record its census in the ledger: each member with what it was
compared against and the outcome, or `none` when nothing applies.

- **Near copies.** For each component, hook, helper, validator rule set, mapping
  or fixture the diff adds or rewrites, search for an equivalent by name,
  signature and body: first in the packages the changed file imports from, their
  fixtures, handlers, helpers and mocks included, then in the same app or
  package, then in the rest of the repository. For a mock or handler, find the
  existing handler of the same route. Compare the diff's new members with one
  another, count the changed files that repeat one literal block, such as a
  fixture data set, and look inside each changed function for a lookup or
  computation it repeats. A near copy, a repeated block or a repeated
  computation is a candidate whose remedy reuses or extends the existing one, or
  computes it once.
- **Copied data.** For each value set the diff copies from another source, such
  as a seed, enum, lookup table or constant list, find the single source or the
  test that keeps the copies equal, and name a sibling that already has such a
  test. Compare what each copy counts or matches, such as characters, UTF-16
  units or bytes, case or a character class, not only its value.
- **One rule per stored value.** For each field whose writing the diff changes,
  such as its normalization, default or the value stored for an unresolved input,
  census every writer, including SQL backfills, migrations, seeds and other
  services, and compare the rule each applies to the same input, such as
  surrounding whitespace, case, an unresolved name or the unit a length counts. A writer the diff adds or
  rewrites, such as a backfill, is compared with every existing writer; a
  difference it introduces belongs to the diff even when those writers are
  unchanged. Two rules for one value are a maintenance cost without a caller
  that sends the differing input; a caller decides only whether the difference
  is also a correctness defect.
- **Integrity and repeated work.** For a column the diff starts to read as a key
  or code, find the constraint that keeps its values valid; writers that
  validate or canonicalize the value do not replace it. For work that depends
  only on static data, check whether the diff rebuilds it per request, row or
  call.

Each supported item becomes a candidate through the ledger contract and is
judged by the protocol. A difference that changes behavior, such as two writers
storing different values for one input, is a correctness candidate. Otherwise the
item is `optional` unless a repository standard requires the change, and its
recommendation follows the protocol's rule for a remedy outside the change's
purpose.
