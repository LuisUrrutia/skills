# Hooks and amend

## Resolve a commit attempt

Use the entrypoint's recorded baseline and post-attempt checks. Classify new
changes relative to that baseline before another write:

For a failed attempt with no new commit, the identity check is unchanged `HEAD`.
Retry requires this state. Apply the entrypoint's new-commit checks only when a
commit exists.

| Observed state | Action |
| --- | --- |
| Commit, message and boundary match; no new hook changes remain | Report `committed` with the short hash |
| Successful commit; hooks dirty only tracked files inside the boundary | Stage those exact paths and amend once with `--no-edit`; recheck |
| Failed commit; hooks changed only tracked files inside the boundary | Stage those exact paths and retry once; recheck |
| New outside-boundary, untracked, generated, lockfile, partially staged, ambiguous or not clearly hook-owned changes | Preserve them; report `blocked` with exact files and reason |
| `HEAD`, parent, message or committed diff mismatches the intended boundary/baseline | Report `blocked` with the mismatch |
| Hook rewrites recur after the permitted retry/amend | Report `blocked` |

The unsafe-change and mismatch rows take precedence over automatic retry/amend.

## Amend an existing commit

All conditions must hold:

1. This agent recorded the exact hash as successfully created in this task.
2. It remains `HEAD`, with no later commit or external branch change.
3. It is local and unpublished, verified against upstream state. If that cannot
   be proved, create a new commit.
4. The staged changes complete or correct the same atomic purpose. A new
   requirement or independently reviewable behavior gets a new commit.

Before amending, record hash, parent, message, complete parent diff, worktree state
and staged addition. Validate the updated boundary. Use `--amend --no-edit` only
when the message still describes it; otherwise supply the corrected message.

Verify one replacement `HEAD`, unchanged parent, accurate message and complete
parent diff, with outside work preserved. Report `amended`. The just-created
hook correction above and this current-task flow are the only amendment paths.
