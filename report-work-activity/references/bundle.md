# Report bundle and helper interface

Read when preparing accepted records and rendering. Python 3.10+ with timezone
data is required; no packages, network or credentials are used by the helper.
Locate `scripts/activity_report.py` inside the loaded skill folder. Run it with
absolute paths; these invocation forms use explicit placeholders:

```text
python3 <skill>/scripts/activity_report.py window yesterday --timezone <IANA-zone>
python3 <skill>/scripts/activity_report.py window last-week --timezone <IANA-zone>
python3 <skill>/scripts/activity_report.py window last-month --timezone <IANA-zone>
python3 <skill>/scripts/activity_report.py window custom --timezone <IANA-zone> --start <YYYY-MM-DD> --end <exclusive-YYYY-MM-DD>
python3 <skill>/scripts/activity_report.py validate <accepted-report.json>
python3 <skill>/scripts/activity_report.py metrics <accepted-report.json>
python3 <skill>/scripts/activity_report.py build <accepted-report.json> --output <run-directory>/bundle
```

`window` supports `--now` with an offset timestamp for reproducibility and
`--week-start 0..6` (Monday..Sunday). Explicit report windows can use offset
timestamps for partial days. `validate`, `metrics` and `build` exit 0 on success
including valid empty results; invalid input, missing files and an existing output
directory exit 2 with an error. They never overwrite a prior bundle. A failed
build may leave a partial new directory; correct the error and use a new directory.
The helper validates structure and references, not the truth of supplied evidence.

Use the user's configured private report root, otherwise
`~/.local/share/work-activity`, resolving `~` to the actual home directory. Create
the root and `runs/<unique-run-id>/` with mode 0700. Persist verified identities
and container/repository classifications in `mappings.json` at that root, mode
0600, with provider/tenant, canonical ID, evidence and last verification time.
Repository exceptions take precedence over organization/container defaults.

Choose worker paths before delegation. Host scratch rules take precedence: in
a checkout, use its ignored `.tmp/report-work-activity/<run-id>/workers/` with
private permissions; verify exclusion first. Without a host scratch convention,
use the run's `workers/` sibling. Each child owns one source file; the primary
owns the accepted input and the new `bundle/` child. Carry retained findings into
the bundle before removing scratch. The builder rejects an existing bundle, not
the enclosing run directory. Do not use scratch as the only retained report or
put personal activity in tracked/public output. The renderer creates missing
ancestors with mode 0700 without changing existing ones, then the bundle and
subdirectories with mode 0700 and files with mode 0600. It escapes all source text,
uses an external stylesheet and makes only HTTP(S) source locators clickable.
It executes no JavaScript and fetches no external assets.

## Accepted input: schema version 1

Supply one JSON object. Strings are plain text, never HTML or pre-rendered Markdown.
Arrays exist even when empty. `tests/fixtures.py` is an executable synthetic
example for package checks, not a source of user data.

| Field | Meaning |
| --- | --- |
| `schema_version` | `1` |
| `title`, `scope_note`, `classification_note` | Report title, declared account/container coverage, and the confirmed mapping rules plus unresolved classifications. |
| `window` | `timezone`, `start`, `end`, `label` from the resolver; timestamps include offsets. |
| `as_of` | Offset timestamp no earlier than any retained retrieval/check or observed event. |
| `identities` | Verified namespace-qualified actor IDs/aliases; no display-name guesses or secrets. |
| `metrics` | Selected keys from `evidence.md`; use meaningful outcome measures rather than every available counter. |
| `sources` | One record per selected workstream/connection, including unavailable/excluded ones. |
| `evidence` | Minimal excerpts with stable locators and retrieval time. |
| `events` | Complete metadata inventory within declared scope plus clearly marked contextual candidates. |
| `stories` | Primary-written concise claims linked to evidence. |
| `obligations` | Current assignments, explicit promises, requests and suggestions, including checked terminal outcomes for follow-up. |

Every source has `id` (lowercase letters, digits, hyphens), `label`, `scope`,
`query`, `collected_at`, `notes`, `metrics`, `pages_exhausted` (boolean), and
`status`: `complete`, `partial`, `unavailable`, `excluded`, `failed` or `blocked`.
`complete` requires exhausted pagination and applies only to the stated scope.
Keep selected unavailable sources associated with their relevant metrics so they
cannot silently turn missing data into exact totals. Intentionally `excluded`
sources are outside the declared counting scope and must use `metrics: []`;
explain that exclusion in their notes and omit their event sightings from the
accepted ledger. The same event may still count through an included source.
`notes` records retention,
caps, authentication/access limitations, and obligation lookback. Include the
actual Luna provider/model/effort/task/status under `extraction` when run; the
manifest preserves this extra metadata. Never claim a worker ran from a template.

Every evidence item has `id`, `source`, `locator`, `excerpt`, `retrieved_at`.
The locator is a canonical URL, host record ID, or exact local path/line. Retain
only enough content to understand the deciding observation offline. Put the
source timestamp, actor and event status in the excerpt when they establish a
count. A link alone is not retained evidence.

Every event has:

- `id`: canonical native event identity, including provider tenant. Repeated
  connector sightings of the same event reuse it. Distinct reviews or transitions
  have distinct event IDs even when their `entity` is the same.
- `entity`: canonical PR, ticket, incident, commit, message or meeting occurrence.
  Cross-system incident aliases need explicit link evidence before sharing it.
- `source`, `kind`, `time` (offset timestamp, or null when unknown).
  Normalized `sources` retains every contributing source ID when sightings merge;
  preserve it when rebuilding a saved ledger. Input may omit it for one sighting.
- `actor`, `author`, `assignee`: namespace-qualified IDs, as supported; omitted or
  null when unknown. Assignee means at the completion event for its metric.
- `scope`: `work`, `open-source`, `personal` or `unclassified`; `repository`:
  canonical host/owner/repo or null for non-repository/multiple-repository work;
  `classification_reason`: the mapping evidence. Map before rendering.
- `title`, `detail`, `evidence` (nonempty IDs), `confirmed` (primary-accepted boolean).
  Optional `current_state` explains reopening, local-only status or other limits.

Countable `kind` values are `pr_merged`, `pr_opened`, `pr_review`, `ticket_closed`,
`incident_response`, `incident_resolved`, `commit_authored`, `email_sent`, and
`meeting_attended`. Other kinds can retain qualitative work or context but do not
enter those metrics. Unknown-time or unconfirmed candidates never count.
Identical events are deduplicated; conflicting identity/time/role/classification
or known current-state fields fail validation and must be reconciled. Normalize
duplicate titles, details and classification reasons to one accepted description;
different wording also fails instead of silently dropping a sighting. Evidence
and contributing sources are combined, independent of sighting order. Related
events remain distinct. Unknown attribution does not count and prevents an exact
total; `metrics.json` includes an `unattributed` count in the metric's own unit.

A story has `title`, `summary`, `scope`, `repository`, `evidence`, and optional
`events` containing event IDs. The primary verifies that its wording, scope and
period match the evidence; structural validation cannot prove those meanings.

An obligation has `id`, `title`, `detail`, `source`, `scope`, `repository`,
`evidence`, `checked_at`, `owner`, optional `due`, `kind` (`commitment`,
`assignment`, `request`, `suggestion`) and `status` (`open`, `done`, `cancelled`,
`unknown`). Commitments and assignments require a verified user owner. Put the
original promise/assignment and later status check in retained evidence. `due`
is a normalized date/instant or explicit source wording when unresolved, not an
invented deadline. Terminal items stay in details; only open/unknown items appear
on the main pending-work list.

## Outputs and follow-up

```text
index.html, styles.css       Concise report, metrics and pending work
details/<group-hash>.html    Per-repository/workstream stories, events and obligations
evidence.html               Readable excerpts and original locators
evidence/<source>.jsonl     Retained excerpts, IDs and retrieval times
manifest.json              Scope, period, snapshot and source coverage
report.json                Complete normalized input for follow-up/rebuilding
events.jsonl               Deduplicated event ledger
metrics.json               Computed counts, units and completeness
obligations.json           Obligations and checked outcomes
```

Keep concise source digests and deciding worker findings in event details/evidence;
preserve query/worker coverage in source records. The primary must carry forward
material contradictory or rejected claims with their reasons rather than saving
only positive findings. Full transcripts and raw provider payloads are unnecessary.

Counts are conservative: a partial relevant source makes that metric an observed
lower bound, even in repository rows. An unclassified candidate also prevents a
complete bucket total. If finer coverage is needed, split the collection scope
into separate reports rather than declaring a global result complete.

Open the generated page, follow a detail and evidence link, verify one work total
against repository rows, and check a narrow viewport. The main answer includes
the report path and material gaps. For later questions, read the retained files
before fetching again and distinguish the historical snapshot from live state.
