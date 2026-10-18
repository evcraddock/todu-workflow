from __future__ import annotations

import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import pytest
from caldav import DAVClient

from radicale_calendar.credentials import Settings
from radicale_calendar.service import CalendarService


@pytest.fixture(scope="session")
def radicale_url(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("radicale")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    config = root / "config"
    config.write_text(
        "\n".join(
            [
                "[server]",
                f"hosts = 127.0.0.1:{port}",
                "[auth]",
                "type = none",
                "[storage]",
                f"filesystem_folder = {root / 'collections'}",
                "[logging]",
                "level = warning",
            ]
        ),
        encoding="utf-8",
    )
    process = subprocess.Popen(  # noqa: S603
        [sys.executable, "-m", "radicale", "--config", str(config)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    url = f"http://127.0.0.1:{port}/"
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.05)
        else:
            output = process.stdout.read() if process.stdout else ""
            pytest.fail(f"Radicale did not start: {output}")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture
def calendar_service(radicale_url: str, tmp_path: Path) -> tuple[CalendarService, str]:
    username = f"user-{tmp_path.name}"
    client = DAVClient(
        url=radicale_url,
        username=username,
        password="test-only",
        require_tls=False,
    )
    calendar = client.principal().make_calendar(name="Integration")
    service = CalendarService(
        Settings(
            url=radicale_url,
            username=username,
            verify_ssl=True,
            allow_insecure_http=True,
        ),
        "test-only",
    )
    return service, service._calendar_id(calendar)
