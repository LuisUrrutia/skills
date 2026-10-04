"""Render an offline report and evidence bundle from a validated ledger."""

import hashlib
from html import escape
import json
from pathlib import Path
from urllib.parse import urlsplit

from ledger import SCOPES, groups, in_window, metrics


def h(value):
    return escape(str(value), quote=True)


def anchor(value):
    return hashlib.sha256(str(value).encode()).hexdigest()[:20]


def detail_name(scope, repository):
    return f"{scope}-{anchor(repository)}.html"


def source_link(locator):
    parsed = urlsplit(locator)
    if parsed.scheme in ("http", "https") and parsed.netloc and not parsed.username and not parsed.password:
        return f'<a href="{h(locator)}" rel="noreferrer">{h(locator)}</a>'
    return f"<code>{h(locator)}</code>"


def refs(ids, prefix=""):
    return " ".join(f'<a href="{prefix}evidence.html#{anchor(item)}">Evidence {index + 1}</a>'
                    for index, item in enumerate(ids))


def document(title, content, prefix=""):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; base-uri 'none'; form-action 'none'">
<title>{h(title)}</title><link rel="stylesheet" href="{prefix}styles.css"></head>
<body><a class="skip" href="#main">Skip to report</a><main id="main">{content}</main></body></html>'''


def write_file(path, text):
    path.write_text(text, encoding="utf-8")
    path.chmod(0o600)


def write_json(path, value):
    write_file(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def obligation_list(items, prefix=""):
    if not items:
        return '<p class="muted">No open items observed in the checked sources. See coverage.</p>'
    return '<ul class="items">' + "".join(
        f'<li><span class="tag">{h(item["kind"])} · {h(item["status"])}</span>'
        f'<h3>{h(item["title"])}</h3><p>{h(item["detail"])}</p>'
        f'<p class="meta">{h(item["scope"])} · {h(item.get("repository") or "Non-repository / multiple repositories")} · '
        f'Owner: {h(item.get("owner") or "Unconfirmed")} · Due: {h(item.get("due") or "Not established")} · '
        f'Checked {h(item["checked_at"])}</p><p>{refs(item["evidence"], prefix)}</p></li>' for item in items
    ) + "</ul>"


def build(data, destination):
    destination = Path(destination)
    for parent in reversed(destination.parents):
        parent.mkdir(mode=0o700, exist_ok=True)
    destination.mkdir(mode=0o700, exist_ok=False)
    for child in ("details", "evidence"):
        (destination / child).mkdir(mode=0o700)
    stylesheet = Path(__file__).resolve().parent.parent / "assets" / "report.css"
    write_file(destination / "styles.css", stylesheet.read_text(encoding="utf-8"))
    computed = metrics(data)
    write_json(destination / "report.json", data)
    write_json(destination / "metrics.json", computed)
    write_json(destination / "obligations.json", data["obligations"])
    write_json(destination / "manifest.json", {k: data[k] for k in
        ("schema_version", "title", "window", "as_of", "scope_note", "classification_note", "sources")})
    write_file(destination / "events.jsonl", "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in data["events"]))
    for source in data["sources"]:
        write_file(destination / "evidence" / (source["id"] + ".jsonl"), "".join(
            json.dumps(e, ensure_ascii=False) + "\n" for e in data["evidence"] if e["source"] == source["id"]))

    evidence_content = '<a href="index.html">← Report</a><h1>Evidence retained with this report</h1>'
    for item in data["evidence"]:
        evidence_content += (f'<article id="{anchor(item["id"])}"><h2>{h(item["id"])}</h2>'
                             f'<p>{h(item["excerpt"])}</p><p>{source_link(item["locator"])}</p>'
                             f'<p class="meta">{h(item["source"])} · Retrieved {h(item["retrieved_at"])}</p></article>')
    write_file(destination / "evidence.html", document("Evidence", evidence_content))

    for scope, repo in groups(data):
        label = repo or "Non-repository / multiple repositories"
        body = f'<a href="../index.html">← Report</a><p class="eyebrow">{h(scope)}</p><h1>{h(label)}</h1>'
        for story in data["stories"]:
            if (story["scope"], story.get("repository")) == (scope, repo):
                body += f'<article><h2>{h(story["title"])}</h2><p>{h(story["summary"])}</p><p>{refs(story["evidence"], "../")}</p></article>'
        body += "<h2>Activity and context</h2>"
        for event in data["events"]:
            if (event["scope"], event.get("repository")) != (scope, repo):
                continue
            timing = "In period" if in_window(event, data["window"]) else "Outside period / time unknown"
            certainty = "Verified" if event["confirmed"] else "Provisional"
            metadata = " · ".join(str(value) for value in
                                  (event["kind"], event["time"] or "Unknown time", event.get("current_state")) if value)
            body += (f'<article><span class="tag">{timing} · {certainty}</span><h3>{h(event["title"])}</h3>'
                     f'<p>{h(event["detail"])}</p><p class="meta">{h(metadata)}</p>'
                     f'<p>{refs(event["evidence"], "../")}</p></article>')
        body += "<h2>Obligations and their recorded outcomes</h2>" + obligation_list(
            [o for o in data["obligations"] if (o["scope"], o.get("repository")) == (scope, repo)], "../")
        write_file(destination / "details" / detail_name(scope, repo), document(label, body, "../"))

    window = data["window"]
    content = f'<header><p class="eyebrow">Activity report</p><h1>{h(data["title"])}</h1>'
    content += f'<p class="period">{h(window["label"])} · {h(window["timezone"])}</p>'
    content += f'<p>{h(data["scope_note"])}</p><p class="meta">Snapshot: {h(data["as_of"])}</p></header>'
    content += '<nav aria-label="Report sections"><a href="#work">Work</a><a href="#open-source">Open source</a><a href="#pending">Pending work</a><a href="#coverage">Coverage</a><a href="evidence.html">Evidence</a></nav>'
    content += '<aside><strong>How to read the numbers.</strong> Counts cover the declared sources. “Observed” is a lower bound; “Unknown” means there is no complete count. PRs, tickets and incidents are different units.</aside>'
    for scope in SCOPES:
        rows = [row for row in computed["groups"] if row["scope"] == scope]
        if not rows and scope not in ("work", "open-source"):
            continue
        title = {"work": "Work", "open-source": "Open source", "personal": "Personal", "unclassified": "Needs classification"}[scope]
        content += f'<section id="{scope}"><h2>{title}</h2>'
        if scope == "work":
            content += '<div class="metrics">' + "".join(
                f'<div class="metric"><strong>{h(value["display"])}</strong><span>{h(value["label"])}</span></div>'
                for value in computed["work_total"].values()) + "</div>"
        for story in data["stories"]:
            if story["scope"] == scope:
                content += (f'<article class="story"><p class="eyebrow">{h(story.get("repository") or "Non-repository work")}</p>'
                            f'<h3>{h(story["title"])}</h3><p>{h(story["summary"])}</p>'
                            f'<a href="details/{detail_name(scope, story.get("repository"))}">Read details →</a></article>')
        if rows:
            content += '<div class="table-wrap"><table><caption>Counts by repository or workstream</caption><thead><tr><th scope="col">Repository / workstream</th>'
            content += "".join(f'<th scope="col">{h(computed["work_total"][key]["label"])}</th>' for key in data["metrics"]) + "</tr></thead><tbody>"
            for row in rows:
                content += f'<tr><th scope="row"><a href="details/{detail_name(scope, row["repository"])}">{h(row["repository"] or "Non-repository / multiple repositories")}</a></th>'
                content += "".join(f'<td>{h(row["metrics"][key]["display"])}</td>' for key in data["metrics"]) + "</tr>"
            content += "</tbody></table></div>"
        else:
            content += '<p class="muted">No activity observed in the checked sources. See coverage.</p>'
        content += "</section>"
    content += '<section id="pending"><h2>Pending work</h2><p>Assignments and explicit promises are separate from requests and suggestions. Status is a snapshot.</p>'
    content += obligation_list([o for o in data["obligations"] if o["status"] in ("open", "unknown")]) + "</section>"
    content += '<section id="coverage"><h2>Coverage and counting rules</h2>'
    content += f'<p>{h(data["classification_note"])}</p><p class="meta">Exact interval: {h(window["start"])} ≤ event time &lt; {h(window["end"])}</p>'
    for source in data["sources"]:
        content += (f'<article><h3>{h(source["label"])} <span class="tag">{h(source["status"])}</span></h3>'
                    f'<p>{h(source["scope"])}</p><p>{h(source["notes"])}</p>'
                    f'<details><summary>Query and retrieval evidence</summary><p>{h(source["query"])}</p>'
                    f'<p>Collected {h(source["collected_at"])} · Pagination exhausted: {h(source["pages_exhausted"])}</p></details></article>')
    content += '<p><a href="manifest.json">Manifest</a> · <a href="metrics.json">Computed metrics</a> · <a href="report.json">Accepted report data</a> · <a href="events.jsonl">Event ledger</a> · <a href="obligations.json">Obligations</a></p></section>'
    content += '<footer>Saved evidence supports follow-up without repeating collection. Refresh named items before relying on their current status.</footer>'
    write_file(destination / "index.html", document(data["title"], content))
    return destination / "index.html"
