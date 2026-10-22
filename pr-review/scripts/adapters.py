"""CLI transport and completion checks; audit criteria belong to the shared packet."""
from __future__ import annotations

import json
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


def build_specs(snapshot: Path, manifest: dict, scratch: Path, pr_json: Path,
                runner: Path, settings: dict) -> list[WorkerSpec]:
    inputs = snapshot.parent
    packet = inputs / "packet.md"
    specs = []
    private_paths = (snapshot, *(Path(path) for path in manifest.get("private_paths", [])))
    for name in ("claude", "codex"):
        if name not in settings["workers"]:
            continue
        output = scratch / name
        output.mkdir(exist_ok=True)
        report = output / "review.md"
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
        else:
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
        wrapper = [] if name == "codex" else guarded(
            [], Path(manifest["repository"]), scratch, inputs, output, private_paths)
        specs.append(WorkerSpec(name, "reviewer", command,
                               output / "stdout.log" if name == "codex" else report,
                               output / "stderr.log", report, packet, tuple(wrapper),
                               "codex-read-only" if name == "codex" else "os-read-only"))
    if "feedback" not in settings["workers"]:
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


def validate_worker(spec: WorkerSpec, snapshot: Path) -> tuple[bool, str, str]:
    if not spec.report_path.is_file():
        return False, "missing output", "invalid"
    if spec.name == "claude" and spec.stderr_path.is_file():
        if str(snapshot.parent) + " is a network path" in spec.stderr_path.read_text(errors="replace"):
            return False, "Claude rejected access to the shared input directory", "invalid"
    if spec.name in {"claude", "codex"}:
        valid, detail = validate_report(spec.report_path, snapshot)
        return valid, detail, "valid" if valid else "invalid"
    try:
        manifest = json.loads(spec.report_path.read_text())
        status = manifest.get("status")
        if status in {"complete", "partial"}:
            return True, f"feedback collection {status}", status
        return False, "invalid feedback manifest", "invalid"
    except (OSError, ValueError) as error:
        return False, str(error), "invalid"
