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

When standardizing a capability or adopting an external skill, read
[reuse.md](reuse.md) to choose installation, a thin wrapper, a derivation, or a
new implementation before writing one.

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

Check the description beside neighboring skills, not only in isolation. A shared
writer can serve project discovery and workflow extraction without repeating
their investigations. Name the handoff and the distinct task that selects each
owner; do not make every description advertise the whole collection.

## Package the instructions

Use `SKILL.md` for shared decisions and steps. Put substantial conditional detail
in references with explicit loading conditions. Keep output templates separate
from instructions.

Prefer code for stable, deterministic work so the agent does not repeat mechanical
checks or transformations by reasoning through them on each run. Reuse an existing
command, project task, or script when its interface fits. Bundle a helper in
`scripts/` when the skill needs reusable composition or result handling; a single
adequate command needs no wrapper. Prior runs are not required when the requested
capability already establishes the automation's purpose.

Give each helper explicit inputs, outputs, failure states, and effects. Use the
project's available runtime, parameterize varying values, and bound external
probes or retries. A failed or unavailable check must remain distinguishable from
a passing one. Diagnostic helpers report state; installation, startup, or repair
follow the workflow's separate authorization and decisions.

State when to run the helper, its invocation, and how the agent uses its results
or handles failure. Keep the algorithm in code and interpretation, tradeoffs, and
unresolved domain decisions in the instructions. Test the helper's actual behavior;
a prose description of intended automation is not an implemented helper.

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
execute added or changed helpers on representative success and failure inputs.
Read [evaluation.md](evaluation.md) for new
behavior or activation changes. Package validity does not establish good decisions
or successful host invocation.

Finish when the requested skill exists, ownership and references are clear, and
checks or their specific limits are reported. Installation, publishing, and
scheduling follow the active request and repository instructions.
