# Lesson artifacts

Read when building a workspace lesson, a reference document, an asset, or a visual
explanation.

## Choose the form

Prose is the default. Use a diagram for parts and the links between them, a
sequence over time, states, or a data path. Use an interactive element only when
the learner learns by changing one input and seeing the effect. Each step up costs
more to build and to check, so take the lowest one that carries the idea. A form
the learner asks for wins. In the conversation, draw diagrams as Mermaid or plain
text.

Build an interactive element around the one variable that drives the mechanism,
and show its consequences, including meaningful boundary cases. A decorative slider
or animation adds nothing. Keep the visual state, displayed values and answer
feedback consistent when inputs change or the learner resets.

Keep each example or view tied to the lesson's win. Use real names and
relationships when explaining a real system; label simplified models and invented
inputs. Put the explanation next to the visual it supports. Reveal a complex system
in steps when that helps, without a fixed number of diagrams.

## Make it usable

Besides what the Lessons section of SKILL.md requires, a lesson holds a worked
example and any exercises with their answer guidance. Link the shared stylesheet
and the components in `./assets/` with relative paths. Load scripts as classic scripts, not
ES modules: lessons open from disk without a server or build step, and browsers
such as Chrome block module scripts on pages opened from disk.

Give every visual a meaningful text alternative, readable labels and controls
usable from the keyboard. Motion explains change and respects reduced-motion
preferences. Reference documents also print cleanly.

## Check before delivery

Render the lesson from its file, as the learner will open it, with the available
browser tool (`playwright-cli` opens `file:` URLs when its configuration sets
`allowUnrestrictedFileAccess`). Use each control once and
check the console for errors. Check links, examples and expected
results. A diagram that does not render is worse than prose. Report which checks
ran: a syntax check, an execution, a visual inspection, or none. A render proves
the lesson displays, not that the learner learned from it.
