# Visual evidence for a PR

Choose the smallest visual that answers a concrete review question better than
prose; label its scope.

| Question | View |
| --- | --- |
| What happens to a request/event? | Mermaid flow/sequence with actual owners, gates and important failures |
| What moved or owns an invariant? | Before/after dependencies, call tree or directory sketch |
| What changes for the user? | Genuine before/after screenshots or a short interaction recording |
| What changes in cost/performance? | Measured comparison with units, workload, baseline, revision and method |

## Diagrams

Derive edges/labels from inspected code, distinguishing existing and proposed
paths. Include relevant authorization/error paths; limit detail to the review
question. Prefer native GitHub Mermaid without requiring another service.
A diagram explains structure, not successful execution, authorization or measured
performance; identify execution evidence separately. Check syntax and rendering
with available tools; disclose when rendering is unverified.

## Screenshots and recordings

Use the real app, applicable `verify` recipe and host browser/device/native capture
tool. Save captures in ignored task storage. Include interactions or alternate
viewports when material; match before/after scenario, data, viewport and theme,
identify revisions, and honor checkout ownership when running another revision.

Without an honest baseline, label the current-state capture and missing comparison.
Never use reconstructed/generated images as runtime evidence or older builds as
current proof. Exclude credentials, private user data and unrelated desktop content.
Inspect actual files and retain scenario, revision, viewport and path for each.

For placement, upload, rendering/access checks and recovery, execute
[attachments](attachments.md) within publication authority. Keep captures relevant
and recordings short enough to find the interaction. Visuals supplement required
repository evidence.
