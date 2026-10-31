# Private review profiles

Read when the target repository is known, before gathering intent. A private
profile holds review context a repository does not track: its stacks and seams,
accessible checkouts, blind spots, rule sources and their authority, tracker
setup, operational scope and findings that failed there before. Keep these
facts outside this package.

## Resolve

Identify the target `owner/repo`: a PR's URL, even for a fork checkout;
otherwise the repository the change will merge into. Ask when forks or several
remotes leave it ambiguous.

```bash
python3 <skill-dir>/scripts/resolve_profile.py <owner/repo>
```

The default directory is the first existing of `review-code-changes/profiles`,
`pr-review/profiles` and the legacy `pr-review-draft/profiles` under
`$XDG_CONFIG_HOME`, or `~/.config` when it is unset. When none exists, no
profile is configured. `--profiles-dir <dir>` selects another directory, which
must exist and be readable. Every `.md` file in the selected directory must be a
valid profile; keep versioned profiles in a private checkout and link the
default directory to it.

- `matched`: read the single exact match and name its source in Review basis.
- `none`: continue from repository evidence; derive seam scope.
- `ambiguous`: report the competing profile paths and resolve the identity conflict.
- `error` (nonzero exit): the directory or a profile is malformed or unreadable;
  its rules are unknown. Do not reinterpret that as `none`.

Matches are case-insensitive exact `owner/repo` values; related repositories get
separate profiles. Do not choose by filename or partial organization match.

## Use

Read Halves and Seams when opening seams, Checkouts when crossing repositories,
Blind spots for schemas and generated or vendored files, Rules for the guides
that govern the changed paths and their authority classes, Tracker for ticket
identity and access, Operational scope for reachability, and Findings that died
here when challenging candidates. Comment bindings and Author names serve callers
that publish.

Repository instructions and contracts govern domain behavior and override
drifted private facts. A profile supplies context, never permission to waive
required repository behavior. Revalidate historical facts on the reviewed
revision; missing decisive evidence becomes a question.

Workers receive only Halves, Blind spots, Operational scope and Findings that
died here, plus sanitized seams and the rules that apply. Checkouts, Tracker
access and personal bindings stay with the coordinator. Inspect what you share
for private access data; headings alone cannot prove a profile contains none.

For an authorized profile creation or repair, read
[profile-schema.md](profile-schema.md).
