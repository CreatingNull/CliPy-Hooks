"""Test cases for checking the cli module functionality."""

from pathlib import Path

import pytest

from clipy_hooks.cli import Command, StaticAnalyzerCmd

# Protected access is okay for testing.
# pylint: disable=W0212


def test_check_installed(static_analyser: StaticAnalyzerCmd):
    """Checks the test command is 'installed'."""
    assert static_analyser.check_installed() is None


def test_check_installed_fails():
    """Check a not found command fails."""
    with pytest.raises(SystemExit):
        StaticAnalyzerCmd("clipy-hooks-testing", []).check_installed()


def test_command_args(command: Command):
    """Check the files are separated correctly from args."""
    assert len(command.args) == 2


def test_command_files(command: Command):
    """Ensure a file argument is loaded into the list correctly."""
    assert len(command.paths) == 1


def test_command_install_path(command: Command):
    """Ensure absolute install path is resolved."""
    assert command.install_path != Path()
    assert command.install_path.is_dir()


def test_command_version_match(command: Command):
    """Check hook version check works correctly."""
    command.args.extend(["--version", "1.0.0"])
    assert command._parse_args() is None


def test_command_version_mismatch(command: Command):
    """Check a mismatched tool version errors correctly."""
    command.args.extend(["--version", "1.0.1"])
    with pytest.raises(SystemExit):
        command._parse_args()


def test_run_static_analyser_on_path():
    """Just check resolving a random program via path."""
    path_cmd = StaticAnalyzerCmd("whoami", [])
    assert path_cmd.run_command()


def test_run_static_analyser_zero(static_analyser: StaticAnalyzerCmd):
    """Check to make sure no error is thrown on run."""
    assert static_analyser.run_command()


def test_run_static_analyser_non_zero(static_analyser: StaticAnalyzerCmd):
    """Check to make sure no error is thrown on run."""
    static_analyser.args.insert(0, "--fail")
    with pytest.raises(SystemExit):
        assert not static_analyser.run_command()
