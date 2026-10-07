"""OS guards for reviewed files and independent worker artifacts."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from snapshot import SnapshotError, git


def codex_permissions(scratch: Path, inputs: Path, output: Path,
                      private_paths: tuple[Path, ...] = ()) -> list[str]:
    filesystem = {str(scratch.resolve()): "deny", str(inputs.resolve()): "read",
                  str(output.resolve()): "read"}
    filesystem.update({str(path.resolve()): "deny" for path in private_paths})
    table = "{" + ", ".join(json.dumps(path) + " = " + json.dumps(access)
                             for path, access in filesystem.items()) + "}"
    return ["-c", 'default_permissions="pr-review"',
            "-c", 'permissions.pr-review.extends=":read-only"',
            "-c", "permissions.pr-review.filesystem=" + table,
            "-c", "permissions.pr-review.network.enabled=false"]


def guarded(command: list[str], repository: Path, scratch: Path,
            inputs: Path, output: Path, private_paths: tuple[Path, ...] = ()) -> list[str]:
    paths = [p.resolve() for p in (repository, scratch, inputs, output)]
    repository, scratch, inputs, output = paths
    if not inputs.is_relative_to(scratch) or not output.is_relative_to(scratch):
        raise SnapshotError("worker inputs and output must be inside its run scratch directory")
    if inputs == output or inputs.is_relative_to(output) or output.is_relative_to(inputs):
        raise SnapshotError("shared inputs and worker output must be separate")
    git_dirs = {
        Path(git(repository, "rev-parse", "--path-format=absolute", flag).decode().strip()).resolve()
        for flag in ("--git-dir", "--git-common-dir")
    }
    if sys.platform == "darwin" and shutil.which("sandbox-exec"):
        quote = lambda p: json.dumps(str(p))
        policy = [
            "(version 1)", "(allow default)",
            f"(deny file-write* (require-all (subpath {quote(repository)}) (require-not (subpath {quote(output)}))))",
            f"(deny file-write* (require-all (subpath {quote(scratch)}) (require-not (subpath {quote(output)}))))",
            f"(deny file-read-data (require-all (subpath {quote(scratch)}) (require-not (subpath {quote(inputs)})) (require-not (subpath {quote(output)}))))",
        ]
        policy += [f"(deny file-write* (subpath {quote(path)}))" for path in sorted(git_dirs)]
        policy += [f"(deny file-read* (subpath {quote(path.resolve())}))" for path in private_paths]
        return [shutil.which("sandbox-exec"), "-p", "\n".join(policy), *command]
    if sys.platform.startswith("linux") and shutil.which("bwrap"):
        prefix = [shutil.which("bwrap"), "--die-with-parent", "--bind", "/", "/",
                  "--ro-bind", str(repository), str(repository)]
        for path in sorted(git_dirs):
            prefix += ["--ro-bind", str(path), str(path)]
        prefix += ["--tmpfs", str(scratch), "--ro-bind", str(inputs), str(inputs),
                   "--bind", str(output), str(output)]
        for path in private_paths:
            prefix += ["--ro-bind", "/dev/null", str(path.resolve())]
        prefix += ["--chdir", str(repository), "--"]
        return prefix + command
    raise SnapshotError("no supported read-only guard: need macOS sandbox-exec or Linux bubblewrap")
