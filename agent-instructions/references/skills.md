# Skill instructions and packaging

Read this when creating, revising, combining, or evaluating a skill. A supplied
capability or workflow contract is enough to start; repeated task history is not
required. `workflow-to-skill` handles discovering a contract from past work when
that is what the user asks for.

## Define activation and responsibility

Read neighboring skill descriptions and the target's relevant resources. Identify
the requested capability, expected output, positive activation cases, likely near
misses, authority, and completion evidence. Extend an existing owner when that
fits the request better than a second skill with the same responsibility.

Before choosing metadata, invocation controls, tool calls, or dependencies, read
[hosts.md](hosts.md). Preserve supported existing metadata and invocation policy.

For composition, inspect donor files and dependencies. Decide which behavior to
retain, adapt, or exclude against the user's contract. Record actual inspirations,
verified revisions, and intentional deviations in `origin.txt` using
[upstream-updates.md](upstream-updates.md). Keep unknown provenance explicit.

## Write the selection description

On creation or review, make `description` the shortest clear answer to when the
skill should be used. State the requested action and distinguishing context so
the name and description suffice for selection before loading the body.

Keep procedures, tool choices, deliverable details, and feature lists in the body
or references. Add an exclusion only to prevent a likely overlap. Preserve words
needed to distinguish related requests; brevity must not broaden or narrow the
intended activation scope.

## Package the instructions

Use `SKILL.md` for shared decisions and steps. Put substantial conditional detail
in references with explicit loading conditions. Include scripts only for a real
recurring operation or a fragile invariant that benefits from deterministic
execution; this criterion applies to helpers, not to whether a skill may exist.
Keep output templates separate from instructions.

For an orchestrator, define each phase's inputs, selection condition, responsible
skill, completion evidence, and continuation. Verify dependencies are available.
The orchestrator owns routing and state; specialists own their procedures. Load
React or GitHub Actions guidance when the task reaches those domains rather than
copying their rules into the coordinator.

## Validate

Check the name and description alone against intended requests and nearby requests
that should not activate the skill. Clarify the distinguishing condition when
selection is ambiguous.

Run the available host validator, resolve local references and dependencies, and
execute added or changed helpers. Read [evaluation.md](evaluation.md) for new
behavior or activation changes. Package validity does not establish good decisions
or successful host invocation.

Finish when the requested skill exists, ownership and references are clear, and
checks or their specific limits are reported. Installation, publishing, and
scheduling follow the active request and repository instructions.
