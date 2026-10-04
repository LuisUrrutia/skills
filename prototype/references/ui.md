# Interface alternatives

Use this when seeing and interacting with a design can resolve a layout,
hierarchy, density, or interaction question.

Read the existing screen, design system, and supplied examples. Seek additional
references only when the direction is open and they will change the options.
Use enough application context to judge the design: surrounding navigation,
realistic data density, loading or empty states, and relevant viewport sizes.
Prefer fixtures or an isolated preview that preserves this context. Use the real
framework when component or routing behavior is part of the question.

If a local application route is necessary, follow its conventions and isolate
the entire experimental surface from production. Verify that isolation; hiding
only the variant selector is insufficient. Keep unrelated fetching, authentication,
and production behavior intact. Stub prototype mutations.

Compare only as many alternatives as the question needs; two or three often
suffice. Make alternatives differ in the structure or interaction being decided,
using comparable data and tasks. Do not inflate one hypothesis into several
cosmetic variants. Give each alternative a clear label and, when comparing them
in one artifact, a visible selector. Use a shareable, reload-stable variant URL
when useful. Optional keyboard shortcuts must not intercept editing controls.

Render every proposed alternative and drive the decisive interaction. Inspect
the relevant viewport sizes, capture screenshots for visual comparisons, and
check that controls allow the intended task. A screenshot alone does not establish
interaction behavior; static source inspection does not establish a rendered UI.

Compare the observations against the stated design goal. Explain tradeoffs and
recommend a direction or a specific combination. Distinguish the agent's judgment
from user preference or usability evidence that has not been collected. If the
choice needs user feedback, hand over the working alternatives with that question
explicit; do not present an unobserved preference as a validated winner.
