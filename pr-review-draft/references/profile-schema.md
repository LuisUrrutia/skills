# External profile schema

Read only when the user asks to create a private profile, or a configured profile
needs repair. Save it in the selected private profiles directory, outside this
package. The skill contains no live organization example or machine-specific path.

`Matches` is required, with one exact current target identity. Other sections are
optional; omit absent information rather than suggesting it was checked. Bind
related repositories separately. Verify claims from their sources and record dates,
revisions and applicability. Repository instructions override drifted private facts.

```markdown
# Example review profile

## Matches

| Repository | Status |
| --- | --- |
| `example-org/service` | current |

## Halves

`api/` publishes the contract consumed by `web/`.
Source: root architecture guide at the reviewed revision.

## Seams

| Diff touches | Kind | Trace into | Read it at | Where a fix lands |
| --- | --- | --- | --- | --- |
| `api/**` | in-repo | `web/` callers | PR head | this PR |

## Blind spots

Generated clients are derived from the committed API schema. Read its provenance
before treating a generated mismatch as a defect.
```

The full vocabulary is:

- **Matches**: exact target `owner/repo`, not a fork, old alias or a related service.
- **Checkouts**: private discovery/access conventions and intended accounts. Do not
  include credential values. Keep this section with the parent.
- **Halves**: stacks and the applications or services they serve.
- **Seams**: directional table above. In-repo counterparts use the PR head;
  external counterparts normally use a resolved merged default-branch SHA.
  Trigger on paths; the sweep decides whether a contract actually changed.
- **Blind spots**: unreadable/generated sources, authoritative proxies and the
  evidence behind calibration claims. They guide tracing, not blanket dismissal.
- **Tracker**: valid project prefixes, retrieval method and where decisions live.
  Keep access details with the parent; sanitize retrieved requirements for workers.
- **Operational scope**: evidenced populations and workflows. Personal tolerance
  for an edge case cannot silently waive a required behavior.
- **Comment bindings**: explicitly stated language familiarity, voice and local
  naming/convention preferences for `comment-style`. Required/optional status
  and certainty survive question phrasing.
- **Findings that died here**: a candidate shape, the evidence that defeated it,
  and its revision. Recheck that evidence; history does not predetermine a verdict.

A separate repository review-policy document is useful only when the repository
needs one and creating it is authorized. Do not migrate private access/history
facts into tracked project docs as a side effect of reviewing a PR.
