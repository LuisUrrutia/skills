"""Resolve calendar periods without assuming a fixed number of hours per day."""

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


def instant(value):
    if not isinstance(value, str):
        raise ValueError("Timestamp must be an ISO 8601 string with an offset")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"Timestamp requires an offset: {value}")
    return parsed.astimezone(timezone.utc)


def resolve_window(period, timezone_name, now=None, start=None, end=None, week_start=0):
    zone = ZoneInfo(timezone_name)
    today = (instant(now) if now else datetime.now(timezone.utc)).astimezone(zone).date()
    if period == "yesterday":
        first, last = today - timedelta(days=1), today
    elif period == "last-week":
        last = today - timedelta(days=(today.weekday() - week_start) % 7)
        first = last - timedelta(days=7)
    elif period == "last-month":
        last = today.replace(day=1)
        first = (last - timedelta(days=1)).replace(day=1)
    elif period == "custom" and start and end:
        first, last = date.fromisoformat(start), date.fromisoformat(end)
    else:
        raise ValueError("Custom periods require --start and exclusive --end dates")
    if first >= last:
        raise ValueError("The period must have positive length")
    boundaries = [datetime.combine(day, time.min, zone) for day in (first, last)]
    for boundary in boundaries:
        if boundary.astimezone(timezone.utc).astimezone(zone) != boundary:
            raise ValueError("This timezone has a skipped midnight; supply explicit instants in the report")
    return {
        "timezone": timezone_name,
        "start": boundaries[0].isoformat(),
        "end": boundaries[1].isoformat(),
        "label": f"{first.isoformat()} to {last.isoformat()} (end exclusive)",
        "week_start": week_start,
    }
