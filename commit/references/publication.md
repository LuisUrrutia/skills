# Publication

Verify branch and upstream with `git branch --show-current` and
`git status --short --branch`. Resolve the remote, repository and ref from the
requested destination or verified configuration: neither `origin` nor an upstream
proves the intended repository.

Verify SSH transport; use an explicit destination, publishing only the verified branch.
Tags need separate authority; plain force is prohibited. For a lease push after an
authorized rebase, continue through `pr` or `stacked-pr`; routine publication does
not rewrite remote history.

A failed push is `blocked`; report its exact command and concise error.
After success, inspect `git status --short --branch`, `git rev-parse HEAD` and
`git rev-parse @{u}`. Finish when the intended upstream contains the verified commit
and report ahead/behind state.

After material publication to an open PR, invoke `pr` in Update mode with the
verified head to rewrite its complete body from the published diff.
