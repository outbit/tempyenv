import subprocess
import sys

import pytest

from tempyenv.cli import TemporaryVenvCreator


def test_basic_init():
    cli = TemporaryVenvCreator()
    assert cli.temp_dir is None
    assert cli.venv_path is None


def test_create_temporary_directory():
    cli = TemporaryVenvCreator()
    cli.create_temporary_directory()
    assert cli.temp_dir is not None
    assert cli.venv_path is not None


def test_python_exec():
    cli = TemporaryVenvCreator(python_exec="python_test")
    assert cli.python_exec == "python_test"


def test_python_exec_defaults_to_sys_executable():
    cli = TemporaryVenvCreator()
    assert cli.python_exec == sys.executable


def test_uv_exec_set_when_uv_available(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.shutil.which",
        lambda name: calls.append(name) or "/usr/local/bin/uv",
    )
    cli = TemporaryVenvCreator()
    assert calls == ["uv"]
    assert cli.uv_exec == "/usr/local/bin/uv"


def test_uv_exec_none_when_uv_unavailable(monkeypatch):
    monkeypatch.setattr("tempyenv.cli.shutil.which", lambda _name: None)
    cli = TemporaryVenvCreator()
    assert cli.uv_exec is None


def test_uses_uv_venv_when_available(monkeypatch):
    monkeypatch.setattr("tempyenv.cli.shutil.which", lambda _name: "/usr/local/bin/uv")
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator(python_exec="python3.10")
    cli.venv_path = "/tmp/fake/venv"
    cli.create_virtual_environment()
    assert calls == [
        (
            ["/usr/local/bin/uv", "venv", "--seed", "--python", "python3.10", "/tmp/fake/venv"],
            {"check": True},
        )
    ]


def test_falls_back_to_stdlib_venv_when_uv_unavailable(monkeypatch):
    monkeypatch.setattr("tempyenv.cli.shutil.which", lambda _name: None)
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator(python_exec="python3.10")
    cli.venv_path = "/tmp/fake/venv"
    cli.create_virtual_environment()
    assert calls == [(["python3.10", "-m", "venv", "/tmp/fake/venv"], {"check": True})]


def test_load_virtual_environment_sets_ps1_when_not_already_set(monkeypatch):
    monkeypatch.delenv("PS1", raising=False)
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator()
    cli.venv_path = "/tmp/fake/venv"
    cli.load_virtual_environment()
    cmd = calls[0][0]
    assert 'export PS1="(tempyenv)$PS1\\$ "' in cmd[2]


def test_load_virtual_environment_skips_ps1_when_already_set(monkeypatch):
    monkeypatch.setenv("PS1", "(tempyenv)$ ")
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator()
    cli.venv_path = "/tmp/fake/venv"
    cli.load_virtual_environment()
    cmd = calls[0][0]
    assert 'export PS1=' not in cmd[2]


def test_load_virtual_environment_honors_virtual_env_disable_prompt(monkeypatch):
    monkeypatch.delenv("PS1", raising=False)
    monkeypatch.setenv("VIRTUAL_ENV_DISABLE_PROMPT", "1")
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator()
    cli.venv_path = "/tmp/fake/venv"
    cli.load_virtual_environment()
    cmd = calls[0][0]
    assert 'export PS1=' not in cmd[2]


def test_load_virtual_environment_uses_user_shell_when_supported(monkeypatch):
    monkeypatch.setenv("SHELL", "/usr/bin/zsh")
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator()
    cli.venv_path = "/tmp/fake/venv"
    cli.load_virtual_environment()
    cmd = calls[0][0]
    assert cmd[0] == "zsh"


def test_load_virtual_environment_raises_when_shell_unsupported_and_bash_missing(monkeypatch):
    monkeypatch.setenv("SHELL", "/usr/bin/fish")
    monkeypatch.setattr("tempyenv.cli.shutil.which", lambda _name: None)
    calls = []
    monkeypatch.setattr(
        "tempyenv.cli.subprocess.run",
        lambda _cmd, **_kwargs: calls.append((_cmd, _kwargs)),
    )
    cli = TemporaryVenvCreator()
    cli.venv_path = "/tmp/fake/venv"
    with pytest.raises(RuntimeError, match="bash-compatible shells"):
        cli.load_virtual_environment()
    assert calls == []


def test_logs_error_when_uv_venv_fails(monkeypatch, caplog):
    monkeypatch.setattr("tempyenv.cli.shutil.which", lambda _name: "/usr/local/bin/uv")

    def raise_error(_cmd, **_kwargs):
        raise subprocess.CalledProcessError(1, "uv")

    monkeypatch.setattr("tempyenv.cli.subprocess.run", raise_error)
    cli = TemporaryVenvCreator()
    cli.venv_path = "/tmp/fake/venv"
    with caplog.at_level("ERROR", logger="tempyenv.cli"):
        cli.create_virtual_environment()
    assert "Error creating virtual environment" in caplog.text
