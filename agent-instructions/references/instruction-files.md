# Persistent instruction files

Read this when creating or editing `AGENTS.md`, `CLAUDE.md`, `claude.md`, or another
file that supplies persistent instructions to an agent.

## Find the source and its scope

Inspect the target, relevant ancestor and nested instruction files, and any imports,
links, or generated-file notices. Follow the repository and session's declared
source of truth. An adapter that imports a tracked file usually points to the
place to edit; duplicating the same rule in the adapter creates a second owner.
Preserve imports and verify the target path before writing through a symlink.

Determine where the requested rule belongs from the user's scope and the host's
actual loading behavior:

| Intended scope | Placement |
| --- | --- |
| Personal rule across projects | The user's configured canonical instruction source |
| This repository | The repository instruction source |
| A subsystem or directory | Its effective local instructions or a precisely scoped reference |
| A conditional procedure | A referenced guide or an existing specialist skill |
| This request only | The current task context, unless persistence was requested |

Keep the existing filename and case. Do not create both `CLAUDE.md` and `claude.md`
as a portability workaround. If creating a host entrypoint, verify which filename
and import syntax that host supports. Resolve uncertain loading or precedence
from the configured host, rather than assuming all agents treat these files alike.

## Make the requested change

Place the rule beside related guidance. Keep its trigger, intended action, scope,
and material exceptions together. Reconcile contradictions with the authorized
change; preserve unrelated rules and local overrides outside its scope.

Keep project commands, package managers, and paths grounded in the repository.
Use a reference when a branch needs substantial detail, with a loading condition
in the entrypoint. A small instruction edit can stay in its existing paragraph.
Do not create a skill merely because the target is an instruction file.

Avoid promoting a single incident, source example, or task-specific permission
into a global requirement. When the user explicitly changes a standing rule,
apply that change at its authoritative scope; repetition is not required.

## Check the result

Read the resulting instruction in context, including its callers and relevant
scope boundaries. Verify imports still resolve and that adapters or narrower
files do not restate a conflicting version of the edited rule. For a behavior
change, use representative in-scope and out-of-scope tasks to check the intended
effect. Report what was inspected or exercised; file edits alone do not prove
that a running host reloaded the instructions.
