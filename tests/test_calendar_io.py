from __future__ import annotations

from datetime import date, datetime

import pytest

from radicale_calendar.calendar_io import build_calendar, master_event, parse_local_datetime
from radicale_calendar.errors import CalendarError
from radicale_calendar.models import EventInput


def test_rejects_nonexistent_dst_time() -> None:
    with pytest.raises(CalendarError, match="does not exist") as caught:
        parse_local_datetime("2025-03-09T02:30:00", "America/New_York")
    assert caught.value.code == "DATETIME_NONEXISTENT"


def test_requires_offset_for_ambiguous_dst_time() -> None:
    with pytest.raises(CalendarError, match="ambiguous") as caught:
        parse_local_datetime("2025-11-02T01:30:00", "America/New_York")
    assert caught.value.code == "DATETIME_AMBIGUOUS"

    parsed = parse_local_datetime("2025-11-02T01:30:00-05:00", "America/New_York")
    assert parsed.fold == 1


def test_builds_all_day_event_with_exclusive_end() -> None:
    calendar = build_calendar(
        EventInput(
            uid="all-day@example",
            title="Conference",
            start="2026-02-02",
            end="2026-02-04",
            timezone="America/Chicago",
            all_day=True,
        )
    )
    event = master_event(calendar)
    assert event.decoded("DTSTART") == date(2026, 2, 2)
    assert event.decoded("DTEND") == date(2026, 2, 4)
    assert str(event["X-RADICALE-CALENDAR-TIMEZONE"]) == "America/Chicago"


def test_recurring_timed_event_keeps_iana_timezone() -> None:
    calendar = build_calendar(
        EventInput.model_validate(
            {
                "uid": "weekly@example",
                "title": "Weekly planning",
                "start": "2026-01-05T09:00:00",
                "end": "2026-01-05T10:00:00",
                "timezone": "America/New_York",
                "recurrence": {"frequency": "weekly", "count": 4, "by_weekday": ["MO"]},
            }
        )
    )
    event = master_event(calendar)
    start = event.decoded("DTSTART")
    assert isinstance(start, datetime)
    assert getattr(start.tzinfo, "key", None) == "America/New_York"
    assert event["RRULE"]["FREQ"] == ["WEEKLY"]
