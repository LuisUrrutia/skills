# Attach screenshots and recordings

Read when placing real visual evidence in a PR. [visual-evidence.md](visual-evidence.md)
owns what to capture and its provenance. [publication.md](publication.md) owns the
actor, exact PR, publication scope and metadata. Draft-only prepares files and
copy without uploading. An authorized PR create/update includes its relevant
attachments; do not ask again for that covered operation.

## Select the available route

Check `gh --version` and the exact command's `--help` for `--attach`. When supported,
prefer `gh pr create` or `gh pr edit` for attaching directly to the description.
The documented upload route supports GitHub.com and GHE.com tenants, with an OAuth
token or classic/fine-grained PAT and repository WRITE, MAINTAIN or ADMIN permission.
GHES and most GitHub App tokens are unsupported. Do not expose tokens while
diagnosing a permission failure; a fork contribution can have different rights
on the head and target repositories.

If the installed CLI or authentication cannot upload, use an available host/browser
attachment control for this PR, or the repository's established reviewer-accessible
asset location. Keep the same publication scope and visibility. If none works,
report the exact capability or permission gap and retain the capture. Do not create
a public upload service or install/update tools as a side effect of drafting a PR.
`gh skill` manages agent skills; it does not upload PR images.

## Place and upload

Inspect each actual saved capture for the intended state, revision and private
content. Keep a local record of scenario, revision, viewport and file so before
and after remain distinguishable. Use concise captions and useful alt text.

In the prepared body file, put local image references inside the repository's
suitable section. For example, when `gh` runs from the target project root:

```markdown
Before: the dialog hides its validation message.
![Validation message hidden](.tmp/pr/before.png)

After: the message remains visible next to the field.
![Validation message visible](.tmp/pr/after.png)
```

The paths in both Markdown and `--attach` resolve from `gh`'s working directory,
not from the body file's directory. Replace the example scenario and files with
the observed evidence. Include only the current-state image if there is no honest
baseline; a missing before capture does not prevent attaching the after capture.

Use the already resolved create command, or edit the exact PR URL, with one flag
per file. These are command shapes; substitute verified values and existing paths:

```text
gh pr create --repo <target> --base <base> --head <head> --draft --title <title> --body-file .tmp/pr/body.md --attach .tmp/pr/before.png --attach .tmp/pr/after.png
gh pr edit <pr-url> --body-file .tmp/pr/body.md --attach .tmp/pr/after.png
```

Keep the resolved initial state; omit `--draft` for a ready preference. `gh`
rewrites matching Markdown references to uploaded URLs and preserves their alt
text; an attached file not referenced in the body is appended. To supply alt text
for an appended image, quote the whole value: `--attach './screen.png#Error state'`.
For precise placement, prefer the body reference. Do not post a comment merely
to upload evidence when the requested destination is the description.

Up to 50 files are accepted per invocation: PNG, JPG/JPEG, GIF, WebP, SVG, MP4,
MOV and WebM. Keep the set small enough to review. Videos do not accept the `#alt`
suffix; a standalone inline image reference to a video becomes its player URL.
Use inline syntax or a normal link for a recording, not a reference-style video
image. `--attach` cannot be combined with `--web`, or with `gh pr create --dry-run`.
Draft-only never uses a create dry-run as a no-write substitute; it can push Git changes.

## Verify and recover

Read back the exact PR body after every upload attempt, even a nonzero exit or
timeout, using `gh pr view <pr-url> --json url,body,headRefOid,baseRefName,isDraft`.
Compare expected images with actual uploaded URLs and confirm surrounding text,
captions, revision and PR state. In an authorized browser/host view, check that the
embeds load for the intended repository audience. Do not require public access to
a private PR or invent an uploaded URL. Retain a rendering/access limitation when
the authenticated view is unavailable; upload success alone is not a visual check.

Uploads stop at the first failure. Earlier successful files can remain attached
and the PR can be created or edited even though the command exits nonzero. A create
with zero uploaded files can still have pushed the branch; an edit can still change
other metadata. Inspect what actually happened before deciding what to retry.

When a PR URL was returned, continue on that exact PR. If identity is uncertain,
use the exact-head discovery procedure before another create. Read the remote body,
preserve already uploaded URLs, and retry only missing attachments with a fresh
body file. Failed references can still be local paths: repair them on retry or
remove the broken embed and explain the unavailable evidence. Recheck the head
before reusing captures, so a concurrent change cannot make them stale.

On a later full-body rewrite, carry forward verified remote URLs for unchanged
captures. Do not overwrite them with the old local draft or upload the same files
again. Replace stale evidence with captures of the current revision, or state the
gap. Report which files are uploaded, rendered, unavailable or still pending.
