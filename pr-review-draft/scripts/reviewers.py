#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from adapters import WorkerSpec, build_specs, validate_worker
from snapshot import SnapshotError, digest, pr_target, verify


STATE_NAME = "reviewers-state.json"
EVENTS_NAME = "reviewer-events"
LEDGER_NAME = "candidate-ledger.md"
REVIEWER_NAMES = ("claude", "codex", "coderabbit")
WORKER_ORDER = (*REVIEWER_NAMES, "feedback")


class LauncherError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def duration_between(started_at: str, finished_at: str | None = None) -> float:
    end = parse_time(finished_at) if finished_at else datetime.now(timezone.utc)
    return round((end - parse_time(started_at)).total_seconds(), 3)


def atomic_write_text(path: Path, value: str) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LauncherError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise LauncherError(f"expected a JSON object in {path}")
    return value


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def process_is_alive(process_id: Any) -> bool:
    if not isinstance(process_id, int) or process_id <= 0:
        return False
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def load_json_stream(value: str) -> list[Any]:
    decoder = json.JSONDecoder()
    documents: list[Any] = []
    offset = 0
    while offset < len(value):
        while offset < len(value) and value[offset].isspace():
            offset += 1
        if offset == len(value):
            break
        try:
            document, offset = decoder.raw_decode(value, offset)
        except json.JSONDecodeError as error:
            raise LauncherError(f"invalid JSON from gh: {error}") from error
        documents.append(document)
    return documents


def run_gh_json(arguments: list[str]) -> list[Any]:
    try:
        completed = subprocess.run(
            ["gh", *arguments], stdin=subprocess.DEVNULL, check=False,
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "GH_PROMPT_DISABLED": "1"},
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise LauncherError(str(error)) from error
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise LauncherError(f"gh {' '.join(arguments[:3])} failed: {detail}")
    return load_json_stream(completed.stdout)


def flatten_pages(documents: list[Any], key: str | None = None) -> list[Any]:
    flattened: list[Any] = []
    for document in documents:
        page = document.get(key) if key and isinstance(document, dict) else document
        if not isinstance(page, list):
            raise LauncherError("expected a paginated JSON array from gh")
        flattened.extend(page)
    return flattened


def flatten_review_threads(documents: list[Any]) -> list[Any]:
    threads: list[Any] = []
    for document in documents:
        if not isinstance(document, dict):
            raise LauncherError("expected a GraphQL document from gh")
        if document.get("errors"):
            raise LauncherError(f"GraphQL errors: {document['errors']}")
        try:
            page = document["data"]["repository"]["pullRequest"]["reviewThreads"]
            nodes = page["nodes"]
        except (KeyError, TypeError) as error:
            raise LauncherError("review-thread response has an unexpected shape") from error
        if not isinstance(nodes, list):
            raise LauncherError("review-thread nodes must be an array")
        threads.extend(nodes)
    return threads


def collect_feedback(pr_json: Path, output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow_log_dir = output_dir / "workflow-logs"
    workflow_log_dir.mkdir(exist_ok=True)

    pr = read_json(pr_json)
    number = pr.get("number")
    head_sha = pr.get("headRefOid")
    if not isinstance(number, int) or not isinstance(head_sha, str) or not head_sha:
        raise LauncherError("pr.json needs integer number and non-empty headRefOid")

    target = pr_target(pr)
    name_with_owner = target["repository"]
    owner, repo = name_with_owner.split("/", 1)

    def gh_json(arguments: list[str]) -> list[Any]:
        return run_gh_json([arguments[0], "--hostname", target["host"], *arguments[1:]])

    errors: list[dict[str, str]] = []
    files: dict[str, str] = {}

    def capture(name: str, operation: Callable[[], Any]) -> Any:
        output_path = output_dir / f"{name}.json"
        try:
            value = operation()
        except (LauncherError, IndexError, KeyError, TypeError) as error:
            value = []
            errors.append({"source": name, "error": str(error)})
        atomic_write_json(output_path, value)
        files[name] = str(output_path)
        return value

    def check_head() -> dict:
        current = gh_json(["api", f"repos/{name_with_owner}/pulls/{number}"])[0]
        if current.get("head", {}).get("sha") != head_sha:
            raise LauncherError("PR head drifted during feedback collection")
        return {"head_sha": head_sha}

    capture("head-before", check_head)
    review_comments = capture(
        "review-comments",
        lambda: flatten_pages(
            gh_json(
                [
                    "api",
                    f"repos/{name_with_owner}/pulls/{number}/comments?per_page=100",
                    "--paginate",
                ]
            )
        ),
    )
    reviews = capture(
        "reviews",
        lambda: flatten_pages(
            gh_json(
                [
                    "api",
                    f"repos/{name_with_owner}/pulls/{number}/reviews?per_page=100",
                    "--paginate",
                ]
            )
        ),
    )
    conversation_comments = capture(
        "conversation-comments",
        lambda: flatten_pages(
            gh_json(
                [
                    "api",
                    f"repos/{name_with_owner}/issues/{number}/comments?per_page=100",
                    "--paginate",
                ]
            )
        ),
    )

    query = """
query($owner:String!,$repo:String!,$n:Int!,$endCursor:String){ repository(owner:$owner,name:$repo){
  pullRequest(number:$n){ reviewThreads(first:100,after:$endCursor){ nodes{
    id isResolved
  } pageInfo{ hasNextPage endCursor } } }
} }
""".strip()
    threads = capture(
        "review-threads",
        lambda: flatten_review_threads(
            gh_json(
                [
                    "api",
                    "graphql",
                    "--paginate",
                    "-F",
                    f"owner={owner}",
                    "-F",
                    f"repo={repo}",
                    "-F",
                    f"n={number}",
                    "-f",
                    f"query={query}",
                ]
            )
        ),
    )

    for thread in threads:
        thread_id = thread["id"]
        def fetch_thread_comments(thread_id: str = thread_id) -> list[Any]:
            query = """query($id:ID!,$endCursor:String){node(id:$id){... on PullRequestReviewThread{
              comments(first:100,after:$endCursor){nodes{id author{login} path line body url
              pullRequestReview{id state commit{oid}}} pageInfo{hasNextPage endCursor}}
            }}}"""
            pages = gh_json(["api", "graphql", "--paginate", "-F", f"id={thread_id}", "-f", f"query={query}"])
            comments = []
            for page in pages:
                if page.get("errors"):
                    raise LauncherError(f"GraphQL errors: {page['errors']}")
                comments.extend(page["data"]["node"]["comments"]["nodes"])
            return comments
        thread["comments"] = {"nodes": capture(f"thread-{len(files)}-comments", fetch_thread_comments)}
    atomic_write_json(output_dir / "review-threads.json", threads)

    check_runs = capture(
        "check-runs",
        lambda: flatten_pages(
            gh_json(
                [
                    "api",
                    f"repos/{name_with_owner}/commits/{head_sha}/check-runs?per_page=100",
                    "--paginate",
                ]
            ),
            "check_runs",
        ),
    )

    def fetch_annotations() -> list[dict[str, Any]]:
        annotations: list[dict[str, Any]] = []
        for check_run in check_runs:
            check_id = check_run.get("id") if isinstance(check_run, dict) else None
            if not isinstance(check_id, int):
                continue
            try:
                pages = gh_json(
                    [
                        "api",
                        f"repos/{name_with_owner}/check-runs/{check_id}/annotations?per_page=100",
                        "--paginate",
                    ]
                )
            except LauncherError as error:
                errors.append({"source": f"check-run-{check_id}-annotations", "error": str(error)})
                continue
            for annotation in flatten_pages(pages):
                if isinstance(annotation, dict):
                    annotations.append({"check_run_id": check_id, **annotation})
        return annotations

    annotations = capture("check-run-annotations", fetch_annotations)
    workflow_runs = capture(
        "workflow-runs",
        lambda: flatten_pages(gh_json(["api", f"repos/{name_with_owner}/actions/runs?head_sha={head_sha}&per_page=100", "--paginate"]), "workflow_runs"),
    )

    workflow_logs: list[dict[str, Any]] = []
    for workflow_run in workflow_runs:
        run_id = workflow_run.get("id") if isinstance(workflow_run, dict) else None
        if not isinstance(run_id, int):
            continue
        log_path = workflow_log_dir / f"{run_id}.log"
        try:
            completed = subprocess.run(
                ["gh", "run", "view", str(run_id), "--repo", f"{target['host']}/{name_with_owner}", "--log"],
                check=False, stdin=subprocess.DEVNULL, timeout=120,
                capture_output=True, text=True,
                env={**os.environ, "GH_PROMPT_DISABLED": "1"},
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            errors.append({"source": f"workflow-log-{run_id}", "error": str(error)})
            workflow_logs.append({"databaseId": run_id, "path": str(log_path), "error": str(error)})
            continue
        atomic_write_text(log_path, completed.stdout)
        entry: dict[str, Any] = {
            "databaseId": run_id,
            "path": str(log_path),
            "exit_code": completed.returncode,
        }
        if completed.returncode != 0:
            detail = completed.stderr.strip() or "workflow log unavailable"
            entry["error"] = detail
            errors.append({"source": f"workflow-log-{run_id}", "error": detail})
        workflow_logs.append(entry)
    atomic_write_json(output_dir / "workflow-log-index.json", workflow_logs)
    files["workflow-log-index"] = str(output_dir / "workflow-log-index.json")

    capture("head-after", check_head)
    manifest = {
        "schema_version": 1,
        "status": "complete" if not errors else "partial",
        "repository": name_with_owner,
        "host": target["host"],
        "pull_request": number,
        "head_sha": head_sha,
        "collected_at": utc_now(),
        "files": files,
        "errors": errors,
        "counts": {
            "review_comments": len(review_comments),
            "reviews": len(reviews),
            "conversation_comments": len(conversation_comments),
            "review_threads": len(threads),
            "check_runs": len(check_runs),
            "annotations": len(annotations),
            "workflow_runs": len(workflow_runs),
        },
    }
    atomic_write_json(output_dir / "manifest.json", manifest)
    return 0


def fingerprint(snapshot: Path, settings: dict[str, Any]) -> dict[str, Any]:
    versions = {}
    for name in (*REVIEWER_NAMES, "gh"):
        executable = shutil.which(name)
        try:
            result = subprocess.run([name, "--version"], stdin=subprocess.DEVNULL,
                                    capture_output=True, text=True, timeout=10)
            versions[name] = {"executable": executable, "version": result.stdout.strip(),
                              "exit_code": result.returncode}
        except (OSError, subprocess.TimeoutExpired) as error:
            versions[name] = {"executable": executable, "error": str(error)}
    return {"snapshot": str(snapshot), "snapshot_sha256": digest(snapshot),
            "settings": settings, "tools": versions,
            "runner": {p.name: digest(p) for p in Path(__file__).parent.glob("*.py")}}


def initial_worker(spec: WorkerSpec) -> dict[str, Any]:
    return {
        "kind": spec.kind,
        "command": spec.command,
        "protection": spec.protection,
        "state": "pending",
        "attempts": 0,
        "pid": None,
        "started_at": None,
        "finished_at": None,
        "duration_seconds": None,
        "exit_code": None,
        "output": str(spec.report_path) if spec.report_path else None,
        "stdout": str(spec.stdout_path),
        "stderr": str(spec.stderr_path),
        "validation": None,
        "detail": None,
    }


def event_files(events_dir: Path) -> list[Path]:
    return sorted(events_dir.glob("[0-9][0-9][0-9][0-9][0-9][0-9]-*.json"))


def append_event(
    state: dict[str, Any],
    state_path: Path,
    events_dir: Path,
    name: str,
) -> None:
    existing_sequences = [int(path.name.split("-", 1)[0]) for path in event_files(events_dir)]
    sequence = max([int(state.get("event_sequence", 0)), *existing_sequences]) + 1
    worker = state["workers"][name]
    event = {
        "sequence": sequence,
        "at": utc_now(),
        "kind": worker["kind"],
        "name": name,
        "state": worker["state"],
        "duration_seconds": worker["duration_seconds"],
        "exit_code": worker["exit_code"],
        "validation": worker["validation"],
        "detail": worker["detail"],
        "output": worker["output"],
    }
    event_path = events_dir / f"{sequence:06d}-{name}.json"
    atomic_write_json(event_path, event)
    state["event_sequence"] = sequence
    atomic_write_json(state_path, state)


def launch(spec: WorkerSpec, repository: Path) -> subprocess.Popen[bytes]:
    stdout_handle = spec.stdout_path.open("wb")
    stderr_handle = spec.stderr_path.open("wb")
    stdin_handle = spec.stdin_path.open("rb") if spec.stdin_path else subprocess.DEVNULL
    try:
        process = subprocess.Popen(
            [*spec.guard, *spec.command],
            cwd=repository,
            stdin=stdin_handle,
            stdout=stdout_handle,
            stderr=stderr_handle,
            start_new_session=True,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GH_PROMPT_DISABLED": "1", "PYTHONDONTWRITEBYTECODE": "1"},
        )
    finally:
        if spec.stdin_path:
            stdin_handle.close()
        stdout_handle.close()
        stderr_handle.close()
    return process


def stop_processes(processes: dict[str, subprocess.Popen[bytes]]) -> None:
    for process in processes.values():
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and any(
        process.poll() is None for process in processes.values()
    ):
        time.sleep(0.1)
    for process in processes.values():
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def initialize_ledger(path: Path, base: str) -> None:
    if path.exists():
        return
    atomic_write_text(
        path,
        (
            "# Candidate ledger\n\n"
            f"Scope: `{base}`\n\n"
            "## Sources\n\n"
            "None.\n\n"
            "## Candidates\n\n"
            "None.\n\n"
            "## Open questions\n\n"
            "None.\n"
        ),
    )


def run_supervisor(args: argparse.Namespace) -> int:
    scratchpad = args.scratchpad.resolve()
    snapshot = args.snapshot.resolve()
    manifest = verify(snapshot)
    repository = Path(manifest["repository"])
    pr_json = args.pr_json.resolve()
    if pr_target(read_json(pr_json)) != manifest["target"]:
        raise LauncherError("feedback PR input differs from the frozen target")
    if not snapshot.parent.is_relative_to(scratchpad):
        raise LauncherError("snapshot inputs must be inside this run's scratchpad")
    settings = {key: getattr(args, key) for key in
                ("codex_model", "codex_effort", "claude_model", "claude_effort", "worker_timeout", "max_attempts")}
    state_path = scratchpad / STATE_NAME
    events_dir = scratchpad / EVENTS_NAME
    events_dir.mkdir(exist_ok=True)
    run_fingerprint = fingerprint(snapshot, settings)
    initialize_ledger(scratchpad / LEDGER_NAME, f"{manifest['merge_base']}..{manifest['target']['head']}")

    if state_path.exists():
        state = read_json(state_path)
        if state.get("fingerprint") != run_fingerprint:
            previous = state.get("fingerprint", {})
            changed = sorted(key for key in previous.keys() | run_fingerprint.keys()
                             if previous.get(key) != run_fingerprint.get(key))
            raise LauncherError("scratchpad contains a different review run; changed: " + ", ".join(changed))
        prior_supervisor = state.get("supervisor_pid")
        if state.get("status") == "running" and process_is_alive(prior_supervisor):
            print(f"reviewers already running under pid {prior_supervisor}")
            return 0
        if state.get("status") == "running":
            live_workers = [
                name
                for name, worker in state.get("workers", {}).items()
                if isinstance(worker, dict) and process_is_alive(worker.get("pid"))
            ]
            if live_workers:
                joined = ", ".join(sorted(live_workers))
                raise LauncherError(
                    f"stale supervisor left live workers: {joined}; wait for them or stop them"
                )
    else:
        if event_files(events_dir):
            raise LauncherError("reviewer events exist without a state file")
        state = {
            "schema_version": 1,
            "fingerprint": run_fingerprint,
            "status": "pending",
            "supervisor_pid": None,
            "started_at": utc_now(),
            "finished_at": None,
            "duration_seconds": None,
            "event_sequence": 0,
            "workers": {},
        }

    specs = build_specs(snapshot, manifest, scratchpad, pr_json, Path(__file__).resolve(), settings)
    state["status"] = "running"
    state["supervisor_pid"] = os.getpid()
    state["finished_at"] = None
    state["duration_seconds"] = None
    for spec in specs:
        record = state["workers"].setdefault(spec.name, initial_worker(spec))
        record.update(
            {
                "kind": spec.kind,
                "output": str(spec.report_path) if spec.report_path else None,
                "stdout": str(spec.stdout_path),
                "stderr": str(spec.stderr_path),
            }
        )
    atomic_write_json(state_path, state)

    pending_specs: list[WorkerSpec] = []
    terminal_before_monitor: list[str] = []
    for spec in specs:
        record = state["workers"][spec.name]
        if record.get("state") == "completed":
            valid, detail, validation = validate_worker(spec, snapshot)
            if spec.report_path.is_file() and record.get("report_sha256") != file_digest(spec.report_path):
                valid, detail = False, "completed report changed since validation"
            if valid:
                record["detail"] = detail
                record["validation"] = validation
                continue
            record.update(state="failed", validation="invalid", detail=detail, pid=None)
            append_event(state, state_path, events_dir, spec.name)
        elif record.get("state") == "running" and not process_is_alive(record.get("pid")):
            record.update(state="failed", validation="interrupted", pid=None,
                          finished_at=utc_now(), detail="worker exited without a recorded completion")
            append_event(state, state_path, events_dir, spec.name)
        if int(record.get("attempts", 0)) < args.max_attempts:
            pending_specs.append(spec)

    processes: dict[str, subprocess.Popen[bytes]] = {}
    monotonic_starts: dict[str, float] = {}
    for spec in pending_specs:
        record = state["workers"][spec.name]
        if record["attempts"]:
            archive = scratchpad / "attempts" / spec.name / str(record["attempts"])
            archive.mkdir(parents=True, exist_ok=True)
            for output in {spec.report_path, spec.stdout_path, spec.stderr_path}:
                if output.is_file():
                    shutil.copy2(output, archive / output.name)
        if spec.report_path.is_file():
            spec.report_path.unlink()
        executable = spec.command[0]
        if shutil.which(executable) is None:
            now = utc_now()
            record.update(
                {
                    "state": "skipped",
                    "attempts": int(record.get("attempts", 0)) + 1,
                    "pid": None,
                    "started_at": now,
                    "finished_at": now,
                    "duration_seconds": 0.0,
                    "exit_code": None,
                    "validation": "not-run",
                    "detail": f"missing executable: {executable}",
                }
            )
            terminal_before_monitor.append(spec.name)
            continue
        started_at = utc_now()
        monotonic_starts[spec.name] = time.monotonic()
        try:
            process = launch(spec, repository)
        except OSError as error:
            record.update(
                {
                    "state": "failed",
                    "attempts": int(record.get("attempts", 0)) + 1,
                    "pid": None,
                    "started_at": started_at,
                    "finished_at": utc_now(),
                    "duration_seconds": round(
                        time.monotonic() - monotonic_starts[spec.name], 3
                    ),
                    "exit_code": None,
                    "validation": "not-run",
                    "detail": f"launch failed: {error}",
                }
            )
            terminal_before_monitor.append(spec.name)
            continue
        processes[spec.name] = process
        record.update(
            {
                "state": "running",
                "attempts": int(record.get("attempts", 0)) + 1,
                "pid": process.pid,
                "started_at": started_at,
                "finished_at": None,
                "duration_seconds": None,
                "exit_code": None,
                "validation": None,
                "detail": None,
            }
        )
    atomic_write_json(state_path, state)
    for name in terminal_before_monitor:
        append_event(state, state_path, events_dir, name)

    def interrupt(_signal_number: int, _frame: Any) -> None:
        raise KeyboardInterrupt

    previous_term = signal.signal(signal.SIGTERM, interrupt)
    previous_int = signal.signal(signal.SIGINT, interrupt)
    try:
        while processes:
            for name, process in list(processes.items()):
                exit_code = process.poll()
                timed_out = time.monotonic() - monotonic_starts[name] >= args.worker_timeout
                if exit_code is None and not timed_out:
                    continue
                if exit_code is None:
                    stop_processes({name: process})
                    exit_code = process.poll()
                spec = next(candidate for candidate in specs if candidate.name == name)
                record = state["workers"][name]
                finished_at = utc_now()
                valid, detail, validation = validate_worker(spec, snapshot)
                if timed_out:
                    valid, detail, validation = False, "worker deadline exceeded", "timeout"
                if exit_code != 0:
                    detail = f"process exit {exit_code}; {detail}; stderr: {spec.stderr_path}"
                try:
                    verify(snapshot)
                except (SnapshotError, OSError) as error:
                    valid, detail, validation = False, str(error), "stale"
                completed = exit_code == 0 and valid
                record.update(
                    {
                        "state": "completed" if completed else "failed",
                        "pid": None,
                        "finished_at": finished_at,
                        "duration_seconds": round(
                            time.monotonic() - monotonic_starts[name], 3
                        ),
                        "exit_code": exit_code,
                        "validation": validation,
                        "detail": detail,
                        "report_sha256": file_digest(spec.report_path) if spec.report_path.is_file() else None,
                    }
                )
                del processes[name]
                append_event(state, state_path, events_dir, name)
            if processes:
                time.sleep(args.poll_interval)
    except KeyboardInterrupt:
        stop_processes(processes)
        for name in list(processes):
            record = state["workers"][name]
            finished_at = utc_now()
            record.update(
                {
                    "state": "failed",
                    "pid": None,
                    "finished_at": finished_at,
                    "duration_seconds": round(
                        time.monotonic() - monotonic_starts[name], 3
                    ),
                    "exit_code": None,
                    "validation": "not-run",
                    "detail": "supervisor interrupted",
                }
            )
            append_event(state, state_path, events_dir, name)
        state["status"] = "interrupted"
        state["supervisor_pid"] = None
        state["finished_at"] = utc_now()
        state["duration_seconds"] = duration_between(
            state["started_at"], state["finished_at"]
        )
        atomic_write_json(state_path, state)
        return 130
    finally:
        signal.signal(signal.SIGTERM, previous_term)
        signal.signal(signal.SIGINT, previous_int)

    try:
        verify(snapshot)
    except (SnapshotError, OSError) as error:
        state["status"] = "stale"
        state["detail"] = str(error)
        state["supervisor_pid"] = None
        state["finished_at"] = utc_now()
        atomic_write_json(state_path, state)
        print(f"reviewer run stale: {error}", file=sys.stderr)
        return 1
    reviewer_states = [state["workers"][name]["state"] for name in REVIEWER_NAMES]
    collector = state["workers"]["feedback"]
    all_reviewers_completed = all(value == "completed" for value in reviewer_states)
    if all_reviewers_completed:
        state["status"] = (
            "completed"
            if collector["state"] == "completed" and collector["validation"] == "complete"
            else "completed_with_warnings"
        )
    elif any(value == "completed" for value in reviewer_states):
        state["status"] = "partial"
    else:
        state["status"] = "failed"
    state["supervisor_pid"] = None
    state["finished_at"] = utc_now()
    state["duration_seconds"] = duration_between(
        state["started_at"], state["finished_at"]
    )
    atomic_write_json(state_path, state)
    print(f"reviewer run {state['status']}: {state_path}")
    return 0 if all_reviewers_completed else 1


def read_events(events_dir: Path, after: int, kind: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in event_files(events_dir):
        sequence = int(path.name.split("-", 1)[0])
        if sequence <= after:
            continue
        event = read_json(path)
        if kind != "all" and event.get("kind") != kind:
            continue
        events.append(event)
    return events


def observed_state(state_path: Path) -> dict[str, Any]:
    state = read_json(state_path)
    if state.get("status") == "running" and not process_is_alive(state.get("supervisor_pid")):
        live = False
        for worker in state.get("workers", {}).values():
            if worker.get("state") == "running":
                worker["recorded_state"] = "running"
                worker["state"] = "orphaned" if process_is_alive(worker.get("pid")) else "interrupted"
                live |= worker["state"] == "orphaned"
        state["recorded_status"] = "running"
        state["status"] = "orphaned" if live else "interrupted"
        state["observation"] = "supervisor is no longer alive; saved execution evidence is unchanged"
    return state


def wait_for_event(args: argparse.Namespace) -> int:
    scratchpad = args.scratchpad.resolve()
    state_path = scratchpad / STATE_NAME
    events_dir = scratchpad / EVENTS_NAME
    deadline = time.monotonic() + args.timeout
    while True:
        if state_path.exists():
            state = observed_state(state_path)
            events = read_events(events_dir, args.after, args.kind)
            if events:
                print(
                    json.dumps(
                        {
                            "events": events,
                            "last_sequence": max(event["sequence"] for event in events),
                            "run_status": state.get("status"),
                        },
                        sort_keys=True,
                    )
                )
                return 0
            if state.get("status") not in {"pending", "running"}:
                print(
                    json.dumps(
                        {
                            "events": [],
                            "last_sequence": args.after,
                            "run_status": state.get("status"),
                        },
                        sort_keys=True,
                    )
                )
                return 0
        if time.monotonic() >= deadline:
            print(
                json.dumps(
                    {
                        "events": [],
                        "last_sequence": args.after,
                        "run_status": "unknown" if not state_path.exists() else "running",
                        "timeout": True,
                    },
                    sort_keys=True,
                )
            )
            return 124
        time.sleep(args.poll_interval)


def format_duration(value: Any, started_at: Any, finished_at: Any) -> str:
    if isinstance(value, (int, float)):
        seconds = float(value)
    elif isinstance(started_at, str):
        seconds = duration_between(
            started_at, finished_at if isinstance(finished_at, str) else None
        )
    else:
        return "-"
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes:02d}:{remainder:02d}"


def show_status(args: argparse.Namespace) -> int:
    state_path = args.scratchpad.resolve() / STATE_NAME
    if not state_path.exists():
        raise LauncherError(f"missing reviewer state: {state_path}")
    state = observed_state(state_path)
    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True))
        return 0

    print(f"run: {state.get('status', 'unknown')}")
    print("worker       kind       state       elapsed  validation")
    for name in WORKER_ORDER:
        worker = state.get("workers", {}).get(name)
        if not isinstance(worker, dict):
            continue
        elapsed = format_duration(
            worker.get("duration_seconds"),
            worker.get("started_at"),
            worker.get("finished_at"),
        )
        validation = worker.get("validation") or "-"
        print(
            f"{name:<12} {worker.get('kind', '-'):<10} "
            f"{worker.get('state', '-'):<11} {elapsed:<8} {validation}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run and observe the pr-review-draft worker roster"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="supervise the fixed reviewer roster")
    run_parser.add_argument("--snapshot", required=True, type=Path)
    run_parser.add_argument("--pr-json", required=True, type=Path)
    run_parser.add_argument("--scratchpad", required=True, type=Path)
    run_parser.add_argument("--codex-model")
    run_parser.add_argument("--codex-effort")
    run_parser.add_argument("--claude-model")
    run_parser.add_argument("--claude-effort")
    run_parser.add_argument("--worker-timeout", type=float, default=1500)
    run_parser.add_argument("--max-attempts", type=int, choices=(1, 2), default=2)
    run_parser.add_argument("--poll-interval", type=float, default=0.25)

    wait_parser = subparsers.add_parser("wait", help="wait for the next terminal event")
    wait_parser.add_argument("--scratchpad", required=True, type=Path)
    wait_parser.add_argument("--after", required=True, type=int)
    wait_parser.add_argument(
        "--kind", choices=("reviewer", "collector", "all"), default="reviewer"
    )
    wait_parser.add_argument("--timeout", type=float, default=60)
    wait_parser.add_argument("--poll-interval", type=float, default=1.0)

    status_parser = subparsers.add_parser("status", help="show the current roster state")
    status_parser.add_argument("--scratchpad", required=True, type=Path)
    status_parser.add_argument("--json", action="store_true")

    collect_parser = subparsers.add_parser(
        "_collect-feedback", help="collect existing feedback for the supervisor"
    )
    collect_parser.add_argument("--pr-json", required=True, type=Path)
    collect_parser.add_argument("--output-dir", required=True, type=Path)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "run":
            if args.poll_interval <= 0 or args.worker_timeout <= 0:
                raise LauncherError("poll interval must be positive")
            with (args.scratchpad / ".supervisor.lock").open("a+") as lock:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    print("reviewers already running (supervisor lock held)")
                    return 0
                return run_supervisor(args)
        if args.command == "wait":
            if args.after < 0 or args.timeout < 0 or args.poll_interval <= 0:
                raise LauncherError("wait values must be non-negative and polling positive")
            return wait_for_event(args)
        if args.command == "status":
            return show_status(args)
        return collect_feedback(args.pr_json.resolve(), args.output_dir.resolve())
    except (LauncherError, SnapshotError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"reviewer launcher failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
