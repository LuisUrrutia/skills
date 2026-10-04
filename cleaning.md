# Cleanup follow-up

Recorded on 2026-10-04 after the upstream adoption work through `903f40b`.
The user requested a full repository checkpoint, including the pre-existing
removal of `walkthrough/SKILL.md`. Repository cleanup remains pending; committing
the current state does not resolve the items below.

## Pending cleanup

- [x] Reconcile the removed `walkthrough` skill with current consumers.
  The registry no longer lists it. `explain-code` (formerly `how`) handles
  requested before/after mechanism explanations; `teach` handles guided lessons.
  Historical source records remain historical.
- [ ] Refresh [HANDOFF.md](HANDOFF.md) before using it for another transfer.
  Its captured baseline, source-progress counts and uncommitted-deletion state
  predate this checkpoint. Include the upstream adoption commits and current
  repository state, retaining the accepted workflow decisions and evidence limits.
- [ ] Review accumulated research and validation artifacts for redundant
  intermediate material. Preserve immutable source baselines, license notices,
  consultation results, behavioral evidence and referenced artifacts. Keep
  historical assessments distinct from current adoption status; a newer report
  alone is not sufficient reason to delete an older one.
- [ ] Inspect ignored `.tmp/` directories with their owners before removing
  obsolete scratch. Observed directories include `verification-skills` and
  `a11y-fable-consult-20261004`. Preserve `activity-preview` while the documented
  demo uses it, and `skill-atlas-server` while the preview process needs it.
  These local temporary files remain outside Git.
- [ ] Complete the outstanding atlas visual checks. Desktop DOM, links and
  filters passed in the [upstream validation report](reports/skill-atlas/upstream-adoption-validation.json),
  but screenshot capture failed and mobile layout was not verified. Record
  actual results after browser automation becomes available.

## Completion criteria

Current registry entries and skill routing resolve to available packages;
historical records remain clearly labeled. The handoff matches the repository.
Any atlas edits preserve `sources.json` / `catalog.js` parity, inventory hashes,
source evidence, links and filters. Removed artifacts have no remaining required
consumers. Record the affected checks and unresolved items when closing this list.
