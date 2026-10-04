#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

FINDING_HEADING = re.compile(
    r"^### (F[1-9][0-9]*) \| (blocker|high|med|low) \| "
    r"([^|]+:[1-9][0-9]*) \| (\S.*)$"
)
QUESTION_HEADING = re.compile(r"^### (Q[1-9][0-9]*) \| (\S.*?) \| (\S.*)$")
EVIDENCE_LINE = re.compile(
    r"^- ([a-z][a-z0-9-]*) \| `([^`]+:[1-9][0-9]*)` \| (\S.*)$"
)
COVERAGE_LINE = re.compile(r"^- (reviewed|partial|unreadable) \| `([^`]+)` \| (\S.*)$")
CHECK_LINE = re.compile(r"^- (pass|fail|not-run) \| `([^`]+)` \| (\S.*)$")
SECTIONS = ("## Review basis", "## Findings", "## Open questions", "## Checks", "## Coverage")
CLASSES = {"correctness", "security", "requirements", "standards", "maintainability", "performance", "verification"}
REQUIRED_FIELDS = (
    "Class:",
    "Action:",
    "Affected:",
    "Diff cause:",
    "Impact:",
    "Evidence:",
    "Recommendation:",
    "Unresolved premise:",
)


class ReportError(ValueError):
    pass


def section(lines: list[str], heading: str, next_heading: str | None) -> list[str]:
    try:
        start = lines.index(heading) + 1
    except ValueError as error:
        raise ReportError(f"missing section: {heading}") from error

    if next_heading is None:
        return lines[start:]

    try:
        end = lines.index(next_heading, start)
    except ValueError as error:
        raise ReportError(f"missing section: {next_heading}") from error
    return lines[start:end]


def nonempty(lines: list[str]) -> list[str]:
    return [line for line in lines if line.strip()]


def validate_report(source: Path, changed_paths: Path | None = None) -> tuple[str, int]:
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "# Code change review":
        raise ReportError("first line must be '# Code change review'")

    if [line for line in lines if line.startswith("## ")] != list(SECTIONS):
        raise ReportError("report needs each canonical section exactly once, in order")

    try:
        findings_index = lines.index("## Findings")
        questions_index = lines.index("## Open questions")
        coverage_index = lines.index("## Coverage")
    except ValueError as error:
        raise ReportError("report needs Findings, Open questions, and Coverage sections") from error
    if not findings_index < questions_index < coverage_index:
        raise ReportError("report sections are out of order")

    scope_lines = [line for line in lines[:findings_index] if line.startswith("Scope: `")]
    if len(scope_lines) != 1 or not scope_lines[0].endswith("`"):
        raise ReportError("report must contain one backtick-delimited Scope line")

    if not scope_lines[0][len("Scope: `") : -1].strip():
        raise ReportError("Scope must not be empty")
    if not nonempty(section(lines, "## Review basis", "## Findings")):
        raise ReportError("Review basis must explain intent, standards and their limits")
    findings = section(lines, "## Findings", "## Open questions")
    questions = section(lines, "## Open questions", "## Checks")
    checks = nonempty(section(lines, "## Checks", "## Coverage"))
    if not checks or any(CHECK_LINE.fullmatch(line) is None for line in checks):
        raise ReportError("Checks needs a result or explicit not-run entry")
    coverage = section(lines, "## Coverage", None)

    finding_starts = [index for index, line in enumerate(findings) if line.startswith("### ")]
    finding_ids: set[str] = set()
    if finding_starts:
        if not nonempty(findings)[0].startswith("### "):
            raise ReportError("Findings contains content before its first finding")
        finding_starts.append(len(findings))
        for pair_index in range(len(finding_starts) - 1):
            start = finding_starts[pair_index]
            end = finding_starts[pair_index + 1]
            block = nonempty(findings[start:end])
            match = FINDING_HEADING.fullmatch(block[0])
            if match is None:
                raise ReportError(f"malformed finding heading: {block[0]}")
            finding_id = match.group(1)
            if finding_id in finding_ids:
                raise ReportError(f"duplicate finding ID: {finding_id}")
            finding_ids.add(finding_id)

            positions: list[int] = []
            for field in REQUIRED_FIELDS:
                matches = [index for index, line in enumerate(block) if line.startswith(field)]
                if len(matches) != 1:
                    raise ReportError(f"{finding_id} must contain one '{field}' field")
                if field != "Evidence:" and not block[matches[0]][len(field):].strip():
                    raise ReportError(f"{finding_id} has an empty '{field}' field")
                positions.append(matches[0])
            if positions != sorted(positions):
                raise ReportError(f"{finding_id} fields are out of order")

            if block[positions[0]][len("Class:"):].strip() not in CLASSES:
                raise ReportError(f"{finding_id} has an unsupported Class")
            if block[positions[1]][len("Action:"):].strip() not in {"required", "optional"}:
                raise ReportError(f"{finding_id} Action must be required or optional")
            evidence_start = positions[5] + 1
            evidence_end = positions[6]
            evidence = block[evidence_start:evidence_end]
            if not evidence or any(EVIDENCE_LINE.fullmatch(line) is None for line in evidence):
                raise ReportError(f"{finding_id} needs one or more well-formed evidence lines")
    elif nonempty(findings) != ["None."]:
        raise ReportError("empty Findings must contain exactly 'None.'")

    question_lines = nonempty(questions)
    if question_lines != ["None."]:
        question_starts = [index for index, line in enumerate(questions) if line.startswith("### ")]
        if not question_starts:
            raise ReportError("Open questions must contain Q headings or 'None.'")
        if not question_lines[0].startswith("### "):
            raise ReportError("Open questions contains content before its first question")
        question_starts.append(len(questions))
        question_ids: set[str] = set()
        for pair_index in range(len(question_starts) - 1):
            start = question_starts[pair_index]
            end = question_starts[pair_index + 1]
            block = nonempty(questions[start:end])
            match = QUESTION_HEADING.fullmatch(block[0])
            if match is None:
                raise ReportError(f"malformed question heading: {block[0]}")
            question_id = match.group(1)
            if question_id in question_ids:
                raise ReportError(f"duplicate question ID: {question_id}")
            question_ids.add(question_id)
            needed = [line for line in block if line.startswith("Needed evidence:")]
            if len(needed) != 1 or not needed[0][len("Needed evidence:"):].strip():
                raise ReportError(f"{question_id} must contain one 'Needed evidence:' field")

    coverage_lines = nonempty(coverage)
    if not coverage_lines:
        raise ReportError("Coverage must list paths or explicitly contain 'None.'")
    if coverage_lines == ["None."]:
        coverage_lines = []
    coverage_matches = [COVERAGE_LINE.fullmatch(line) for line in coverage_lines]
    if any(match is None for match in coverage_matches):
        raise ReportError("Coverage needs one well-formed entry per changed path")
    coverage_paths = [match.group(2) for match in coverage_matches if match is not None]
    if len(coverage_paths) != len(set(coverage_paths)):
        raise ReportError("Coverage contains duplicate paths")

    if changed_paths is not None:
        try:
            expected = json.loads(changed_paths.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ReportError(f"invalid changed-path inventory: {error}") from error
        if not isinstance(expected, list) or any(not isinstance(path, str) or not path.strip() for path in expected):
            raise ReportError("changed-path inventory must be an array of nonempty strings")
        if len(expected) != len(set(expected)):
            raise ReportError("changed-path inventory contains duplicates")
        if set(expected) != set(coverage_paths):
            missing = sorted(set(expected) - set(coverage_paths))
            extra = sorted(set(coverage_paths) - set(expected))
            raise ReportError(f"Coverage differs from inventory; missing={missing}, extra={extra}")
    elif not coverage_paths:
        raise ReportError("empty Coverage requires an explicit empty changed-path inventory")

    if not coverage_paths and finding_ids:
        raise ReportError("an empty change cannot contain findings")

    return scope_lines[0][len("Scope: `") : -1], len(finding_ids)


def inline_markup(value: str) -> str:
    parts = value.split("`")
    rendered: list[str] = []
    for index, part in enumerate(parts):
        escaped = html.escape(part)
        rendered.append(f"<code>{escaped}</code>" if index % 2 else escaped)
    return "".join(rendered)


def markdown_body(lines: list[str]) -> str:
    rendered: list[str] = []
    list_open = False

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            rendered.append("</ul>")
            list_open = False

    for line in lines:
        if not line:
            close_list()
            continue
        if line.startswith("### "):
            close_list()
            finding = FINDING_HEADING.fullmatch(line)
            severity = f' class="finding {finding.group(2)}"' if finding else ""
            rendered.append(f"<h3{severity}>{inline_markup(line[4:])}</h3>")
        elif line.startswith("## "):
            close_list()
            rendered.append(f"<h2>{inline_markup(line[3:])}</h2>")
        elif line.startswith("# "):
            close_list()
            rendered.append(f"<h1>{inline_markup(line[2:])}</h1>")
        elif line.startswith("- "):
            if not list_open:
                rendered.append("<ul>")
                list_open = True
            rendered.append(f"<li>{inline_markup(line[2:])}</li>")
        else:
            close_list()
            label = re.match(r"^([A-Za-z ]+):(.*)$", line)
            if label:
                rendered.append(
                    f"<p><strong>{html.escape(label.group(1))}:</strong>"
                    f"{inline_markup(label.group(2))}</p>"
                )
            else:
                rendered.append(f"<p>{inline_markup(line)}</p>")
    close_list()
    return "\n".join(rendered)


def render_report(source: Path, output: Path, changed_paths: Path | None = None) -> int:
    scope, finding_count = validate_report(source, changed_paths)
    stylesheet = output.with_suffix(".css")
    if source.resolve() in {output.resolve(), stylesheet.resolve()} or output.resolve() == stylesheet.resolve():
        raise ReportError("render outputs must not overwrite the canonical report or each other")
    body = markdown_body(source.read_text(encoding="utf-8").splitlines())
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Code change review — {html.escape(scope)}</title>
<link rel="stylesheet" href="{html.escape(stylesheet.name, quote=True)}">
</head>
<body><main>
{body}
</main></body>
</html>
"""
    stylesheet.write_text((Path(__file__).resolve().parents[1] / "assets/report.css").read_text(encoding="utf-8"), encoding="utf-8")
    output.write_text(document, encoding="utf-8")
    return finding_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and render code-change review reports")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("report", type=Path)
    validate_parser.add_argument("--changed-paths", type=Path)

    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("report", type=Path)
    render_parser.add_argument("output", type=Path)
    render_parser.add_argument("--changed-paths", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "validate":
            _, finding_count = validate_report(args.report, args.changed_paths)
        else:
            finding_count = render_report(args.report, args.output, args.changed_paths)
    except (OSError, ReportError) as error:
        print(f"invalid code change review: {error}", file=sys.stderr)
        return 1

    print(f"report format valid: {finding_count} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
