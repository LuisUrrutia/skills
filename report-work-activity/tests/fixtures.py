"""Synthetic report fixture; run directly to emit input for the report helper."""

import json


def example():
    snapshot = "2026-10-04T12:00:00+02:00"
    user = "github:example-user"
    data = {
        "schema_version": 1,
        "title": "September, in perspective",
        "scope_note": "Synthetic example · Fictional organizations, events and evidence. This is not a report of your actual activity.",
        "classification_note": "Acme is work, including its public SDK. Community repositories are open source. Classification is explicit; repository visibility is not used.",
        "window": {"timezone": "Europe/Madrid", "start": "2026-09-01T00:00:00+02:00", "end": "2026-10-01T00:00:00+02:00", "label": "September 2026"},
        "as_of": snapshot,
        "identities": [user, "linear:example-user", "slack:example-user", "mail:example-user", "incident:example-user"],
        "metrics": ["authored_prs_merged", "prs_reviewed", "tickets_closed", "incidents_attended", "incidents_resolved"],
        "sources": [], "evidence": [], "events": [], "stories": [], "obligations": [],
    }

    def source(key, label, metric_keys, status="complete", notes="Synthetic fixture inventory; all declared pages supplied."):
        data["sources"].append({"id": key, "label": label, "scope": "Fictional accounts and projects in this fixture only", "query": "Synthetic September events and current open assignments", "collected_at": snapshot, "notes": notes, "metrics": metric_keys, "pages_exhausted": status == "complete", "status": status})

    source("github-owned", "GitHub · authored PRs", ["authored_prs_merged", "prs_merged_by_you", "prs_opened"])
    source("github-reviews", "GitHub · reviews", ["prs_reviewed", "reviews_submitted"])
    source("linear", "Linear · tickets and assignments", ["tickets_closed", "assigned_tickets_completed"])
    source("incidents", "Incident timeline", ["incidents_attended", "incidents_resolved"])
    source("slack", "Slack · decisions and commitments", [], "partial", "Only the fictional platform channel is included; older unresolved promises may exist elsewhere.")
    source("agent-chats", "Agent conversations", [], "complete", "Synthetic selected messages include a resumed session and a later correction; session creation is outside September.")
    source("calendar", "Calendar · scheduled meetings", ["meetings_attended"])
    source("gmail", "Gmail · sent mail", ["emails_sent"])
    source("outlook", "Outlook", ["emails_sent"], "unavailable", "No Outlook connector was supplied to this synthetic run.")
    source("granola", "Granola", ["meetings_attended"], "unavailable", "No meeting notes were available to corroborate attendance.")

    def event(key, src, kind, scope, repo, title, detail, **fields):
        data["evidence"].append({"id": key, "source": src, "locator": f"https://example.invalid/evidence/{key}", "excerpt": detail, "retrieved_at": snapshot})
        row = {"id": key, "entity": key, "source": src, "kind": kind, "time": "2026-09-20T10:00:00+02:00", "title": title, "detail": detail, "scope": scope, "repository": repo, "classification_reason": "Explicit synthetic ownership map", "evidence": [key], "confirmed": True, **fields}
        data["events"].append(row)
        return row

    for repo, count, scope in [("acme/platform", 12, "work"), ("acme/public-sdk", 8, "work"), ("community/cli", 3, "open-source"), ("community/widgets", 2, "open-source")]:
        for number in range(1, count + 1):
            event(f"github:{repo}:{number}:merge", "github-owned", "pr_merged", scope, repo,
                  f"{repo} PR {number}", f"Synthetic merge record: {repo} PR {number}, authored by example-user and merged by a teammate on September 20. No deployment evidence is supplied.",
                  entity=f"github:{repo}:pr:{number}", author=user, actor="github:teammate")
    for number in range(1, 5):
        event(f"github:review:{number}", "github-reviews", "pr_review", "work", "acme/platform", "Review of retry behavior",
              "Submitted review by example-user on September 20; the fourth submission revisits the first PR.", actor=user,
              entity=f"github:acme/platform:pr:{100 + ((number - 1) % 3)}")
    for number in range(1, 4):
        event(f"linear:{number}:closed", "linear", "ticket_closed", "work", "acme/platform", f"PLAT-{number}: reliability follow-up",
              "Synthetic status history confirms that example-user completed this ticket on September 20.", actor="linear:example-user", assignee="linear:example-user",
              entity=f"linear:PLAT-{number}", current_state="Reopened on October 2; assigned to you" if number == 3 else "Done")
    for number in (1, 2):
        event(f"incident:{number}:response", "incidents", "incident_response", "work", None, f"INC-{number}: investigated service degradation",
              "The incident timeline records your investigation and mitigation action, rather than only an on-call assignment.", actor="incident:example-user", entity=f"incident:INC-{number}")
    event("incident:1:resolved", "incidents", "incident_resolved", "work", None, "INC-1: service recovered",
          "The timeline attributes resolution to you. INC-2 was resolved by another responder, so only one resolution is credited here.", actor="incident:example-user", entity="incident:INC-1")
    event("slack:promise", "slack", "message_sent", "work", "acme/platform", "Committed to the retry proposal",
          "September 23: I will write the retry proposal by October 6. October 4 thread check: no cancellation or completion; owner is example-user.", actor="slack:example-user")
    event("chat:resumed:message", "agent-chats", "assisted_work", "work", "acme/platform", "Investigated a retry race with an agent",
          "Session created in August, resumed September 20. The agent reproduced a retry race in a local fixture. A later message clarifies that the fix was not deployed; this is investigation evidence, not another merged PR.", actor=user)
    event("calendar:planning:occurrence", "calendar", "meeting_scheduled", "work", None, "Planning meeting on the calendar",
          "The invitation was accepted. No attendance log or attributable meeting notes were available, so attendance and duration are unconfirmed.", confirmed=False)
    for number in (1, 2):
        event(f"gmail:sent:{number}", "gmail", "email_sent", "work", None, "Sent a rollout coordination email",
              "Synthetic Sent message from the verified user alias, sent September 20; not a draft or quoted incoming message.", actor="mail:example-user")
    data["stories"] = [
        {"scope": "work", "repository": "acme/platform", "title": "Advanced the platform reliability work", "summary": "Twelve authored PRs merged, three other PRs received your reviews, and you completed three tickets. One ticket reopened in October and is back in your pending work. The agent-assisted retry investigation remained local.", "evidence": ["github:acme/platform:1:merge", "linear:3:closed", "chat:resumed:message"]},
        {"scope": "work", "repository": "acme/public-sdk", "title": "Completed eight SDK changes for work", "summary": "The SDK is public, but its eight merged PRs belong to work because Acme owns the project. They are included in the work total of 20.", "evidence": ["github:acme/public-sdk:1:merge"]},
        {"scope": "work", "repository": None, "title": "Responded to two incidents", "summary": "You helped investigate and mitigate two service incidents. One resolution is attributable to you; the other was completed by a teammate. Sent mail also records rollout coordination. Calendar entries alone do not establish meeting attendance.", "evidence": ["incident:1:response", "incident:2:response", "incident:1:resolved", "calendar:planning:occurrence"]},
        {"scope": "open-source", "repository": "community/cli", "title": "Improved the community CLI", "summary": "Three authored PRs merged in this repository. Their contribution is kept separate from your work activity.", "evidence": ["github:community/cli:1:merge"]},
        {"scope": "open-source", "repository": "community/widgets", "title": "Completed two widget changes", "summary": "Two authored PRs merged in this repository, with individual evidence retained in the detail page.", "evidence": ["github:community/widgets:1:merge"]},
    ]
    data["obligations"] = [
        {"id": "promise:retry", "source": "slack", "kind": "commitment", "status": "open", "owner": "slack:example-user", "scope": "work", "repository": "acme/platform", "title": "Write the retry proposal", "detail": "An explicit promise in your own message; still open at the thread check.", "due": "2026-10-06", "checked_at": snapshot, "evidence": ["slack:promise"]},
        {"id": "assignment:PLAT-3", "source": "linear", "kind": "assignment", "status": "open", "owner": "linear:example-user", "scope": "work", "repository": "acme/platform", "title": "Revisit PLAT-3", "detail": "The September completion remains in the historical count. The ticket reopened on October 2 and is currently assigned to you.", "due": None, "checked_at": snapshot, "evidence": ["linear:3:closed"]},
    ]
    for key in ("events", "stories", "obligations"):
        for record in data[key]:
            if record["repository"]:
                record["repository"] = "github.com/" + record["repository"]
    return data


if __name__ == "__main__":
    print(json.dumps(example(), indent=2))
