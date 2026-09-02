from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import unquote, urlparse
from uuid import uuid4

from caldav import DAVClient
from caldav.elements import dav
from caldav.lib import error as caldav_error
from caldav.objects import Calendar as DavCalendar
from caldav.objects import Event as DavEvent
from icalendar import Calendar, Event

from .calendar_io import (
    build_calendar,
    component_to_json,
    ensure_supported_recurrence,
    has_recurrence_exceptions,
    master_event,
    parse_local_datetime,
    primary_event,
)
from .credentials import Settings
from .errors import CalendarError, ConflictError
from .models import CreateInput, DeleteInput, EventInput, RangeInput, UpdateInput

MANAGED_PROPERTIES = (
    "SUMMARY",
    "DTSTART",
    "DTEND",
    "DESCRIPTION",
    "LOCATION",
    "RRULE",
    "X-RADICALE-CALENDAR-TIMEZONE",
)


class CalendarService:
    def __init__(self, settings: Settings, password: str, *, timeout: int = 30) -> None:
        parsed = urlparse(settings.url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise CalendarError("CONFIG_INVALID", "Radicale URL must be an absolute HTTP(S) URL")
        if parsed.username or parsed.password:
            raise CalendarError("CONFIG_INVALID", "Radicale URL must not contain credentials")
        if parsed.scheme == "http" and not settings.allow_insecure_http:
            raise CalendarError(
                "INSECURE_CONNECTION",
                "plain HTTP is disabled; use HTTPS or explicitly allow insecure HTTP "
                "for local testing",
            )
        self.client = DAVClient(
            url=settings.url,
            username=settings.username,
            password=password,
            ssl_verify_cert=settings.verify_ssl,
            timeout=timeout,
            require_tls=not settings.allow_insecure_http,
        )

    @staticmethod
    def _calendar_id(calendar: DavCalendar) -> str:
        return unquote(calendar.url.path.rstrip("/"))

    def _calendars(self) -> list[DavCalendar]:
        try:
            return self.client.principal().calendars()
        except caldav_error.AuthorizationError as exc:
            raise CalendarError("AUTHENTICATION_FAILED", "Radicale authentication failed") from exc
        except Exception as exc:
            raise CalendarError(
                "CALDAV_CONNECTION_FAILED",
                "could not connect to or discover calendars on Radicale",
                details={"exception": type(exc).__name__},
            ) from exc

    def calendars(self) -> list[dict[str, str]]:
        result = []
        for calendar in self._calendars():
            calendar_id = self._calendar_id(calendar)
            try:
                name = calendar.get_display_name() or calendar_id.rsplit("/", 1)[-1]
            except Exception:
                name = calendar_id.rsplit("/", 1)[-1]
            result.append({"id": calendar_id, "name": name, "url": str(calendar.url)})
        return sorted(result, key=lambda item: (item["name"].casefold(), item["id"]))

    def _resolve_calendar(self, reference: str) -> tuple[DavCalendar, str]:
        matches: list[tuple[DavCalendar, str]] = []
        for calendar in self._calendars():
            calendar_id = self._calendar_id(calendar)
            try:
                name = calendar.get_display_name() or ""
            except Exception:
                name = ""
            if reference in {calendar_id, str(calendar.url), name}:
                matches.append((calendar, calendar_id))
        if not matches:
            raise CalendarError(
                "CALENDAR_NOT_FOUND",
                "calendar reference did not match a discovered calendar",
                details={"calendar": reference},
            )
        if len(matches) > 1:
            raise CalendarError(
                "CALENDAR_AMBIGUOUS",
                "calendar reference matches more than one calendar; use a discovered calendar id",
                details={"calendar": reference, "matches": [item[1] for item in matches]},
            )
        return matches[0]

    @staticmethod
    def _etag(resource: DavEvent) -> str:
        resource.load()
        etag = resource.props.get(dav.GetEtag.tag)
        if not etag:
            etag = resource.get_property(dav.GetEtag())
        if not etag:
            raise CalendarError("ETAG_MISSING", "server did not provide an ETag for the event")
        return str(etag)

    @staticmethod
    def _resource_json(resource: DavEvent, calendar_id: str) -> dict[str, object]:
        etag = CalendarService._etag(resource)
        calendar = resource.icalendar_instance
        return component_to_json(
            primary_event(calendar),
            etag=etag,
            calendar_id=calendar_id,
            has_exceptions=has_recurrence_exceptions(calendar),
        )

    def list_events(self, request: RangeInput) -> list[dict[str, object]]:
        calendar, calendar_id = self._resolve_calendar(request.calendar)
        start = parse_local_datetime(request.start, request.timezone)
        end = parse_local_datetime(request.end, request.timezone)
        if end <= start:
            raise CalendarError("RANGE_INVALID", "range end must be after range start")
        try:
            resources = calendar.search(
                start=start,
                end=end,
                event=True,
                expand=False,
                split_expanded=False,
            )
            events = [self._resource_json(resource, calendar_id) for resource in resources]
        except CalendarError:
            raise
        except Exception as exc:
            raise CalendarError(
                "CALDAV_LIST_FAILED",
                "Radicale failed to list events in the requested range",
                details={"exception": type(exc).__name__},
            ) from exc
        return sorted(events, key=lambda event: (str(event["start"]), str(event["uid"])))

    def create_event(self, request: CreateInput) -> dict[str, object]:
        calendar, calendar_id = self._resolve_calendar(request.calendar)
        event_data = request.event.model_copy(
            update={"uid": request.event.uid or f"{uuid4()}@radicale-calendar"}
        )
        payload = build_calendar(event_data).to_ical()
        try:
            resource = calendar.save_event(ical=payload, no_overwrite=True)
            return self._resource_json(resource, calendar_id)
        except caldav_error.ConsistencyError as exc:
            raise CalendarError(
                "UID_CONFLICT",
                "an event with this UID already exists",
                details={"uid": event_data.uid},
            ) from exc
        except CalendarError:
            raise
        except Exception as exc:
            raise CalendarError(
                "CALDAV_CREATE_FAILED",
                "Radicale failed to create the event",
                details={"exception": type(exc).__name__},
            ) from exc

    @staticmethod
    def _check_scope(scope: str) -> None:
        if scope != "series":
            raise CalendarError(
                "UNSUPPORTED_RECURRENCE_MUTATION",
                "single-occurrence and future-occurrence mutations are unsupported; use series",
                details={"requested_scope": scope, "supported_scope": "series"},
            )

    @staticmethod
    def _find_event(calendar: DavCalendar, uid: str) -> DavEvent:
        try:
            resource = calendar.event_by_uid(uid)
            resource.load()
            return resource
        except caldav_error.NotFoundError as exc:
            raise CalendarError(
                "EVENT_NOT_FOUND", "event UID was not found", details={"uid": uid}
            ) from exc

    @staticmethod
    def _event_input(component: Event) -> EventInput:
        data = component_to_json(component, etag="unused", calendar_id="unused")
        timezone_name = data["timezone"] or component.get("X-RADICALE-CALENDAR-TIMEZONE")
        if not timezone_name:
            timezone_name = "UTC"
        return EventInput.model_validate(
            {
                "uid": data["uid"],
                "title": data["title"],
                "start": data["start"],
                "end": data["end"],
                "timezone": str(timezone_name),
                "all_day": data["all_day"],
                "description": data["description"],
                "location": data["location"],
                "recurrence": data["recurrence"],
            }
        )

    @staticmethod
    def _apply_managed_properties(target: Event, source: Event) -> None:
        for name in MANAGED_PROPERTIES:
            target.pop(name, None)
            if name in source:
                target[name] = source[name]
        target["DTSTAMP"] = source["DTSTAMP"]
        target.pop("LAST-MODIFIED", None)
        target.add("LAST-MODIFIED", datetime.now(UTC))
        sequence = target.get("SEQUENCE")
        target.pop("SEQUENCE", None)
        target.add("SEQUENCE", int(sequence) + 1 if sequence is not None else 1)

    def update_event(self, request: UpdateInput) -> dict[str, object]:
        self._check_scope(request.recurrence_scope)
        calendar, calendar_id = self._resolve_calendar(request.calendar)
        resource = self._find_event(calendar, request.uid)
        current_etag = self._etag(resource)
        if current_etag != request.etag:
            raise ConflictError(
                "event changed since it was read",
                details={"expected": request.etag, "actual": current_etag},
            )
        existing_calendar: Calendar = resource.icalendar_instance
        existing_component = master_event(existing_calendar)
        ensure_supported_recurrence(existing_component)
        current = self._event_input(existing_component)
        patch = request.event.model_dump(exclude_unset=True)
        merged = current.model_copy(update=patch)
        validated = EventInput.model_validate(merged.model_dump())
        replacement = master_event(build_calendar(validated))
        self._apply_managed_properties(existing_component, replacement)
        response = self.client.put(
            str(resource.url),
            existing_calendar.to_ical(),
            {"Content-Type": 'text/calendar; charset="utf-8"', "If-Match": current_etag},
        )
        if response.status == 412:
            raise ConflictError("event changed concurrently while it was being updated")
        if response.status not in {201, 204}:
            raise CalendarError(
                "CALDAV_UPDATE_FAILED",
                "Radicale rejected the event update",
                details={"status": response.status},
            )
        resource.load()
        return self._resource_json(resource, calendar_id)

    def delete_event(self, request: DeleteInput) -> dict[str, str | bool]:
        self._check_scope(request.recurrence_scope)
        if not request.confirm:
            raise CalendarError(
                "CONFIRMATION_REQUIRED",
                "deletion requires confirm=true after explicit user confirmation",
            )
        calendar, calendar_id = self._resolve_calendar(request.calendar)
        resource = self._find_event(calendar, request.uid)
        primary_event(resource.icalendar_instance)
        current_etag = self._etag(resource)
        if current_etag != request.etag:
            raise ConflictError(
                "event changed since it was read",
                details={"expected": request.etag, "actual": current_etag},
            )
        response = self.client.request(
            str(resource.url), "DELETE", headers={"If-Match": current_etag}
        )
        if response.status == 412:
            raise ConflictError("event changed concurrently while it was being deleted")
        if response.status not in {200, 204}:
            raise CalendarError(
                "CALDAV_DELETE_FAILED",
                "Radicale rejected the event deletion",
                details={"status": response.status},
            )
        return {"calendar": calendar_id, "uid": request.uid, "deleted": True}
