# Native and terminal interfaces

Read only for the relevant non-web surface. Use the project's supported OS,
framework version, and platform guidance to select actual APIs and checks.
Do not add web ARIA attributes to a native control or apply CSS-pixel thresholds
to platform points or density-independent pixels.

## Native applications

Prefer platform controls and established components, then inspect the rendered
accessibility tree for this composition. Check useful names, roles or traits,
values, states, grouping, reading order, and available actions. Keep independently
operable children reachable. An automation identifier is not an accessible name;
visible text can already supply the name without a redundant override.

Exercise the complete task using the relevant assistive technology, such as
VoiceOver on Apple platforms or TalkBack on Android. Include modal presentation,
dismissal, navigation, errors, and recovery. Check hardware keyboard, switch,
voice, and gesture alternatives as relevant to the platform and support target.
An inspector, UI automation, or a simulator screenshot does not prove spoken
output or compatibility with every device and input service.

Use system text scaling and test the supported accessibility sizes, including
controls, long content, and failure states. Check themes, increased contrast,
reduced motion, and non-audio alternatives where relevant. Measure the effective
activation area and spacing, including overlap with neighboring controls.
Android guidance recommends at least 48 by 48 dp for touch targets. Apple's
current HIG distinguishes a 44 by 44 pt default from a 28 by 28 pt minimum for
iOS/iPadOS controls; other Apple platforms differ. Confirm the current table and
input context rather than treating 44 pt as a universal legal or WCAG minimum.

Record OS, device or simulator, assistive technology, settings, and actual
actions. If the required device or service is unavailable, complete independent
source checks and state the missing direct test. Keep it out of the passing
subset. Use official SDK guidance when a framework wrapper's semantics are unclear.

Platform references checked 2026-10-04:

- Apple accessibility HIG: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Apple's machine-readable HIG content: https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json
- Android principles: https://developer.android.com/guide/topics/ui/accessibility/apps
- Android testing: https://developer.android.com/guide/topics/ui/accessibility/testing

## Terminal interfaces

Check whether a user can perceive the prompt, enter an answer, correct a mistake,
cancel, and understand the result with the relevant terminal and assistive
technology. Cursor-driven redraws and animated progress can be difficult for
speech or braille output to follow. Where needed, provide a stable line-oriented
interaction or supported noninteractive equivalent, readable progress and errors,
and color-independent meaning. Respect configurable terminal colors and existing
plain-output conventions.

GitHub CLI's accessibility implementation demonstrates these choices; its
particular flags and settings are not requirements for other programs. Do not
change a user's global terminal or CLI settings to make a test pass. Name the
actual environment tested and any untested assistive-technology behavior.
