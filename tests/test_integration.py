from __future__ import annotations

import pytest

from radicale_calendar.calendar_io import primary_event
from radicale_calendar.errors import CalendarError, ConflictError
from radicale_calendar.models import CreateInput, DeleteInput, RangeInput, UpdateInput
from radicale_calendar.service import CalendarService


def timed_event(calendar_id: str, *, uid: str = "timed@example") -> CreateInput:
    return CreateInput.model_validate(
        {
            "calendar": calendar_id,
            "event": {
                "uid": uid,
                "title": "Team sync",
                "start": "2026-03-02T09:00:00",
                "end": "2026-03-02T09:30:00",
                "timezone": "America/Chicago",
            },
        }
    )


def test_calendar_discovery_and_timed_crud_with_etags(
    calendar_service: tuple[CalendarService, str],
) -> None:
    service, calendar_id = calendar_service
    assert service.calendars() == [
        {
            "id": calendar_id,
            "name": "Integration",
            "url": service.calendars()[0]["url"],
        }
    ]

    created = service.create_event(timed_event(calendar_id))
    assert created["uid"] == "timed@example"
    assert created["etag"]
    listed = service.list_events(
        RangeInput(
            calendar=calendar_id,
            start="2026-03-01T00:00:00",
            end="2026-03-04T00:00:00",
            timezone="America/Chicago",
        )
    )
    assert [event["uid"] for event in listed] == ["timed@example"]

    updated = service.update_event(
        UpdateInput.model_validate(
            {
                "calendar": calendar_id,
                "uid": "timed@example",
                "etag": created["etag"],
                "event": {"title": "Renamed sync"},
            }
        )
    )
    assert updated["title"] == "Renamed sync"
    assert updated["etag"] != created["etag"]

    with pytest.raises(ConflictError):
        service.update_event(
            UpdateInput.model_validate(
                {
                    "calendar": calendar_id,
                    "uid": "timed@example",
                    "etag": created["etag"],
                    "event": {"title": "Stale update"},
                }
            )
        )

    with pytest.raises(CalendarError) as confirmation:
        service.delete_event(
            DeleteInput(
                calendar=calendar_id,
                uid="timed@example",
                etag=updated["etag"],
                confirm=False,
            )
        )
    assert confirmation.value.code == "CONFIRMATION_REQUIRED"
    deleted = service.delete_event(
        DeleteInput(
            calendar=calendar_id,
            uid="timed@example",
            etag=updated["etag"],
            confirm=True,
        )
    )
    assert deleted == {"calendar": calendar_id, "uid": "timed@example", "deleted": True}


def test_all_day_and_recurring_whole_series_management(
    calendar_service: tuple[CalendarService, str],
) -> None:
    service, calendar_id = calendar_service
    all_day = service.create_event(
        CreateInput.model_validate(
            {
                "calendar": calendar_id,
                "event": {
                    "uid": "holiday@example",
                    "title": "Holiday",
                    "start": "2026-07-04",
                    "end": "2026-07-05",
                    "timezone": "America/Chicago",
                    "all_day": True,
                },
            }
        )
    )
    assert all_day["all_day"] is True
    assert all_day["start"] == "2026-07-04"
    all_day_results = service.list_events(
        RangeInput(
            calendar=calendar_id,
            start="2026-07-03T00:00:00",
            end="2026-07-06T00:00:00",
            timezone="America/Chicago",
        )
    )
    assert [event["uid"] for event in all_day_results] == ["holiday@example"]

    recurring = service.create_event(
        CreateInput.model_validate(
            {
                "calendar": calendar_id,
                "event": {
                    "uid": "series@example",
                    "title": "Standup",
                    "start": "2026-07-06T09:00:00",
                    "end": "2026-07-06T09:15:00",
                    "timezone": "America/Chicago",
                    "recurrence": {"frequency": "weekly", "count": 3, "by_weekday": ["MO"]},
                },
            }
        )
    )
    assert recurring["recurrence"]["frequency"] == "weekly"

    for scope in ("occurrence", "future"):
        with pytest.raises(CalendarError) as unsupported:
            service.update_event(
                UpdateInput.model_validate(
                    {
                        "calendar": calendar_id,
                        "uid": "series@example",
                        "etag": recurring["etag"],
                        "event": {"title": "Do not apply"},
                        "recurrence_scope": scope,
                    }
                )
            )
        assert unsupported.value.code == "UNSUPPORTED_RECURRENCE_MUTATION"

    updated = service.update_event(
        UpdateInput.model_validate(
            {
                "calendar": calendar_id,
                "uid": "series@example",
                "etag": recurring["etag"],
                "event": {"title": "Whole series"},
                "recurrence_scope": "series",
            }
        )
    )
    assert updated["title"] == "Whole series"
    assert updated["recurrence"]["count"] == 3
    service.delete_event(
        DeleteInput(
            calendar=calendar_id,
            uid="series@example",
            etag=updated["etag"],
            confirm=True,
            recurrence_scope="series",
        )
    )


def test_unsupported_existing_recurrence_is_not_modified(
    calendar_service: tuple[CalendarService, str],
) -> None:
    service, calendar_id = calendar_service
    calendar, _ = service._resolve_calendar(calendar_id)
    resource = calendar.save_event(
        ical="""BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//integration test//EN\r
BEGIN:VEVENT\r
UID:complex-series@example\r
DTSTAMP:20260101T000000Z\r
DTSTART:20260701T140000Z\r
DTEND:20260701T150000Z\r
SUMMARY:Complex series\r
RRULE:FREQ=YEARLY;BYMONTH=7\r
END:VEVENT\r
END:VCALENDAR\r
"""
    )
    current = service._resource_json(resource, calendar_id)

    with pytest.raises(CalendarError) as unsupported:
        service.update_event(
            UpdateInput.model_validate(
                {
                    "calendar": calendar_id,
                    "uid": "complex-series@example",
                    "etag": current["etag"],
                    "event": {"title": "Must not apply"},
                }
            )
        )
    assert unsupported.value.code == "UNSUPPORTED_RECURRENCE_MUTATION"

    unchanged = calendar.event_by_uid("complex-series@example").load()
    component = primary_event(unchanged.icalendar_instance)
    assert str(component["SUMMARY"]) == "Complex series"
    assert component["RRULE"]["BYMONTH"] == [7]
