---
name: verification-authoring
description: Use when creating or maintaining a project's executable verification skill and feature map.
---

# Verification authoring

Create and maintain a project-local `verify-<app>` skill that another agent can
use cold: start the real application, establish which instance it is driving,
exercise user behavior, retain proof, and clean up its own resources.
`verify` selects and runs these skills; this skill owns their creation and upkeep.

Resolve and use `agent-instructions` by its registered name for instruction
writing and host packaging. It owns those general rules; this skill supplies
the application-verification contract. A missing required authoring dependency
blocks writing, not independent repository inspection.

## Establish the target

Identify the target project root separately from this skill's installed folder.
Read the request, project guidance, runnable surfaces, existing verification
skills, scripts, and feature maps. Reuse a suitable local owner rather than
creating another skill for the same application. Resolve skills by registered
name from the host catalog or named skills supplied by the caller, and apply
their instructions using the host's supported mechanism. Supplied context can
guide the task without global installation; it does not prove host discovery,
implicit selection, or a separate invocation.

Use the project's supported local skill location. Name a new skill
`verify-<app>`, with the actual application name in its description. Keep it
project-local; do not turn this request into a global installation. If the target,
intended behavior, or host location cannot be resolved from available evidence,
ask and pause the affected work.

- **Create:** no suitable recipe exists, or the caller requests a new application
  surface. Read [references/create.md](references/create.md).
- **Maintain:** the caller requests an audit or update of an existing recipe.
  Read [references/maintain.md](references/maintain.md). Missing targets require
  creation; several plausible targets require a selection.
- **Run verification:** the caller wants evidence about a change or application,
  rather than recipe changes. Use `verify` with the project, scope, and authority.

Authoring and maintenance change the verification skill, its feature map, and its
owned helpers. Product repairs and new test infrastructure require the active
task to include them; a failed check alone does not expand that scope. An existing
implementation task may already authorize repair. Keep recipe corrections and
product defects distinguishable in either case.

## Check the package and the live result

Read [references/feature-map.md](references/feature-map.md) when writing or
reviewing the map. From the target project root, run the read-only map check using
this skill's resolved installed folder and the target skill's actual path:

```sh
python3 "<installed-verification-authoring>/scripts/check-feature-map.py" --skill-dir "<target-verification-skill>"
```

Replace both paths before execution; the helper requires Python 3.9 or newer
with only its standard library. It prints JSON diagnostics: exit 0
means the map structure and local links pass; exit 1 means defects were found;
exit 2 means an input could not be read. It writes nothing and does not launch or
verify the application. Resolve its findings within the authoring scope, then
run the host's package validator when available and test every added helper on
representative success and failure inputs.

Creation requires one mapped feature driven end to end using the generated
instructions. Maintenance requires source and live coverage of every feature.
Both require evidence to remain readable after cleanup. Report the actual paths,
commands, coverage, corrections, product gaps, and blockers. A recipe that could
not be executed is a draft, even when its Markdown and scripts are valid.

The caller and repository rules own commits, PRs, and scheduling. Do not infer a
periodic job or PR from maintenance alone. For a requested check or update of
this skill's own sources, read
[references/upstream-updates.md](references/upstream-updates.md).
