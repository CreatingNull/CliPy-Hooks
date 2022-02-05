#!/usr/bin/env python
"""Command Class functionality for calling a CLI tool."""
import difflib
import os
import re
import shutil
import subprocess as sp
import sys
from pathlib import Path
from typing import List


# This is the original design by pocc so ignore unless refactored.
# pylint: disable=R0902
class Command:
    """Super class that all commands inherit."""

    def __init__(self, command: str, look_behind: str, args: List[str], help_url: str):
        """Constructor for the cli command class.

        :param command: Name of the command, must be on path or define install location.
        :param look_behind: Defines the text preceding version output.
        :param args: Additional arguments to provide to the CLI tool.
        :param help_url: URL of project documentation to assist when things go wrong.
        """
        self.args = args
        self.look_behind = look_behind
        self.command = command
        # Will be [] if not run using pre-commit or if there are no committed files
        self.files = self.get_added_files()
        self.edit_in_place = False

        self.stdout = b""
        self.stderr = b""
        self.returncode = 0

        self.help_url = help_url
        self.install_path = ""
        self.parse_args(self.args)

    def check_installed(self):
        """Check if command is installed and fail exit if not."""
        if self.install_path == "":  # Resolve command from PATH
            path = shutil.which(self.command)
        else:  # Resolve absolute executable
            path = Path(self.install_path).joinpath(self.command)
            if not path.exists():
                path = None  # Executable not found
        if path is None:
            check_path = (
                f" at '{self.install_path}'"
                if self.install_path != ""
                else " and on your PATH"
            )
            details = (
                f"Make sure {self.command} is installed {check_path}.\n"
                f"For more info: {self.help_url}"
            )
            self.raise_error(f"{self.command} not found", details)

    def get_added_files(self):
        """Find added files using git."""
        added_files = sys.argv[1:]  # 1: don't include the hook file
        # cfg files are used by uncrustify and won't be source files
        added_files = [
            f for f in added_files if os.path.exists(f) and not f.endswith(".cfg")
        ]

        # Taken from:
        # https://github.com/pre-commit/pre-commit-hooks/blob/master/pre_commit_hooks/util.py
        # If no files are provided and if this is used as a command,
        # Find files the same way pre-commit does.
        if len(added_files) == 0:
            cmd = ["git", "diff", "--staged", "--name-only", "--diff-filter=A"]
            sp_child = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, check=False)
            if sp_child.stderr or sp_child.returncode != 0:
                self.raise_error(
                    "Problem determining which files are being committed using git.",
                    sp_child.stderr.decode(),
                )
            added_files = sp_child.stdout.decode().splitlines()
        return added_files

    def parse_args(self, args: List[str]):
        """Parse the args into usable variables."""
        self.args = list(args[1:])  # don't include calling function
        for arg in args:
            if arg in self.files and not arg.startswith("-"):
                self.args.remove(arg)
            if arg.startswith("--version"):
                # If --version is passed in as 2 arguments, where the second is version
                if arg == "--version" and args.index(arg) != len(args) - 1:
                    expected_version = args[args.index(arg) + 1]
                # Expected split of --version=8.0.0 or --version 8.0.0 with as many spaces as needed
                else:
                    expected_version = (
                        arg.replace(" ", "").replace("=", "").replace("--version", "")
                    )
                actual_version = self.get_version_str()
                self.assert_version(actual_version, expected_version)
            if arg.startswith("--install-path"):
                # Special arg for setting absolute installation path.
                install_path = args[args.index(arg) + 1]
                if not Path(install_path).exists():
                    self.raise_error(
                        "Install path argument is invalid.",
                        f"The path '{install_path}' does not exist on the system.",
                    )
                # Resolve relative paths to absolute.
                self.install_path = Path(install_path).resolve().__str__()

    def add_if_missing(self, new_args: List[str]):
        """Add a default if it's missing from the command. This library exists
        to force checking, so prefer those options. len(new_args) should be 1,
        or 2 for options like --key=value.

        If first arg is missing, add new_args to command's args
        Do not change an option - in those cases return.
        """
        new_arg_key = new_args[0].split("=")[0]
        for arg in self.args:
            existing_arg_key = arg.split("=")[0]
            if existing_arg_key == new_arg_key:
                return
        self.args += new_args

    def assert_version(self, actual_ver: str, expected_ver: str):
        """--version hook arg enforces specific versions of tools."""
        expected_len = len(expected_ver)  # allows for fuzzy versions
        if expected_ver not in actual_ver[:expected_len]:
            problem = "Version of " + self.command + " is wrong"
            details = (
                f"Expected version: {expected_ver} Found version: {actual_ver}"
                "Edit your pre-commit config or use a different version "
                f"of {self.command}."
            )
            self.raise_error(problem, details)
        # If the version is correct, exit normally
        sys.exit(0)

    def raise_error(self, problem: str, details: str):
        """Raise a formatted error."""
        format_list = [self.command, problem, details]
        stderr_str = """Problem with {}: {}\n{}\n""".format(*format_list)
        # All strings are generated by this program, so decode should be safe
        self.stderr = stderr_str.encode()
        self.returncode = 1
        sys.stderr.buffer.write(self.stderr)
        sys.exit(self.returncode)

    def get_version_str(self):
        """Get the version string like 8.0.0 for a given command."""
        args = [self.install_path + self.command, "--version"]
        sp_child = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE, check=False)
        version_str = str(sp_child.stdout, encoding="utf-8")
        # After version like `8.0.0` is expected to be '\n' or ' '
        regex = self.look_behind + r"((?:\d+\.)+[\d+_\+\-a-z]+)"
        search = re.search(regex, version_str)
        if not search:
            details = "The version format for this command has changed."
            self.raise_error("getting version", details)
        version = search.group(1)
        return version


class StaticAnalyzerCmd(Command):
    """Commmands that analyze code and are not formatters."""

    def run_command(self, args: List[str]):
        """Run the command and check for errors.

        Args includes options and filepaths
        """
        self.check_installed()
        args = [self.install_path + self.command, *args]
        sp_child = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE, check=False)
        self.stdout += sp_child.stdout
        self.stderr += sp_child.stderr
        self.returncode = sp_child.returncode
        self.exit_on_error()

    def exit_on_error(self):
        """On non-zero code writes buffered error message and exits.

        :return:
        """
        if self.returncode != 0:
            sys.stderr.buffer.write(self.stdout + self.stderr)
            sys.exit(self.returncode)


class FormatterCmd(Command):
    """Commands that format code."""

    def compare_to_formatted(self, filename_str: str) -> None:
        """Compare the expected formatted output to file contents."""
        # This string encode is from argparse, so we should be able to trust it.
        filename = filename_str.encode()
        actual = self.get_file_lines(filename_str)
        expected = self.get_formatted_lines(filename_str)
        if self.edit_in_place:
            # If edit in place is used, the formatter will fix in place with
            # no stdout. So compare the before/after file for hook pass/fail
            expected = self.get_file_lines(filename_str)
        diff = list(
            difflib.diff_bytes(
                difflib.unified_diff,
                actual,
                expected,
                fromfile=b"original",
                tofile=b"formatted",
            )
        )
        if len(diff) > 0:
            header = filename + b"\n" + 20 * b"=" + b"\n"
            self.stderr += header + b"\n".join(diff) + b"\n"
            self.returncode = 1

    def get_formatted_lines(self, filename: str) -> List[bytes]:
        """Get the expected output for a command applied to a file."""
        args = [self.install_path + self.command, *self.args, filename]
        child = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE, check=False)
        if len(child.stderr) > 0 or child.returncode != 0:
            self.raise_error(
                "Unexpected Stderr/return code received "
                f"when analyzing {filename}.\nArgs: {args}",
                child.stdout.decode() + child.stderr.decode(),
            )
        if child.stdout == b"":
            return []
        return child.stdout.split(b"\x0a")

    def get_file_lines(self, filename: str):
        """Get the lines in a file."""
        if not os.path.exists(filename):
            self.raise_error(
                f"File {filename} not found", "Check your path to the file."
            )
        with open(filename, "rb") as file:
            file_text = file.read()
        return file_text.split(b"\x0a")