import json
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from tests.script_loader import load_script_module


opencode_digest = load_script_module("opencode_digest.py")


def millis(value: str) -> int:
    return int(datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)


def insert_json(conn, table: str, values: dict) -> None:
    columns = ", ".join(values.keys())
    placeholders = ", ".join("?" for _ in values)
    conn.execute(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        tuple(values.values()),
    )


class OpenCodeDigestTests(unittest.TestCase):
    def create_db(self, path: Path) -> None:
        conn = sqlite3.connect(path)
        conn.executescript(
            """
            CREATE TABLE project (
                id text PRIMARY KEY,
                worktree text NOT NULL
            );
            CREATE TABLE session (
                id text PRIMARY KEY,
                project_id text NOT NULL,
                title text NOT NULL,
                directory text NOT NULL,
                path text,
                summary_files integer,
                summary_diffs text,
                time_created integer NOT NULL
            );
            CREATE TABLE message (
                id text PRIMARY KEY,
                session_id text NOT NULL,
                time_created integer NOT NULL,
                data text NOT NULL
            );
            CREATE TABLE part (
                id text PRIMARY KEY,
                message_id text NOT NULL,
                session_id text NOT NULL,
                time_created integer NOT NULL,
                data text NOT NULL
            );
            """
        )
        insert_json(conn, "project", {"id": "proj", "worktree": "/tmp/demo"})
        insert_json(conn, "project", {"id": "proj2", "worktree": "/tmp/other"})
        insert_json(
            conn,
            "session",
            {
                "id": "ses_1234567890abcdef",
                "project_id": "proj",
                "title": "Fix authentication bug",
                "directory": "/tmp/demo",
                "path": "/tmp/demo",
                "summary_files": 2,
                "summary_diffs": None,
                "time_created": millis("2026-01-20T10:30:00"),
            },
        )
        insert_json(
            conn,
            "session",
            {
                "id": "ses_second_project",
                "project_id": "proj2",
                "title": "Review deployment plan",
                "directory": "/tmp/other",
                "path": "/tmp/other",
                "summary_files": 0,
                "summary_diffs": None,
                "time_created": millis("2026-01-20T11:30:00"),
            },
        )
        insert_json(
            conn,
            "session",
            {
                "id": "ses_other",
                "project_id": "proj",
                "title": "Other day",
                "directory": "/tmp/demo",
                "path": "/tmp/demo",
                "summary_files": 0,
                "summary_diffs": None,
                "time_created": millis("2026-01-21T10:30:00"),
            },
        )
        insert_json(
            conn,
            "message",
            {
                "id": "msg1",
                "session_id": "ses_1234567890abcdef",
                "time_created": millis("2026-01-20T10:31:00"),
                "data": json.dumps({"role": "user"}),
            },
        )
        insert_json(
            conn,
            "part",
            {
                "id": "part1",
                "message_id": "msg1",
                "session_id": "ses_1234567890abcdef",
                "time_created": millis("2026-01-20T10:31:00"),
                "data": json.dumps({"type": "text", "text": "Please fix auth"}),
            },
        )
        insert_json(
            conn,
            "part",
            {
                "id": "part2",
                "message_id": "msg1",
                "session_id": "ses_1234567890abcdef",
                "time_created": millis("2026-01-20T10:32:00"),
                "data": json.dumps(
                    {
                        "type": "tool",
                        "tool": "bash",
                        "state": {"input": {"command": "pytest tests"}},
                    }
                ),
            },
        )
        insert_json(
            conn,
            "part",
            {
                "id": "part3",
                "message_id": "msg1",
                "session_id": "ses_1234567890abcdef",
                "time_created": millis("2026-01-20T10:33:00"),
                "data": json.dumps(
                    {
                        "type": "tool",
                        "tool": "read",
                        "state": {"input": {"filePath": "/tmp/demo/auth.ts"}},
                    }
                ),
            },
        )
        insert_json(
            conn,
            "part",
            {
                "id": "part4",
                "message_id": "msg1",
                "session_id": "ses_1234567890abcdef",
                "time_created": millis("2026-01-20T10:34:00"),
                "data": json.dumps({"type": "patch", "files": ["/tmp/demo/login.ts"]}),
            },
        )
        conn.commit()
        conn.close()

    def test_get_sessions_for_date_defaults_to_all_projects(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "opencode.db"
            self.create_db(db_path)

            sessions = opencode_digest.get_sessions_for_date(
                datetime(2026, 1, 20), db_path=db_path
            )

        self.assertEqual(len(sessions), 2)
        self.assertEqual(sessions[0]["id"], "ses_12345678")
        self.assertEqual(sessions[0]["title"], "Fix authentication bug")
        self.assertEqual(sessions[0]["project"], "/tmp/demo")
        self.assertEqual(sessions[0]["files"], ["auth.ts", "login.ts"])
        self.assertEqual(sessions[0]["commands_count"], 1)
        self.assertEqual(sessions[1]["project"], "/tmp/other")

    def test_project_filter_matches_resolved_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "opencode.db"
            self.create_db(db_path)

            sessions = opencode_digest.get_sessions_for_date(
                datetime(2026, 1, 20), project_path="/tmp/demo", db_path=db_path
            )
            missing = opencode_digest.get_sessions_for_date(
                datetime(2026, 1, 20), project_path="/tmp/missing", db_path=db_path
            )

        self.assertEqual(len(sessions), 1)
        self.assertEqual(missing, [])

    def test_format_json_matches_digest_contract(self):
        sessions = [
            {
                "id": "ses_123",
                "title": "Fix auth",
                "project": "/tmp/demo",
                "branch": None,
                "files": ["auth.ts"],
                "commands_count": 1,
            }
        ]

        payload = opencode_digest.format_json(sessions, datetime(2026, 1, 20))

        self.assertEqual(payload["date"], "2026-01-20")
        self.assertEqual(payload["session_count"], 1)
        self.assertEqual(payload["sessions"][0]["title"], "Fix auth")


if __name__ == "__main__":
    unittest.main()
