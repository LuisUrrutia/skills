# Attach screenshots and recordings

Before selecting captures, read [visual evidence](visual-evidence.md) for capture
and provenance. [Publication](publication.md) owns identity and writes. Authorized PR create/update
includes relevant attachments. Draft-only prepares files/copy without uploading.

## Select the available route

Check `gh --version` and exact subcommand `--help` for `--attach`; prefer supported
`gh pr create/edit` uploads directly to the body. The documented route supports
GitHub.com/GHE.com, OAuth or classic/fine-grained PATs and WRITE/MAINTAIN/ADMIN
repository access; GHES and most GitHub App tokens are unsupported. Diagnose
permissions without exposing tokens; head and target rights can differ for forks.

If unavailable, try a host/browser attachment control for this PR or an established
reviewer-accessible repository asset location, preserving scope and visibility.
Otherwise report the exact capability/permission gap and retain captures. Do not
create a public upload service or install/upgrade tools as part of drafting.
`gh skill` manages skills, not PR images.

## Place and upload

Put actual saved captures in the prepared body's suitable section, with concise
captions and alt text stating what the reviewer should observe:

```markdown
After: validation remains beside the field.
![Visible validation message](.tmp/pr/after.png)
```

Substitute observed evidence. A missing baseline does not prevent attaching the
current-state capture. Markdown paths and attachment paths both resolve from
**gh's working directory**, not the body file's directory.

Add one `--attach <file>` per capture to the resolved create/edit command, keeping
its initial-state preference. For example:

```text
gh pr edit <exact-pr-url> --body-file .tmp/pr/body.md --attach .tmp/pr/after.png
```

`gh` replaces matching Markdown destinations with uploaded URLs, preserving alt
text; unreferenced files are appended. Prefer body references for precise placement.
For appended image alt text, quote the whole value: `--attach './screen.png#Error state'`.
Keep requested evidence in the description rather than posting an upload comment.

Maximum 50 files per invocation: PNG, JPG/JPEG, GIF, WebP, SVG, MP4, MOV and WebM;
use a reviewable subset. Videos take no `#alt` suffix. A standalone inline image
reference becomes the video player URL; use inline syntax or a normal link, not
reference-style video images. `--attach` conflicts with `--web` and create
`--dry-run`. A create dry-run can push: never use it for Draft-only.

## Verify and recover

After every upload attempt, including failure/timeout, read the exact body with
`gh pr view <url> --json url,body,headRefOid,baseRefName,isDraft`. Verify uploaded
URLs, surrounding text/captions, revision and PR state. Check embeds in an
authorized browser/host view for the intended audience; private PRs need no public
access. Report unavailable access/rendering evidence: upload alone proves neither.
Never invent an uploaded URL.

Uploads stop on the first failure; earlier uploads and PR creation/edit can
persist despite nonzero exit. Zero-upload creation can still push; edits can still
change metadata. Inspect actual state before retrying.

Use any returned exact PR URL; if identity is uncertain, perform exact-head
discovery before another create. Preserve successful remote URLs in a fresh body
and upload only missing files. Repair remaining local references or remove broken
embeds and explain unavailable evidence. Recheck head before reusing captures.

Later full-body rewrites retain verified remote URLs for unchanged captures,
without reverting to the local draft or reuploading. Replace stale evidence with
current captures or state the gap. Report uploaded, rendered, unavailable and
pending files separately.
