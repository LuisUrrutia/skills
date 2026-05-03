#!/usr/bin/env python3
"""
Get OpenCode conversation digest for daily standup integration.

Usage:
    opencode_digest.py [--date DATE] [--project PATH] [--format json|text]

Examples:
    opencode_digest.py                    # Yesterday's digest (default)
    opencode_digest.py --date today       # Today's digest
    opencode_digest.py --date 2026-01-20  # Specific date
    opencode_digest.py --format json      # JSON output for parsing
    opencode_digest.py --db ~/opencode.db # Read a specific OpenCode DB

By default, the digest scans every project in the OpenCode database. Use
--project only when you want to narrow the digest to one project path.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def get_opencode_db_path() -> Path:
    """Get the default OpenCode SQLite database path."""
    override = os.environ.get("OPENCODE_DB")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def parse_date_arg(date_arg: str) -> datetime:
    """Parse date argument."""
    today = datetime.now()

    if date_arg == "today":
        return today
    if date_arg == "yesterday":
        return today - timedelta(days=1)

    try:
        return datetime.strptime(date_arg, "%Y-%m-%d")
    except ValueError:
        print(
            f"Invalid date: {date_arg}. Use 'today', 'yesterday', or YYYY-MM-DD",
            file=sys.stderr,
        )
        sys.exit(1)


def day_bounds_ms(target_date: datetime) -> tuple[int, int]:
    """Return local-day start/end timestamps in milliseconds."""
    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000)


def parse_json(value: Optional[str]) -> dict:
    if not value:
        return {}
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def clean_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > 80:
        return value[:77] + "..."
    return value or "Untitled session"


def maybe_file(value) -> Optional[str]:
    if not isinstance(value, str) or not value.strip():
        return None
    cleaned = value.strip()
    if cleaned.startswith(("http://", "https://")):
        return None
    path = Path(cleaned).expanduser()
    if cleaned.endswith(("/", "\\")) or (path.exists() and path.is_dir()):
        return None
    name = Path(cleaned).name
    if path.exists():
        return name if path.is_file() else None
    if Path(name).suffix or name in {"Dockerfile", "Makefile", "LICENSE"}:
        return name
    return None


def add_file(files: set[str], value) -> None:
    filename = maybe_file(value)
    if filename:
        files.add(filename)


def add_files_from_patch(files: set[str], value) -> None:
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                add_file(files, item)
            elif isinstance(item, dict):
                for key in ("path", "filename", "file", "old", "new"):
                    add_file(files, item.get(key))
    elif isinstance(value, dict):
        for key, item in value.items():
            add_file(files, key)
            if isinstance(item, dict):
                for nested_key in ("path", "filename", "file", "old", "new"):
                    add_file(files, item.get(nested_key))


def add_files_from_tool_input(files: set[str], value) -> None:
    if not isinstance(value, dict):
        return

    for key in (
        "filePath",
        "file_path",
        "path",
        "filename",
        "oldPath",
        "newPath",
    ):
        add_file(files, value.get(key))


def session_details(conn: sqlite3.Connection, session_id: str) -> tuple[list[str], int, str]:
    """Extract touched files, bash command count, and first user text."""
    files: set[str] = set()
    commands_count = 0
    first_user_message = ""

    rows = conn.execute(
        """
        SELECT message.data, part.data
        FROM message
        LEFT JOIN part ON part.message_id = message.id
        WHERE message.session_id = ?
        ORDER BY message.time_created, message.id, part.time_created, part.id
        """,
        (session_id,),
    ).fetchall()

    for message_data, part_data in rows:
        message = parse_json(message_data)
        part = parse_json(part_data)

        if (
            not first_user_message
            and message.get("role") == "user"
            and part.get("type") == "text"
        ):
            text = part.get("text", "")
            if isinstance(text, str):
                first_user_message = text

        part_type = part.get("type")
        if part_type == "tool":
            tool_name = str(part.get("tool", "")).lower()
            if tool_name == "bash":
                commands_count += 1
            state = part.get("state")
            if isinstance(state, dict):
                add_files_from_tool_input(files, state.get("input"))
        elif part_type == "patch":
            add_files_from_patch(files, part.get("files"))
        elif part_type == "file":
            add_file(files, part.get("filename"))

    return sorted(files)[:10], commands_count, first_user_message


def get_sessions_for_date(
    target_date: datetime,
    project_path: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> list[dict]:
    """Get all OpenCode sessions for a specific date."""
    database = db_path or get_opencode_db_path()
    if not database.exists():
        return []

    start_ms, end_ms = day_bounds_ms(target_date)
    project_filter = None
    if project_path:
        project_filter = str(Path(project_path).expanduser().resolve())

    conn = sqlite3.connect(database)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT
                session.id,
                session.title,
                session.directory,
                session.path,
                session.summary_files,
                session.summary_diffs,
                session.time_created,
                project.worktree
            FROM session
            LEFT JOIN project ON project.id = session.project_id
            WHERE session.time_created >= ? AND session.time_created < ?
            ORDER BY session.time_created
            """,
            (start_ms, end_ms),
        ).fetchall()

        sessions = []
        for row in rows:
            project = row["directory"] or row["path"] or row["worktree"] or ""
            if project_filter:
                candidates = [project, row["path"], row["worktree"]]
                resolved = {
                    str(Path(candidate).expanduser().resolve())
                    for candidate in candidates
                    if candidate
                }
                if project_filter not in resolved:
                    continue

            files, commands_count, first_user_message = session_details(conn, row["id"])
            summary_files = row["summary_files"] or 0
            title = clean_title(row["title"] or first_user_message)

            sessions.append(
                {
                    "id": row["id"][:12],
                    "title": title,
                    "project": project,
                    "branch": None,
                    "files": files,
                    "commands_count": commands_count,
                    "timestamp": datetime.fromtimestamp(
                        row["time_created"] / 1000
                    ).isoformat(),
                    "summary_files": summary_files,
                }
            )
    finally:
        conn.close()

    return sessions


def format_text(sessions: list[dict], target_date: datetime) -> str:
    """Format sessions as Markdown text."""
    date_str = target_date.strftime("%B %d, %Y")

    if not sessions:
        return f"No OpenCode sessions found for {date_str}"

    lines = [
        f"## {date_str} - {len(sessions)} OpenCode session{'s' if len(sessions) != 1 else ''}",
        "",
    ]

    for index, session in enumerate(sessions, 1):
        lines.append(f"### {index}. {session['title']}")
        lines.append(f"   Session: `{session['id']}`")
        if session["project"]:
            lines.append(f"   Project: `{session['project']}`")
        if session["files"]:
            lines.append(f"   Files: {', '.join(session['files'][:5])}")
        elif session["summary_files"]:
            lines.append(f"   Files changed: {session['summary_files']}")
        if session["commands_count"]:
            lines.append(f"   Commands: {session['commands_count']} executed")
        lines.append("")

    return "\n".join(lines)


def format_json(sessions: list[dict], target_date: datetime) -> dict:
    """Format sessions as JSON-compatible data."""
    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "session_count": len(sessions),
        "sessions": [
            {
                "id": session["id"],
                "title": session["title"],
                "project": session["project"],
                "branch": session["branch"],
                "files": session["files"],
                "commands_count": session["commands_count"],
            }
            for session in sessions
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Get OpenCode conversation digest for daily standup"
    )
    parser.add_argument(
        "--date",
        "-d",
        default="yesterday",
        help="Date to get digest for (today, yesterday, or YYYY-MM-DD). Default: yesterday",
    )
    parser.add_argument(
        "--project",
        "-p",
        help="Filter to a specific project path (default: all projects)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="Path to OpenCode SQLite database (default: ~/.local/share/opencode/opencode.db)",
    )

    args = parser.parse_args()
    target_date = parse_date_arg(args.date)
    sessions = get_sessions_for_date(target_date, args.project, args.db)

    if args.format == "json":
        print(json.dumps(format_json(sessions, target_date), indent=2))
    else:
        print(format_text(sessions, target_date))


if __name__ == "__main__":
    main()
