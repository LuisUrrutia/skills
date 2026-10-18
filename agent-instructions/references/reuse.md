# Reuse and standardization

Read this when choosing how to standardize a capability or adopt an external
skill. Start with installed owners and the user's candidate sources. Read their
instructions and relevant dependencies before choosing; similar descriptions do
not establish equivalent behavior.

## Choose what to maintain

| Approach | Use when | Local responsibility |
| --- | --- | --- |
| Install unchanged | An existing skill fits the task, host, and authority | Select and validate the installed version |
| Wrap | The upstream procedure fits and needs only a small adapter | Invocation, inputs, local additions, and result checks |
| Base | One upstream skill fits the goal and stays recognizable after local corrections | The deviations and their reasons; upstream changes are adopted by default |
| Derive | Useful ideas require changes throughout the procedure | The local implementation and relevant source changes |
| Create | No suitable implementation covers the requested capability | The new behavior and its validation |

Prefer the option with the least local behavior to maintain that still meets the
contract. An installed skill needs no wrapper merely to give it another name.
If a wrapper must replace the donor's scope, tools, ordering, authoring owner, or
external actions across several steps, compare a base or a small derivation
instead.

Record the choice and its concrete reason with `skill-maintenance`. Distinguish
the skill's author or team from the repository hosting it. Inspect licensing and
notices before distributing upstream files; a source citation does not replace
required notices.

## Keep wrappers thin

Resolve the real installed identity and supported invocation mechanism. State the
inputs handed over, expected output, local additions, and completion checks. Keep
the upstream implementation managed by its installer or package manager; editing
it in place turns an adapter into a maintained fork.

Preserve the active user's authority and host rules. A wrapper's prose is not a
sandbox and does not guarantee it overrides contradictory downstream instructions.
Choose a compatible dependency or an explicit derivation when conflicts persist.

Verify required dependencies before dependent work and report an unavailable one
with the prepared inputs. Do not pretend an absent skill ran or silently substitute
a different procedure. Avoid two automatic entrypoints competing for the same
request; use the host's supported selection and dependency controls.
