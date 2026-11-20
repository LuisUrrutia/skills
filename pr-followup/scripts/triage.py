#!/usr/bin/env python3
"""Decide whether a watch wake on the author's PR changed anything a Drive turn must judge."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

QUERY = """query($owner:String!,$repo:String!,$number:Int!,$after:String){repository(owner:$owner,name:$repo){pullRequest(number:$number){
  state isDraft headRefOid baseRefName mergeable mergeStateStatus reviewDecision %s}}}"""
THREADS = "reviewThreads(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id isResolved}}"
CHECKS = """commits(last:1){nodes{commit{oid statusCheckRollup{contexts(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{
  __typename ... on CheckRun{databaseId name status conclusion} ... on StatusContext{context state createdAt}}}}}}}"""


class TriageError(RuntimeError):
    pass


class GitHub:
    def __init__(self, host: str):
        self.host = host

    def call(self, endpoint: str, payload: dict | None = None):
        paginate = "per_page=100" in endpoint
        command = ["gh", "api", "--hostname", self.host, endpoint] + (["--input", "-"] if payload else [])
        command += ["--paginate", "--slurp"] if paginate else []
        result = subprocess.run(command, input=json.dumps(payload) if payload else "", capture_output=True,
                                text=True, timeout=120, env={**os.environ, "GH_PROMPT_DISABLED": "1"})
        if result.returncode:
            raise TriageError(f"GitHub request failed: {result.stderr.strip()}")
        value = json.loads(result.stdout)
        if isinstance(value, dict) and value.get("errors"):
            raise TriageError(f"GraphQL errors: {value['errors']}")
        return [item for page in value for item in page] if paginate else value


def parse_pr(url: str) -> dict:
    match = re.fullmatch(r"https://([^/]+)/([^/]+)/([^/]+)/pull/(\d+)/?", url)
    if not match:
        raise TriageError(f"not a pull request URL: {url}")
    host, owner, repo, number = match.groups()
    return {"url": f"https://{host}/{owner}/{repo}/pull/{number}", "host": host, "owner": owner,
            "repo": repo, "number": int(number)}


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def pages(api, variables: dict, connection: str, path) -> tuple[dict, list]:
    """Every node of one GraphQL connection, with the pull request read alongside its first page."""
    nodes, after, first = [], None, None
    while True:
        pr = api.call("graphql", {"query": QUERY % connection, "variables": {**variables, "after": after}})[
            "data"]["repository"]["pullRequest"]
        first = first or pr
        page = path(pr)
        if after and pr["headRefOid"] != first["headRefOid"]:
            raise TriageError("the PR head moved while it was read; run triage again")
        nodes += page["nodes"] if page else []
        if not page or not page["pageInfo"]["hasNextPage"]:
            return first, nodes
        after = page["pageInfo"]["endCursor"]


def snapshot(target: dict, actor: str, api) -> tuple[str, dict]:
    if (login := api.call("user").get("login")) != actor:
        raise TriageError(f"GitHub actor differs: gh authenticates as {login!r}; bind {actor}'s token to the command")
    variables = {"owner": target["owner"], "repo": target["repo"], "number": target["number"]}
    pr, checks = pages(api, variables, CHECKS, lambda pr: ((pr["commits"]["nodes"] or [{"commit": {}}])[0]["commit"]
                                                         .get("statusCheckRollup") or {}).get("contexts"))
    _, threads = pages(api, variables, THREADS, lambda pr: pr["reviewThreads"])
    rest = f"repos/{target['owner']}/{target['repo']}"
    inline = api.call(f"{rest}/pulls/{target['number']}/comments?per_page=100")
    reviews = api.call(f"{rest}/pulls/{target['number']}/reviews?per_page=100")
    conversation = api.call(f"{rest}/issues/{target['number']}/comments?per_page=100")
    # Check progress counts only as completed runs, identified so a rerun with the same result still counts: T3
    # wakes on failures, on the required gate and when all checks finish, and each can carry feedback or decide
    # readiness. Running states change no decision.
    seen = {
        "head": pr["headRefOid"], "base": pr["baseRefName"], "draft": pr["isDraft"],
        "conflicting": pr["mergeable"] == "CONFLICTING", "behind": pr["mergeStateStatus"] == "BEHIND",
        "decision": pr["reviewDecision"],
        "resolved": {t["id"]: t["isResolved"] for t in threads},
        "inline": {str(c["id"]): digest(c["body"]) for c in inline},
        "reviews": {str(r["id"]): digest([r["state"], r["body"]]) for r in reviews if r["state"] != "PENDING"},
        "conversation": {str(c["id"]): digest(c["body"]) for c in conversation},
        "completed_checks": sorted([c["name"], c["conclusion"], c["databaseId"]] if c["__typename"] == "CheckRun"
                                   else [c["context"], c["state"], c["createdAt"]]
                                   for c in checks if c.get("status", "COMPLETED") == "COMPLETED"
                                   and c.get("state") not in {"PENDING", "EXPECTED"}),
        "checks_pending": any(c.get("status", "COMPLETED") != "COMPLETED" or c.get("state") in {"PENDING", "EXPECTED"}
                              for c in checks),
    }
    return pr["state"], seen


def load(state_file: Path, target: dict, actor: str) -> dict:
    data = json.loads(state_file.read_text()) if state_file.exists() else {"pr": target["url"], "actor": actor}
    if data.get("pr") != target["url"] or data.get("actor") != actor:
        raise TriageError(f"state file belongs to {data.get('pr')} as {data.get('actor')}")
    return data


def triage(url: str, actor: str, state_file: Path, api=None) -> dict:
    target = parse_pr(url)
    data = load(state_file, target, actor)
    pr_state, seen = snapshot(target, actor, api or GitHub(target["host"]))
    if pr_state != "OPEN":
        return {"verdict": "stop", "reasons": [f"the PR is {pr_state.lower()}"]}
    if data.get("seen") != seen:
        return {"verdict": "act", "reasons": ["no Drive turn has judged this PR state"]}
    return {"verdict": "quiet", "reasons": []}


def record(url: str, actor: str, state_file: Path, api=None) -> dict:
    target = parse_pr(url)
    data = load(state_file, target, actor)
    data["seen"] = snapshot(target, actor, api or GitHub(target["host"]))[1]
    temporary = state_file.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(state_file)
    return {"recorded": data["seen"]["head"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("triage", "record"))
    parser.add_argument("--pr", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--state-file", required=True, type=Path)
    args = parser.parse_args()
    try:
        operation = triage if args.command == "triage" else record
        print(json.dumps(operation(args.pr, args.actor, args.state_file.resolve()), indent=2))
        return 0
    except (TriageError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"pr-followup triage stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
