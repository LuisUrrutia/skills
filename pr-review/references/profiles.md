# Repository rules and private profiles

Read at PR intake. The PR URL identifies its target `owner/repo`; a fork checkout's
`gh repo view` may identify a different repository. Capture the PR metadata first.
For a non-PR audit use `review-code-changes`, rather than guessing a review
target from remotes.

Repository-owned instructions and contracts are the authority for domain behavior.
Read existing AGENTS/task guides and linked review policy, if present. Creating
or changing another repository's policy is separate work. A private profile holds
local checkout/access details, tracker setup, personal wording bindings and
historical calibration. Do not bundle those facts in the portable skill.

Resolve the private overlay with this package's `scripts/resolve_profile.py`:

```bash
python3 "$SKILL_DIR/scripts/resolve_profile.py" "$TARGET_REPOSITORY"
```

The default location is `$XDG_CONFIG_HOME/pr-review/profiles`, or
`~/.config/pr-review/profiles` when XDG_CONFIG_HOME is unset. When that directory
is absent, the legacy `pr-review-draft/profiles` beside it is used. An absent default
means no configured profile. An explicit `--profiles-dir "$PRIVATE_PROFILES"`
selects a different private directory and must exist and be readable.

Keep versioned profiles in a private checkout and link the default directory to
that folder, or pass it through `--profiles-dir`. Every `.md` file in the selected
directory must be a valid profile; keep folder documentation outside it.

- `matched`: read the single exact target match and name its source in the brief.
- `none`: continue a generic review from repository evidence; derive seam scope.
- `ambiguous`: report the competing profile paths and resolve the identity conflict.
- `error` (nonzero exit): the supplied directory/profile is malformed or unreadable;
  its rules are unknown. Do not reinterpret that as `none`.

Matches are case-insensitive exact `owner/repo` values; related repositories get
separate bindings. A malformed candidate profile is an error even if no match can
be determined. Do not silently choose a filename or partial organization match.

Read a resolved profile's Halves and Seams while opening boundaries; Checkouts
when crossing repositories; Blind spots for schemas and generated/vendored files;
Tracker for ticket identity/access; Operational scope for reachability; Findings
that died here when challenging candidates; Comment bindings for wording.
Revalidate historical facts on the recorded revision. Repository rules govern a
conflict with personal preferences; missing decisive evidence becomes a question.

Only Halves, Blind spots, Operational scope and Findings that died here are
filtered into the shared packet. The parent supplies sanitized seam definitions
and any applicable domain rules in the context/shared rule files. Keep account,
checkout-access, tracker and personal voice details with the parent. Inspect the
filtered packet for private access data before dispatch; headings alone cannot
prove that a poorly organized profile contains none.

For an authorized profile creation or repair, read
[profile-schema.md](profile-schema.md). No profile is required for a generic review.
