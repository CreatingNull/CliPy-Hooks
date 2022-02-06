"""Test cases for checking the cli module functionality."""
import pytest

from pre_commit_pycli.cli import Command
from pre_commit_pycli.cli import StaticAnalyzerCmd


def test_check_installed(static_analyser: StaticAnalyzerCmd):
    """Checks the test command is 'installed'."""
    assert static_analyser.check_installed() is None


def test_check_installed_fails():
    """Check a not found command fails."""
    with pytest.raises(SystemExit):
        StaticAnalyzerCmd("pre-commit-pycli-testing", []).check_installed()


def test_command_files(command: Command):
    """Ensure a file argument is loaded into the list correctly."""
    assert len(command.files) == 1


def test_command_install_path(command: Command):
    """Ensure absolute install path is resolved."""
    assert len(command.install_path) > 0


def test_command_args(command: Command):
    """Check the files are seperated correctly from args."""
    assert len(command.args) == 0


def test_command_version_match(command: Command):
    """Check hook version check works correctly."""
    command.args.extend(["--version", "1.0.0"])
    assert command.parse_args() is None


def test_command_version_mismatch(command: Command):
    """Check a mismatched tool version errors correctly."""
    command.args.extend(["--version", "1.0.1"])
    with pytest.raises(SystemExit):
        command.parse_args()


def test_run_static_analyser_zero(static_analyser: StaticAnalyzerCmd):
    """Check to make sure no error is thrown on run."""
    assert static_analyser.run_command()


def test_run_static_analyser_non_zero(static_analyser: StaticAnalyzerCmd):
    """Check to make sure no error is thrown on run."""
    static_analyser.args.append("--fail")
    with pytest.raises(SystemExit):
        assert not static_analyser.run_command()
