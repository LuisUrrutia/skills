# Skill packaging

Read this before creating a skill package, adding or moving its files, helpers or
templates, or validating it.

## Bundle the resources

Bundle the instructions, reference material, templates and helpers a skill needs
inside its folder. Place reference material in `references/`, link it from the
entrypoint with package-relative paths, and keep output templates apart from
instructions. Follow nested links and symlinks to their final targets; every
target stays inside the resolved skill directory. Resolving a symlink to the
author's repository is not a portability fix, and neither is a hardcoded checkout
location, username, home directory or operating-system-specific installation
path.

Locate bundled resources relative to the skill's resolved installation, without
assuming its path or the caller's directory. Keep them apart from runtime inputs,
output destinations, external URLs and skills resolved by registered name. A task
may supply a project root and authorize an output outside the package: document
those inputs and destinations instead of assuming the author's checkout layout,
and pass project paths explicitly when running from the skill folder.
Machine-specific paths may stay as labeled inventory data, not installation
requirements. When moving authoritative references into a skill, update their
readers and writers and keep one source of truth within the authorized scope.

## Helpers

Prefer code for stable, deterministic work, so the agent does not repeat
mechanical checks or transformations by reasoning through them on each run.
Reuse an existing command, project task or script when its interface fits.
Bundle a helper in `scripts/` when the skill needs reusable composition or result
handling; a single adequate command needs no wrapper. Prior runs are not required
when the requested capability already establishes the automation's purpose.

Give each helper explicit inputs, outputs, failure states and effects. Use the
project's available runtime, parameterize varying values, and bound external
probes or retries. A failed or unavailable check stays distinguishable from a
passing one. Diagnostic helpers report state; installation, startup or repair
follow the workflow's separate authorization and decisions.

State when to run the helper, its invocation and working directory, and how the
agent uses its results or handles failure. Keep the algorithm in code, and the
interpretation, tradeoffs and unresolved domain decisions in the instructions.
Test the helper's actual behavior; a prose description of intended automation is
not an implemented helper.

## Host tools and dependencies

If the host supplies a skill creator, such as Codex's `skill-creator`, use it
for its packaging requirements, its metadata files and its validators: it
supplies mechanics, and this skill owns composition and evaluation. Reconcile
the applicable instructions explicitly rather than nesting two complete
authoring workflows or installing a second creator with the same name. Prefer
available host tooling; a donor's reference to its CLI, task manager, evaluator
or viewer neither installs it nor makes it necessary.

Loading a Markdown file and invoking a skill are not interchangeable on every
host. Resolve each skill dependency by registered name through the installed
catalog and the host's invocation mechanism, and detect a missing required
dependency before the work that needs it.

## Validate

Run the available host validator, resolve local references and dependencies,
and execute added or changed helpers on representative success and failure
inputs.

For a new package or changed resource paths, inspect resolved targets in the
source package, then copy only the skill folder, symlinks preserved, to a neutral
directory under a different account layout. Exercise the required reads from
another working directory with the original checkout unavailable. Check resolved
targets as well as file existence, so a surviving symlink or absolute path cannot
hide an external dependency. Report simulated account layouts and the platforms
actually tested without implying another operating system or login was
exercised.

Validate on each supported host before claiming compatibility; when only
structural checks or supplied-context trials ran, say so. Package validity does
not establish good decisions, and file presence does not prove installation,
implicit selection or runtime execution.

Finish when the requested skill exists, its ownership and references are clear,
and each check or its specific limit is reported. Installation, publishing and
scheduling follow the active request and repository instructions.
