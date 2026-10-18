# Skill record format

Read this when creating, converting, or editing a skill's `origin.toml`, or when
listing the records that depend on a skill.
[updates.md](updates.md) uses these records to judge upstream changes.

`origin.toml` sits at the skill root as UTF-8 TOML with `format_version = 2`. It
records the skill's goal, the decisions that shape it, and the external material it
builds on and why, so an agent that never saw the original conversation can keep
those decisions when it edits the skill or judges an upstream change. Keep the
skill's own drafts and renames in Git history; the record is not a changelog.

## Choose each source's role

| Role | Meaning | The record holds | Default for an upstream change |
| --- | --- | --- | --- |
| `base` | The skill started from this material's text and still follows its structure | Every intentional deviation from it | Merge the change into the local text |
| `ideas` | The material contributed concepts that shaped the skill; its text is not tracked | The ideas taken and the material declines | Reassess the ideas; copy no text |

A skill has at most one base. A base stays valid while it stays recognizable
after local corrections, so upstream diffs still map onto local sections. Judge
that whenever a change adds, replaces or removes a deviation, including a new
record's first ones. Start from the deviations' `change` fields, then confirm
against the base text: a source at `reviewed_through`, fetched as
[updates.md](updates.md) describes, or a snapshot base at its recorded commit or
file. The base still fits while most of its sections keep their purpose and much
of their text in a local section, so an upstream edit there could merge hunk by
hunk. The number of deviations and the growth of the entry file do not decide it
alone: a skill can keep most base sentences under many added sections, and a
short base can be buried under local text. When the base text cannot be read,
record the change and report the fit as not judged.

When deviations replace most of the base, changing it into an `ideas` source
changes how every later update is judged. Propose it with the base sections
kept, replaced and removed and the base and local entry sizes, and let the user
decide; never change the approach or a role silently. A rebuild from newer
material gets a new source record, because a baseline never moves.

Any copied text needs a license that permits it and its notice in
`THIRD-PARTY-NOTICES.txt`, whatever the role; the role only governs updates. A
source without such a license can only be an `ideas` source, described in local
words. An `ideas` source or snapshot whose text was not copied says so in its
`license` field. A base snapshot of the user's own package needs no notice.

## Top-level fields

- `format_version`: `2`.
- `skill`: the registered skill name.
- `created`: the date the record began.
- `approach`: the reuse choice the skill follows, chosen with the
  `agent-instructions` reuse guidance and revised when a later source changes
  it, stated as one of:
  - `base`: exactly one source or snapshot has the role `base`.
  - `derive`: one or more `ideas` sources or snapshots, and no base.
  - `create`: local design with no sources and no material snapshots; reference
    documents, session evidence and dependencies are allowed.
  - `wrap`: a thin adapter over an `installed` dependency.
- `goal`: the outcome the skill produces, for whom, and what success looks like,
  in one to three sentences. Ideas, deviations and upstream changes are judged
  against it. It may restate the skill's opening; keep the two consistent.
- `[[invariants]]` (optional): local behavior that later edits and source updates
  must preserve and that no single source explains, such as authority limits, scope
  boundaries, host constraints, and user decisions. Each has `rule`, an optional
  `reason` (the incident, decision or constraint behind it, dated when that
  matters) and an optional `where`. A rule that answers one donor feature is a
  decline instead.

## Locations

`where` fields hold a list of local locations. Each is a path relative to the skill
root, optionally followed by `#` and the GitHub-style slug of a Markdown heading in
that file, such as `SKILL.md#launch`; anchors are lowercase, and a repeated
heading's anchors gain `-1`, `-2`, and so on. Add the anchor when the entry lives
in one section. A removal names the file the base text was removed from. Renaming
a heading or moving a file requires updating the locations that name it.

## Write the entries

Each decision lives in one entry. Another entry that depends on it refers to it by
its content, such as "the invariant that drafting never publishes", instead of
restating it; restated copies drift apart and contradict each other. A deviation
records one change. State the rule in a sentence or two rather than copying the
skill's text, which stays the source of its wording; the checker flags any field
over 100 words.

A `reason` names the lasting cause: a user decision, a named document such as a
brief, ruling or standard, an incident and what went wrong in it, a host
constraint, or the goal or an invariant the entry serves. Date it when that
matters. Credit each part to its actual source: a reason says "user decision"
only for what the user said, a ruling, brief or analysis by someone else is named
as such, and a clause someone added to the user's decision gets its own evidence
or a question to the user. Review rounds and findings, trial and probe results,
eval case IDs and earlier wordings ("previously", "now", "carried from") show how
the text was validated, not why the skill behaves that way, so they are never a
reason or part of a decision entry. A source review's `validation` list is the one
place that records checks, those of its own update run.

Evidence produced by the change that writes the record is described in words, or
cited by its pull request URL. Cite a commit of the skill's own repository only
once its default branch contains it, because rebasing a pull request or squash
merging it replaces the branch's commits. Local paths outside the repository,
such as a scratch directory, are not evidence a later reader can open.

## Repository sources

Each `[[sources]]` entry has:

- `id`, `author` when known, `repository` (human URL), `remote` (SSH Git URL),
  `ref` (tracked branch), `license`, and `role`.
- `baseline_commit` and `baseline_paths`: immutable evidence of the original
  material. A replacement or fresh derivation gets a new source record.
- `reviewed_through`: the last commit whose in-scope changes are fully resolved.
  It starts at the baseline and means **reviewed and decided**, not "all content
  adopted".
- `paths`: the current review scope, initially the baseline paths, including
  relevant references and license files. Update verified renames without changing
  the baseline. A path added later brings its changes up to `reviewed_through`
  into the cursor's claim, so review them before adding it.

Commits are full 40-character hexadecimal IDs. A candidate that was considered
and rejected is not a source; name it in the decision report instead.

### Base deviations

A base lists each intentional difference an upstream change could collide with as
a `deviations` table:

- `change`: the difference stated as an action on the base: replaced X with Y,
  removed X, added X, or restructured X into Y.
- `reason`: the goal, invariant, host constraint or user decision that requires it.
- `where`: the local locations.

Wording edits that keep the base's meaning need no entry. A section the base
lacks needs one short `added` entry; its content stays in the skill text.

### Ideas and declines

An `ideas` source has one or more `ideas` tables:

- `idea`: the concept in the skill's own terms, with its mechanism and the
  condition where it applies. A reader who never saw the source must understand
  it. A donor quote or a bare "adopt X" is not an idea.
- `serves`: the part of the goal it advances or the failure it prevents.
- `where`: the local locations where the idea lives.
- `shapes`: how the idea changed the skill's structure there, such as a step
  order, a section or a replaced rule. It names only text the idea produced;
  text inherited from a base belongs to the base.
- `adapted` (optional): how the local form differs from the donor's, and why.

Incorporating an idea means reshaping the affected part of the skill around it and
removing what it supersedes, not appending a rule. `where` and `shapes` record
that result. When the skill changes, keep each entry's `idea`, `where`, `shapes`
and `adapted` true to the current text; the reviews keep the history.

Record a donor behavior that a future update could propose again as a `declined`
table with `feature` and `reason`. Material not taken needs no entry unless it is
that kind of candidate. Delete a decline when the user adopts the feature.

### Reviews

Each update run adds a `reviews` table with `from_commit`, `to_commit`, and the
lists `incorporated`, `skipped`, `deferred` and `validation`; lists may be empty.
The first review starts at the baseline, each later one starts where the previous
one ended, and the last resolved one ends at `reviewed_through`. A review with
`deferred` items is pending: it is the last review, it starts at
`reviewed_through`, and the run that resolves it updates that review instead of
adding another. State reasons and local paths.
Refer to other records by their content, such as the declined feature, never by
line number. Reviews are dated history: line references they make into skill files
describe the text at that time and are not maintained.

## Other records

- `[[local_snapshots]]`: material without a tracked upstream feed, with `id` and
  `kind`. A snapshot is historical evidence, not an update feed; never invent a
  matching upstream commit. Its `kind` sets the evidence it needs:
  - `installed-file`: `path`, `sha256` and `update_policy`, plus a verified
    `local_repository_commit` with its `repository_commit_status` when known.
  - `repository-commit`: a private or local `repository`, its `commit`, the
    `paths` used, and how the commit was checked in `verification`; named hashes
    such as `entrypoint_sha256` are optional.
  - `session`: observed work with no file to hash; `verification` states which
    session and what it showed. It holds no role: record its lessons as
    invariants whose reasons cite it.

  An `installed-file` or `repository-commit` snapshot has an optional `license`
  and a `role` like a source,
  with `deviations` for a base or `ideas` and `declined` for ideas. A skill
  migrated from a whole package kept in another repository uses that package as
  its base; with no feed, its deviations document the migration only. Earlier
  versions in the skill's own repository are Git history, not a base.
- `[[reference_documents]]`: a consulted standard or article with `url`,
  `checked`, `role` (what the skill takes from it), and optional `id` and
  `coverage` (what was actually read).
- `[[dependencies]]`: a skill or tool the skill calls or hands part of its work
  to at runtime, with `kind`, `name`, `required`, and `role` describing what the
  skill uses it for, plus optional `resolution` and
  `decisions` (a list of local decisions about its use). A `local` dependency is
  resolved by registered name. An `installed` dependency also records
  `repository`, `remote`, `paths`, the `approved_commit`, its `installation`
  location, and optionally `found_commit` and `local_additions`. The approved
  commit is the revision the skill was validated with; `found_commit` is the one
  actually installed, and file presence alone does not show that it can be
  invoked. Each skill records only its direct dependencies, and a local dependency
  is maintained in its own repository rather than fetched as a feed. Skills used
  only to edit or maintain this skill are not its dependencies.
  [updates.md](updates.md) owns dependency updates.

## Example

A fictional `release-notes` skill built on an upstream skill, with one idea from
another:

```toml
format_version = 2
skill = "release-notes"
created = "2026-10-01"
approach = "base"
goal = "Draft release notes from merged pull requests that a user can read quickly, and return them without publishing anything."

[[invariants]]
rule = "Drafting notes never creates a release or a tag."
reason = "The user authorizes publication as a separate request."
where = ["SKILL.md#return"]

[[sources]]
id = "example-release-notes"
author = "Example Author"
repository = "https://example.com/example/skills"
remote = "git@example.com:example/skills.git"
ref = "refs/heads/main"
license = "MIT; notice retained in THIRD-PARTY-NOTICES.txt"
role = "base"
baseline_commit = "6997a3f780e5ed6d2dc20a80d008edc46e1a7a7b"
reviewed_through = "6997a3f780e5ed6d2dc20a80d008edc46e1a7a7b"
baseline_paths = ["skills/release-notes/SKILL.md", "LICENSE"]
paths = ["skills/release-notes/SKILL.md", "LICENSE"]

[[sources.deviations]]
change = "Replaced saving the PR list under .cursor/release/ with saving it in the task's scratch directory."
reason = "The skill runs in Claude Code and Codex, which have no .cursor directory."
where = ["SKILL.md#collect"]

[[sources.deviations]]
change = "Replaced the Publish step with returning the notes to the user."
reason = "The invariant that drafting notes never creates a release."
where = ["SKILL.md#return"]

[[sources]]
id = "example-notes-style"
author = "Example Author"
repository = "https://example.com/example/skills"
remote = "git@example.com:example/skills.git"
ref = "refs/heads/main"
license = "MIT; ideas only, no source text copied"
role = "ideas"
baseline_commit = "6997a3f780e5ed6d2dc20a80d008edc46e1a7a7b"
reviewed_through = "6997a3f780e5ed6d2dc20a80d008edc46e1a7a7b"
baseline_paths = ["skills/notes-style/SKILL.md"]
paths = ["skills/notes-style/SKILL.md"]

[[sources.ideas]]
idea = "Each entry states the impact a user notices before the mechanism behind it."
serves = "Readers learn first what changed for them."
where = ["SKILL.md#write"]
shapes = "The Write step orders each line impact first."

[[sources.declined]]
feature = "Internal ticket numbers in every entry."
reason = "Readers of release notes cannot open the internal tracker."
```

## Check the record

Run the bundled checker from this skill's installed directory after editing a
record, and after renaming headings or moving files in a skill that has one:

```sh
python3 "<installed-skill-maintenance>/scripts/check-origin.py" --skill-dir "<target-skill>"
```

It needs Python 3.11 or later. It prints JSON diagnostics and exits 0 when the
record is valid, 1 when diagnostics remain, and 2 on a usage error. Fix every diagnostic. The checker
validates structure, roles, review chains, local locations and field length. In
a Git checkout with a default branch (`origin/HEAD`, else `main` or `master`) it
also reports:

- `unmerged-commit`: a text field cites a commit that exists in the repository
  but not on the default branch.
- `baseline-moved`: a source keeps its `id` but its `baseline_commit` differs
  from the published record, the copy where the current history joins the
  default branch.
- `reviews-dropped`: a review of the published record is missing, or a completed
  one changed its range. A pending last review may be updated in place, not
  removed.

A record that is new on the branch has no published copy to compare. In a Git
checkout, the JSON lists under `skipped` each comparison it could not make, such
as in a shallow clone. Correcting a baseline that was recorded in error keeps
`baseline-moved`; report it with the user's confirmation. The checker cannot
judge whether an entry is clear, true or credited to the right source, or whether
a base still fits, which needs the base text; reread each entry as a newcomer to
the source would.

## List dependents

```sh
python3 "<installed-skill-maintenance>/scripts/check-origin.py" --dependents "<skill>" --root "<repository>"
```

It prints JSON with each `origin.toml` under the root, outside `.git` and
including fixtures, whose `dependencies` name the skill, with that entry's
`kind`, `required`, `role` and `decisions`, and exits 0. It exits 1 and names
the record under `unreadable` when a record or its `dependencies` cannot be
read, because the list may then be incomplete. This skill judges which listed
roles and decisions rely on a changed contract. `agent-instructions` checks the
dependents' text and searches the repository for other text that names the
skill, which also finds callers without a dependency entry; a dependent whose
text changes comes back to this skill for its record.
