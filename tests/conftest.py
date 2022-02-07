"""Pytest configuration to create reusable fixtures."""
import pytest

from pre_commit_pycli.cli import Command
from pre_commit_pycli.cli import StaticAnalyzerCmd


CALL_ARGS = [
    "__main__.py",
    "--a-flag",
    "--an-arg=cli/__main__.py",
    "--install-dir",
    "cli/",
    "cli/__init__.py",
]


@pytest.fixture(scope="function")
def static_analyser() -> StaticAnalyzerCmd:
    """Create a StaticAnalyzerCmd fixture using the mocked CLI."""
    return StaticAnalyzerCmd(
        CALL_ARGS[0],
        CALL_ARGS,
    )


@pytest.fixture(scope="function")
def command() -> Command:
    """Create a generic Command fixture for testing abstract functionality."""
    return Command(
        CALL_ARGS[0],
        CALL_ARGS,
    )
