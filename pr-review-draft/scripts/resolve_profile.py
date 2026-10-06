#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

MATCH_ROW = re.compile(
    r"^\|\s*`(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)`\s*\|"
)


class ProfileError(RuntimeError):
    pass


def normalize_repo(value: str) -> str:
    repo = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ProfileError(f"expected owner/repo, got {value!r}")
    owner, name = repo.split("/", 1)
    if not owner or not name:
        raise ProfileError(f"expected owner/repo, got {value!r}")
    return repo.casefold()


def profile_matches(path: Path) -> set[str]:
    matches: set[str] = set()
    in_matches = False
    found_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "## Matches":
            in_matches = True
            found_section = True
            continue
        if in_matches and line.startswith("## "):
            break
        if not in_matches:
            continue
        row = MATCH_ROW.match(line)
        if row and row.group("repo") != "owner/repo":
            matches.add(normalize_repo(row.group("repo")))
    if not found_section:
        raise ProfileError(f"profile has no Matches section: {path}")
    if not matches:
        raise ProfileError(f"profile has no repository match: {path}")
    if len(matches) != 1:
        raise ProfileError(f"profile must match exactly one repository: {path}")
    return matches


def resolve_profile(repo: str, profiles_dir: Path | None = None) -> dict[str, Any]:
    normalized_repo = normalize_repo(repo)
    explicit = profiles_dir is not None
    if profiles_dir is None:
        profiles_dir = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "pr-review-draft/profiles"
    if not profiles_dir.exists() and not profiles_dir.is_symlink() and not explicit:
        return {"repo": normalized_repo, "status": "none", "profile": None}
    if not profiles_dir.is_dir():
        raise ProfileError(f"missing profiles directory: {profiles_dir}")

    profiles = [
        path.resolve()
        for path in sorted(profiles_dir.iterdir()) if path.suffix == ".md"
        if normalized_repo in profile_matches(path)
    ]
    if not profiles:
        return {"repo": normalized_repo, "status": "none", "profile": None}
    if len(profiles) == 1:
        return {
            "repo": normalized_repo,
            "status": "matched",
            "profile": str(profiles[0]),
        }
    return {
        "repo": normalized_repo,
        "status": "ambiguous",
        "profile": None,
        "profiles": [str(path) for path in profiles],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve a pr-review-draft profile for one GitHub repository"
    )
    parser.add_argument("repo", help="GitHub repository as owner/repo")
    parser.add_argument(
        "--profiles-dir",
        type=Path,
        help="External private profile directory; defaults to XDG_CONFIG_HOME/pr-review-draft/profiles",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = resolve_profile(args.repo, args.profiles_dir.resolve() if args.profiles_dir else None)
    except (OSError, ProfileError) as error:
        print(json.dumps({"status": "error", "profile": None, "error": str(error)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
