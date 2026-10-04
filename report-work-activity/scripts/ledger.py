"""Validate accepted evidence and calculate explicitly defined activity metrics."""

from copy import deepcopy
import re
from zoneinfo import ZoneInfo

from period import instant


METRICS = {
    "authored_prs_merged": ("Your PRs merged", "pr_merged", "author", "entity"),
    "prs_merged_by_you": ("PRs you merged", "pr_merged", "actor", "entity"),
    "prs_opened": ("PRs opened", "pr_opened", "author", "entity"),
    "prs_reviewed": ("PRs reviewed", "pr_review", "actor", "entity"),
    "reviews_submitted": ("Reviews submitted", "pr_review", "actor", "id"),
    "tickets_closed": ("Tickets you closed", "ticket_closed", "actor", "entity"),
    "assigned_tickets_completed": ("Assigned tickets completed", "ticket_closed", "assignee", "entity"),
    "incidents_attended": ("Incidents attended", "incident_response", "actor", "entity"),
    "incidents_resolved": ("Incidents you resolved", "incident_resolved", "actor", "entity"),
    "commits_authored": ("Commits authored", "commit_authored", "author", "entity"),
    "emails_sent": ("Emails sent", "email_sent", "actor", "entity"),
    "meetings_attended": ("Meetings attended", "meeting_attended", "actor", "entity"),
}
SCOPES = ("work", "open-source", "personal", "unclassified")
STATUSES = ("complete", "partial", "unavailable", "excluded", "failed", "blocked")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strings(value, label, nonempty=False):
    require(isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value),
            f"{label} must be a list of nonempty strings")
    require(not nonempty or bool(value), f"{label} cannot be empty")


def text_fields(record, fields, label):
    require(isinstance(record, dict), f"{label} must be an object")
    for field in fields:
        require(isinstance(record.get(field), str) and record[field].strip(),
                f"{label}.{field} must be a nonempty string")


def scoped(record, label):
    require(record.get("scope") in SCOPES, f"{label}.scope is invalid")
    require(record.get("repository") is None or
            isinstance(record["repository"], str) and re.fullmatch(r"[^/\s:]+(?:/[^/\s]+){2,}", record["repository"]),
            f"{label}.repository must be null or host/namespace/repository")


def validate(data):
    require(isinstance(data, dict), "Report must be a JSON object")
    data = deepcopy(data)
    require(data.get("schema_version") == 1, "schema_version must be 1")
    text_fields(data, ("title", "as_of", "scope_note", "classification_note"), "report")
    window = data.get("window", {})
    text_fields(window, ("timezone", "start", "end", "label"), "window")
    ZoneInfo(window["timezone"])
    require(instant(window["start"]) < instant(window["end"]), "Window must have positive length")
    as_of = instant(data["as_of"])
    strings(data.get("identities"), "identities", True)
    strings(data.get("metrics"), "metrics")
    require(len(data["metrics"]) == len(set(data["metrics"])), "Duplicate selected metric")
    require(set(data["metrics"]) <= METRICS.keys(), "Unknown metric key")
    for key in ("sources", "evidence", "events", "stories", "obligations"):
        require(isinstance(data.get(key), list), f"{key} must be an array")
    sources = {}
    for source in data["sources"]:
        text_fields(source, ("id", "label", "scope", "query", "collected_at", "notes"), "source")
        require(re.fullmatch(r"[a-z0-9][a-z0-9-]*", source["id"]), "Unsafe source ID")
        require(source["id"] not in sources, "Duplicate source ID")
        require(source.get("status") in STATUSES, "Unknown source status")
        require(type(source.get("pages_exhausted")) is bool, "pages_exhausted must be boolean")
        require(source["status"] != "complete" or source["pages_exhausted"],
                "Complete retrieval requires exhausted pagination")
        require(instant(source["collected_at"]) <= as_of, "Source retrieval is after snapshot")
        strings(source.get("metrics"), "source.metrics")
        require(set(source["metrics"]) <= METRICS.keys(), "Unknown source metric")
        require(source["status"] != "excluded" or not source["metrics"],
                "Excluded sources are outside metric coverage and must declare metrics: []")
        sources[source["id"]] = source
    evidence = {}
    for item in data["evidence"]:
        text_fields(item, ("id", "source", "locator", "excerpt", "retrieved_at"), "evidence")
        require(item["id"] not in evidence, "Duplicate evidence ID")
        require(item["source"] in sources, "Evidence refers to an unknown source")
        require(instant(item["retrieved_at"]) <= as_of, "Evidence retrieval is after snapshot")
        evidence[item["id"]] = item

    def citations(record, label):
        strings(record.get("evidence"), f"{label}.evidence", True)
        require(set(record["evidence"]) <= evidence.keys(), f"{label} has dangling evidence")

    events = {}
    entity_groups = {}
    for event in data["events"]:
        text_fields(event, ("id", "entity", "source", "kind", "title", "detail", "classification_reason"), "event")
        scoped(event, "event")
        citations(event, "event")
        require(event["source"] in sources, "Unknown event source")
        strings(event.get("sources", []), "event.sources")
        event["sources"] = sorted(set(event.get("sources", []) + [event["source"]]))
        require(set(event["sources"]) <= sources.keys(), "Unknown contributing event source")
        require(all(sources[key]["status"] != "excluded" for key in event["sources"]),
                "Event cites an excluded source; remove that sighting or revise the declared scope")
        require(event.get("current_state") is None or isinstance(event["current_state"], str),
                "current_state must be text or null")
        group = (event["scope"], event.get("repository"))
        require(event["entity"] not in entity_groups or entity_groups[event["entity"]] == group,
                "One entity must have one counting group; reconcile cross-repository or classification conflicts")
        entity_groups[event["entity"]] = group
        require(type(event.get("confirmed")) is bool, "event.confirmed must be boolean")
        require("time" in event, "event.time must be present (null when unknown)")
        if event["time"] is not None:
            require(instant(event["time"]) <= as_of, "Activity event is after snapshot")
        for role in ("actor", "author", "assignee"):
            require(event.get(role) is None or isinstance(event[role], str) and event[role].strip(), f"Invalid {role}")
        if event["id"] in events:
            existing = events[event["id"]]
            fields = ("entity", "kind", "time", "scope", "repository", "actor", "author", "assignee", "confirmed", "title", "detail", "classification_reason")
            require(all(existing.get(k) == event.get(k) for k in fields),
                    f"Conflicting duplicate event: {event['id']}")
            existing["evidence"] = sorted(set(existing["evidence"] + event["evidence"]))
            existing["sources"] = sorted(set(existing["sources"] + event["sources"]))
            existing["source"] = existing["sources"][0]
            require(not existing.get("current_state") or not event.get("current_state") or
                    existing["current_state"] == event["current_state"],
                    f"Conflicting current state: {event['id']}")
            existing["current_state"] = existing.get("current_state") or event.get("current_state")
        else:
            events[event["id"]] = event
    data["events"] = list(events.values())
    for story in data["stories"]:
        text_fields(story, ("title", "summary"), "story")
        scoped(story, "story")
        citations(story, "story")
        strings(story.get("events", []), "story.events")
        require(set(story.get("events", [])) <= events.keys(), "Story has dangling event IDs")
    obligation_ids = set()
    for item in data["obligations"]:
        text_fields(item, ("id", "title", "detail", "source", "checked_at"), "obligation")
        require(item["id"] not in obligation_ids, "Duplicate obligation ID")
        obligation_ids.add(item["id"])
        scoped(item, "obligation")
        citations(item, "obligation")
        require(item["source"] in sources, "Unknown obligation source")
        require(item.get("kind") in ("commitment", "assignment", "request", "suggestion"), "Unknown obligation kind")
        require(item.get("status") in ("open", "done", "cancelled", "unknown"), "Unknown obligation status")
        require(instant(item["checked_at"]) <= as_of, "Obligation check is after snapshot")
        if item["kind"] in ("commitment", "assignment"):
            require(item.get("owner") in data["identities"], "Commitment/assignment requires a verified user owner")
        require(item.get("due") is None or isinstance(item["due"], str), "due must be text or null")
    return data


def in_window(event, window):
    return event["time"] is not None and instant(window["start"]) <= instant(event["time"]) < instant(window["end"])


def metric(data, key, scope, repository=None, total=False):
    label, kind, role, unit = METRICS[key]
    candidates = [e for e in data["events"] if e["kind"] == kind
                  and (e.get(role) is None or e.get(role) in data["identities"])
                  and (e["time"] is None or in_window(e, data["window"]))]
    selected = [e for e in candidates if e["scope"] == scope and (total or e.get("repository") == repository)]
    counted = {e[unit] for e in selected if e["confirmed"] and e.get(role) in data["identities"] and in_window(e, data["window"])}
    observed_sources = {source for e in candidates for source in e["sources"]}
    relevant = [s for s in data["sources"] if key in s["metrics"] or s["id"] in observed_sources]
    complete = bool(relevant) and all(s["status"] == "complete" and key in s["metrics"] for s in relevant)
    uncertain = any(not e["confirmed"] or e["time"] is None or e.get(role) is None for e in selected)
    unclassified = scope != "unclassified" and any(e["scope"] == "unclassified" for e in candidates)
    complete = complete and not uncertain and not unclassified
    return {"label": label, "count": len(counted), "complete": complete,
            "unattributed": len({e[unit] for e in selected if e.get(role) is None}),
            "display": str(len(counted)) if complete else f"{len(counted)} observed" if counted else "Unknown · 0 observed",
            "unit": "distinct reviews" if key == "reviews_submitted" else "distinct entities",
            "event_kind": kind, "user_role": role,
            "sources": [s["id"] for s in relevant]}


def groups(data):
    found = {(e["scope"], e.get("repository")) for key in ("events", "stories", "obligations") for e in data[key]}
    return sorted(found, key=lambda pair: (SCOPES.index(pair[0]), pair[1] or ""))


def metrics(data):
    return {
        "work_total": {key: metric(data, key, "work", total=True) for key in data["metrics"]},
        "groups": [{"scope": scope, "repository": repo,
                    "metrics": {key: metric(data, key, scope, repo) for key in data["metrics"]}}
                   for scope, repo in groups(data)],
    }
