#!/usr/bin/env python3
"""Apply an authorized comment plan to a PENDING review, without submission."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from snapshot import DIFF_OPTIONS, SnapshotError, digest, git, verify


class PendingError(RuntimeError):
    pass


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
            raise PendingError(f"GitHub request failed: {result.stderr.strip()}")
        value = json.loads(result.stdout)
        if isinstance(value, dict) and value.get("errors"):
            raise PendingError(f"GraphQL errors: {value['errors']}")
        if paginate:
            if not isinstance(value, list) or any(not isinstance(page, list) for page in value):
                raise PendingError("expected paginated review/comment arrays")
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


def validate_plan(plan: dict, manifest: dict, snapshot: Path) -> None:
    if set(plan) - {"comments", "replies"}:
        raise PendingError("plan accepts only comments and replies; submission is not supported")
    paths = json.loads((snapshot.parent / "changed-paths.json").read_text())
    keys = set()
    for kind in ("comments", "replies"):
        items = plan.get(kind, [])
        if not isinstance(items, list):
            raise PendingError(f"{kind} must be an array")
        for item in items:
            if not isinstance(item, dict):
                raise PendingError("comment entries must be objects")
            for field in ("key", "body"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise PendingError(f"comment needs {field}")
            if item["key"] in keys:
                raise PendingError("comment keys must be unique across all sites and replies")
            keys.add(item["key"])
            if kind == "replies":
                if set(item) != {"key", "body", "thread_id"} or not isinstance(item["thread_id"], str):
                    raise PendingError("reply needs only key, body and thread_id")
                continue
            if set(item) - {"key", "body", "path", "line", "side", "start_line", "start_side"}:
                raise PendingError("unknown comment fields")
            if item.get("path") not in paths or item.get("side") not in {"LEFT", "RIGHT"}:
                raise PendingError("comment must anchor in the frozen diff")
            lines = anchor_lines(Path(manifest["repository"]), manifest["merge_base"],
                                 manifest["target"]["head"], item["path"],
                                 manifest.get("renames", {}).get(item["path"]))[item["side"]]
            end, start = item.get("line"), item.get("start_line", item.get("line"))
            if type(start) is not int or type(end) is not int or start > end or start not in lines or end not in lines or lines[start] != lines[end]:
                raise PendingError("line/range is outside one frozen diff hunk")
            if ("start_line" in item) != ("start_side" in item) or item.get("start_side", item["side"]) != item["side"]:
                raise PendingError("range must specify both start_line and the same start_side")


def save(path: Path, state: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n")
    temporary.replace(path)


def apply(snapshot: Path, plan_path: Path, actor: str, receipt: Path, api=None) -> dict:
    manifest = verify(snapshot)
    target = manifest["target"]
    plan = json.loads(plan_path.read_text())
    validate_plan(plan, manifest, snapshot)
    api = api or GitHub(target["host"])
    prefix = f"repos/{target['repository']}/pulls/{target['number']}"
    identity = {"target": target, "actor": actor, "plan_sha256": digest(plan_path)}
    state = json.loads(receipt.read_text()) if receipt.exists() else {"identity": identity, "comments": {}}
    if state.get("identity") != identity:
        raise PendingError("receipt belongs to a different actor, target, head or plan")
    if state.get("pending_operation"):
        raise PendingError("previous write outcome is uncertain; reconcile its read-back before retrying")

    def preflight():
        verify(snapshot)
        if api.call("user").get("login") != actor:
            raise PendingError("active GitHub actor differs from the intended actor")
        current = api.call(prefix)
        if current.get("head", {}).get("sha") != target["head"] or current.get("base", {}).get("sha") != target["base"]:
            raise PendingError("PR base or head drifted; refresh the review before writing")
        return current

    current = preflight()
    if not plan.get("comments") and not plan.get("replies"):
        return {"status": "no-comments", "written": 0}
    reviews = api.call(prefix + "/reviews?per_page=100", paginate=True)
    pending = [r for r in reviews if r.get("state") == "PENDING" and r.get("user", {}).get("login") == actor]
    if len(pending) > 1:
        raise PendingError("ambiguous pending review ownership")
    review = pending[0] if pending else None
    if state.get("review_id") and (not review or review["id"] != state["review_id"]):
        raise PendingError("the recorded pending review is no longer pending; preserve the user's decision")
    if review and review.get("commit_id") != target["head"]:
        raise PendingError("existing pending review belongs to another head; preserve it")

    def write(operation: str, endpoint: str, payload: dict):
        preflight()
        if state.get("review_id"):
            live = api.call(prefix + f"/reviews/{state['review_id']}")
            if live.get("state") != "PENDING" or live.get("commit_id") != target["head"] or live.get("user", {}).get("login") != actor:
                raise PendingError("review changed before writing; preserve the user's decision")
        state["pending_operation"] = operation
        save(receipt, state)
        return api.call(endpoint, payload)

    if review is None:
        review = write("create-review", prefix + "/reviews", {"commit_id": target["head"]})
        if review.get("state") != "PENDING" or review.get("user", {}).get("login") != actor or review.get("commit_id") != target["head"]:
            raise PendingError("created review did not read back as actor-owned PENDING at the frozen head")
        state.update(review_id=review["id"], review_node_id=review["node_id"])
        state.pop("pending_operation", None)
        save(receipt, state)
    else:
        state.update(review_id=review["id"], review_node_id=review["node_id"])
        save(receipt, state)

    review_node = state["review_node_id"]

    def check_recorded(comments):
        by_node = {comment.get("node_id"): comment for comment in comments}
        for saved in state["comments"].values():
            if not saved.get("id") or saved["id"] not in by_node or by_node[saved["id"]].get("body") != saved["body"]:
                raise PendingError("comment was changed or not associated on read-back; preserve edits and reconcile")

    existing = api.call(prefix + f"/reviews/{review['id']}/comments?per_page=100", paginate=True)
    check_recorded(existing)
    for kind in ("comments", "replies"):
        for item in plan.get(kind, []):
            if item["key"] in state["comments"]:
                continue
            # Existing user comments are preserved; matching content is not overwritten.
            matches = [comment for comment in existing if kind == "comments" and
                       all(comment.get(field) == item.get(field)
                           for field in ("body", "path", "line", "side", "start_line", "start_side"))]
            if matches:
                match = matches[0]
                if not isinstance(match.get("node_id"), str):
                    raise PendingError("existing matching comment has no identity for read-back")
                state["comments"][item["key"]] = {"status": "already-present", "id": match["node_id"], "body": item["body"]}
                save(receipt, state)
                continue
            if kind == "replies":
                thread = api.call("graphql", {"query": "query($id:ID!){node(id:$id){... on PullRequestReviewThread{pullRequest{id}}}}", "variables": {"id": item["thread_id"]}})
                if thread["data"]["node"]["pullRequest"]["id"] != current["node_id"]:
                    raise PendingError("reply thread belongs to a different PR")
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
                raise PendingError("comment body or PENDING review association did not verify; inspect visibility immediately")
            state["comments"][item["key"]] = {"id": comment["id"], "body": item["body"]}
            state.pop("pending_operation", None)
            save(receipt, state)
    preflight()
    final = api.call(prefix + f"/reviews/{review['id']}")
    comments = api.call(prefix + f"/reviews/{review['id']}/comments?per_page=100", paginate=True)
    if final.get("state") != "PENDING" or final.get("commit_id") != target["head"] or final.get("user", {}).get("login") != actor:
        raise PendingError("review is no longer actor-owned PENDING at the reviewed head")
    check_recorded(comments)
    state["status"] = "PENDING"
    save(receipt, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("snapshot", "plan", "receipt"):
        parser.add_argument("--" + flag, required=True, type=Path)
    parser.add_argument("--actor", required=True)
    args = parser.parse_args()
    try:
        state = apply(args.snapshot.resolve(), args.plan.resolve(), args.actor, args.receipt.resolve())
        print(json.dumps({"status": state["status"], "review_id": state.get("review_id")}))
        return 0
    except (PendingError, SnapshotError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"pending review stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
