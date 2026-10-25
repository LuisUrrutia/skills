# Seam sweep

The parent reads this after opening seam scope in the brief and while independent
workers review the frozen PR. A seam connects the changed side to another stack,
generated contract or repository. Workers stop at explicitly caller-owned seams;
the parent records both sides at exact revisions.

For in-repo counterparts, use the PR head for the same-version comparison. Read relevant generated/vendored files
and provenance, including ignored contracts when accessible. A readable committed
proxy can settle a claim only when its provenance supports the relationship.
For external counterparts, resolve the intended merged default branch to a SHA,
unless the caller supplies another authoritative comparison. A linked PR's last
commit or body does not prove the change shipped.

Use the profile's Checkouts section or verified inventory to find accessible
copies, following host checkout-ownership rules. Read without switching or editing
them. If source retrieval is needed, use the authorized API/SSH transport at the
recorded SHA. A 404 can mean access failure, a wrong revision or a missing path;
it does not by itself identify which. Preserve authentication and distinguish
unknown from absent.

For an operation both sides perform, such as a delete or a status change, compare
its semantics as well as its shapes: soft or hard, reversible or not, and what
each side keeps. When that comparison shows a field removed, renamed or newly
required, and the profile or the repository's deploy configuration shows a window
in which the two sides run different versions, such as separate deploys, a
rolling rollout or a client that keeps an old build, also compare each side at the
base revision with the other side at the head, in both directions; each direction
is its own row and names its window. For each opened row, record:

- `matches`: the contract, revisions and evidence on both sides; a path-triggered
  change with no contract effect can explain that finding here.
- `gap`: the incompatibility, both revision-specific locations and where a fix belongs.
- `unreadable`: the exact missing repository, revision, path, permission or check.

Only an evidenced gap becomes a candidate. A decisive unknown stays a question.
A skew gap is evidenced when the old side reads or sends the changed field; it is
a candidate, not a question. It is a defect when its window can outlast a release,
such as a separately deployed or rolled-back side or an old client build still
running, or when what it writes outlasts the window; otherwise, when only the
rollout of a release that ships both sides opens it, it is an optional
improvement. An earlier PR that shipped the same pattern is not a recorded
decision. The remedy is an overlap release that accepts or emits both shapes, or
a deploy order enforced where deploys are driven; a PR-body statement of order is
a claim to verify there.
Every opened seam needs a verdict; an empty set needs the brief's explicit reason.
