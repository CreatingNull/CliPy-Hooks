#!/usr/bin/env python
"""Command Class functionality for calling a CLI tool."""
import re
import shutil
import subprocess as sp
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List


class Command:
    """Super class that all commands inherit."""

    def __init__(self, command: str, args: List[str], help_url: str = ""):
        """Constructor for the cli command class.

        :param command: Name of the command, must be on path or define install location.
        :param args: Additional arguments to provide to the CLI tool.
        :param help_url: URL of project documentation to assist when things go wrong.
        """
        self.args = args
        self.command = command
        self.install_path = Path()
        # Most use-cases should be either files or dir not both.
        self.paths = []  # Positional path arguments to provide to CLI tool

        self.stdout = b""
        self.stderr = b""
        self.return_code = 0
        self.help_url = help_url

        self._parse_args()

    def check_installed(self):
        """Check if command is installed and fail exit if not."""
        if self.install_path != Path():  # Resolve absolute executable
            path = Path(self.install_path).joinpath(self.command)
            if not path.exists() or not path.is_file():
                path = None  # Executable not found
        else:  # Resolve command from PATH
            path = shutil.which(self.command)
        if path is None:
            check_path = (
                f"at '{self.install_path}'"
                if self.install_path != Path()
                else "and on your PATH"
            )
            details = f"Make sure {self.command} is installed {check_path}.\n" + (
                f"For more info: {self.help_url}" if self.help_url != "" else ""
            )
            self.raise_error(f"{self.command} not found", details)

    def _parse_args(self):
        """Validates and separates provided arguments.

        Removes arguments consumed by the shim. Separates positional
        file/dir arguments. Leaves self.args populated with cmd args.
        """
        self.args = self.args[1:]  # We don't use the argv[0] call arg.
        # Due to ambiguity in '--arg value/arg' format
        # non-shim CLI args should be provided in '--arg=value' form
        parser = ArgumentParser()
        parser.add_argument("--install-dir", type=Path, default=self.install_path)
        parser.add_argument("--version", type=str)
        parser.add_argument("paths", nargs="*")
        shim_args, self.args = parser.parse_known_args(self.args)
        self.install_path = shim_args.install_dir
        self.paths = shim_args.paths
        if shim_args.version is not None:  # Verify the version before continuing
            self._assert_version(
                self.get_version_str(),
                shim_args.version,
            )

    def _assert_version(self, actual_ver: str, expected_ver: str):
        """--version hook arg enforces specific versions of tools."""
        if expected_ver in actual_ver:
            return  # If the version is correct, continue execution
        problem = "Version of " + self.command + " is wrong."
        details = (
            f"Expected version: {expected_ver} Found version: {actual_ver}. "
            "Edit your pre-commit config or use a different version "
            f"of {self.command}."
        )
        self.raise_error(problem, details)

    def raise_error(self, problem: str, details: str):
        """Raise a formatted error."""
        format_list = [self.command, problem, details]
        stderr_str = """Problem with {}: {}\n{}\n""".format(*format_list)
        # All strings are generated by this program, so decode should be safe
        self.stderr = stderr_str.encode()
        self.return_code = 1
        sys.stderr.buffer.write(self.stderr)
        raise SystemExit(self.return_code)

    def get_version_str(self):
        """Get the semantic version string for a given command."""
        sp_child = self._execute_with_arguments(["--version"])
        version_str = str(sp_child.stdout, encoding="utf-8")
        # After version like `8.0.0` is expected to be '\n' or ' '
        # (\d.){1,2}(\d)
        regex = r"((?:\d+\.)+[\d+_\+\-a-z]+)"
        search = re.search(regex, version_str)
        if not search:
            details = "The version format for this command has changed."
            self.raise_error("getting version", details)
        return search.group(1)

    def _execute_with_arguments(self, args) -> sp.CompletedProcess:
        args = [
            (
                self.install_path.joinpath(self.command).resolve()
                if self.install_path != Path()
                else Path(self.command)  # On path
            ),
            *args,
        ]
        if args[0].suffix == ".py":  # Run python script
            args.insert(0, "python")
        return sp.run(  # nosec B603
            # We assemble the args internally so should be safe
            args,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            check=False,
            shell=False,
        )


class StaticAnalyzerCmd(Command):
    """Commands that analyze code and do not modify it."""

    def run_command(self) -> bool:
        """Execute the static analyser command."""
        self.check_installed()
        sp_child = self._execute_with_arguments([*self.args, *self.paths])
        self.stdout += sp_child.stdout
        self.stderr += sp_child.stderr
        self.return_code = sp_child.returncode
        self.exit_on_error()
        return self.return_code == 0

    def exit_on_error(self):
        """On non-zero code writes buffered error message and exits.

        :return:
        """
        if self.return_code != 0:
            sys.stderr.buffer.write(self.stdout + self.stderr)
            raise SystemExit(self.return_code)