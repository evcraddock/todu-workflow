from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import keyring
from keyring.errors import KeyringError, NoKeyringError

from .errors import CalendarError

SERVICE_NAME = "radicale-calendar-cli"


@dataclass(frozen=True)
class Settings:
    url: str
    username: str
    verify_ssl: bool = True
    allow_insecure_http: bool = False


class CredentialStore:
    """Keep non-secret settings on disk and passwords in the OS credential store."""

    def __init__(self, config_path: Path | None = None) -> None:
        configured = os.environ.get("RADICALE_CALENDAR_CONFIG")
        self.config_path = config_path or (
            Path(configured).expanduser()
            if configured
            else Path.home() / ".config" / "radicale-calendar" / "config.json"
        )

    def save(self, settings: Settings, password: str) -> None:
        if not password:
            raise CalendarError("CONFIG_INVALID", "password must not be empty")
        try:
            keyring.set_password(SERVICE_NAME, settings.username, password)
        except (KeyringError, NoKeyringError) as exc:
            raise CalendarError(
                "CREDENTIAL_STORE_UNAVAILABLE",
                "no secure OS credential store is available",
                details={
                    "hint": "Configure a supported keyring backend; plaintext fallback is disabled."
                },
            ) from exc
        self.config_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        temporary = self.config_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(asdict(settings), indent=2) + "\n", encoding="utf-8")
        temporary.chmod(0o600)
        temporary.replace(self.config_path)
        self.config_path.chmod(0o600)

    def load(self) -> tuple[Settings, str]:
        try:
            raw = json.loads(self.config_path.read_text(encoding="utf-8"))
            settings = Settings(
                url=raw["url"],
                username=raw["username"],
                verify_ssl=raw.get("verify_ssl", True),
                allow_insecure_http=raw.get("allow_insecure_http", False),
            )
        except FileNotFoundError as exc:
            raise CalendarError(
                "NOT_CONFIGURED",
                "Radicale is not configured; run the configure command first",
            ) from exc
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise CalendarError("CONFIG_INVALID", "configuration file is invalid") from exc

        try:
            password = keyring.get_password(SERVICE_NAME, settings.username)
        except (KeyringError, NoKeyringError) as exc:
            raise CalendarError(
                "CREDENTIAL_STORE_UNAVAILABLE",
                "secure OS credential store could not be read",
            ) from exc
        if password is None:
            raise CalendarError("CREDENTIAL_NOT_FOUND", "password is missing from credential store")
        return settings, password
