# Staged delivery

Read when a vertical slice needs an enabling change, a migration, or separate
backend and frontend work. Prefer a demonstrable result after each prerequisite;
do not present every intermediate stage as independently deployable.

## Separate layers only for a concrete reason

Name the constraint that prevents a small complete path: an independently useful
API, a shared contract required by several slices, a deployment boundary, or a
migration that must precede its consumers. An enabling refactor needs the current
capability it unlocks and a behavior-preserving check, not a general cleanup goal.

For a backend, frontend and integration split:

1. Bound the backend to the smallest required contract and prove it against real
   data/storage and relevant permission/error paths with the project's checks.
2. A frontend unit may use contract fixtures for isolated behavior, but label that
   evidence accurately. Mock data does not prove the backend connects or that the
   feature works in production.
3. Assign the connection and first real end-to-end check to an explicit unit, with
   its prerequisites and expected observable result. Keep this integration unit
   within its own review budget; do not use it to hide most of the feature.

If units cannot pass independently, identify the coupled group and first point
where its combined checks can pass. Prefer buildable, behavior-preserving states
using established compatibility or feature controls. Do not add a flag framework
solely to make the diagram look independent. Record rollout prerequisites and
recovery where the change requires them; merged code is not necessarily released.

## Stage compatibility changes

For changes whose consumers cannot move together, consider expand, migrate,
contract: introduce a compatible form, migrate bounded consumer groups, then retire
the old form only after checking all required consumers have moved. Account for
deployed clients and data; an empty repository search does not prove an external
contract unused. Each stage needs its supported behavior and deciding check.

Keep regression coverage beside the behavior it protects. Put the combined check
at the first stage that can exercise the real connection, and carry it forward as
later units extend the result. Release and data-migration prerequisites remain
explicit after their code merges.
