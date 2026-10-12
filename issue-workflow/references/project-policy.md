# Project transition policy

`docs/agents/issue-tracker.md` belongs to the consuming repository. It describes
that project's tracker and decisions, not generic API instructions. It names no
skill, agent tool or connector, so it stays valid whatever tooling applies it.
Respect an
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

Write it for the agent that applies it: record decisions and the facts needed to
act on them. Leave out the evidence gathered to reach them, conventions that do
not apply, and rules this skill already enforces; drop a template field that
changes no decision, and state a value shared by every row once. Verification
evidence belongs in the commit or PR that adds the policy.

Record enough to decide a transition:

- Canonical tracker and the conventions an agent acts on.
- Workflow scopes. Identify the projects and issue types this repository's
  tickets use, from recent ticket references and the user, then read each
  workflow's states and transitions with the tools available; where they cannot
  list a workflow, observe its tickets and their available transitions. Each
  distinct workflow, and each team rule set within a shared workflow, is one
  scope. Give each scope a selector built from stable fields of the fetched
  ticket, as the provider adapter defines; where it names no field to separate
  teams, use a stable field the user designates. Selectors must not overlap
  unless the document states precedence. List excluded scopes explicitly; an
  unlisted scope authorizes no transition.
- How PRs link tickets, and how completing versus contributing PRs are
  distinguished. Avoid GitHub auto-close keywords when QA must remain open.
- For each scope and event: qualifying target branches, allowed source states,
  destination, conditions, required transition-field values when applicable, and
  exactly one owner (`agent` or a named native/external rule).
- Merge completion criteria for partial work, multiple PRs and stacked branches.
  Name the final integration branch; do not equate a layer merge with completion.
- The identity of each automation rule that owns a transition.
- Exceptions for rework, reopening or manual progress, when the project has
  them. Omit branches the project does not use.

Record each state by its provider ID where one exists, beside a readable name in
the policy's language; the ID governs. Resolve Jira's currently available
transition IDs at execution time: they are operations, not status IDs. An
inactive/unresolved row must never authorize a guessed transition. A rule that
omits source guards, ownership or the provider ID of a state that has one is
incomplete, even if its destination exists.

When configuring policy, recommend the conditional route below so work-start
selection is explicit. Add it when project instruction edits are included in the
request, using the repository's canonical AGENTS.md or CLAUDE.md. Otherwise report
that activation depends on the installed catalog or explicit invocation. Preserve
its existing import arrangement; do not create both host files or edit global
instructions. For example:

> When starting implementation from a ticket, creating a linked PR, or observing
> its merge, apply `docs/agents/issue-tracker.md`. Reading or triaging a ticket
> alone does not change its state.

Creating this document does not enable provider automation. Configure external
rules only within separately authorized setup work, then verify their actual
event filters, branches, destination and enabled state. If the document and live
automation disagree, report the mismatch; do not add a competing agent transition.

## Interpret an existing policy

Select the scope as [../SKILL.md](../SKILL.md) describes. Never carry one scope's
states or rules to a ticket from another, even when status names match. Specific
branch rules take precedence only when the document says
so; otherwise overlapping matches are ambiguous. `Any` as a target branch means
any verified branch of the repository that holds the policy, and a resolved row
is active unless the policy marks it inactive. Explicit source states protect
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
