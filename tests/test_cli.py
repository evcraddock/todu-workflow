from __future__ import annotations

import json
from pathlib import Path

import pytest

from radicale_calendar import cli
from radicale_calendar.credentials import CredentialStore, Settings


def test_cli_returns_stable_json_validation_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.stdin.read", lambda: '{"calendar":"x"}')
    result = cli.main(["list"])
    output = json.loads(capsys.readouterr().out)
    assert result == 1
    assert output["ok"] is False
    assert output["schema_version"] == "1"
    assert output["error"]["code"] == "JSON_VALIDATION_FAILED"
    assert {item["path"] for item in output["error"]["details"]["errors"]} == {
        "start",
        "end",
        "timezone",
    }


def test_cli_returns_json_for_invalid_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    result = cli.main(["unknown"])
    output = json.loads(capsys.readouterr().out)
    assert result == 1
    assert output["error"]["code"] == "ARGUMENT_INVALID"


def test_credential_store_keeps_password_out_of_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    recorded: dict[str, str] = {}
    monkeypatch.setattr(
        "radicale_calendar.credentials.keyring.set_password",
        lambda service, username, password: recorded.update(
            service=service, username=username, password=password
        ),
    )
    monkeypatch.setattr(
        "radicale_calendar.credentials.keyring.get_password",
        lambda service, username: recorded["password"],
    )
    path = tmp_path / "config.json"
    store = CredentialStore(path)
    settings = Settings("https://calendar.example.test", "alice")
    store.save(settings, "top-secret")

    assert "top-secret" not in path.read_text(encoding="utf-8")
    assert path.stat().st_mode & 0o777 == 0o600
    assert store.load() == (settings, "top-secret")


def test_unexpected_errors_do_not_expose_exception_message(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.stdin.read", lambda: "{}")
    monkeypatch.setattr(
        cli,
        "execute",
        lambda *args: (_ for _ in ()).throw(RuntimeError("secret leaked here")),
    )
    result = cli.main(["calendars"])
    output = capsys.readouterr().out
    assert result == 2
    assert "secret leaked here" not in output
    assert json.loads(output)["error"]["code"] == "INTERNAL_ERROR"
