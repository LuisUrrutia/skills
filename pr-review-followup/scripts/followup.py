#!/usr/bin/env python3
"""Read and act on the reviewer's threads of one GitHub PR, approving only through its gate."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

THREADS_QUERY = """query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$number){
  id state headRefOid baseRefName author{login}
  reviewThreads(first:100){pageInfo{hasNextPage} nodes{id isResolved isOutdated path line
    resolvedBy{login} viewerCanResolve viewerCanUnresolve
    comments(first:100){pageInfo{hasNextPage} nodes{databaseId author{login} body createdAt}}}}}}}"""
THREAD_MUTATION = "mutation($id:ID!){%s(input:{threadId:$id}){thread{id isResolved}}}"
REVIEW_IN_PROGRESS = timedelta(hours=3)


class FollowupError(RuntimeError):
    pass


class RejectedError(FollowupError):
    """GitHub definitely refused the request (HTTP 4xx); nothing was written."""


class GitHub:
    def __init__(self, host: str):
        self.host = host

    def call(self, endpoint: str, payload: dict | None = None):
        paginate = "per_page=100" in endpoint
        command = ["gh", "api", "--hostname", self.host, endpoint]
        if payload is not None:
            command += ["--input", "-"]
        if paginate:
            command += ["--paginate", "--slurp"]
        result = subprocess.run(command, input=json.dumps(payload) if payload is not None else "",
                                capture_output=True, text=True, timeout=120,
                                env={**os.environ, "GH_PROMPT_DISABLED": "1"})
        if result.returncode:
            if re.search(r"HTTP 4\d\d", result.stderr):
                raise RejectedError(f"GitHub rejected the request: {result.stderr.strip()}")
            raise FollowupError(f"GitHub request failed: {result.stderr.strip()}")
        value = json.loads(result.stdout)
        if isinstance(value, dict) and value.get("errors"):
            raise FollowupError(f"GraphQL errors: {value['errors']}")
        return [item for page in value for item in page] if paginate else value


def parse_pr(url: str) -> dict:
    match = re.fullmatch(r"https://([^/]+)/([^/]+)/([^/]+)/pull/(\d+)/?", url)
    if not match:
        raise FollowupError(f"not a pull request URL: {url}")
    host, owner, repo, number = match.groups()
    return {"url": f"https://{host}/{owner}/{repo}/pull/{number}", "host": host, "owner": owner,
            "repo": repo, "number": int(number), "prefix": f"repos/{owner}/{repo}/pulls/{number}"}


def save(path: Path, data: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def load_state(state_file: Path, target: dict, actor: str) -> dict:
    data = json.loads(state_file.read_text()) if state_file.exists() else {"pr": target["url"], "actor": actor}
    if data.get("pr") != target["url"] or data.get("actor") != actor:
        raise FollowupError(f"state file belongs to {data.get('pr')} as {data.get('actor')}")
    return data


def read_pr(target: dict, actor: str, api) -> dict:
    data = api.call("graphql", {"query": THREADS_QUERY, "variables": {
        "owner": target["owner"], "repo": target["repo"], "number": target["number"]}})
    pr = data["data"]["repository"]["pullRequest"]
    author = (pr["author"] or {}).get("login")
    if author == actor:
        raise FollowupError("the reviewer authored this PR; follow it with pr-followup instead")
    if pr["reviewThreads"]["pageInfo"]["hasNextPage"]:
        raise FollowupError("more than 100 review threads; refusing to act on a partial view")
    roles = {actor: "reviewer", author: "author"}
    threads = []
    for node in pr["reviewThreads"]["nodes"]:
        comments = node["comments"]["nodes"]
        if not comments or (comments[0]["author"] or {}).get("login") != actor:
            continue
        if node["comments"]["pageInfo"]["hasNextPage"]:
            raise FollowupError(f"thread {node['id']} has more than 100 comments; refusing to act on a partial view")
        listed = [{"role": roles.get((c["author"] or {}).get("login"), "other"),
                   "author": (c["author"] or {}).get("login"), "at": c["createdAt"], "body": c["body"]}
                  for c in comments]
        threads.append({
            "id": node["id"], "path": node["path"], "line": node["line"], "outdated": node["isOutdated"],
            "resolved": node["isResolved"], "resolved_by": (node["resolvedBy"] or {}).get("login"),
            "can_resolve": node["viewerCanResolve"], "can_unresolve": node["viewerCanUnresolve"],
            "root_comment": comments[0]["databaseId"], "awaiting_reviewer": listed[-1]["role"] != "reviewer",
            "last_reviewer_body": next(c["body"] for c in reversed(listed) if c["role"] == "reviewer"),
            "comments": listed,
        })
    reviews = [r for r in api.call(target["prefix"] + "/reviews?per_page=100")
               if (r.get("user") or {}).get("login") == actor]
    return {"state": pr["state"], "head": pr["headRefOid"], "base_ref": pr["baseRefName"], "author": author,
            "threads": threads, "pending_review": any(r.get("state") == "PENDING" for r in reviews),
            "approved_head": any(r.get("state") == "APPROVED" and r.get("commit_id") == pr["headRefOid"]
                                 for r in reviews)}


def summarize(pr: dict, data: dict, actor: str) -> dict:
    reviewed = data.get("reviewed") or {}
    current = reviewed.get("head") == pr["head"] and reviewed.get("base_ref") == pr["base_ref"]
    reviewing = data.get("reviewing") or {}
    started = datetime.fromisoformat(reviewing["started_at"]) if reviewing else None
    unresolved = [t["id"] for t in pr["threads"] if not t["resolved"]]
    unverified = [t["id"] for t in pr["threads"] if t["resolved"] and t["resolved_by"] != actor
                  and t["id"] not in data.get("verified", [])]
    return {"current": current, "complete": current and reviewed.get("complete") is True,
            "standing": reviewed.get("standing") if current else None,
            "in_progress": reviewing.get("head") == pr["head"] and started is not None
            and datetime.now(timezone.utc) - started < REVIEW_IN_PROGRESS,
            "unresolved": unresolved, "unverified": unverified}


def state(url: str, actor: str, state_file: Path, api=None) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    pr = read_pr(target, actor, api or GitHub(target["host"]))
    view = summarize(pr, data, actor)
    return {"pr": target["url"], "author": pr["author"], "state": pr["state"], "head": pr["head"],
            "base_ref": pr["base_ref"], "reviewed": data.get("reviewed"), "review_current": view["current"],
            "review_complete": view["complete"], "standing_required": view["standing"],
            "review_in_progress": view["in_progress"], "pending_review": pr["pending_review"],
            "approved_head": pr["approved_head"], "done": pr["approved_head"] and not view["unresolved"],
            "pending_operation": data.get("pending_operation"), "unresolved": len(view["unresolved"]),
            "needs_verification": view["unverified"], "threads": pr["threads"]}


def begin(url: str, actor: str, state_file: Path, head: str) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    data["reviewing"] = {"head": head, "started_at": datetime.now(timezone.utc).isoformat()}
    save(state_file, data)
    return data


def record(url: str, actor: str, state_file: Path, snapshot: Path, complete: bool, standing: int) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    frozen = json.loads(snapshot.read_text())["target"]
    if parse_pr(frozen["url"])["url"] != target["url"]:
        raise FollowupError("the review snapshot belongs to another PR")
    if type(standing) is not int or standing < 0:
        raise FollowupError("standing must be a non-negative count of required findings outside reviewer threads")
    data["reviewed"] = {"head": frozen["head"], "base_ref": frozen["base_name"], "complete": complete,
                        "standing": standing, "snapshot_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest()}
    data.pop("reviewing", None)
    save(state_file, data)
    return data


def validate_plan(plan: object) -> dict:
    fields = {"expected_head", "replies", "resolve", "unresolve", "verified", "approve"}
    if not isinstance(plan, dict) or set(plan) - fields or not isinstance(plan.get("expected_head"), str):
        raise FollowupError(f"plan accepts {', '.join(sorted(fields))}, with expected_head required")
    for field in ("resolve", "unresolve", "verified"):
        if not isinstance(plan.get(field, []), list) or not all(isinstance(i, str) for i in plan.get(field, [])):
            raise FollowupError(f"plan field {field} must be a list of thread IDs")
    replies = plan.get("replies", [])
    if not isinstance(replies, list) or not all(
            isinstance(r, dict) and set(r) == {"thread_id", "body"} and isinstance(r["thread_id"], str)
            and isinstance(r["body"], str) and r["body"].strip() for r in replies):
        raise FollowupError("plan replies need only a string thread_id and a non-empty string body")
    if not isinstance(plan.get("approve", False), bool):
        raise FollowupError("plan field approve must be a boolean")
    return plan


def apply(url: str, actor: str, state_file: Path, plan_path: Path, receipt: Path, api=None) -> dict:
    target = parse_pr(url)
    api = api or GitHub(target["host"])
    plan = validate_plan(json.loads(plan_path.read_text()))
    data = load_state(state_file, target, actor)
    if data.get("pending_operation"):
        raise FollowupError(f"previous write outcome is uncertain ({data['pending_operation']}); "
                            "read back the thread or review, then clear pending_operation")
    identity = {"pr": target["url"], "actor": actor, "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest()}
    done = json.loads(receipt.read_text()) if receipt.exists() else {"identity": identity, "completed": []}
    if done.get("identity") != identity:
        raise FollowupError("receipt belongs to a different PR, actor or plan")

    def preflight() -> dict:
        if api.call("user").get("login") != actor:
            raise FollowupError("active GitHub actor differs from the intended reviewer")
        pr = read_pr(target, actor, api)
        if pr["state"] != "OPEN":
            raise FollowupError(f"PR is not open ({pr['state']})")
        if pr["head"] != plan["expected_head"]:
            raise FollowupError("PR head moved since the plan was made; reassess on the new head")
        if pr["pending_review"]:
            raise FollowupError("the reviewer has an unsubmitted review; it belongs to the user")
        return pr

    pr = preflight()
    mine = {t["id"]: t for t in pr["threads"]}
    replies, resolve, unresolve = plan.get("replies", []), plan.get("resolve", []), plan.get("unresolve", [])
    for thread_id in [r["thread_id"] for r in replies] + resolve + unresolve + plan.get("verified", []):
        if thread_id not in mine:
            raise FollowupError(f"{thread_id} is not a thread the reviewer started on this PR")
    for thread_id in resolve:
        if not mine[thread_id]["resolved"] and not mine[thread_id]["can_resolve"]:
            raise FollowupError(f"the reviewer cannot resolve {thread_id}; report it instead")
    for thread_id in unresolve:
        if mine[thread_id]["resolved"] and not mine[thread_id]["can_unresolve"]:
            raise FollowupError(f"the reviewer cannot reopen {thread_id}; report it instead")
    if plan.get("approve"):
        data["verified"] = sorted(set(data.get("verified", [])) | set(plan.get("verified", [])))
        view = summarize(pr, data, actor)
        if not view["current"]:
            raise FollowupError("the current head has not been reviewed")
        if not view["complete"]:
            raise FollowupError("the review of the current head is incomplete")
        if view["standing"]:
            raise FollowupError("required findings outside reviewer threads still stand")
        if set(view["unresolved"]) - set(resolve) or set(unresolve):
            raise FollowupError("reviewer threads remain unresolved")
        if view["unverified"]:
            raise FollowupError("threads resolved by someone else have not been verified")

    def write(key: str, endpoint: str, payload: dict):
        if key in done["completed"]:
            return None
        preflight()
        data["pending_operation"] = key
        save(state_file, data)
        try:
            return api.call(endpoint, payload)
        except RejectedError:
            data.pop("pending_operation", None)
            save(state_file, data)
            raise

    def finish(key: str):
        done["completed"].append(key)
        data.pop("pending_operation", None)
        save(receipt, done)
        save(state_file, data)

    result = {"replied": [], "resolved": [], "reopened": [], "approved": None}
    for thread_id in unresolve:
        if mine[thread_id]["resolved"]:
            thread = write(f"unresolve:{thread_id}", "graphql",
                           {"query": THREAD_MUTATION % "unresolveReviewThread", "variables": {"id": thread_id}})
            if thread and thread["data"]["unresolveReviewThread"]["thread"] != {"id": thread_id, "isResolved": False}:
                raise FollowupError("thread did not read back as reopened")
            finish(f"unresolve:{thread_id}")
        result["reopened"].append(thread_id)
    for reply in replies:
        thread_id = reply["thread_id"]
        key = f"reply:{thread_id}:{hashlib.sha256(reply['body'].encode()).hexdigest()[:12]}"
        if mine[thread_id]["last_reviewer_body"] != reply["body"]:
            comment = write(key, target["prefix"] + f"/comments/{mine[thread_id]['root_comment']}/replies",
                            {"body": reply["body"]})
            if comment:
                review = api.call(target["prefix"] + f"/reviews/{comment.get('pull_request_review_id')}")
                if comment.get("body") != reply["body"] or review.get("state") == "PENDING":
                    raise FollowupError("reply did not read back as a published comment; inspect the thread")
                finish(key)
        result["replied"].append(thread_id)
    for thread_id in resolve:
        if not mine[thread_id]["resolved"]:
            thread = write(f"resolve:{thread_id}", "graphql",
                           {"query": THREAD_MUTATION % "resolveReviewThread", "variables": {"id": thread_id}})
            if thread and thread["data"]["resolveReviewThread"]["thread"] != {"id": thread_id, "isResolved": True}:
                raise FollowupError("thread did not read back as resolved")
            finish(f"resolve:{thread_id}")
        result["resolved"].append(thread_id)
    data["verified"] = sorted(set(data.get("verified", [])) | set(plan.get("verified", [])))
    data["verified"] = [i for i in data["verified"] if i not in unresolve]
    save(state_file, data)
    if plan.get("approve"):
        current = preflight()
        if summarize(current, data, actor)["unresolved"]:
            raise FollowupError("reviewer threads remain unresolved")
        if not current["approved_head"]:
            review = write("approve", target["prefix"] + "/reviews", {"commit_id": current["head"], "event": "APPROVE"})
            if review.get("state") != "APPROVED" or review.get("commit_id") != current["head"]:
                raise FollowupError("approval did not read back at the current head")
            finish("approve")
        result["approved"] = current["head"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    read = commands.add_parser("state", help="report the PR, the recorded review and the reviewer's threads")
    start = commands.add_parser("begin", help="mark a full review of a head as in progress")
    mark = commands.add_parser("record", help="record the review a pr-review snapshot covered")
    write = commands.add_parser("apply", help="publish replies, settle threads and approve through the gate")
    for command in (read, start, mark, write):
        command.add_argument("--pr", required=True)
        command.add_argument("--actor", required=True)
        command.add_argument("--state-file", required=True, type=Path)
    start.add_argument("--head", required=True)
    mark.add_argument("--snapshot", required=True, type=Path)
    mark.add_argument("--complete", choices=("true", "false"), required=True)
    mark.add_argument("--standing", required=True, type=int)
    write.add_argument("--plan", required=True, type=Path)
    write.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    state_file = args.state_file.resolve()
    try:
        if args.command == "state":
            output = state(args.pr, args.actor, state_file)
        elif args.command == "begin":
            output = begin(args.pr, args.actor, state_file, args.head)
        elif args.command == "record":
            output = record(args.pr, args.actor, state_file, args.snapshot.resolve(),
                            args.complete == "true", args.standing)
        else:
            output = apply(args.pr, args.actor, state_file, args.plan.resolve(), args.receipt.resolve())
        print(json.dumps(output, indent=2))
        return 0
    except (FollowupError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"pr-review-followup stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
