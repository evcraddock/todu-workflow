# Radicale Calendar CLI

`radicale-calendar` is a narrow CalDAV client for calendar discovery and safe event management. It uses the maintained `caldav` and `icalendar` Python libraries, accepts command input as JSON, emits one stable JSON envelope, addresses events by calendar ID and UID, and protects mutations with ETags.

## Install

Python 3.11 or newer is required. From this repository, install the CLI with:

```bash
uv tool install .
```

For development:

```bash
uv sync --extra test
uv run radicale-calendar --help
```

The repository's `skills/` directory must be linked or configured as a pi skill source. The standard repository installation described in the top-level README makes `skills/radicale-calendar/SKILL.md` globally discoverable. Restart pi after installing or updating skills.

## Secure configuration

The non-secret server URL, username, TLS policy, and local-test HTTP policy are stored in `~/.config/radicale-calendar/config.json` with mode `0600`. The password is entered through a terminal prompt and stored by Python `keyring`; it is never accepted as a command argument, included in the JSON input, written to the config file, or returned in output.

On macOS, `keyring` uses Keychain. On Linux, configure a supported Secret Service or another secure keyring backend. The CLI fails closed with `CREDENTIAL_STORE_UNAVAILABLE` when no secure backend is available; it never falls back to plaintext.

Configure an HTTPS server:

```bash
printf '%s' '{"url":"https://calendar.example.com/","username":"alice"}' | radicale-calendar configure
```

The password prompt reads from the controlling terminal. For a local test-only Radicale server using plain HTTP, set `"allow_insecure_http":true`. Do not enable that setting for remote servers. Set `"verify_ssl":false` only when connecting to a trusted development server with a self-signed certificate.

Set `RADICALE_CALENDAR_CONFIG` to override the non-secret config path. There is intentionally no password environment variable.

## Connectivity requirements

The configured URL must be the Radicale server root or another URL from which CalDAV principal discovery works. The account must be able to discover its principal, enumerate calendars, query calendar data, and perform PUT and DELETE requests. HTTPS and valid certificate verification are required by default. Firewalls and reverse proxies must allow `PROPFIND`, `REPORT`, `PUT`, and `DELETE`, preserve ETag and If-Match headers, and pass CalDAV XML request and response bodies unchanged.

## Command and envelope format

Invoke one command and provide exactly one JSON object on standard input. `--input PATH` can read a non-secret request from a file. Every response is a single JSON object on standard output.

Success envelope:

```json
{"data":{},"ok":true,"schema_version":"1"}
```

Error envelope:

```json
{"error":{"code":"ERROR_CODE","details":{},"message":"Human-readable summary"},"ok":false,"schema_version":"1"}
```

Expected command or validation failures exit with status `1`, ETag conflicts with status `3`, and unexpected internal failures with status `2`. Unexpected exception messages are not emitted.

## Calendar discovery

```bash
printf '{}' | radicale-calendar calendars
```

Discovery returns each calendar's exact `id`, display `name`, and `url`. Use the exact ID for subsequent operations. A unique exact display name is accepted, but ambiguous names fail with `CALENDAR_AMBIGUOUS`.

## Date-range listing

```bash
printf '%s' '{"calendar":"/alice/work","start":"2026-04-01T00:00:00","end":"2026-05-01T00:00:00","timezone":"America/Chicago"}' | radicale-calendar list
```

Ranges are half-open: `start` is inclusive and `end` is exclusive. The timezone must be an IANA name. Local times that do not exist during a daylight-saving transition are rejected. Ambiguous repeated local times require an explicit UTC offset, such as `2026-11-01T01:30:00-06:00`.

## Create events

Timed event:

```bash
printf '%s' '{"calendar":"/alice/work","event":{"title":"Planning","start":"2026-04-07T09:00:00","end":"2026-04-07T10:00:00","timezone":"America/Chicago"}}' | radicale-calendar create
```

All-day event dates use an exclusive end date:

```bash
printf '%s' '{"calendar":"/alice/personal","event":{"title":"Vacation","start":"2026-06-12","end":"2026-06-15","timezone":"America/Chicago","all_day":true}}' | radicale-calendar create
```

The optional `uid` must be unique within the calendar. If omitted, the CLI generates one. Optional event properties are `description`, `location`, and `recurrence`.

## Update events

Updates require the exact calendar ID, UID, and ETag returned by list or create. The `event` object is a patch. A conditional PUT with `If-Match` protects against modifications made after the event was read.

```bash
printf '%s' '{"calendar":"/alice/work","uid":"c5ca@example","etag":"\"abc123\"","event":{"title":"Updated planning"},"recurrence_scope":"series"}' | radicale-calendar update
```

If the ETag is stale, the command returns `ETAG_CONFLICT` and does not overwrite the current event. Fetch the event again, review the new state, and only then retry with the new ETag.

## Delete events

Deletion requires the exact calendar ID, UID, current ETag, and `"confirm":true`. Callers and skills must obtain explicit human confirmation before setting that value.

```bash
printf '%s' '{"calendar":"/alice/work","uid":"c5ca@example","etag":"\"abc123\"","confirm":true,"recurrence_scope":"series"}' | radicale-calendar delete
```

Without confirmation, deletion fails with `CONFIRMATION_REQUIRED`. Delete also uses `If-Match`, so a stale ETag fails safely.

## Recurrence support

Basic daily, weekly, monthly, and yearly recurrence is supported. `interval` defaults to `1`; `count` and `until` are mutually exclusive; `by_weekday` is supported for weekly rules.

```json
{"frequency":"weekly","interval":1,"count":8,"by_weekday":["MO","WE"]}
```

Create includes recurrence under `event.recurrence`. Update can replace the recurrence or set it to `null` to remove recurrence. Mutations apply only to the complete series and must use `"recurrence_scope":"series"`. `occurrence`, `future`, recurrence IDs, and calendars containing exception VEVENT components are rejected with `UNSUPPORTED_RECURRENCE_MUTATION` before a mutation is sent.

## Schema summary

All command models reject unknown fields. Timed events require ISO 8601 date-times, an explicit IANA timezone, and an end after the start. All-day events require ISO dates and an exclusive end after the start. See `skills/radicale-calendar/references/schemas.md` for complete request examples and safe agent behavior.

## Development and tests

Run the complete local gate:

```bash
./scripts/pre-pr.sh
```

The test suite starts an isolated Radicale process on a loopback port with temporary storage. It covers discovery, range listing, timed and all-day CRUD, ETag conflicts, recurrence series safety, JSON validation, credential output safety, and daylight-saving edge cases. The test server deliberately uses Radicale's unauthenticated mode and plain loopback HTTP; those settings are for tests only.
