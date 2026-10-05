# Project transition policy

`docs/agents/issue-tracker.md` belongs to the consuming repository. It describes
that project's tracker and decisions, not generic API instructions. Respect an
existing canonical tracker document referenced by project instructions. Keep one
owner and link to it rather than creating a second mapping.

## Establish the policy

When configuration is requested, inspect the project's current tracker, real
workflow states, connected development automation and written conventions.
Discover technical IDs from the service. Ask only for choices the evidence does
not settle, such as whether merge means Ready for QA or Done. Do not derive that
business decision from available status names, their order or an example here.

Start from [../assets/issue-tracker.md](../assets/issue-tracker.md), preserve useful
existing content, and replace unresolved values with verified facts or explicitly
leave the affected rule inactive. Examples are not executable defaults. The
policy can be prose and tables; no special parser or new configuration service
is required.

Record enough to decide a transition:

- Canonical tracker, scope identifiers, repository and project/board when relevant.
- Exact ticket lookup/linking conventions, and how completing versus contributing
  PRs are distinguished. Avoid GitHub auto-close keywords when QA must remain open.
- For each event: qualifying target branches, allowed source states, destination,
  conditions, required transition-field values when applicable, and exactly one
  owner (`agent` or a named native/external rule).
- Merge completion criteria for partial work, multiple PRs and stacked branches.
  Name the final integration branch; do not equate a layer merge with completion.
- Native rule identity and enabled/configuration evidence, or the explicit limit
  that an agent must be running or invoked again to observe merge.
- Exceptions for rework, reopening, manual progress or projects with distinct
  workflows. Omit branches the project does not use.

Use stable IDs where useful, alongside readable names. Resolve Jira's currently
available transition IDs at execution time: they are operations, not status IDs.
An inactive/unresolved row must never authorize a guessed transition. A rule that
omits source guards or ownership is incomplete, even if its destination exists.

When configuring policy, recommend the conditional route below so work-start
selection is explicit. Add it when project instruction edits are included in the
request, using the repository's canonical AGENTS.md or CLAUDE.md. Otherwise report
that activation depends on the installed catalog or explicit invocation. Preserve
its existing import arrangement; do not create both host files or edit global
instructions. For example:

> When starting implementation from a ticket, creating a linked PR, or observing
> its merge, use `issue-workflow` with `docs/agents/issue-tracker.md`. Reading or
> triaging a ticket alone does not change its state.

Creating this document does not enable provider automation. Configure external
rules only within separately authorized setup work, then verify their actual
event filters, branches, destination and enabled state. If the document and live
automation disagree, report the mismatch; do not add a competing agent transition.

## Interpret an existing policy

Select by the actual ticket scope and event; do not apply one team's workflow to
another team. Specific branch rules take precedence only when the document says
so; otherwise overlapping matches are ambiguous. Explicit source states protect
manual progress without inventing a universal "higher state" ordering.

Use the event definitions in [../SKILL.md](../SKILL.md). The requested progression
is In Progress, In Review, then the project's chosen postmerge state. Map those
intentions to real states; record any override to the review event or merge target
by branch explicitly.

In normal operation, use the active policy as data. Ask once when a material
choice is missing and report that transition pending; keep unrelated work moving.
Do not quietly persist a one-off answer as a standing rule unless that scope was
requested. Recheck remote state on resumption; old observations are not current
transition authority.
