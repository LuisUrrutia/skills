#!/usr/bin/env python3
"""Check a local verification feature map without executing its recipes."""

import argparse
import json
from pathlib import Path
import re
import sys


LINK = re.compile(r"\[[^\[\]]+\]\(([^\s)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def prose_lines(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            yield number, ""
        else:
            yield number, line if fence is None else ""


def inspect_map(skill_dir):
    diagnostics = []
    index = skill_dir / "features" / "README.md"
    feature_dir = index.parent

    def issue(path, code, message, line=None):
        item = {"path": str(path), "code": code, "message": message}
        if line is not None:
            item["line"] = line
        diagnostics.append(item)

    def read(path):
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            issue(path, "unreadable", str(error))
            return None

    def is_local(path):
        try:
            return path.resolve().parent == feature_dir.resolve()
        except (OSError, RuntimeError):
            return False

    if not is_local(index):
        issue(index, "escaping-link", "The index must be a local file.")
        return diagnostics, []
    contents = read(index)
    if contents is None:
        return diagnostics, []
    lines = list(prose_lines(contents))
    sections = [(n, text) for n, text in lines if text == "## Features"]
    if len(sections) != 1:
        issue(index, "feature-section", "Expected exactly one '## Features' section.")

    links = []
    inside = False
    for number, line in lines:
        heading = HEADING.match(line)
        if heading and len(heading[1]) <= 2:
            inside = line == "## Features"
            continue
        if inside:
            for target in LINK.findall(line):
                links.append((number, target))
    if not links:
        issue(index, "empty-index", "The Features section needs inline links to feature files.")

    indexed = set()
    for number, target in links:
        name = target.split("#", 1)[0]
        if (not name.endswith(".md") or name == "README.md"
                or "/" in name or "\\" in name or ":" in name
                or "%" in name or "?" in name or name in {".", ".."}):
            issue(index, "invalid-link", "Link a direct sibling .md feature file.", number)
            continue
        if name in indexed:
            issue(index, "duplicate-link", f"Feature is linked more than once: {name}", number)
        indexed.add(name)
        path = feature_dir / name
        if not is_local(path):
            issue(index, "escaping-link", f"Feature resolves outside its directory: {name}", number)
        elif not path.is_file():
            issue(index, "missing-feature", f"Feature file does not exist: {name}", number)

    try:
        files = {path.name for path in feature_dir.iterdir() if path.suffix == ".md" and path.name != "README.md"}
    except OSError as error:
        issue(feature_dir, "unreadable", str(error))
        files = set()
    for name in sorted(files - indexed):
        issue(feature_dir / name, "unindexed-feature", "Feature is absent from the index.")

    for name in sorted(files | indexed):
        path = feature_dir / name
        if not is_local(path) or not path.is_file():
            continue
        contents = read(path)
        if contents is None:
            continue
        lines = list(prose_lines(contents))
        headings = [(n, len(match[1]), match[2]) for n, line in lines if (match := HEADING.match(line))]
        titles = [(n, title) for n, level, title in headings if level == 1]
        sections = [(n, title) for n, level, title in headings if level == 2]
        if len(titles) != 1 or not headings or headings[0][1] != 1:
            issue(path, "feature-title", "Expected one initial H1 feature title.")
        if titles and sections and not any(line.strip() for n, line in lines if titles[0][0] < n < sections[0][0]):
            issue(path, "feature-description", "Add a user-visible description before the sections.")
        names = [title for _, title in sections]
        if (len(names) != 4 or names[:2] != ["Sub-features", "How to get to it (user POV)"]
                or names[-1:] != ["Gotchas"] or not names[2].startswith("Driving it with ")):
            issue(path, "feature-sections", "Expected Sub-features, How to get to it (user POV), Driving it with <actual name>, and Gotchas, in order.")
        elif (not names[2].removeprefix("Driving it with ").strip()
                or re.search(r"[<>]|\b(?:actual|real|your) harness\b|\bTBD\b", names[2], re.I)):
            issue(path, "harness-placeholder", "Name the actual driving harness.")
        for position, (number, title) in enumerate(sections):
            end = sections[position + 1][0] if position + 1 < len(sections) else len(contents.splitlines()) + 1
            if not any(line.strip() for line in contents.splitlines()[number:end - 1]):
                issue(path, "empty-section", f"Section is empty: {title}", number)

    return diagnostics, sorted(indexed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True, type=Path)
    args = parser.parse_args()
    diagnostics, features = inspect_map(args.skill_dir)
    exit_code = 2 if any(item["code"] == "unreadable" for item in diagnostics) else int(bool(diagnostics))
    print(json.dumps({"valid": exit_code == 0, "features": features, "diagnostics": diagnostics}, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
