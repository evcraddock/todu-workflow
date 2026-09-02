from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from icalendar import Calendar, Event
from icalendar.prop import vRecur

from .errors import CalendarError
from .models import EventInput, Recurrence

PRODID = "-//radicale-calendar-cli//EN"


def timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise CalendarError("TIMEZONE_INVALID", f"unknown IANA timezone: {name}") from exc


def parse_local_datetime(value: str, timezone_name: str) -> datetime:
    zone = timezone(timezone_name)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise CalendarError("DATETIME_INVALID", f"invalid ISO 8601 datetime: {value}") from exc

    if parsed.tzinfo is not None:
        local = parsed.astimezone(zone)
        if local.replace(tzinfo=None) != parsed.replace(tzinfo=None):
            raise CalendarError(
                "DATETIME_TIMEZONE_MISMATCH",
                f"datetime offset does not represent local time in {timezone_name}: {value}",
            )
        return local

    candidates: list[datetime] = []
    for fold in (0, 1):
        candidate = parsed.replace(tzinfo=zone, fold=fold)
        round_trip = candidate.astimezone(UTC).astimezone(zone)
        if round_trip.replace(tzinfo=None) == parsed and round_trip.fold == fold:
            candidates.append(candidate)
    unique_offsets = {item.utcoffset() for item in candidates}
    if not candidates:
        raise CalendarError(
            "DATETIME_NONEXISTENT",
            f"local datetime does not exist because of a timezone transition: {value}",
        )
    if len(unique_offsets) > 1:
        raise CalendarError(
            "DATETIME_AMBIGUOUS",
            f"local datetime is ambiguous; include its UTC offset: {value}",
        )
    return candidates[0]


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise CalendarError("DATE_INVALID", f"invalid ISO 8601 date: {value}") from exc


def event_times(event: EventInput) -> tuple[date | datetime, date | datetime]:
    if event.all_day:
        start = parse_date(event.start)
        end = parse_date(event.end)
    else:
        start = parse_local_datetime(event.start, event.timezone)
        end = parse_local_datetime(event.end, event.timezone)
    if end <= start:
        raise CalendarError("EVENT_TIME_INVALID", "event end must be after event start")
    return start, end


def recurrence_value(recurrence: Recurrence, *, all_day: bool, timezone_name: str) -> vRecur:
    value: dict[str, Any] = {
        "FREQ": [recurrence.frequency.upper()],
        "INTERVAL": [recurrence.interval],
    }
    if recurrence.count is not None:
        value["COUNT"] = [recurrence.count]
    if recurrence.until is not None:
        value["UNTIL"] = [
            parse_date(recurrence.until)
            if all_day
            else parse_local_datetime(recurrence.until, timezone_name).astimezone(UTC)
        ]
    if recurrence.by_weekday:
        value["BYDAY"] = recurrence.by_weekday
    return vRecur(value)


def build_calendar(event_input: EventInput) -> Calendar:
    start, end = event_times(event_input)
    calendar = Calendar()
    calendar.add("prodid", PRODID)
    calendar.add("version", "2.0")
    event = Event()
    event.add("uid", event_input.uid)
    event.add("dtstamp", datetime.now(UTC))
    event.add("summary", event_input.title)
    event.add("dtstart", start)
    event.add("dtend", end)
    event.add("x-radicale-calendar-timezone", event_input.timezone)
    if event_input.description is not None:
        event.add("description", event_input.description)
    if event_input.location is not None:
        event.add("location", event_input.location)
    if event_input.recurrence is not None:
        event.add(
            "rrule",
            recurrence_value(
                event_input.recurrence,
                all_day=event_input.all_day,
                timezone_name=event_input.timezone,
            ),
        )
    calendar.add_component(event)
    return calendar


def primary_event(calendar: Calendar) -> Event:
    masters = [
        component for component in calendar.walk("VEVENT") if "RECURRENCE-ID" not in component
    ]
    if len(masters) != 1:
        raise CalendarError("EVENT_DATA_INVALID", "calendar data does not contain one master event")
    return masters[0]


def has_recurrence_exceptions(calendar: Calendar) -> bool:
    return any("RECURRENCE-ID" in component for component in calendar.walk("VEVENT"))


def master_event(calendar: Calendar) -> Event:
    event = primary_event(calendar)
    if has_recurrence_exceptions(calendar):
        raise CalendarError(
            "UNSUPPORTED_RECURRENCE_MUTATION",
            "calendar data contains recurrence exceptions; "
            "only basic whole-series updates are supported",
        )
    return event


def decoded_text(component: Event, name: str) -> str | None:
    value = component.get(name)
    if value is None:
        return None
    decoded = component.decoded(name)
    return decoded.decode() if isinstance(decoded, bytes) else str(decoded)


def serialize_datetime(value: date | datetime) -> str:
    return value.isoformat()


def recurrence_to_json(component: Event) -> dict[str, Any] | None:
    rule = component.get("RRULE")
    if rule is None:
        return None
    result: dict[str, Any] = {
        "frequency": str(rule["FREQ"][0]).lower(),
        "interval": int(rule.get("INTERVAL", [1])[0]),
    }
    if "COUNT" in rule:
        result["count"] = int(rule["COUNT"][0])
    if "UNTIL" in rule:
        result["until"] = serialize_datetime(rule["UNTIL"][0])
    if "BYDAY" in rule:
        result["by_weekday"] = [str(day) for day in rule["BYDAY"]]
    return result


def component_to_json(
    component: Event,
    *,
    etag: str,
    calendar_id: str,
    has_exceptions: bool = False,
) -> dict[str, Any]:
    start = component.decoded("DTSTART")
    end = component.decoded("DTEND")
    all_day = isinstance(start, date) and not isinstance(start, datetime)
    timezone_name = decoded_text(component, "X-RADICALE-CALENDAR-TIMEZONE")
    if not timezone_name and not all_day:
        timezone_name = getattr(start.tzinfo, "key", None) or str(start.tzinfo)
    return {
        "calendar": calendar_id,
        "uid": decoded_text(component, "UID"),
        "etag": etag,
        "title": decoded_text(component, "SUMMARY") or "",
        "start": serialize_datetime(start),
        "end": serialize_datetime(end),
        "timezone": timezone_name,
        "all_day": all_day,
        "description": decoded_text(component, "DESCRIPTION"),
        "location": decoded_text(component, "LOCATION"),
        "recurrence": recurrence_to_json(component),
        "has_recurrence_exceptions": has_exceptions,
    }
