"""Local tmux integration checks; no agents, personal sockets, or server-wide cleanup."""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/tmux/scripts"
TMUX = shutil.which("tmux")


@pytest.fixture
def terminal(tmp_path: Path) -> Iterator:
    assert TMUX is not None, "Install tmux to run the tmux helper integration checks"
    # Unix socket paths must remain short, including on macOS.
    with tempfile.TemporaryDirectory(prefix="tw-tmux-", dir="/tmp") as directory:
        root = Path(directory)
        home = root / "home"
        home.mkdir()
        env = {
            **os.environ,
            "HOME": str(home),
            "SHELL": "/bin/sh",
            "TMUX": "",
            "TMUX_PANE": "",
            "TMUX_SKILL_SOCKET_DIR": str(root),
        }

        class Terminal:
            socket = root / "tmux-skill.sock"
            observer_socket = root / "observer.sock"
            owned: set[tuple[Path, str]] = set()

            def command(self, socket, *args, check=True):
                return subprocess.run(
                    [TMUX, "-f", "/dev/null", "-S", str(socket), *args],
                    env=env,
                    text=True,
                    capture_output=True,
                    timeout=5,
                    check=check,
                )

            def sessions(self, socket):
                result = self.command(socket, "list-sessions", "-F", "#{session_id}", check=False)
                return set(result.stdout.splitlines()) if result.returncode == 0 else set()

            def record(self):
                # Only fixture-created sockets are observed. Record exact returned IDs,
                # including leaked resources from the script under test, for teardown.
                for socket in (self.socket, self.observer_socket):
                    self.owned.update((socket, item) for item in self.sessions(socket))

            def run(self, script, *args, extra_env=None):
                try:
                    return subprocess.run(
                        [str(SCRIPTS / script), *map(str, args)],
                        env={**env, **(extra_env or {})},
                        cwd=root,
                        text=True,
                        capture_output=True,
                        timeout=10,
                    )
                finally:
                    self.record()

            def start(self, *extra):
                result = self.run("start-session.sh", "--session", "test", *extra)
                assert result.returncode == 0, result.stderr
                return self.fields(result.stdout)

            def fields(self, output):
                return dict(line.split("=", 1) for line in output.splitlines() if "=" in line)

            def pane(self, socket, session):
                return self.command(
                    socket, "list-panes", "-t", session, "-F", "#{pane_id}"
                ).stdout.strip()

            def close(self, fields):
                if fields.get("OBSERVER_PANE_ID"):
                    kind = fields["OBSERVER_KIND"]
                    self.command(
                        Path(fields["OBSERVER_SOCKET"]),
                        "kill-window" if kind == "window" else "kill-pane",
                        "-t",
                        fields["OBSERVER_WINDOW_ID"]
                        if kind == "window"
                        else fields["OBSERVER_PANE_ID"],
                    )
                self.command(Path(fields["SOCKET"]), "kill-session", "-t", fields["SESSION_ID"])

        value = Terminal()
        for socket in (value.socket, value.observer_socket):
            session = value.command(
                socket, "new-session", "-d", "-s", "unrelated", "-P", "-F", "#{session_id}"
            ).stdout.strip()
            value.owned.add((socket, session))
        value.guard = next(iter(value.sessions(value.socket)))
        value.observer_guard = next(iter(value.sessions(value.observer_socket)))
        value.observer_target = value.pane(value.observer_socket, value.observer_guard)
        value.environment = env
        value.root = root
        try:
            yield value
        finally:
            value.record()
            for socket, session in value.owned:
                value.command(socket, "kill-session", "-t", session, check=False)


def test_creation_returns_exact_owned_ids_and_preserves_unrelated_session(terminal):
    fields = terminal.start()
    assert fields["SESSION_ID"].startswith("$")
    assert fields["PANE_ID"].startswith("%")
    assert fields["WINDOW_ID"].startswith("@")
    assert terminal.sessions(terminal.socket) == {terminal.guard, fields["SESSION_ID"]}
    terminal.close(fields)
    assert terminal.sessions(terminal.socket) == {terminal.guard}


@pytest.mark.parametrize("kind", ["window", "pane"])
def test_observer_ids_allow_exact_cleanup_without_closing_unrelated_panes(terminal, kind):
    fields = terminal.start(
        "--visible",
        "--observer-socket",
        terminal.observer_socket.name if kind == "pane" else terminal.observer_socket,
        "--observer-target",
        terminal.observer_target,
        "--display-mode",
        kind,
    )
    assert fields["OBSERVER_KIND"] == kind
    assert Path(fields["OBSERVER_SOCKET"]).is_absolute()
    assert Path(fields["OBSERVER_SOCKET"]).resolve() == terminal.observer_socket.resolve()
    assert fields["OBSERVER_PANE_ID"] != terminal.observer_target
    terminal.close(fields)
    assert terminal.sessions(terminal.socket) == {terminal.guard}
    assert (
        terminal.pane(terminal.observer_socket, terminal.observer_guard) == terminal.observer_target
    )


def test_observer_failure_cleans_only_created_worker(terminal):
    result = terminal.run(
        "start-session.sh",
        "-s",
        "test",
        "--visible",
        "--observer-socket",
        terminal.observer_socket,
        "--observer-target",
        "%999999",
    )
    assert result.returncode != 0
    assert terminal.sessions(terminal.socket) == {terminal.guard}
    assert (
        terminal.pane(terminal.observer_socket, terminal.observer_guard) == terminal.observer_target
    )


def test_existing_session_names_are_never_reused_or_killed(terminal):
    first = terminal.start()
    second = terminal.start()
    assert first["SESSION_ID"] != second["SESSION_ID"]
    terminal.close(first)
    assert terminal.sessions(terminal.socket) == {terminal.guard, second["SESSION_ID"]}
    terminal.close(second)


@pytest.mark.parametrize(
    "script,option",
    [
        ("start-session.sh", "--session"),
        ("start-session.sh", "--observer-target"),
        ("start-session.sh", "--command"),
        ("wait-for-text.sh", "--pattern"),
        ("wait-for-text.sh", "--timeout"),
        ("find-sessions.sh", "--socket-path"),
        ("find-sessions.sh", "--query"),
    ],
)
@pytest.mark.parametrize("following", [[], ["--help"]])
def test_missing_values_have_contextual_errors(terminal, script, option, following):
    result = terminal.run(script, option, *following)
    assert result.returncode != 0
    assert f"Missing value for {option}" in result.stderr
    assert terminal.sessions(terminal.socket) == {terminal.guard}


def test_visible_mode_requires_explicit_observer_ownership_context(terminal):
    result = terminal.run("start-session.sh", "-s", "test", "--visible")
    assert result.returncode != 0
    assert "--observer-socket" in result.stderr
    assert terminal.sessions(terminal.socket) == {terminal.guard}


def test_wait_reads_exact_pane_on_private_socket(terminal):
    fields = terminal.start()
    terminal.command(
        terminal.socket,
        "send-keys",
        "-t",
        fields["PANE_ID"],
        "printf 'ready-literal.*\\n'",
        "Enter",
    )
    result = terminal.run(
        "wait-for-text.sh",
        "-t",
        fields["PANE_ID"],
        "-p",
        "ready-literal.*",
        "--fixed",
        "-T",
        "3",
        "-i",
        "0.05",
    )
    assert result.returncode == 0, result.stderr
    terminal.close(fields)


def test_wait_timeout_is_bounded_and_does_not_destroy_caller_resources(terminal):
    fields = terminal.start()
    before = time.monotonic()
    result = terminal.run(
        "wait-for-text.sh",
        "-t",
        fields["PANE_ID"],
        "-p",
        "never-printed-token",
        "-T",
        "1",
        "-i",
        "0.05",
    )
    assert result.returncode == 124, result.stderr
    assert time.monotonic() - before < 3
    assert "Timed out" in result.stderr
    assert terminal.sessions(terminal.socket) == {terminal.guard, fields["SESSION_ID"]}
    terminal.close(fields)


@pytest.mark.parametrize(
    "args,message",
    [
        (["-t", "%999999", "-p", "foo"], "Cannot capture pane"),
        (["-t", "unrelated", "-p", "foo"], "pane ID"),
        (["-t", "%0", "-p", "["], "Invalid regex"),
        (["-t", "%0", "-p", "foo", "-T", "900"], "timeout"),
        (["-t", "%0", "-p", "foo", "-i", "-1"], "interval"),
        (["-t", "%0", "-p", "foo", "-i", "600"], "interval"),
    ],
)
def test_wait_failures_are_not_hidden_as_timeouts(terminal, args, message):
    result = terminal.run("wait-for-text.sh", *args)
    assert result.returncode != 0
    assert message in result.stderr
    assert terminal.sessions(terminal.socket) == {terminal.guard}


def test_wait_interruption_leaves_caller_owned_session_intact(terminal):
    fields = terminal.start()
    process = subprocess.Popen(
        [
            str(SCRIPTS / "wait-for-text.sh"),
            "-t",
            fields["PANE_ID"],
            "-p",
            "not-present",
            "-T",
            "10",
            "-i",
            "0.05",
        ],
        env=terminal.environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        # A real signal, not a fabricated completion; wait for the child to be running.
        process.send_signal(signal.SIGTERM)
        process.communicate(timeout=3)
        assert process.returncode != 0
        assert terminal.sessions(terminal.socket) == {terminal.guard, fields["SESSION_ID"]}
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=3)
        terminal.close(fields)


def test_discovery_defaults_to_private_socket_and_query_is_literal(terminal):
    result = terminal.run("find-sessions.sh")
    assert result.returncode == 0, result.stderr
    assert terminal.guard in result.stdout
    result = terminal.run("find-sessions.sh", "--query", "unrelated.*")
    assert result.returncode == 0, result.stderr
    assert "No sessions" in result.stdout
    assert terminal.sessions(terminal.socket) == {terminal.guard}


@pytest.mark.parametrize("failure_mode", ["interruption", "verification-failure"])
def test_start_failure_after_observer_creation_cleans_owned_resources(
    terminal, tmp_path, failure_mode
):
    ready = tmp_path / "ready"
    release = tmp_path / "release"
    shim = tmp_path / "tmux"
    shim.write_text(f"""#!{sys.executable}
import os
import subprocess
import sys
import time
from pathlib import Path
args = sys.argv[1:]
if "display-message" in args and Path(os.environ["TEST_READY"]).exists():
    while not Path(os.environ["TEST_RELEASE"]).exists():
        time.sleep(0.01)
    sys.exit(1)
result = subprocess.run([{TMUX!r}, *args], capture_output=True, text=True)
print(result.stdout, end="", flush=True)
print(result.stderr, end="", file=sys.stderr, flush=True)
if "new-window" in args and result.returncode == 0:
    Path(os.environ["TEST_READY"]).touch()
sys.exit(result.returncode)
""")
    shim.chmod(0o755)
    process = subprocess.Popen(
        [
            str(SCRIPTS / "start-session.sh"),
            "-s",
            "test",
            "--visible",
            "--observer-socket",
            str(terminal.observer_socket),
            "--observer-target",
            terminal.observer_target,
        ],
        env={
            **terminal.environment,
            "PATH": f"{tmp_path}:{os.environ['PATH']}",
            "TEST_READY": str(ready),
            "TEST_RELEASE": str(release),
        },
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.monotonic() + 5
        while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.01)
        assert ready.exists(), process.communicate(timeout=1)
        if failure_mode == "interruption":
            process.send_signal(signal.SIGTERM)
        release.touch()
        process.communicate(timeout=5)
        assert process.returncode != 0
        assert terminal.sessions(terminal.socket) == {terminal.guard}
        assert (
            terminal.pane(terminal.observer_socket, terminal.observer_guard)
            == terminal.observer_target
        )
    finally:
        release.touch()
        if process.poll() is None:
            process.kill()
            process.wait(timeout=3)
        terminal.record()
