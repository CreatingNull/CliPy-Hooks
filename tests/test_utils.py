#!/usr/bin/env python3
import difflib
import os
import re
import shutil
import subprocess as sp
import sys
import uuid

import pytest

test_file_strs = {
    "ok.c": '// Copyright 2021 Ross Jacobs\n#include <stdio.h>\n\nint main() {\n  printf("Hello World!\\n");\n  return 0;\n}\n',
    "ok.cpp": '// Copyright 2021 Ross Jacobs\n#include <iostream>\n\nint main() {\n  std::cout << "Hello World!\\n";\n  return 0;\n}\n',
    "err.c": "#include <stdio.h>\nint main(){int i;return;}",
    "err.cpp": "#include <string>\nint main(){int i;return;}",
}


def assert_equal(expected, actual):
    """Stand in for Python's assert which is annoying to work with."""
    actual = actual.replace(b"\r", b"")  # ignore windows file ending differences
    if expected != actual:
        print(f"\n\nExpected:`{expected}`")
        print(f"\n\nActual__:`{actual}`")
        if isinstance(expected, bytes) and isinstance(actual, bytes):
            expected_str = expected.decode()
            actual_str = actual.decode()
            print("String comparison:", expected_str == actual_str)
            diff_lines_gen = difflib.context_diff(expected_str, actual_str, "Expected", "Actual")
            diff_lines = "".join(list(diff_lines_gen))
            print(f"\n\nDifference:\n{diff_lines}")
        else:
            print(f"Expected is type {type(expected)}\nActual is type {type(actual)}")
        pytest.fail("Test failed!")


def get_versions():
    """Returns a dict of commands and their versions."""
    commands = ["clang-format", "clang-tidy", "uncrustify", "cppcheck", "cpplint"]
    if os.name != "nt":  # oclint doesn't work on windows, iwyu needs to be compiled on windows
        commands += ["oclint", "include-what-you-use"]
    # Regex for all versions. Unit tests: https://regex101.com/r/rzJE0I/1
    regex = r"[- ]((?:\d+\.)+\d+[_+\-a-z\d]*)(?![\s\S]*OCLint version)"
    versions = {}
    for cmd in commands:
        if not shutil.which(cmd):
            sys.exit("Command " + cmd + " not found.")
        cmds = [cmd, "--version"]
        child = sp.run(cmds, stdout=sp.PIPE, stderr=sp.PIPE)
        if len(child.stderr) > 0:
            print(f"Received error when running {cmds}:\n{child.stderr}")
            sys.exit(1)
        output = child.stdout.decode("utf-8")
        try:
            versions[cmd] = re.search(regex, output).group(1)
        except AttributeError:
            print(f"Received `{output}`. Version regexes have broken.")
            print("Please file a bug (github.com/pocc/pre-commit-hooks).")
            sys.exit(1)
    return versions


# Required for testing with clang-tidy and oclint
def set_compilation_db(filenames):
    """Create a compilation database for clang static analyzers."""
    cdb = "["
    clang_location = shutil.which("clang")
    file_dir = os.path.dirname(os.path.abspath(filenames[0]))
    for f in filenames:
        file_base = os.path.basename(f)
        clang_suffix = ""
        if f.endswith("cpp"):
            clang_suffix = "++"
        cdb += """\n{{
    "directory": "{0}",
    "command": "{1}{2} {3} -o {3}.o",
    "file": "{3}"
}},""".format(
            file_dir, clang_location, clang_suffix, os.path.join(file_dir, file_base)
        )
    cdb = cdb[:-1] + "]"  # Subtract extra comma and end json
    # Required for clang-tidy
    if os.name == "nt":
        cdb = cdb.replace("\\", "\\\\").replace("Program Files", 'Program" "Files')
    with open(file_dir + "/" + "compile_commands.json", "w") as f:
        f.write(cdb)


def set_git_identity():
    """Set a git identity if one does not exist."""
    sp_child = sp.run(["git", "config", "--list"], stdout=sp.PIPE)
    if "user.name" not in sp_child.stdout.decode() or "user.email" not in sp_child.stdout.decode():
        sp.run(["git", "config", "--global", "user.name", "Test Runner"])
        sp.run(["git", "config", "--global", "user.email", "test@example.com"])
        sp.run(["git", "config", "--global", "init.defaultbranch", "master"])


def run_in(commands, tmpdir):
    sp_child = sp.run(commands, cwd=tmpdir, stdout=sp.PIPE, stderr=sp.PIPE)
    if sp_child.returncode != 0:
        err_msg = (
            f"commands {commands} failed with\n"
            + f"stdout: {sp_child.stdout.decode()}"
            + f"stderr: {sp_child.stderr.decode()}\n"
        )
        pytest.fail(err_msg)
