#!/usr/bin/env python3
"""Resolve periods, validate accepted activity ledgers, and render local reports."""

import argparse
import json
from pathlib import Path
import sys

from ledger import metrics, validate
from period import resolve_window
from render_report import build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    window = commands.add_parser("window")
    window.add_argument("period", choices=("yesterday", "last-week", "last-month", "custom"))
    window.add_argument("--timezone", required=True)
    window.add_argument("--now", help="Offset ISO timestamp; defaults to current time")
    window.add_argument("--start", help="Inclusive local date for custom period")
    window.add_argument("--end", help="Exclusive local date for custom period")
    window.add_argument("--week-start", type=int, choices=range(7), default=0)
    for command in ("validate", "metrics", "build"):
        child = commands.add_parser(command)
        child.add_argument("input", type=Path)
        if command == "build":
            child.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "window":
            result = resolve_window(args.period, args.timezone, args.now, args.start, args.end, args.week_start)
        else:
            data = validate(json.loads(args.input.read_text(encoding="utf-8")))
            if args.command == "build":
                result = {"index": str(build(data, args.output).resolve())}
            elif args.command == "metrics":
                result = metrics(data)
            else:
                result = {"valid": True, "events": len(data["events"]), "sources": len(data["sources"])}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"activity-report: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
