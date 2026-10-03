# Reuse and standardization

Read this when choosing how to standardize a capability, adopt an external skill,
or update a skill that delegates to one. Start with installed owners and the
user's candidate sources. Read their instructions and relevant dependencies before
choosing; similar descriptions do not establish equivalent behavior.

## Choose what to maintain

| Approach | Use when | Local responsibility |
| --- | --- | --- |
| Install unchanged | An existing skill fits the task, host, and authority | Select and validate the installed version |
| Wrap | The upstream procedure fits and needs only a small adapter | Invocation, inputs, local additions, and result checks |
| Derive | Useful ideas require changes throughout the procedure | The local implementation and relevant source changes |
| Create | No suitable implementation covers the requested capability | The new behavior and its validation |

Prefer the option with the least local behavior to maintain that still meets the
contract. An installed skill needs no wrapper merely to give it another name.
If a wrapper must replace the donor's scope, tools, ordering, authoring owner, or
external actions across several steps, compare a small derivation instead.

Record the choice and its concrete reason. Distinguish the skill's author or team
from the repository hosting it. Inspect licensing and notices before distributing
upstream files; a source citation does not replace required notices.

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

## Record sources and dependencies separately

Use `origin.txt` for actual external inspiration and dependencies. The skill's own
renames and superseded drafts belong in Git history. Record rejected candidates
in the decision report, not as active source feeds.

Use `[[sources]]` from [upstream-updates.md](upstream-updates.md) for ideas adapted
into local instructions. Use `[[dependencies]]` for runtime dependencies: a local
dependency records its registered name, role, and whether it is required; the host
resolves the name.
An installed upstream also records its repository, SSH remote, relevant paths,
approved full commit, installation or lockfile location, and local additions.
Distinguish the approved revision from the revision actually found in the host;
file presence alone does not verify invocation. Each owner tracks its direct
dependencies; callers do not copy its source manifest. Local dependencies are
maintained in their owning repository rather than fetched as upstream feeds.

## Update a dependency without maintaining a fork

On a requested check or update, resolve the current approved version and one
candidate version. Use the supported installer and version controls; do not fetch
a floating branch on each skill invocation.

Review changes that can affect the wrapper's contract: activation, inputs, outputs,
tools, newly loaded instructions, authority, and completion behavior. Follow moved
paths and changed references. Unrelated donor edits need no local merge or rewrite.
If the affected scope is unclear, widen inspection before claiming compatibility.

Exercise the wrapper and candidate together on a representative task and a nearby
case that should stay out of scope. Observe relevant side effects. In check mode,
report the candidate and evidence without changing the installation or approved
revision. In update mode, adopt the candidate only after the required checks pass;
preserve the working version when they fail. Record the tested revision and limits.

This reduces maintenance of copied instructions. It does not make dependency
updates automatically compatible or remove the need to verify local additions.
