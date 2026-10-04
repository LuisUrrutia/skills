# Visual evidence for a PR

Use a visual when it answers a concrete review question more clearly than prose.
Select the smallest view that preserves the relevant behavior and labels its scope.

| Review question | Useful view |
| --- | --- |
| What happens to this request or event? | A short Mermaid flow or sequence showing actual owners, gates and important failure paths. |
| What moved, or who now owns an invariant? | A compact before/after dependency view, call tree or directory sketch. |
| What does a user see or do differently? | Genuine before/after screenshots, or a short recording for an interaction. |
| What changed in cost or performance? | A measured comparison with units, workload, baseline, revision and method. |

## Diagrams

Derive edges and labels from inspected code. Distinguish an existing path from a
proposed one; include a relevant authorization gate or error path rather than
implying universal success. Limit detail to the decision under review. Use native
GitHub Mermaid when suitable; do not require a separate diagram service.

A structural diagram explains implementation. It does not prove that the code
ran, that a permission check works, or that performance improved. Keep execution
evidence separately identified. Check the diagram's syntax and rendered output with
available tooling; report an unrendered diagram as such rather than claiming visual QA.

## Screenshots and recordings

For visible UI changes, use the project's actual app and applicable `verify`
recipe. Use the host's actual browser, device or native-app capture tool and save
the resulting file in ignored task storage. Capture the relevant state, including
an interaction or alternate viewport when it materially changes the result.
Match before and after scenario, data,
viewport and theme; identify baseline and changed revisions. Respect checkout
ownership when running another revision.

If no honest baseline is available, label a current-state capture and explain the
missing comparison. Never reconstruct a fake before image, use generated images as
runtime evidence, or present a screenshot from an earlier build as current proof.
Do not expose credentials, private user data or unrelated desktop content.

Read [attachments.md](attachments.md) to upload and place the captures in the PR.
Complete that operation when available under the authorized PR publication scope;
do not stop at recommending screenshots or listing local paths. Verify that the
final embeds render for the intended repository audience. If access or rendering
cannot be observed, report the exact limit and retain the available evidence.

Use concise captions and alt text explaining what the reviewer should observe.
Avoid dumping whole pages, unrelated screenshots or recordings too long to locate
the changed interaction. Visuals supplement required repository evidence.
