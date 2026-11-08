# Visual evidence for a PR

Choose the smallest visual that answers a concrete review question better than
prose, and place it under What changes beside the change it shows.

| Question | View |
| --- | --- |
| Which path does a request take, when a decision or race is hard to follow in prose? | Small Mermaid flowchart of that decision |
| What does the change turn one value into, step by step? | Mermaid diagram of the steps |
| What does each kind of item get under a rule? | Mermaid diagram linking each kind to what it gets |
| What changes for the user? | Genuine before/after screenshots or a short interaction recording |
| What changes in cost/performance? | Measured comparison with units, workload, baseline, revision and method |

A one-to-one mapping, such as statuses to stages, is a two-column table, and a
simple move or rename is bullets. Flowcharts with long labels and tables of rules
read worse than either.

## Diagrams

Derive boxes and arrows from inspected code. Draw left to right with one- or
two-word boxes and no crossing arrows. Put the reasons, and any case whose arrows
would cross, in one sentence above. Boxes name what each step is; show values
only when they explain it, such as a made-up identifier split into its parts.

A diagram explains structure, not successful execution, authorization or measured
performance; identify execution evidence separately. Render it with GitHub's
Mermaid version before publishing: quote labels that contain `<br>` or `=`, and
widen `flowchart.wrappingWidth` in front matter when a label wraps mid-word.
Disclose when rendering is unverified.

## Screenshots and recordings

Use the real app, applicable `verify` recipe and host browser/device/native capture
tool; use Storybook only when no app uses the change yet. Show the app's capture
alone, not beside the design. Save captures in ignored task storage. Include
interactions or alternate viewports when material; match before/after scenario,
data, viewport and theme, identify revisions, and honor checkout ownership when
running another revision.

Show captures inline when the change is mainly visual, and an unexpected visible
difference always; fold captures that only confirm the stated behavior in a
`<details>` block. Put a before/after pair side by side in a table with widths
that fit the column.

Without an honest baseline, label the current-state capture and missing comparison.
Never use reconstructed/generated images as runtime evidence or older builds as
current proof. Exclude credentials, private user data and unrelated desktop content.
Inspect actual files and retain scenario, revision, viewport and path for each.

For placement, upload, rendering/access checks and recovery, execute
[attachments](attachments.md) within publication authority. Keep captures relevant
and recordings short enough to find the interaction. Visuals supplement required
repository evidence.
