from __future__ import annotations

from typing import Any


class CalendarError(Exception):
    """An expected error with a stable machine-readable code."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}
        self.exit_code = exit_code


class ConflictError(CalendarError):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__("ETAG_CONFLICT", message, details=details, exit_code=3)
