---
name: create-project-instructions
description: Investigate a project and its available knowledge sources to create or update evidence-based AGENTS.md or CLAUDE.md instructions.
---

# Create project instructions

Establish what an agent needs to know to work on this project, then write the
requested instructions. Investigate implementation, operating procedures, and
business decisions; code alone may not explain the intended behavior.

This skill owns project discovery and the evidence handoff. `agent-instructions`
owns writing, scope, packaging, and behavioral validation. A narrow wording or
already-decided rule change can go directly to that writer. Extracting a reusable
procedure from completed work belongs to `workflow-to-skill`.

## Establish the project and available context

Identify the target checkout, project boundaries, instruction files and their
canonical owners, intended readers, and repository visibility. Preserve existing
host entrypoints, imports, and nested exceptions. Use accessible context to resolve
routine choices; ask only when a material decision remains open.

Inspect the repository's existing instructions, overview, manifests, task runners,
CI, architecture and domain documentation, representative implementation, and
tests. Follow relevant history, issues, or PRs when they explain a consequential
decision. Build a map of where different kinds of answers live; reading every
file is not a completion criterion.

Inventory the relevant sources actually available through the current tools,
provided exports, and project links. These can include Notion, Confluence, Jira,
GitHub issues and PRs, Linear, Slack, or other project knowledge. Match the project,
team, workspace, and linked identifiers before searching beyond the repository.
Access to an account does not make its unrelated content relevant.

Read [references/project-evidence.md](references/project-evidence.md) when using
external knowledge, reconciling business intent with implementation, or resolving
source conflicts. Follow the host's required connector guidance for actual reads.
Use available access; installing a connector or obtaining credentials is a
separate action, not an assumed prerequisite for every project.

## Establish the instruction contract

For each consequential rule, retain its evidence pointer, scope, reason, status,
and any material exception. Distinguish current implementation, approved intent,
proposals, obsolete decisions, and inference. Resolve differences from the source's
authority over that claim and evidence of supersession, not just recency or which
platform stores it. Tests can confirm today's behavior without proving policy.

Seek enough context to answer the questions that change how an agent should work:

- What the project does, for whom, and which domain terms affect implementation.
- How to start, test, build, and inspect it, with actual working directories,
  prerequisites, effects, and success signals.
- Which business invariants, ownership boundaries, integration contracts, or
  operational constraints must survive a change, and why.
- Which local conventions and non-obvious pitfalls matter, and where to find
  conditional procedures or the detailed rationale.

Inspect command definitions before running bounded checks. Use the configured
toolchain; do not invent commands from the apparent stack. Authoring instructions
does not authorize deployment, production mutation, or destructive setup. Mark
commands as inspected, executed, passed, failed, or blocked according to the
evidence; an unavailable prerequisite does not turn inspection into execution.

When an unresolved question could change a material rule, ask it immediately and
pause the affected clause. Continue independent work. Do not encode an inferred
policy as mandatory or silently choose between equally authoritative decisions.
An inaccessible source blocks the claims that depend on it; report that exact
gap without guessing its contents or declaring the whole investigation complete.

## Write the project instructions

Resolve `agent-instructions` by name in the installed catalog and use it with
the target files, established contract, evidence, unresolved questions, and
representative tasks. It is a required writing dependency. If unavailable, retain
the research and report the missing owner rather than inventing a parallel writer.
The evidence handoff is ready for writing; it must not restart discovery through
this skill.

Create or update the requested canonical files. Keep root guidance useful across
the project and place conditional detail where the configured host can reach it.
Preserve the project's layout and confirmed overrides; creating both AGENTS.md
and CLAUDE.md is not automatically necessary. Keep commands and constraints
traceable through approved source links or durable project documentation.

Use the minimum publishable context needed to guide work. Private access is not
permission to copy internal discussions, customer data, or restricted decision
links into a public repository. Preserve approved constraints in an appropriate
summary; report any publication decision needed for material restricted context.
Keep detailed research in the permitted scratch location unless a durable record
is requested or needed. No instruction may depend on a scratch file that will be
removed.

## Check and finish

Use the writer's validation guidance to check command accuracy, references,
imports, scope, and representative tasks. Include a task that needs a business
constraint and a conditional path when those are part of the new instructions.
Creating a file does not prove the running host loaded it.

Finish with the requested files and a concise report of their scope, source
coverage, checks actually performed, contradictions resolved, and remaining
questions or blocked claims. Separate unavailable access, no relevant results,
and sources outside scope. Stop research when the material instructions are
supported and remaining gaps are explicit; do not keep expanding the search to
fill a template.

For requested maintenance of this skill's recorded inspiration, use
`agent-instructions` with this folder as the target. Ordinary project discovery
does not update this skill or its upstream sources.
