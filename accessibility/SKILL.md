---
name: accessibility
description: Design, implement, or audit accessible user interfaces. Use for keyboard and assistive-technology support, focus, names and semantics, contrast, zoom, motion, forms, media alternatives, or WCAG checks across a user flow.
---

# Accessibility

Make the intended task perceivable, operable, and understandable through the
supported ways of accessing the interface. Check the complete interaction,
including entry, state changes, errors, recovery, and the resulting destination.
A component with the right attributes can still prevent someone from finishing.

## Establish the task and authority

Resolve the platform, affected flow, current revision, project requirements,
design-system components, and supported browser or OS and assistive technologies.
Use the request and available project evidence; ask only when an unresolved choice
would materially change the behavior or acceptance criteria.

An audit produces findings and coverage. Implement corrections when the active
task authorizes them. A screenshot supports visual observations and design advice;
it does not establish keyboard behavior, accessible names, or spoken output.
An unrelated backend change does not need a UI audit.

For web work, use the project's accessibility target; if absent, state WCAG 2.2
Level AA as the engineering baseline. This is a scoped working target, not a
claim of legal compliance or whole-product conformance. Read
[references/web.md](references/web.md) before selecting web checks. For native
apps or terminal interfaces, read
[references/platforms.md](references/platforms.md) and consult the relevant
platform documentation. Web attributes, CSS pixels, and platform units are not
interchangeable. Confirm the exact criterion and its exceptions before treating
a preference, pattern recommendation, or enhanced target as a requirement.

## Define the interaction before changing it

Trace the affected task through its relevant states, including loading, empty,
invalid input, denied access, interruption, and success where they exist. Identify
what users must perceive, what actions they can take, where focus should go, and
how they discover the outcome and recover. Include essential embedded or
third-party steps in that coverage even when their code is outside our control.

Prefer native controls and the project's established accessible components.
Inspect their actual composition and runtime behavior: a library's reputation or
an ARIA attribute does not prove this use works. For a custom interaction, resolve
its semantics, keyboard model, focus lifecycle, and announcements together.
Use the applicable platform or WAI-ARIA pattern without copying an incomplete
example or adding redundant handlers to controls that already handle the key.

Keep the product's behavior and visual identity unless correcting the barrier
requires a change. Make the smallest coherent repair at the responsible component
or shared primitive. Check affected callers when changing a shared control.
Do not hide content, remove an essential action, or disable an accessibility
check merely to eliminate a finding.

## Collect evidence that matches the claim

Choose checks from the affected interaction and required coverage, not a fixed
number of screens or a tool's default scan. Use the host's available UI tools and
the project's existing harness. When applicable, invoke `verify` with this flow
and its accessibility criteria; the matching `verify-<app>` owns startup, health,
fixtures, driving, and cleanup. A missing specialist does not prevent source
inspection, but missing execution remains a limitation.

Combine the evidence the claim needs:

- Inspect the composed source and accessibility tree for names, roles, states,
  relationships, order, and hidden content. Check the meaning, not just presence.
- Drive the real keyboard or platform input path through the task and its
  transitions. Observe focus entry, movement, visibility, dismissal, and return.
  A composite widget may use one Tab stop and arrow keys internally.
- Use the relevant screen reader or assistive technology when verifying its
  experience: navigation, announcements, action, error, and recovery. A tree,
  synthetic event, or automated scan cannot stand in for that interaction.
- Check relevant visual conditions, such as text enlargement, reflow, contrast,
  effective hit areas, supported themes, and reduced motion. Record the actual
  condition; narrowing a viewport is not evidence that browser zoom was used.
- Run applicable existing lint, component, or automated accessibility checks.
  Inspect their scope, exclusions, inconclusive results, and false positives.
  An empty violation list proves only what that run could check.

For an observed defect, preserve enough of the failing action and result to
compare after the repair. Add a focused regression where the repository's tests
can protect the behavior, then rerun the affected path and relevant neighbors on
the final revision. Do not replace an unavailable manual check with a passing
automation score. State the missing environment or action and the next check.

## Report barriers and coverage

For each supported finding, give the location or state, affected user task and
input method, reproduction or source evidence, expected and observed behavior,
and a concrete correction. Cite the applicable criterion or platform guidance
when making a standards claim. Distinguish a confirmed failure, a usability
recommendation, and a question that needs execution. Prioritize by blocked tasks,
impact, reach, and available alternatives rather than a universal severity label.

State what passed within the tested scope, what failed, and what remains untested,
blocked, or inconclusive. Include the revision, relevant environment and settings,
checks actually run, and retained evidence. Required missing checks prevent a
complete result; third-party ownership does not turn a blocked task into a pass.
Do not report a whole flow as accessible based only on its first screen, a source
patch, a screenshot, or an automated score.

## Compose only where needed

- `review-code-changes` keeps the review scope and final findings when requesting
  this specialist. Return evidence in its format without starting another audit.
- `verification-authoring` maintains a reusable local verification recipe when
  requested; this skill supplies accessibility criteria for that recipe.
- `error-handling` owns failure and recovery semantics; this skill checks whether
  users can perceive the error and reach the recovery action.
- `design-code-structure` owns module and interface boundaries when a repair
  needs structural design. Ordinary accessibility work does not require it.

For a requested source check or update, read
[references/upstream-updates.md](references/upstream-updates.md).
