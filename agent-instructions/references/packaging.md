# Skill packaging

## Bundle the resources

Bundle required instructions, references, templates and helpers inside the skill
folder. Keep references in `references/`, linked from the entrypoint with
package-relative paths; keep output templates apart from instructions. Follow
nested links and symlinks to their final targets inside
the resolved package. Hardcoded checkout or installation paths, including symlinks
back to the author's repository, are not portable.

Resolve resources from the installed skill, independently of the caller's working
directory. Distinguish them from supplied project roots, runtime inputs, output
destinations, URLs and skills resolved by registered name. Pass project paths
explicitly. Machine paths may be labeled inventory data, not requirements.
When moving authoritative references, update their readers and writers within scope.

## Helpers

Prefer code for stable deterministic work. Reuse an adequate command or project
task; bundle a `scripts/` helper when composition or result handling warrants it.

Define inputs, outputs, effects and failure states. Use the project's available
runtime, parameterize variable inputs and bound retries or probes. Keep failed,
unavailable and passing checks distinguishable. Diagnostics report state;
installation, startup and repair retain their own authorization.

Document invocation, working directory, selection condition and result handling.
Code owns the algorithm; prose owns interpretation and domain decisions. Test
actual success and failure behavior.

## Host tools and dependencies

Use an installed host creator, such as `skill-creator`, for packaging, metadata
and validators; this skill owns composition and evaluation. Reconcile their
requirements without repeating whole workflows or installing a duplicate creator.
If a documented creator is absent, write metadata from its documentation and
name the missing creator and unrun validators as a limit, not a blocker.
A donor's tools do not become dependencies merely because its guide names them.

Resolve required skills by registered name and the host's invocation mechanism
before dependent work. Reading Markdown may not invoke a skill.

## Validate

Run available host validators, resolve local references and dependencies, and
execute changed helpers on representative success and failure inputs.

For new packages or resource-path changes, inspect resolved source targets and
copy only the skill folder, symlinks preserved, to a neutral account layout.
Exercise required reads from another working directory with the source checkout
unavailable. Check final targets, not just file existence. Report simulated
layouts and actual platforms accurately.

Compatibility claims require checks on each supported host; structural or
supplied-context trials prove neither installation nor implicit selection.
Report the created package, ownership, checks and limits. Installation,
publication and scheduling follow the active request and repository rules.
