# Web accessibility checks

Read for web work. Select the relevant checks for the task; this is a practical
guide, not the complete WCAG conformance procedure. WCAG is normative; the
Understanding documents and WAI-ARIA Authoring Practices Guide (APG) explain
criteria and interaction patterns. Recheck current documentation when an exact
criterion, exception, or browser support determines a finding.

## Semantics and content

Check the composed page, including shared layouts and components. Use native
links for navigation and buttons for actions. Inspect the computed accessible
name, role, value, and state; do not add labels that override useful visible text.
The accessible name should contain the visible label for speech input. Associate
instructions and errors with the relevant control; placeholders do not replace
labels. Group related controls and expose required, invalid, selected, expanded,
and disabled states where applicable.

Expose a meaningful reading order, headings, landmarks, and a way to bypass
repeated content. Judge the full outline rather than demanding an h1 in each
component. Do not turn a preferred heading convention into an automatic WCAG
failure without checking the actual relationship or criterion. Data tables need
programmatically available header relationships; layout grids are a different
structure. Check virtualization for reachable items and meaningful positions.

Give informative images an alternative that serves their purpose; remove purely
decorative imagery from the accessibility experience. Complex charts may need a
nearby explanation or data alternative. Check captions, transcripts, audio
description, and player operation as required for the media and target level;
captions alone do not convey essential visual information in a video. Review the
meaning and accuracy of alternatives, not merely whether a track or alt exists.
Set page language and identify language changes where applicable.

## Keyboard, focus, and dynamic interfaces

Exercise Tab and Shift+Tab, activation keys, and the pattern's navigation keys.
Preserve text editing, browser shortcuts, and input composition. Do not make every
item in a roving composite a separate Tab stop. Avoid positive tabindex as a
repair for a broken source order. Focus must remain perceivable and follow a
useful sequence; content updates do not all warrant moving focus.

For a modal dialog, test opening, an appropriate initial focus, Tab containment,
dismissal, and return to the invoking control or a logical successor if it has
gone or the task moved on. The background must actually be unavailable while
modal; aria-modal alone does not implement that behavior. A non-modal popover
does not inherit a modal's focus trap. Match custom widgets to their APG pattern
and test the supported browser/assistive-technology combination.

Check focus after route changes, item removal, validation, asynchronous updates,
and overlay closure when those events occur in the task. Keep a required action
reachable beneath sticky headers, consent panels, and other overlays. Distinguish
the AA requirements for visible focus (2.4.7) and focus not entirely obscured by
author-created content (2.4.11) from AAA Focus Appearance (2.4.13). Partly hidden
focus can still harm usability; do not mislabel it as an automatic 2.4.11 failure.

Expose status changes without unnecessarily interrupting or moving the user.
Choose live regions or alerts for the actual urgency and verify their timing,
including repeated updates. Do not put every field error in an assertive alert or
announce every keystroke. Where content appears on hover or focus, check the
applicable dismissible, hoverable, and persistent behavior (1.4.13); put interactive
actions in an operable surface instead of a tooltip that cannot receive them.

## Visual conditions and input alternatives

| Concern | Check and interpretation |
| --- | --- |
| Text contrast | Under 1.4.3 AA, normal text needs 4.5:1 and large text 3:1, subject to the criterion's exceptions. Large means at least 18 pt regular or 14 pt bold, approximately 24 or 18.67 CSS px, not 18 px regular. Measure the actual foreground/background combination and relevant states; do not round a failing ratio up. |
| Non-text contrast | Check the visual information needed to identify controls, states, and meaningful graphics under 1.4.11, including its exceptions. A universal border requirement is not the criterion. |
| Color | Errors, links, charts, and status must remain understandable without color alone. Preserve useful user color and forced-color settings. |
| Enlargement | Check 200% text resizing where 1.4.4 applies, including controls and error states. Browser zoom, text-only resizing, and a narrower viewport exercise different conditions; identify the one actually tested. |
| Reflow | Under 1.4.10, check vertical content at an equivalent width of 320 CSS px, or horizontal content at 256 CSS px height, without loss or unnecessary two-dimensional scrolling. A necessary two-dimensional table or map can be excepted; that does not exempt surrounding content. Clipping or hiding overflow is not a repair. |
| Text spacing | Under 1.4.12, test simultaneous overrides where applicable: line height 1.5 times font size, paragraph spacing 2 times, letter spacing 0.12 times, and word spacing 0.16 times. Check loss and overlap; these are tolerances for user overrides, not mandatory default typography. |
| Target size | 2.5.8 AA uses 24 by 24 CSS px or its spacing, equivalent-control, inline, user-agent, or essential exceptions. Measure the effective clickable region, occlusion, and nearby targets. A 20 px icon inside a larger button is not a 20 px target. 44 by 44 CSS px belongs to enhanced 2.5.5 AAA, not a blanket AA minimum. |
| Gestures and motion | Provide applicable single-pointer alternatives to multipoint/path gestures and dragging. Preserve useful feedback with reduced motion. Check moving or auto-updating content, pause controls, flashing, and timing against the relevant criteria; disabling all animation alone does not establish compliance. |

## Forms, authentication, and recovery

Follow submission through invalid input, correction, pending state, success, and
failure as applicable. Users must identify the field, understand the error, reach
the correction, and know whether the action succeeded. Preserve usable values and
avoid redundant entry where 3.3.7 applies. For consequential submissions, check
the applicable error-prevention provisions, not just the label on the button.

Check timeout warnings and extension or recovery against the relevant exceptions.
For authentication, preserve password managers, autofill, and paste, including a
complete one-time code. Evaluate cognitive-function tests under 3.3.8 and its
alternatives or exceptions. Do not declare every CAPTCHA forbidden, or silently
remove authentication controls; identify a usable supported path.

## Evidence limits and primary references

Run automated checks on the actual reachable states, including dialogs and
errors. Confirm the engine, version, target rules, exclusions, and incomplete
checks. Keep required embedded payments, identity, or consent steps in the task
coverage; inaccessible cross-origin content remains unverified or a demonstrated
barrier. Attribution to a vendor is a remediation decision, not an exemption.

Sources checked 2026-10-04:

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- APG patterns: https://www.w3.org/WAI/ARIA/apg/patterns/
- Modal dialog: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- Contrast: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Target size: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Focus: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- Text spacing: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- Hover/focus: https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
- Authentication: https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html
