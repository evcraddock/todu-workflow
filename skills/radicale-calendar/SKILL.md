---
name: radicale-calendar
description: Safely list, create, update, or delete events on a configured Radicale CalDAV account through the structured radicale-calendar CLI. Use for calendar requests, scheduling events, checking availability, changing calendar events, or removing events. Require clarification for ambiguous calendar details and explicit confirmation before deletion.
compatibility: Requires the radicale-calendar CLI, a configured Radicale account, and an OS credential store.
---

# Radicale Calendar

Use the `radicale-calendar` command with JSON on standard input. Never put credentials in commands, JSON, notes, logs, or responses. Read [request schemas](references/schemas.md) when constructing an operation.

## Safety gates

1. Clarify ambiguous dates, local times, timezones, durations or end times, recurrence, and target calendars before running a mutation.
2. Require an explicit IANA timezone for every request. Do not infer a timezone from the machine or account.
3. Run `calendars` when the user did not provide an exact discovered calendar ID. Ask the user to choose when more than one calendar could apply.
4. Address updates and deletes only by exact calendar ID plus UID. Never select a mutation target by title alone.
5. List the relevant date range to obtain the current UID and ETag before updating or deleting. If title or other details match multiple events, ask the user which UID is intended.
6. Treat `ETAG_CONFLICT` as a hard stop. Re-list, explain that the event changed, and ask the user to review the current event before retrying.
7. Support recurring mutations only with `recurrence_scope` set to `series`. Never translate a request for one occurrence, this-and-future occurrences, or an existing recurrence outside the documented basic subset into a whole-series mutation; report that the operation is unsupported.
8. Before deletion, show the selected calendar, title, start/end, UID, and recurrence status in normal chat and ask for explicit confirmation. Only after confirmation may the delete JSON include `"confirm":true`.

## Operations

Discover calendars:

```bash
printf '%s' '{}' | radicale-calendar calendars
```

List a half-open date range:

```bash
printf '%s' '<validated-json>' | radicale-calendar list
```

Create after all required details are unambiguous:

```bash
printf '%s' '<validated-json>' | radicale-calendar create
```

Update only with a fresh UID and ETag from list/create output:

```bash
printf '%s' '<validated-json>' | radicale-calendar update
```

Delete only after the explicit confirmation gate:

```bash
printf '%s' '<validated-json-with-confirm-true>' | radicale-calendar delete
```

Prefer a quoted heredoc over shell interpolation when JSON contains user-provided text. Do not enable debug HTTP logging because calendar bodies and authorization metadata may be sensitive.

## Response handling

Parse the JSON envelope. Continue only when `ok` is `true`. On `JSON_VALIDATION_FAILED`, use `error.details.errors` to identify missing or invalid fields and clarify them with the user. On `CALENDAR_AMBIGUOUS`, present the returned calendar IDs. On any authentication, credential-store, TLS, connectivity, unsupported recurrence, confirmation, or ETag error, stop without claiming that a mutation succeeded.

Summarize successful mutations with the exact calendar ID, UID, start/end, timezone, recurrence status, and returned ETag. Do not expose unrelated event details or credential/configuration internals.
