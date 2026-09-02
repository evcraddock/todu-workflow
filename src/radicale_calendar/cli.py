from __future__ import annotations

import argparse
import getpass
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .credentials import CredentialStore, Settings
from .errors import CalendarError
from .models import (
    ConfigureInput,
    CreateInput,
    DeleteInput,
    EmptyInput,
    RangeInput,
    UpdateInput,
)
from .service import CalendarService

SCHEMA_VERSION = "1"
COMMAND_MODELS = {
    "configure": ConfigureInput,
    "calendars": EmptyInput,
    "list": RangeInput,
    "create": CreateInput,
    "update": UpdateInput,
    "delete": DeleteInput,
}


def success(data: Any) -> dict[str, Any]:
    return {"ok": True, "schema_version": SCHEMA_VERSION, "data": data}


def failure(error: CalendarError) -> dict[str, Any]:
    return {
        "ok": False,
        "schema_version": SCHEMA_VERSION,
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details,
        },
    }


def read_json(path: str) -> dict[str, Any]:
    try:
        text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
        value = json.loads(text or "{}")
    except (OSError, json.JSONDecodeError) as exc:
        raise CalendarError("JSON_INVALID", "input must be valid JSON") from exc
    if not isinstance(value, dict):
        raise CalendarError("JSON_INVALID", "input JSON must be an object")
    return value


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CalendarError("ARGUMENT_INVALID", message)


def parser() -> argparse.ArgumentParser:
    result = JsonArgumentParser(
        prog="radicale-calendar",
        description="Manage Radicale calendar events using structured JSON.",
    )
    result.add_argument("command", choices=COMMAND_MODELS)
    result.add_argument(
        "--input",
        default="-",
        metavar="PATH",
        help="read JSON input from PATH instead of stdin",
    )
    return result


def execute(command: str, payload: dict[str, Any], store: CredentialStore) -> Any:
    try:
        request = COMMAND_MODELS[command].model_validate(payload)
    except ValidationError as exc:
        errors = [
            {
                "path": ".".join(str(part) for part in item["loc"]),
                "message": item["msg"],
                "type": item["type"],
            }
            for item in exc.errors()
        ]
        raise CalendarError(
            "JSON_VALIDATION_FAILED",
            "input does not match the command schema",
            details={"errors": errors},
        ) from exc

    if command == "configure":
        assert isinstance(request, ConfigureInput)
        password = getpass.getpass("Radicale password (stored in OS credential store): ")
        settings = Settings(**request.model_dump())
        store.save(settings, password)
        return {"configured": True, "url": settings.url, "username": settings.username}

    settings, password = store.load()
    service = CalendarService(settings, password)
    if command == "calendars":
        return {"calendars": service.calendars()}
    if command == "list":
        assert isinstance(request, RangeInput)
        return {"events": service.list_events(request)}
    if command == "create":
        assert isinstance(request, CreateInput)
        return {"event": service.create_event(request)}
    if command == "update":
        assert isinstance(request, UpdateInput)
        return {"event": service.update_event(request)}
    if command == "delete":
        assert isinstance(request, DeleteInput)
        return service.delete_event(request)
    raise CalendarError("COMMAND_INVALID", "unsupported command")


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        result = success(execute(args.command, read_json(args.input), CredentialStore()))
        exit_code = 0
    except CalendarError as exc:
        result = failure(exc)
        exit_code = exc.exit_code
    except Exception as exc:  # pragma: no cover - final secret-safe boundary
        result = failure(
            CalendarError(
                "INTERNAL_ERROR",
                "an unexpected internal error occurred",
                details={"exception": type(exc).__name__},
                exit_code=2,
            )
        )
        exit_code = 2
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
