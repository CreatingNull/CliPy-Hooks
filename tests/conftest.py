"""Pytest configuration to create reusable fixtures."""
import pytest

from pre_commit_pycli.cli import Command
from pre_commit_pycli.cli import StaticAnalyzerCmd


@pytest.fixture(scope="session")
def static_analyser() -> StaticAnalyzerCmd:
    """Create a StaticAnalyzerCmd fixture using the mocked CLI."""
    return StaticAnalyzerCmd(
        "__main__.py", ["--install-dir", "cli/", "cli/__init__.py"]
    )


@pytest.fixture(scope="session")
def command() -> Command:
    """Create a generic Command fixture for testing abstract functionality."""
    return Command("__main__.py", ["--install-dir", "cli/", "cli/__init__.py"])
