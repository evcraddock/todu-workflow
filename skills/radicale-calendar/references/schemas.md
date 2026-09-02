# Radicale Calendar Request Schemas

Every request is one JSON object. Unknown fields are rejected. Send requests on standard input or from a non-secret file with `--input PATH`.

## Configure

```json
{
  "url": "https://calendar.example.com/",
  "username": "alice",
  "verify_ssl": true,
  "allow_insecure_http": false
}
```

The password is entered only through the controlling-terminal prompt and stored in the OS credential store. Never add a password field.

## Calendars

```json
{}
```

## List

```json
{
  "calendar": "/alice/work",
  "start": "2026-04-01T00:00:00",
  "end": "2026-05-01T00:00:00",
  "timezone": "America/Chicago"
}
```

Use half-open ranges. Ambiguous daylight-saving times require an explicit offset. The IANA timezone remains required when an offset is included.

## Create a timed event

```json
{
  "calendar": "/alice/work",
  "event": {
    "title": "Planning",
    "start": "2026-04-07T09:00:00",
    "end": "2026-04-07T10:00:00",
    "timezone": "America/Chicago",
    "all_day": false,
    "description": "Quarterly planning",
    "location": "Room 2"
  }
}
```

`uid` is optional on create. Never invent an event end or duration when the user's intent is ambiguous.

## Create an all-day event

```json
{
  "calendar": "/alice/personal",
  "event": {
    "title": "Vacation",
    "start": "2026-06-12",
    "end": "2026-06-15",
    "timezone": "America/Chicago",
    "all_day": true
  }
}
```

The end date is exclusive, so this example covers June 12 through June 14.

## Basic recurrence

Add this object as `event.recurrence`:

```json
{
  "frequency": "weekly",
  "interval": 1,
  "count": 8,
  "by_weekday": ["MO", "WE"]
}
```

Allowed frequencies are `daily`, `weekly`, `monthly`, and `yearly`. `count` and `until` are mutually exclusive. `by_weekday` is allowed only for weekly recurrence. Allowed weekday values are `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, and `SU`. Existing series with other RRULE keys, recurrence dates, exclusion dates, or recurrence exceptions cannot be updated through this CLI and fail without modification.

## Update

```json
{
  "calendar": "/alice/work",
  "uid": "c5ca@example",
  "etag": "\"abc123\"",
  "event": {
    "title": "Updated planning"
  },
  "recurrence_scope": "series"
}
```

The `event` patch accepts `title`, `start`, `end`, `timezone`, `all_day`, `description`, `location`, and `recurrence`. Setting `description`, `location`, or `recurrence` to `null` removes it. Always use a fresh ETag. The only supported recurrence scope is `series`.

## Delete

```json
{
  "calendar": "/alice/work",
  "uid": "c5ca@example",
  "etag": "\"abc123\"",
  "confirm": true,
  "recurrence_scope": "series"
}
```

Do not construct this request with `confirm` set to `true` until the human explicitly confirms deletion of the event shown in normal chat. If the event changes before deletion, stop on `ETAG_CONFLICT` and repeat the selection and confirmation flow with the new state.
