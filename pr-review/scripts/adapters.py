"""CLI transport and completion checks; audit criteria belong to the shared packet."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from read_only import codex_permissions, guarded


@dataclass(frozen=True)
class WorkerSpec:
    name: str
    kind: str
    command: list[str]
    stdout_path: Path
    stderr_path: Path
    report_path: Path
    stdin_path: Path | None = None
    guard: tuple[str, ...] = ()
    protection: str = "none"
    preflight_error: str | None = None
    limitations: tuple[str, ...] = ()


def build_specs(snapshot: Path, manifest: dict, scratch: Path, pr_json: Path,
                runner: Path, settings: dict) -> list[WorkerSpec]:
    inputs = snapshot.parent
    packet = inputs / "packet.md"
    specs = []
    private_paths = (snapshot, *(Path(path) for path in manifest.get("private_paths", [])))
    for name in ("claude", "codex", "coderabbit"):
        if name not in settings.get("workers", ("claude", "codex", "coderabbit", "feedback")):
            continue
        preflight_error = None
        limitations = ()
        output = scratch / name
        output.mkdir(exist_ok=True)
        report = output / ("review.jsonl" if name == "coderabbit" else "review.md")
        if name == "claude":
            command = ["claude", "-p", "--restricted", "--tools", "Read,Glob,Grep",
                       "--add-dir", str(inputs),
                       "--permission-mode", "dontAsk", "--permission-prompts", "none",
                       "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                       "--setting-sources", "", "--settings", '{"disableAllHooks":true}',
                       "--disable-slash-commands", "--no-chrome", "--no-session-persistence"]
            if settings["claude_model"]:
                command += ["--model", settings["claude_model"]]
            if settings["claude_effort"]:
                command += ["--effort", settings["claude_effort"]]
        elif name == "codex":
            command = ["codex", "exec", "--ignore-user-config", "--ignore-rules",
                       "--ephemeral", "--strict-config",
                       *codex_permissions(scratch, inputs, output, private_paths),
                       "-c", 'approval_policy="never"', "-c", 'web_search="disabled"',
                       "-c", "features.multi_agent=false", "-c", "features.apps=false",
                       "-c", "features.plugins=false", "-c", "features.hooks=false",
                       "-c", "features.skip_host_skill_discovery=true",
                       "-c", "project_doc_max_bytes=0",
                       "-c", "projects={" + json.dumps(manifest["repository"]) + '={trust_level="untrusted"}}',
                       "-o", str(report), "-"]
            if settings["codex_model"]:
                command += ["--model", settings["codex_model"]]
            if settings["codex_effort"]:
                command += ["-c", "model_reasoning_effort=" + json.dumps(settings["codex_effort"])]
        else:
            try:
                help_result = subprocess.run(
                    ["coderabbit", "review", "--help"], stdin=subprocess.DEVNULL,
                    capture_output=True, text=True, timeout=10)
                if help_result.returncode:
                    raise ValueError("CodeRabbit review --help failed")
                flags = set(re.findall(r"^\s*(?:-\w,\s+)?(--[a-z][a-z-]*)\b", help_result.stdout, re.M))
                required = {"--agent", "--committed", "--base", "--base-commit", "--config"}
                if not required <= flags:
                    raise ValueError("CodeRabbit lacks required options: " + ", ".join(sorted(required - flags)))
                fresh = ["--fresh"] if "--fresh" in flags else []
                if not fresh:
                    limitations = ("CodeRabbit does not support --fresh; checkpoint reuse is not excluded by the invocation",)
            except (OSError, ValueError, subprocess.TimeoutExpired) as error:
                fresh = []
                preflight_error = str(error)
            command = ["coderabbit", "review", "--agent", *fresh, "--committed",
                       "--base", manifest["target"]["base_name"],
                       "--base-commit", manifest["merge_base"], "--config", str(packet)]
        wrapper = [] if name == "codex" else guarded(
            [], Path(manifest["repository"]), scratch, inputs, output, private_paths)
        specs.append(WorkerSpec(name, "reviewer", command,
                               output / "stdout.log" if name == "codex" else report,
                               output / "stderr.log", report,
                               packet if name in {"claude", "codex"} else None, tuple(wrapper),
                               "codex-read-only" if name == "codex" else "os-read-only", preflight_error, limitations))
    if "feedback" not in settings.get("workers", ("claude", "codex", "coderabbit", "feedback")):
        return specs
    output = scratch / "existing-feedback"
    specs.append(WorkerSpec("feedback", "collector",
                 [sys.executable, str(runner), "_collect-feedback", "--pr-json", str(pr_json),
                  "--output-dir", str(output)], scratch / "feedback-collector.out",
                 scratch / "feedback-collector.err", output / "manifest.json"))
    return specs


def validate_report(report: Path, snapshot: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(snapshot.parent / "report.py"), "validate", str(report),
         "--changed-paths", str(snapshot.parent / "changed-paths.json")],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
    )
    detail = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if result.returncode:
        return False, detail
    manifest = json.loads(snapshot.read_text())
    expected = f"Scope: `{manifest['merge_base']}..{manifest['target']['head']}`"
    scope = next(line for line in report.read_text().splitlines() if line.startswith("Scope: `"))
    if scope != expected:
        return False, f"report Scope differs from the frozen comparison; expected {expected}"
    return True, detail


def validate_jsonl(report: Path, snapshot: Path) -> tuple[bool, str]:
    try:
        events = [json.loads(line) for line in report.read_text().splitlines() if line.strip()]
        if not events or any(not isinstance(event, dict) for event in events):
            return False, "CodeRabbit emitted no structured review events"
        allowed = {"review_context", "status", "heartbeat", "finding", "complete"}
        for event in events:
            if event.get("type") in {"error", "action_required"}:
                return False, "CodeRabbit failure: " + json.dumps(event)
            if event.get("type") not in allowed:
                return False, f"unsupported CodeRabbit event: {event.get('type')!r}"
        context = [e for e in events if e["type"] == "review_context"]
        manifest = json.loads(snapshot.read_text())
        if len(context) != 1 or context[0].get("reviewType") != "committed" or context[0].get("baseCommit") != manifest["merge_base"]:
            return False, "CodeRabbit did not confirm the frozen comparison"
        completions = [e for e in events if e["type"] == "complete"]
        if len(completions) != 1 or events[-1] != completions[0]:
            return False, "CodeRabbit needs exactly one final completion event"
        findings = [e for e in events if e["type"] == "finding"]
        complete = completions[0]
        unreviewed = complete.get("unreviewedFileCount", 0)
        if type(unreviewed) is not int or unreviewed < 0:
            return False, "malformed CodeRabbit unreviewedFileCount"
        if complete.get("outcome") == "failed" or unreviewed:
            return False, "CodeRabbit completion reports an incomplete review"
        if "no fresh detailed file review" in str(complete.get("message", "")).casefold():
            return False, "CodeRabbit reused a local checkpoint without a fresh review"
        if type(complete.get("findings")) is not int or complete["findings"] != len(findings):
            return False, "CodeRabbit finding count disagrees with its events"
        paths = json.loads((snapshot.parent / "changed-paths.json").read_text())
        if complete.get("status") == "review_skipped":
            if paths or findings:
                return False, "CodeRabbit skipped a nonempty scope"
        elif complete.get("status") != "review_completed":
            return False, "CodeRabbit review did not complete"
        for finding in findings:
            if not all(isinstance(finding.get(key), str) and finding[key].strip()
                       for key in ("fileName", "severity", "codegenInstructions")):
                return False, "malformed CodeRabbit finding"
        reported = complete.get("reviewedFiles")
        if reported is not None and (not isinstance(reported, list) or any(not isinstance(p, str) for p in reported)):
            return False, "malformed CodeRabbit reviewedFiles"
        if paths and reported == []:
            return False, "CodeRabbit reported no reviewed files for a nonempty scope"
        return True, f"CodeRabbit complete: {len(findings)} findings; native reviewedFiles={reported!r}; no canonical per-path coverage claimed"
    except (OSError, ValueError, KeyError) as error:
        return False, str(error)


def validate_worker(spec: WorkerSpec, snapshot: Path) -> tuple[bool, str, str]:
    if not spec.report_path.is_file():
        return False, "missing output", "invalid"
    if spec.name == "claude" and spec.stderr_path.is_file():
        if str(snapshot.parent) + " is a network path" in spec.stderr_path.read_text(errors="replace"):
            return False, "Claude rejected access to the shared input directory", "invalid"
    if spec.name in {"claude", "codex"}:
        valid, detail = validate_report(spec.report_path, snapshot)
    elif spec.name == "coderabbit":
        valid, detail = validate_jsonl(spec.report_path, snapshot)
    else:
        try:
            manifest = json.loads(spec.report_path.read_text())
            status = manifest.get("status")
            if status in {"complete", "partial"}:
                return True, f"feedback collection {status}", status
            return False, "invalid feedback manifest", "invalid"
        except (OSError, ValueError) as error:
            return False, str(error), "invalid"
    if spec.limitations:
        detail += "; " + "; ".join(spec.limitations)
    return valid, detail, "valid" if valid else "invalid"
