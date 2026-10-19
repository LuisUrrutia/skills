# Reuse and standardization

Read installed owners, candidate sources and relevant dependencies before
reconciling guidance or adopting a skill. Similar descriptions can hide different
actions or authority. Compare trigger, owner, action and completion evidence;
resolve conflicts by authority, scope or a user decision. Check invocation,
approvals, tests, tools and external writes especially carefully.

## Choose what to maintain

| Approach | Fit | Local responsibility |
| --- | --- | --- |
| Install unchanged | Existing task, host and authority fit | Select and validate version |
| Wrap | Procedure fits with a small adapter | Inputs, additions and result checks |
| Base | Upstream structure stays recognizable | Deviations; adopt upstream changes by default |
| Derive | Ideas need changes throughout | Local implementation and relevant source changes |
| Create | No suitable implementation | New behavior and validation |

Choose the least local behavior that meets the contract. Renaming needs no wrapper;
replacing scope, tools, ordering, ownership or external actions across several
steps suggests a base or derivation.

Keep the choice and reason; `skill-maintenance` records them where required.
Distinguish authorship from repository hosting. Check licenses and required
notices before distributing source text; citations do not replace notices.

## Keep wrappers thin

Resolve the installed identity and supported invocation mechanism. Specify inputs,
outputs, local additions and completion checks. Keep upstream installer-managed;
editing it creates a fork.

Preserve user authority and host rules. Prose cannot sandbox a contradictory
dependency: choose a compatible dependency or explicit derivation. Verify required
dependencies before dependent work; report an absent one with prepared inputs
rather than claiming execution or silently substituting another procedure.
Use host selection controls to avoid competing automatic entrypoints.
