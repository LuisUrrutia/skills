# Skill changes

## Size budget

Apply [Pruning](../SKILL.md#pruning) across the entrypoint and all instructional
references before measuring. Count words in the candidate and previous revision:

- Entry file.
- Each reference and their combined total.
- Whole instructional package: entry file plus references.

For a recorded `base`, also count its entry file at `reviewed_through`. When
files move, compare the same content boundaries. Keep records, evals and notices
separate from runtime instructions; moving guidance into them cannot hide growth.

When claiming reduced load, inspect what relevant tasks load. Distinguish measured
load from file size; absent a host trace, label the path estimate. Moving text
between files does not reduce the package total.

For growth against the previous version, or entry growth against the base, name
the distinct behavior each added passage buys (a user decision, contract or
observed failure). Justify entrypoint additions for every branch.
If agents might skip pointers, strengthen them instead of inlining conditional
procedures.
Cut passages that buy none. Require branch-specific references to earn their
own words; the entrypoint's reduction cannot offset unexplained reference growth.

If most base sections are renamed or replaced, hand `skill-maintenance` the
counts and a base-to-local section map to judge whether the base still fits.
Keep the recorded approach until that decision is settled.

## Dependent text

When name, activation, inputs, outputs, evidence, ownership or a named section or
file changes, search the repository for the skill and changed names, including
README entries. Use `skill-maintenance`'s dependents report when available.
Update callers within scope; report the rest by path and line. Record changes
belong to `skill-maintenance`.

Claims about another skill or file identify the revision read: branches can differ.

## Records

If the target or another skill in the repository has `origin.toml`, hand new
skills and changed rules, source ideas, base deviations or dependencies to
`skill-maintenance` with the user's reason. Installed skills outside that
repository do not establish this requirement. Elsewhere, records require a user
request. After headings or files move in a recorded skill, have that skill check
the record.

Hand over decisions and reasons, not a record file. Forward supplied proposed
entries, reasons and authority labels (user's words, inferred, unresolved)
unchanged; when the skill text states such a reason, retain the user's words.
If `skill-maintenance` cannot run, report the handoff and leave `origin.toml`
unwritten, including drafts. When it coordinates the change, it records the result.

## Review a skill change

Reviewers, including the model pair, check the sections above and
[evaluation evidence](evaluation.md#iterate-proportionately): actual hosts,
revision attribution, diff-supported carryover reasons, and unrun cases with
blocked claims. Missing counts, unjustified growth, repeated guidance, omitted
record checks, stale callers or unsupported cross-skill claims are findings.

## Report

Include the size comparison, record handoff and check results (or absence of
repository records), and dependent text updated or still stale.
