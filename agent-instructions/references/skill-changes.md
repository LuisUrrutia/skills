# Skill changes

Read this before finishing a change to a skill, and before reviewing someone
else's. It covers the entry file's size budget, the text that depends on the
skill, its record, and what a review of the change checks.

## Size budget

Count the entry file's words (`wc -w SKILL.md`) in the candidate, in the previous
version (the revision the change starts from), and, when the skill's record has
`approach = "base"`, in the base's entry file at the record's `reviewed_through`
commit. An entry file larger than either names, for each added passage, the
behavior it buys (a user decision, a contract, or a failure observed or measured
without it) and why every branch needs it there. Move a passage that only some
branches need into a reference whose pointer names those branches
([levers](levers.md#information-hierarchy)), and cut one that buys no behavior.
Moving text into a reference that every branch must read reduces no load.

When the change renames or replaces most of the base's sections, hand the
approach question (base or derive) to `skill-maintenance` with the three counts
and a map from each base section to its local home. That skill judges whether the
base still fits; keep the `base` label until that question is settled.

## Dependent text

A change that alters what other text relies on, such as the skill's name, its
description or trigger, inputs, outputs, completion evidence, ownership boundary,
or a section or file that others name, leaves that text stale until someone
updates it. Find it:

- Search the repository for the skill's name and for each renamed section or
  file: other skills and their records, README entries, and other
  documentation.
- Ask `skill-maintenance` which records list the skill as a dependency, when it
  offers that report.

Update each dependent text inside the request's scope, and list the rest with its
path and line in the report. A README entry that describes the changed behavior
is dependent text too. Entries in another skill's record go to `skill-maintenance`.

A claim about another skill or file names the revision it was read from, such as
`origin/<branch>:<path>:<line>`: the default branch and an open branch can say
different things.

## Records

A repository keeps skill records when the target skill or another skill in it has
an `origin.toml`; skills installed in the host outside that repository do not
count. There, hand each new skill, and each change that adds, removes or alters a
rule, a source idea, a deviation from its base or a dependency, to
`skill-maintenance` with the user's reason; when `skill-maintenance` coordinates
the change, it records the result itself. After headings or files move in a skill
with a record, have `skill-maintenance` check the record. Elsewhere, a record
exists only when the user asks for one, and `skill-maintenance` creates it.

The hand-over is the decisions with their reasons, never a record file. When
`skill-maintenance` cannot run, put the hand-over in the report and leave every
`origin.toml` unwritten, even as a draft or placeholder.

## Review a skill change

A review of a skill change, by this skill or by the model pair it briefs, checks
at least:

- **Size and base:** the three counts above, the behavior each growth buys, and,
  when most base sections were renamed or replaced, the approach question handed
  to `skill-maintenance` with the section map.
- **Evaluation evidence:** the hosts that ran, results labeled with the revision
  they ran on, a diff-based reason for each result carried over from an earlier
  revision that the diff supports, and the unrun cases with the claims they block
  ([evaluation](evaluation.md#iterate-proportionately)).
- **Records:** each change to a rule, idea, deviation or dependency went to
  `skill-maintenance`, and its record check passed or its diagnostics are
  reported.
- **Dependent text:** updated or listed, with the search that found it.
- **Cross-skill claims:** each names the revision read.

A missing item is a finding, not a pass.

## Report

For a skill, the report adds the three word counts, the record changes handed to
`skill-maintenance` or that the repository keeps no records, and the dependent
text updated or listed.
