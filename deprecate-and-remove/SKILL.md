---
name: deprecate-and-remove
description: Use when deprecating, retiring, or replacing a dependency, API, or feature.
---

# Deprecate and remove

Retire something the project no longer wants to maintain. Replace it when needed,
preserve the behavior that must remain, and complete the cleanup once its
consumers and support obligations allow removal.

This skill owns the retirement from decision through closure. A replacement is
optional: ending a feature can be the intended outcome. A routine version bump,
new feature, or behavior-preserving cleanup uses its existing workflow unless
the task also retires a dependency or supported path.

## Establish the retirement

Identify the target, intended replacement if any, reason, requested outcome,
and authorized work. Preserve the user's chosen replacement and product decision;
investigate alternatives only when those choices remain open. A planning request
ends with a usable plan; an implementation request continues through its
authorized changes and checks.

Establish which behavior must survive and which behavior intentionally ends.
Read applicable support commitments, release constraints, data-retention rules,
and any agreed notice or removal date. Ask about a missing decision only when
its plausible answers change the public contract, affected users, data disposal,
or authority to proceed. Continue independent work while that decision is open.

## Find consumers and retirement conditions

Trace the target through real uses, not just its name: callers and imports,
routes and direct APIs, jobs and queues, configuration, permissions, generated
artifacts, stored values, external integrations, and separately deployed clients
where relevant. Record what each consumer needs to change or stop using.

Separate repository evidence from deployed usage. No search matches or recent
requests does not establish that an offline client, scheduled job, stored payload,
or external caller no longer depends on the target. Mark inaccessible consumers
and missing observations; they leave their removal conditions unproven.

Keep a proportionate record of each affected consumer or group, its remaining
change, responsible owner when known, and evidence that permits retirement.
Use the project's existing task record or a short list; a contained replacement
does not need a new tracking system. Include shared dependencies that must remain
for other consumers and the behavior checks that will protect them.

Use `analyze-change-effects` when an indirect-consumer or compatibility assumption
needs investigation. Give it the target change, consumers already identified,
and the deciding unknown; continue the retirement with its findings and limits.

## Choose the path and order the work

For a coordinated internal change, establish that all consumers are under the
task's control and can move together, without an incompatible persisted or
deployed version left behind. Migrate them, verify the required behavior, and
remove the old path in the same change when those conditions hold.

Use a staged retirement when users, independent releases, stored state, or
support commitments need a transition. Define what changes at each stage, the
evidence for advancing, how to stop or recover, and who handles outstanding work.
Choose stages and observation windows from those constraints; elapsed time,
an arbitrary rollout percentage, or a fixed number of releases is not proof.

When the target has stored data, independently deployed consumers, or external
resources, read [retirement-boundaries.md](references/retirement-boundaries.md).
Use `design-code-structure` for an unsettled replacement interface or ownership
decision, and `ci-cd-automation` for delivery ordering and recovery. Supply the
retirement conditions and use their results to advance this task; do not copy
their full procedures into a second workflow.

## Replace or close access

For either path, where notice is required, prepare the affected audience, change,
effective date or condition, and any action users need to take. Use
`write-documentation` for substantial migration or sunset guides. Preparing a
notice does not mean it was delivered; actual delivery follows the active task's
authorization and available channel. When a stage keeps the target available,
use applicable project deprecation conventions to identify its successor or end
condition without changing behavior that is still supported.

**With a replacement:** establish the caller-visible contract, migrate the
consumers and related configuration, then exercise that contract through their
real interfaces. A matching type signature or successful import does not prove
matching behavior. Where old and new must coexist, define the compatibility
window and the condition for removing each temporary adapter or flag. For a
large change, keep each landed increment usable and checked; a partially moved
consumer still has outstanding transition work.

**Without a replacement:** implement the agreed end of access.

At the agreed stage, close the retired entry points across the relevant backend,
API, administration, automation, background paths, and UI. Preserve the replacement
and any adapter still under support. Decide how work already accepted finishes
or is cancelled under the product contract before removing its handlers. Keep
other permissions and adjacent functionality working. A hidden control is not a
closed entry point.

Run the authorized stages and update the remaining-consumer record from observed
results. Do not stop after producing a plan, replacement, or notice when further
authorized work can proceed. A future date, unmet support commitment, inaccessible
consumer, or unavailable required check stops the dependent removal; finish
independent work and record the exact condition and next action for resumption.
Do not invent a schedule or claim that a future stage has executed.

Commits, pushes, and PRs follow the active task and repository rules through
`commit` and `pr`; retiring something grants no additional publication authority.

## Remove obsolete artifacts and verify

Once the removal conditions have evidence, remove the obsolete implementation
and its exclusive callers, routes, exports, dependencies, configuration,
permissions, flags, obsolete deprecation markers, assets, and documentation
within scope. Update manifests
and lockfiles through the project's package manager. Check shared usage before
removing a package, secret reference, service, or infrastructure resource.

Remove tests that only describe the retired behavior; retain or adapt tests for
the replacement, shared contracts, and intentional denial of the retired entry
points. Preserve required history, records, legal notices, supported-version
guidance, and deployed migration history. A string matching the old name is a
lead to classify, not an instruction to delete its file.

Verify both the changed path and an adjacent path that must remain available.
For a replacement, exercise the required old behavior through the new route.
For a sunset, check that the retired entry points behave as agreed, including
direct calls and relevant background work. Check residual references, runtime
reachability, dependency removal, and the project's applicable build and tests.

Use `verify` for execution evidence and `review-code-changes` when a review of
the resulting change is needed. Pass the intended preserved and retired behavior,
stage reached, and removal conditions; consume their evidence and continue the
remaining authorized work. Resolve specialists by registered name. If optional
help is unavailable, do the bounded work directly and state material gaps;
unavailable essential evidence still blocks its dependent claim.

## Close at the state actually reached

Report what was replaced or retired, the consumers addressed, removed artifacts,
deliberately retained pieces and reasons, exact checks and results, and any next
stage with its owner or unresolved condition. Scale the report to the change.

Keep notice prepared, notice delivered, access disabled, consumers transitioned,
code removed, and removal deployed distinct when they apply. A repository change
can complete a requested code change without proving production retirement.
Claim full retirement only when all required consumers and removal conditions
have evidence; otherwise name the completed stage and outstanding work.

For a requested check or update from this skill's sources, read
[upstream-updates.md](references/upstream-updates.md).
