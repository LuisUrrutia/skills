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
  state isDraft headRefOid baseRefName mergeable mergeStateStatus reviewDecision
  reviewThreads(last:100){nodes{id isResolved comments(last:100){nodes{id body}}}}
  reviews(last:100){nodes{id state body}}
  comments(last:100){nodes{id body}}
  commits(last:1){nodes{commit{%s}}}}}}"""
CHECKS = """oid statusCheckRollup{contexts(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{
  __typename ... on CheckRun{name status conclusion} ... on StatusContext{context state}}}}"""
CHECKS_QUERY = """query($owner:String!,$repo:String!,$number:Int!,$after:String){repository(owner:$owner,name:$repo){
  pullRequest(number:$number){commits(last:1){nodes{commit{%s}}}}}}""" % CHECKS
FAILED = {"FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE", "ERROR"}


class TriageError(RuntimeError):
    pass


class GitHub:
    def __init__(self, host: str):
        self.host = host

    def call(self, endpoint: str, payload: dict | None = None):
        command = ["gh", "api", "--hostname", self.host, endpoint] + (["--input", "-"] if payload else [])
        result = subprocess.run(command, input=json.dumps(payload) if payload else "", capture_output=True,
                                text=True, timeout=120, env={**os.environ, "GH_PROMPT_DISABLED": "1"})
        if result.returncode:
            raise TriageError(f"GitHub request failed: {result.stderr.strip()}")
        value = json.loads(result.stdout)
        if isinstance(value, dict) and value.get("errors"):
            raise TriageError(f"GraphQL errors: {value['errors']}")
        return value


def parse_pr(url: str) -> dict:
    match = re.fullmatch(r"https://([^/]+)/([^/]+)/([^/]+)/pull/(\d+)/?", url)
    if not match:
        raise TriageError(f"not a pull request URL: {url}")
    host, owner, repo, number = match.groups()
    return {"url": f"https://{host}/{owner}/{repo}/pull/{number}", "host": host, "owner": owner,
            "repo": repo, "number": int(number)}


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def snapshot(target: dict, actor: str, api) -> tuple[str, dict]:
    if (login := api.call("user").get("login")) != actor:
        raise TriageError(f"GitHub actor differs: gh authenticates as {login!r}; bind {actor}'s token to the command")
    variables = {"owner": target["owner"], "repo": target["repo"], "number": target["number"]}
    pr = api.call("graphql", {"query": QUERY % CHECKS, "variables": variables})["data"]["repository"]["pullRequest"]
    checks, commit = [], (pr["commits"]["nodes"] or [{"commit": {}}])[0]["commit"]
    # Large repositories run more than one page of checks; each later page must still belong to the head.
    while contexts := (commit.get("statusCheckRollup") or {}).get("contexts"):
        checks += contexts["nodes"]
        if not contexts["pageInfo"]["hasNextPage"]:
            break
        commit = api.call("graphql", {"query": CHECKS_QUERY, "variables": {
            **variables, "after": contexts["pageInfo"]["endCursor"]}})["data"]["repository"]["pullRequest"]["commits"]["nodes"][0]["commit"]
        if commit["oid"] != pr["headRefOid"]:
            raise TriageError("the PR head moved while its checks were read; run triage again")
    # Progress between the first and the last check result changes no decision, so only failures and completion
    # count. Feedback lists keep their newest 100 items, where new activity lands; edits to older items go unseen.
    seen = {
        "head": pr["headRefOid"], "base": pr["baseRefName"], "draft": pr["isDraft"],
        "conflicting": pr["mergeable"] == "CONFLICTING", "behind": pr["mergeStateStatus"] == "BEHIND",
        "decision": pr["reviewDecision"],
        "threads": {t["id"]: digest([t["isResolved"], [c["body"] for c in t["comments"]["nodes"]]])
                    for t in pr["reviewThreads"]["nodes"]},
        "reviews": {r["id"]: digest([r["state"], r["body"]]) for r in pr["reviews"]["nodes"] if r["state"] != "PENDING"},
        "comments": {c["id"]: digest(c["body"]) for c in pr["comments"]["nodes"]},
        "failed_checks": sorted(c.get("name") or c.get("context") for c in checks
                                if (c.get("conclusion") or c.get("state")) in FAILED),
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
