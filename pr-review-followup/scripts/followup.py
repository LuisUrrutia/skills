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


def review_key(pr: dict) -> str:
    return f"{pr['head']}@{pr['base_ref']}"


def summarize(pr: dict, data: dict, plan: dict | None = None) -> dict:
    """The approval gate: one predicate for approving and for declaring the follow-up done."""
    plan = plan or {}
    reviewed = data.get("reviewed") or {}
    current = reviewed.get("head") == pr["head"] and reviewed.get("base_ref") == pr["base_ref"]
    reviewing = data.get("reviewing") or {}
    started = datetime.fromisoformat(reviewing["started_at"]) if reviewing else None
    verified = data.get("verified") if isinstance(data.get("verified"), dict) else {}
    resolve, unresolve = set(plan.get("resolve", [])), set(plan.get("unresolve", []))
    checked = resolve | set(plan.get("verified", []))
    closed = {t["id"] for t in pr["threads"] if (t["resolved"] or t["id"] in resolve) and t["id"] not in unresolve}
    unresolved = [t["id"] for t in pr["threads"] if t["id"] not in closed]
    unverified = [i for i in sorted(closed) if verified.get(i) != review_key(pr) and i not in checked]
    blockers = []
    if not current:
        blockers.append("the current head has not been reviewed")
    elif reviewed.get("complete") is not True or not all(
            type(reviewed.get(field)) is int for field in ("standing", "questions")):
        blockers.append("the review of the current head is incomplete")
    else:
        if reviewed.get("standing"):
            blockers.append("required findings outside reviewer threads still stand")
        if reviewed.get("questions"):
            blockers.append("decisive questions remain open")
    if unresolved:
        blockers.append("reviewer threads remain unresolved")
    if unverified:
        blockers.append("resolved threads have not been verified on the current head")
    return {"current": current, "complete": current and reviewed.get("complete") is True,
            "standing": reviewed.get("standing") if current else None,
            "questions": reviewed.get("questions") if current else None,
            "in_progress": reviewing.get("head") == pr["head"] and started is not None
            and datetime.now(timezone.utc) - started < REVIEW_IN_PROGRESS,
            "unresolved": unresolved, "unverified": unverified, "blockers": blockers}


def state(url: str, actor: str, state_file: Path, api=None) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    pr = read_pr(target, actor, api or GitHub(target["host"]))
    view = summarize(pr, data)
    return {"pr": target["url"], "author": pr["author"], "state": pr["state"], "head": pr["head"],
            "base_ref": pr["base_ref"], "reviewed": data.get("reviewed"), "review_current": view["current"],
            "review_complete": view["complete"], "standing_required": view["standing"],
            "open_questions": view["questions"], "review_in_progress": view["in_progress"],
            "pending_review": pr["pending_review"], "approved_head": pr["approved_head"],
            "done": pr["approved_head"] and not view["blockers"], "approval_blockers": view["blockers"],
            "pending_operation": data.get("pending_operation"), "unresolved": len(view["unresolved"]),
            "needs_verification": view["unverified"], "threads": pr["threads"]}


def begin(url: str, actor: str, state_file: Path, head: str) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    data["reviewing"] = {"head": head, "started_at": datetime.now(timezone.utc).isoformat()}
    save(state_file, data)
    return data


def counts(standing: int, questions: int) -> None:
    for name, value in (("standing", standing), ("questions", questions)):
        if type(value) is not int or value < 0:
            raise FollowupError(f"{name} must be a non-negative count")


def record(url: str, actor: str, state_file: Path, snapshot: Path, complete: bool, standing: int,
           questions: int) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    frozen = json.loads(snapshot.read_text())["target"]
    if parse_pr(frozen["url"])["url"] != target["url"]:
        raise FollowupError("the review snapshot belongs to another PR")
    counts(standing, questions)
    data["reviewed"] = {"head": frozen["head"], "base_ref": frozen["base_name"], "complete": complete,
                        "standing": standing, "questions": questions,
                        "snapshot_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest()}
    data.pop("reviewing", None)
    save(state_file, data)
    return data


def settle(url: str, actor: str, state_file: Path, standing: int, questions: int, api=None) -> dict:
    target = parse_pr(url)
    data = load_state(state_file, target, actor)
    counts(standing, questions)
    pr = read_pr(target, actor, api or GitHub(target["host"]))
    if not summarize(pr, data)["current"]:
        raise FollowupError("settle applies only to the review of the current head; review it first")
    data["reviewed"].update(standing=standing, questions=questions)
    save(state_file, data)
    return data


def validate_plan(plan: object) -> dict:
    fields = {"expected_head", "expected_base_ref", "replies", "resolve", "unresolve", "verified", "approve"}
    if (not isinstance(plan, dict) or set(plan) - fields or not isinstance(plan.get("expected_head"), str)
            or not isinstance(plan.get("expected_base_ref"), str)):
        raise FollowupError(f"plan accepts {', '.join(sorted(fields))}, with expected_head and expected_base_ref required")
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
    if set(plan.get("resolve", [])) & set(plan.get("unresolve", [])):
        raise FollowupError("plan cannot resolve and reopen the same thread")
    if set(plan.get("verified", [])) & set(plan.get("unresolve", [])):
        raise FollowupError("plan cannot reopen and verify the same thread")
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
        if pr["base_ref"] != plan["expected_base_ref"]:
            raise FollowupError("PR base branch changed since the plan was made; reassess on the new base")
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
    for thread_id in plan.get("verified", []):
        if not mine[thread_id]["resolved"] and thread_id not in resolve:
            raise FollowupError(f"plan verifies {thread_id}, which is not resolved")
    if plan.get("approve") and (blockers := summarize(pr, data, plan)["blockers"]):
        raise FollowupError(blockers[0])

    def write(key: str, endpoint: str, payload: dict, check=None):
        if key in done["completed"]:
            return None
        live = preflight()
        if check:
            check(live)
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

    key_now = review_key(pr)
    verified = data["verified"] if isinstance(data.get("verified"), dict) else {}
    data["verified"] = verified
    result = {"replied": [], "skipped": [], "resolved": [], "reopened": [], "approved": None}
    for thread_id in unresolve:
        if mine[thread_id]["resolved"]:
            thread = write(f"unresolve:{thread_id}", "graphql",
                           {"query": THREAD_MUTATION % "unresolveReviewThread", "variables": {"id": thread_id}})
            if thread and thread["data"]["unresolveReviewThread"]["thread"] != {"id": thread_id, "isResolved": False}:
                raise FollowupError("thread did not read back as reopened")
            finish(f"unresolve:{thread_id}")
        verified.pop(thread_id, None)
        result["reopened"].append(thread_id)
    for reply in replies:
        thread_id = reply["thread_id"]
        key = f"reply:{thread_id}:{hashlib.sha256(reply['body'].encode()).hexdigest()[:12]}"
        if mine[thread_id]["last_reviewer_body"] == reply["body"]:
            result["skipped"].append(thread_id)
            continue
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
        verified[thread_id] = key_now
        result["resolved"].append(thread_id)
    for thread_id in plan.get("verified", []):
        verified[thread_id] = key_now
    save(state_file, data)
    def gate(live: dict) -> None:
        if blockers := summarize(live, data)["blockers"]:
            raise FollowupError(blockers[0])

    if plan.get("approve"):
        current = preflight()
        gate(current)
        if not current["approved_head"]:
            review = write("approve", target["prefix"] + "/reviews", {"commit_id": current["head"], "event": "APPROVE"},
                           check=gate)
            if review.get("state") != "APPROVED" or review.get("commit_id") != current["head"]:
                raise FollowupError("approval did not read back at the current head")
            finish("approve")
        result["approved"] = current["head"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    read = commands.add_parser("state", help="report the PR, the recorded review, the approval gate and the reviewer's threads")
    start = commands.add_parser("begin", help="mark a full review of a head as in progress")
    mark = commands.add_parser("record", help="record the review a pr-review snapshot covered")
    close = commands.add_parser("settle", help="update the standing findings and open questions of the current review")
    write = commands.add_parser("apply", help="publish replies, settle threads and approve through the gate")
    for command in (read, start, mark, close, write):
        command.add_argument("--pr", required=True)
        command.add_argument("--actor", required=True)
        command.add_argument("--state-file", required=True, type=Path)
    start.add_argument("--head", required=True)
    mark.add_argument("--snapshot", required=True, type=Path)
    mark.add_argument("--complete", choices=("true", "false"), required=True)
    for command in (mark, close):
        command.add_argument("--standing", required=True, type=int)
        command.add_argument("--questions", required=True, type=int)
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
                            args.complete == "true", args.standing, args.questions)
        elif args.command == "settle":
            output = settle(args.pr, args.actor, state_file, args.standing, args.questions)
        else:
            output = apply(args.pr, args.actor, state_file, args.plan.resolve(), args.receipt.resolve())
        print(json.dumps(output, indent=2))
        return 0
    except (FollowupError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"pr-review-followup stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
