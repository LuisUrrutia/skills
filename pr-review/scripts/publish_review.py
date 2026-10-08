#!/usr/bin/env python3
"""Publish an authorized review plan at the frozen head as one Comment or Approve review."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from snapshot import DIFF_OPTIONS, SnapshotError, digest, git, verify


class PublishError(RuntimeError):
    pass


class RejectedError(PublishError):
    """GitHub definitely refused the request (HTTP 4xx); nothing was written."""


class GitHub:
    def __init__(self, host: str):
        self.host = host

    def call(self, endpoint: str, payload: dict | None = None, paginate: bool = False):
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
            raise PublishError(f"GitHub request failed: {result.stderr.strip()}")
        value = json.loads(result.stdout)
        if isinstance(value, dict) and value.get("errors"):
            raise PublishError(f"GraphQL errors: {value['errors']}")
        if paginate:
            if not isinstance(value, list) or any(not isinstance(page, list) for page in value):
                raise PublishError("expected paginated review/comment arrays")
            return [item for page in value for item in page]
        return value


def anchor_lines(repository: Path, base: str, head: str, path: str, old_path: str | None = None) -> dict:
    paths = [path] if not old_path else [old_path, path]
    patch = git(repository, "diff", *DIFF_OPTIONS, base, head, "--", *paths).decode()
    anchors = {"LEFT": {}, "RIGHT": {}}
    old = new = hunk = 0
    for line in patch.splitlines():
        match = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if match:
            old, new = int(match[1]), int(match[2])
            hunk += 1
        elif hunk and line.startswith("-"):
            anchors["LEFT"][old] = hunk
            old += 1
        elif hunk and line.startswith("+"):
            anchors["RIGHT"][new] = hunk
            new += 1
        elif hunk and line.startswith(" "):
            anchors["LEFT"][old] = anchors["RIGHT"][new] = hunk
            old += 1
            new += 1
    return anchors


EVENTS = {"COMMENT": "COMMENTED", "APPROVE": "APPROVED"}
OWN_THREADS = """query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$number){
  reviewThreads(first:100){pageInfo{hasNextPage} nodes{isResolved comments(first:1){nodes{author{login}}}}}}}}"""


def validate_plan(plan: dict, manifest: dict, snapshot: Path) -> None:
    if set(plan) - {"event", "body", "comments", "replies"}:
        raise PublishError("unknown plan fields; only event, body, comments and replies are supported")
    if plan.get("event") not in EVENTS:
        raise PublishError("event must be COMMENT or APPROVE")
    if "body" in plan and not isinstance(plan["body"], str):
        raise PublishError("body must be a string")
    paths = json.loads((snapshot.parent / "changed-paths.json").read_text())
    keys = set()
    for kind in ("comments", "replies"):
        items = plan.get(kind, [])
        if not isinstance(items, list):
            raise PublishError(f"{kind} must be an array")
        for item in items:
            if not isinstance(item, dict):
                raise PublishError("comment entries must be objects")
            for field in ("key", "body"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise PublishError(f"comment needs {field}")
            if item["key"] in keys:
                raise PublishError("comment keys must be unique across all sites and replies")
            keys.add(item["key"])
            if kind == "replies":
                if set(item) != {"key", "body", "thread_id"} or not isinstance(item["thread_id"], str):
                    raise PublishError("reply needs only key, body and thread_id")
                continue
            if set(item) - {"key", "body", "path", "line", "side", "start_line", "start_side"}:
                raise PublishError("unknown comment fields")
            if item.get("path") not in paths or item.get("side") not in {"LEFT", "RIGHT"}:
                raise PublishError("comment must anchor in the frozen diff")
            lines = anchor_lines(Path(manifest["repository"]), manifest["merge_base"],
                                 manifest["target"]["head"], item["path"],
                                 manifest.get("renames", {}).get(item["path"]))[item["side"]]
            end, start = item.get("line"), item.get("start_line", item.get("line"))
            if type(start) is not int or type(end) is not int or start > end or start not in lines or end not in lines or lines[start] != lines[end]:
                raise PublishError("line/range is outside one frozen diff hunk")
            if ("start_line" in item) != ("start_side" in item) or item.get("start_side", item["side"]) != item["side"]:
                raise PublishError("range must specify both start_line and the same start_side")
    if plan["event"] == "APPROVE" and (plan.get("comments") or plan.get("replies")):
        raise PublishError("APPROVE carries no comments or replies; publish findings as COMMENT")
    if plan["event"] == "COMMENT" and not (plan.get("comments") or plan.get("replies") or plan.get("body", "").strip()):
        raise PublishError("COMMENT has nothing to publish")


def save(path: Path, state: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n")
    temporary.replace(path)


def apply(snapshot: Path, plan_path: Path, actor: str, receipt: Path, api=None, max_event: str = "APPROVE") -> dict:
    manifest = verify(snapshot)
    target = manifest["target"]
    plan = json.loads(plan_path.read_text())
    validate_plan(plan, manifest, snapshot)
    if max_event == "COMMENT" and plan["event"] != "COMMENT":
        raise PublishError("this caller allows only COMMENT; approval belongs to pr-review-followup")
    api = api or GitHub(target["host"])
    prefix = f"repos/{target['repository']}/pulls/{target['number']}"
    identity = {"target": target, "actor": actor, "plan_sha256": digest(plan_path)}
    state = json.loads(receipt.read_text()) if receipt.exists() else {"identity": identity, "comments": {}}
    if state.get("identity") != identity:
        raise PublishError("receipt belongs to a different actor, target, head or plan")
    if state.get("pending_operation"):
        raise PublishError("previous write outcome is uncertain; reconcile its read-back before retrying")
    final_state = EVENTS[plan["event"]]
    if state.get("status") == final_state:
        return state

    def preflight():
        verify(snapshot)
        if api.call("user").get("login") != actor:
            raise PublishError("active GitHub actor differs from the intended actor")
        current = api.call(prefix)
        if current.get("user", {}).get("login") == actor:
            raise PublishError("the actor authored this PR; follow it with pr-followup instead")
        base = current.get("base", {}).get("sha")
        if current.get("base", {}).get("ref") != target["base_name"]:
            raise PublishError("PR base branch changed since the snapshot; refresh the review before writing")
        if current.get("head", {}).get("sha") != target["head"]:
            raise PublishError("PR base or head drifted; refresh the review before writing")
        if base != target["base"]:
            compare = api.call(f"repos/{target['repository']}/compare/{base}...{target['head']}")
            if compare.get("merge_base_commit", {}).get("sha") != manifest["merge_base"]:
                raise PublishError("PR base or head drifted; refresh the review before writing")
        return current

    def check_own_threads():
        owner, name = target["repository"].split("/")
        threads = api.call("graphql", {"query": OWN_THREADS, "variables": {"owner": owner, "repo": name, "number": target["number"]}})
        threads = threads["data"]["repository"]["pullRequest"]["reviewThreads"]
        if threads["pageInfo"]["hasNextPage"]:
            raise PublishError("the PR has more than 100 review threads; refusing to approve on a partial view")
        if any(
                not node["isResolved"] and (node["comments"]["nodes"][0]["author"] or {}).get("login") == actor
                for node in threads["nodes"] if node["comments"]["nodes"]):
            raise PublishError("the actor has unresolved threads on this PR; approval belongs to pr-review-followup")

    current = preflight()
    if plan["event"] == "APPROVE":
        check_own_threads()
    reviews = api.call(prefix + "/reviews?per_page=100", paginate=True)
    pending = [r for r in reviews if r.get("state") == "PENDING" and r.get("user", {}).get("login") == actor]
    if len(pending) > 1:
        raise PublishError("ambiguous pending review ownership")
    review = pending[0] if pending else None
    if review and review["id"] != state.get("review_id"):
        raise PublishError("the actor has an unsubmitted review this run did not create; publishing would submit it")
    if state.get("review_id") and not review:
        raise PublishError("the recorded review is no longer pending; read back its state before retrying")

    def write(operation: str, endpoint: str, payload: dict):
        preflight()
        if state.get("review_id"):
            live = api.call(prefix + f"/reviews/{state['review_id']}")
            if live.get("state") != "PENDING" or live.get("commit_id") != target["head"] or live.get("user", {}).get("login") != actor:
                raise PublishError("review changed before writing; read back its state before retrying")
        state["pending_operation"] = operation
        save(receipt, state)
        try:
            return api.call(endpoint, payload)
        except RejectedError:
            state.pop("pending_operation", None)
            save(receipt, state)
            raise

    if review is None:
        review = write("create-review", prefix + "/reviews", {"commit_id": target["head"]})
        if review.get("state") != "PENDING" or review.get("user", {}).get("login") != actor or review.get("commit_id") != target["head"]:
            raise PublishError("created review did not read back as actor-owned PENDING at the frozen head")
        state.update(review_id=review["id"], review_node_id=review["node_id"])
        state.pop("pending_operation", None)
        save(receipt, state)

    review_node = state["review_node_id"]

    def check_recorded(comments):
        by_node = {comment.get("node_id"): comment for comment in comments}
        for saved in state["comments"].values():
            if saved["id"] not in by_node or by_node[saved["id"]].get("body") != saved["body"]:
                raise PublishError("comment was changed or not associated on read-back; reconcile before submitting")

    check_recorded(api.call(prefix + f"/reviews/{review['id']}/comments?per_page=100", paginate=True))
    for kind in ("comments", "replies"):
        for item in plan.get(kind, []):
            if item["key"] in state["comments"]:
                continue
            if kind == "replies":
                thread = api.call("graphql", {"query": "query($id:ID!){node(id:$id){... on PullRequestReviewThread{pullRequest{id}}}}", "variables": {"id": item["thread_id"]}})
                if thread["data"]["node"]["pullRequest"]["id"] != current["node_id"]:
                    raise PublishError("reply thread belongs to a different PR")
                mutation = "addPullRequestReviewThreadReply"
                payload = {"pullRequestReviewId": review_node, "pullRequestReviewThreadId": item["thread_id"], "body": item["body"]}
                output = "comment{id body pullRequestReview{id state}}"
            else:
                mutation = "addPullRequestReviewThread"
                payload = {"pullRequestReviewId": review_node, "body": item["body"], "path": item["path"], "line": item["line"], "side": item["side"]}
                if "start_line" in item:
                    payload.update(startLine=item["start_line"], startSide=item["start_side"])
                output = "thread{comments(first:1){nodes{id body pullRequestReview{id state}}}}"
            query = f"mutation($input:{mutation[0].upper() + mutation[1:]}Input!){{{mutation}(input:$input){{{output}}}}}"
            result = write(item["key"], "graphql", {"query": query, "variables": {"input": payload}})["data"][mutation]
            comment = result["comment"] if kind == "replies" else result["thread"]["comments"]["nodes"][0]
            if comment.get("body") != item["body"] or comment.get("pullRequestReview") != {"id": review_node, "state": "PENDING"}:
                raise PublishError("comment body or review association did not verify; inspect visibility immediately")
            state["comments"][item["key"]] = {"id": comment["id"], "body": item["body"]}
            state.pop("pending_operation", None)
            save(receipt, state)

    members = api.call(prefix + f"/reviews/{review['id']}/comments?per_page=100", paginate=True)
    check_recorded(members)
    live = api.call(prefix + f"/reviews/{review['id']}")
    expected = {saved["id"] for saved in state["comments"].values()}
    if {comment.get("node_id") for comment in members} != expected or (live.get("body") or ""):
        raise PublishError("the review holds unexpected content, likely the user's; stop rather than submit it")
    if plan["event"] == "APPROVE":
        check_own_threads()
    submission = {"event": plan["event"]}
    if plan.get("body", "").strip():
        submission["body"] = plan["body"]
    write("submit-review", prefix + f"/reviews/{review['id']}/events", submission)
    final = api.call(prefix + f"/reviews/{review['id']}")
    if (final.get("state") != final_state or final.get("commit_id") != target["head"]
            or final.get("user", {}).get("login") != actor or (final.get("body") or "") != submission.get("body", "")):
        raise PublishError("submitted review did not read back with the requested event, body and head")
    check_recorded(api.call(prefix + f"/reviews/{review['id']}/comments?per_page=100", paginate=True))
    state.pop("pending_operation", None)
    state["status"] = final_state
    save(receipt, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("snapshot", "plan", "receipt"):
        parser.add_argument("--" + flag, required=True, type=Path)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--max-event", choices=sorted(EVENTS), default="APPROVE",
                        help="pass COMMENT when pr-review-followup owns approval")
    args = parser.parse_args()
    try:
        state = apply(args.snapshot.resolve(), args.plan.resolve(), args.actor, args.receipt.resolve(),
                      max_event=args.max_event)
        print(json.dumps({"status": state["status"], "review_id": state.get("review_id")}))
        return 0
    except (PublishError, SnapshotError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"review publication stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
