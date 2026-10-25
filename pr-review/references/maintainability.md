# Maintainability sweep

The parent reads this after freezing the packet and runs the sweep while the
workers review, beside the seam sweep. It compares what the diff adds with what
the repository already holds, so a copy does not depend on a worker's structure
lens to surface. Run each check over the production and test paths the diff adds
or changes, and record its census in the ledger: each member with what it was
compared against and the outcome, or `none` when nothing applies.

- **Near copies.** For each component, hook, helper, validator rule set, mapping
  or fixture the diff adds, search the repository by name, signature and body for
  an equivalent, and compare the diff's new members with one another. A near
  copy, or a block the diff repeats across files, is a candidate whose remedy
  reuses or extends the existing one.
- **Copied data.** For each value set the diff copies from another source, such
  as a seed, enum, lookup table or constant list, find the single source or the
  test that keeps the copies equal, and name a sibling that already has such a
  test.
- **One rule per stored value.** For each field whose writing the diff changes,
  such as its normalization, default or the value stored for an unresolved input,
  census every writer, including SQL backfills, migrations, seeds and other
  services, and compare the rule each applies.
- **Integrity and repeated work.** For a column the diff starts to read as a key
  or code, find the constraint that keeps its values valid. For work that depends
  only on static data, check whether the diff rebuilds it per request, row or
  call.

Each supported item becomes a candidate through the ledger contract and is
judged by the protocol. A difference that changes behavior, such as two writers
storing different values for one input, is a correctness candidate. Otherwise the
item is `optional` unless a repository standard requires the change, and its
recommendation follows the protocol's rule for a remedy outside the change's
purpose.
