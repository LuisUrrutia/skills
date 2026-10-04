# Trace the relevant history

Read this when Git history is available for the decision. Use the existing
checkout and inspection commands; do not switch branches to read an old version.
Use only a repository that belongs to the permitted target. An exported snapshot
inside another checkout does not authorize reading that checkout's index or
history. If the supplied scope excludes historical records, work from the supplied
files and report that limit without probing surrounding repositories.

Locate the actual decision before assigning a motive to a commit. Blame identifies
the last edit to a line, which may be a move, formatter run, or copied pattern.
Read patches and earlier versions to find when the behavior entered the system
and when its rationale changed. Useful searches include:

```sh
git blame -L <start>,<end> -- <file>
git log --follow --format=fuller -p -- <file>
git log -S '<literal>' -p -- <path>
git log -G '<pattern>' -p -- <path>
git show <commit> -- <path>
git show <commit>:<path-at-that-revision>
```

`--follow` follows one file at a time; string and pattern searches limited to its
current path may miss a previous path. Follow verified renames or widen the path
scope when the relevant origin lies elsewhere. A deleted rationale may survive
in the introducing version, even when the current file has no explanation.

Read the substantive change and its contemporaneous records. A formatter commit,
squash message, bot label, or copied implementation is a lead, not an explanation.
For linked PRs, inspect the body, relevant inline review threads, conversation,
and recorded outcome. A summary of submitted reviews need not include the inline
discussion. Resolve the actual repository and PR association rather than
inventing a URL from a number alone.

Use explicit repository arguments for remote reads when checkout context could
select the wrong repository. Follow linked issues or decision documents when
they explain a constraint, rejected option, or later reversal. Do not replace
missing historical documentation with today's external API behavior.

Check coverage before reporting an origin as complete. A shallow clone, unavailable
object, squash, imported snapshot, or failed remote lookup limits what can be
established. Retrieve missing history only through permitted Git access; otherwise
describe the available range and continue independent evidence. Preserve HEAD,
the index, and working files. Record a failed lookup as unavailable, not as an
empty search or proof that the discussion never existed.
