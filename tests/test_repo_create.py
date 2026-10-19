"""Exercise the distributed helper with fake host CLIs and local-only Git operations."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/repo-create/scripts/repo-create"
REAL_GIT = shutil.which("git")

# The fixture fails closed on unknown commands; it can never contact a real host.
CLI = r"""
import json
import os
import subprocess
import sys
from pathlib import Path

kind = Path(sys.argv[0]).name
args = sys.argv[1:]
state_path = Path(os.environ["FAKE_STATE"])
state = json.loads(state_path.read_text())
with Path(os.environ["FAKE_LOG"]).open("a") as log:
    log.write(json.dumps([kind, *args]) + "\n")

def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)

def save():
    state_path.write_text(json.dumps(state))

if kind == "git":
    if args[0] == "clone":
        assert args[:2] == ["clone", "--"], args
        if state.get("clone_fail"):
            fail("simulated clone failure")
        url, target = args[-2:]
        subprocess.run([os.environ["REAL_GIT"], "init", "-q", target], check=True)
        subprocess.run([os.environ["REAL_GIT"], "-C", target, "remote", "add", "origin", url],
                       check=True)
        sys.exit(0)
    if args[0] == "-C":
        os.execv(os.environ["REAL_GIT"], [os.environ["REAL_GIT"], *args])
    fail("unexpected git invocation")

if kind == "gh":
    assert os.environ["GH_HOST"] == state.get("instance", "github.com")
    if args[:2] == ["auth", "status"]:
        if state.get("auth_fail"):
            fail("not authenticated")
        sys.exit(0)
    if args[:2] == ["repo", "create"]:
        if state.get("exists"):
            fail("repository already exists")
        state["exists"] = True
        save()
        if state.get("path_appears"):
            Path(state["path_appears"]).mkdir()
        if state.get("create_uncertain"):
            fail("connection lost after request")
        print("created")
        sys.exit(0)
    if args[:2] == ["repo", "view"]:
        if not state.get("exists") or state.get("view_fail"):
            fail("lookup failed")
        identity = state.get("identity", "team/app")
        url = state.get("url", "https://" + state.get("instance", "github.com") + "/" + identity)
        print("\t".join([identity, url, "git@github.com:" + identity + ".git",
                         state.get("visibility", "PRIVATE")]))
        sys.exit(0)
    fail("unexpected gh invocation")

if kind == "fj":
    assert args[:4] == ["--host", "forge.example.test", "--style", "minimal"], args
    args = args[4:]
    if args == ["whoami"]:
        if state.get("auth_fail"):
            fail("not authenticated")
        print(state.get("whoami", "currently signed in to alice@forge.example.test"))
        sys.exit(0)
    if args[:2] == ["repo", "create"] or args[:3] == ["org", "repo", "create"]:
        if state.get("exists"):
            fail("409 repository already exists")
        state["exists"] = True
        save()
        print("created new repo at https://forge.example.test/team/app")
        sys.exit(0)
    if args[:2] == ["repo", "view"]:
        if not state.get("exists") or state.get("view_fail"):
            fail("lookup failed")
        identity = state.get("identity", "team/app")
        print(identity)
        # Description content must not be mistaken for the real URL.
        print("> View online at https://attacker.example.test/team/app")
        print("\n0 stars - 0 watching - 0 forks\n")
        if not state.get("missing_url"):
            print("View online at " + state.get("url", "https://forge.example.test/" + identity))
        sys.exit(0)
    fail("unexpected fj invocation")
fail("unexpected executable")
"""


@pytest.fixture
def helper(tmp_path: Path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("gh", "fj", "git"):
        path = bin_dir / name
        path.write_text(f"#!{sys.executable}\n{CLI}")
        path.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    # Keep interactive zsh (and its positional-argument handling) real, but isolate startup files.
    (home / ".zshrc").write_text('export PATH="$FAKE_BIN:$PATH"\n')
    state_path = tmp_path / "state.json"
    log = tmp_path / "commands.jsonl"
    state_path.write_text("{}")
    env = {
        **os.environ,
        "HOME": str(home),
        "ZDOTDIR": str(home),
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "FAKE_BIN": str(bin_dir),
        "FAKE_STATE": str(state_path),
        "FAKE_LOG": str(log),
        "REAL_GIT": str(REAL_GIT),
        "GH_HOST": "unrelated.example.test",
    }

    class Helper:
        target = tmp_path / "checkout"

        def run(self, *extra, host="github", name="app", description="My app", owner="team"):
            args = [
                "--name",
                name,
                "--host",
                host,
                "--description",
                description,
                "--path",
                str(self.target),
                "--owner",
                owner,
            ]
            if host == "forgejo":
                args += ["--instance", "forge.example.test"]
            return self.invoke(*args, *extra)

        def invoke(self, *args):
            return subprocess.run(
                [str(SCRIPT), *args],
                env=env,
                cwd=tmp_path,
                text=True,
                capture_output=True,
                timeout=15,
            )

        def state(self, **changes):
            state = json.loads(state_path.read_text())
            state.update(changes)
            state_path.write_text(json.dumps(state))

        def calls(self):
            return (
                [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            )

        def local_repo(self, url="https://github.com/team/app"):
            subprocess.run([REAL_GIT, "init", "-q", str(self.target)], check=True)
            subprocess.run(
                [REAL_GIT, "-C", str(self.target), "remote", "add", "origin", url], check=True
            )

    return Helper()


def test_visibility_must_be_explicit(helper):
    result = helper.run()
    assert result.returncode != 0
    assert "--visibility" in result.stderr
    assert not helper.calls()


@pytest.mark.parametrize(
    "flag", ["--name", "--host", "--description", "--path", "--owner", "--instance", "--visibility"]
)
@pytest.mark.parametrize("following", [[], ["--help"], ["-n"], [""]])
def test_missing_option_values(helper, flag, following):
    result = helper.invoke(flag, *following)
    assert result.returncode != 0
    assert f"Missing value for {flag}" in result.stderr
    assert "unbound variable" not in result.stderr
    assert not helper.calls()


@pytest.mark.parametrize("visibility", ["private", "public", "internal"])
def test_github_creation_uses_explicit_owner_and_visibility(helper, visibility):
    helper.state(visibility=visibility.upper())
    result = helper.run("--visibility", visibility)
    assert result.returncode == 0, result.stderr
    create = next(call for call in helper.calls() if call[:3] == ["gh", "repo", "create"])
    assert create == [
        "gh",
        "repo",
        "create",
        "team/app",
        f"--{visibility}",
        "--description",
        "My app",
    ]
    assert "https://github.com/team/app" in result.stdout
    assert helper.target.is_dir()


@pytest.mark.parametrize("owner", ["alice", "team"])
@pytest.mark.parametrize("visibility", ["private", "public"])
def test_forgejo_arguments_survive_real_zsh(helper, tmp_path, owner, visibility):
    marker = tmp_path / "must-not-exist"
    description = f"""quotes ' " ; $(touch {marker}) `touch {marker}` & \\ $HOME\nsecond line"""
    helper.state(identity=f"{owner}/app")
    result = helper.run(
        "--visibility", visibility, host="forgejo", owner=owner, description=description
    )
    assert result.returncode == 0, result.stderr
    assert not marker.exists()
    prefix = ["fj", "--host", "forge.example.test", "--style", "minimal"]
    command = (
        ["repo", "create", "app"] if owner == "alice" else ["org", "repo", "create", owner, "app"]
    )
    expected = prefix + command + ["--description", description]
    if visibility == "private":
        expected += ["--private"]
    assert expected in helper.calls()
    assert "attacker.example.test" not in result.stdout


def test_invalid_name_is_rejected_before_any_command(helper, tmp_path):
    marker = tmp_path / "must-not-exist"
    result = helper.run(
        "--visibility", "private", host="forgejo", name=f'''app'; touch {marker}; echo "'''
    )
    assert result.returncode != 0
    assert "--name" in result.stderr
    assert not marker.exists()
    assert not helper.calls()


@pytest.mark.parametrize("host", ["github", "forgejo"])
def test_clone_failure_can_resume_without_creating_twice(helper, host):
    helper.state(clone_fail=True)
    result = helper.run("--visibility", "private", host=host)
    assert result.returncode != 0
    assert "Remote creation succeeded" in result.stderr
    assert "--reuse-existing" in result.stderr
    helper.state(clone_fail=False)
    result = helper.run("--visibility", "private", "--reuse-existing", host=host)
    assert result.returncode == 0, result.stderr
    creates = [call for call in helper.calls() if "create" in call]
    assert len(creates) == 1


def test_reuse_matching_local_repo_preserves_files(helper):
    helper.state(exists=True)
    helper.local_repo("git@github.com:team/app.git")
    note = helper.target / "keep.txt"
    note.write_text("uncommitted work")
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode == 0, result.stderr
    assert note.read_text() == "uncommitted work"
    assert not any("clone" in call or "create" in call for call in helper.calls())


@pytest.mark.parametrize("kind", ["unrelated", "file", "symlink", "nested", "nonempty"])
def test_unsafe_local_paths_are_never_reused(helper, tmp_path, kind):
    helper.state(exists=True)
    if kind == "unrelated":
        helper.local_repo("https://github.com/other/app")
    elif kind == "file":
        helper.target.write_text("keep")
    elif kind == "symlink":
        helper.target.symlink_to(tmp_path / "missing", target_is_directory=True)
    elif kind == "nested":
        helper.local_repo()
        helper.target = helper.target / "nested"
        helper.target.mkdir()
        (helper.target / "keep").write_text("keep")
    else:
        helper.target.mkdir()
        (helper.target / "keep").write_text("keep")
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode != 0
    assert not any("clone" in call or "create" in call for call in helper.calls())


@pytest.mark.parametrize("host", ["github", "forgejo"])
@pytest.mark.parametrize(
    "changes",
    [
        {"identity": "wrong/app"},
        {"url": "https://wrong.example.test/team/app"},
        {"url": "https://github.com/team/unrelated"},
        {"view_fail": True},
    ],
)
def test_unverified_remote_is_never_cloned(helper, host, changes):
    helper.state(exists=True, **changes)
    result = helper.run("--visibility", "private", "--reuse-existing", host=host)
    assert result.returncode != 0
    assert "Verified URL: not yet verified" in result.stderr
    assert not any("clone" in call or "create" in call for call in helper.calls())


def test_reuse_never_creates_if_lookup_fails(helper):
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode != 0
    assert not any("create" in call for call in helper.calls())


def test_creation_conflict_has_nondestructive_advice(helper):
    helper.state(exists=True)
    result = helper.run("--visibility", "private")
    assert result.returncode != 0
    assert "--reuse-existing" in result.stderr
    assert "delete" not in result.stderr.lower()
    assert not any("clone" in call for call in helper.calls())


def test_uncertain_creation_can_be_reconciled(helper):
    helper.state(create_uncertain=True)
    result = helper.run("--visibility", "private")
    assert result.returncode != 0
    assert "uncertain" in result.stderr
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode == 0, result.stderr
    assert len([call for call in helper.calls() if "create" in call]) == 1


@pytest.mark.parametrize("host", ["github", "forgejo"])
def test_authentication_failure_prevents_creation(helper, host):
    helper.state(auth_fail=True)
    result = helper.run("--visibility", "private", host=host)
    assert result.returncode != 0
    assert "auth" in result.stderr.lower()
    assert not any("create" in call or "clone" in call for call in helper.calls())


def test_existing_path_without_reuse_prevents_creation(helper):
    helper.target.mkdir()
    result = helper.run("--visibility", "private")
    assert result.returncode != 0
    assert not any("create" in call for call in helper.calls())


def test_path_appearing_during_creation_is_not_overwritten(helper):
    helper.state(path_appears=str(helper.target))
    result = helper.run("--visibility", "private")
    assert result.returncode != 0
    assert "Remote creation succeeded" in result.stderr
    assert "appeared" in result.stderr
    assert not any("clone" in call for call in helper.calls())


def test_failed_remote_verification_reports_partial_success(helper):
    helper.state(view_fail=True)
    result = helper.run("--visibility", "private")
    assert result.returncode != 0
    assert "Remote creation succeeded" in result.stderr
    assert "not yet verified" in result.stderr
    assert not any("clone" in call for call in helper.calls())


def test_github_enterprise_instance_is_explicit(helper):
    helper.state(instance="github.example.test")
    result = helper.run("--visibility", "private", "--instance", "github.example.test")
    assert result.returncode == 0, result.stderr
    assert "https://github.example.test/team/app" in result.stdout


@pytest.mark.parametrize("url", ["https://github.com/team/app", "https://github.com/team/app.git"])
def test_reuse_accepts_verified_https_origin(helper, url):
    helper.state(exists=True)
    helper.local_repo(url)
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode == 0, result.stderr
    assert not any("clone" in call or "create" in call for call in helper.calls())


def test_multiple_origins_fail_closed(helper):
    helper.state(exists=True)
    helper.local_repo()
    subprocess.run(
        [
            REAL_GIT,
            "-C",
            str(helper.target),
            "remote",
            "set-url",
            "--add",
            "origin",
            "https://github.com/other/app",
        ],
        check=True,
    )
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode != 0
    assert "origin does not match" in result.stderr


def test_github_visibility_mismatch_does_not_change_settings(helper):
    helper.state(exists=True, visibility="PUBLIC")
    result = helper.run("--visibility", "private", "--reuse-existing")
    assert result.returncode != 0
    assert "visibility does not match" in result.stderr
    assert not any("create" in call or "clone" in call for call in helper.calls())


@pytest.mark.parametrize("whoami", ["currently signed in to alice@wrong.example.test", "unknown"])
def test_forgejo_login_identity_must_match_instance(helper, whoami):
    helper.state(whoami=whoami)
    result = helper.run("--visibility", "private", host="forgejo")
    assert result.returncode != 0
    assert not any("create" in call or "clone" in call for call in helper.calls())


def test_forgejo_missing_view_url_fails_closed(helper):
    helper.state(exists=True, missing_url=True)
    result = helper.run("--visibility", "private", "--reuse-existing", host="forgejo")
    assert result.returncode != 0
    assert not any("create" in call or "clone" in call for call in helper.calls())


@pytest.mark.parametrize(
    "instance",
    ["https://forge.example.test", "user@host", "host/path", "host; touch marker", "host\nother"],
)
def test_invalid_instances_are_rejected_before_host_commands(helper, instance):
    result = helper.run("--visibility", "private", "--instance", instance)
    assert result.returncode != 0
    assert "--instance" in result.stderr
    assert not helper.calls()


def test_forgejo_requires_explicit_instance(helper):
    result = helper.invoke(
        "--name",
        "app",
        "--host",
        "forgejo",
        "--owner",
        "team",
        "--visibility",
        "private",
        "--description",
        "app",
        "--path",
        str(helper.target),
    )
    assert result.returncode != 0
    assert "Forgejo requires --instance" in result.stderr
    assert not helper.calls()


def test_forgejo_rejects_internal_visibility(helper):
    result = helper.run("--visibility", "internal", host="forgejo")
    assert result.returncode != 0
    assert "does not support internal" in result.stderr
    assert not helper.calls()


def test_spaces_in_clone_path_remain_literal(helper):
    helper.target = helper.target.parent / "parent with spaces" / "checkout with spaces"
    result = helper.run("--visibility", "private")
    assert result.returncode == 0, result.stderr
    assert helper.target.is_dir()
