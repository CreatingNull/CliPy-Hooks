# ![NullTek Documentation](https://raw.githubusercontent.com/CreatingNull/NullTek-Assets/main/img/logo/NullTekDocumentationLogo.png) Pre-Commit PyCLI

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre-commit-pycli?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/pre-commit-pycli/)
[![PyPI](https://img.shields.io/pypi/v/pre-commit-pycli?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/pre-commit-pycli/)
[![Tests](https://img.shields.io/github/workflow/status/CreatingNull/pre-commit-pycli/pre-commit?logo=pre-commit&style=flat-square&label=format)](https://github.com/CreatingNull/pre-commit-pycli/actions/workflows/run-pre-commit.yaml)
[![Tests](https://img.shields.io/github/workflow/status/CreatingNull/pre-commit-pycli/tests?logo=GitHub&style=flat-square&label=tests)](https://github.com/CreatingNull/pre-commit-pycli/actions/workflows/run-tests.yaml)
[![License](https://img.shields.io/github/license/CreatingNull/pre-commit-pycli?style=flat-square)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

This project is a library handling generic execution of command line interfaces using python, it is a cross-platform shim between pre-installed system executables and pre-commit.
The intended use-case is for creating new [pre-commit](https://pre-commit.com) hooks without fussing over the boilerplate of handling the CLI.

Credit to pocc's awesome [pre-commit hooks](https://github.com/pocc/pre-commit-hooks) as he wrote the underlying class as part of his C linters.

---

## Getting Started

### Installing

The easiest way to use the project is to install the latest pypi release via pip.

```shell
pip install pre-commit-pycli
```

## License

The source of this repo maintains the Apache 2.0 open-source license of the original code, for details on the current licensing see [LICENSE](https://github.com/CreatingNull/Pre-Commit-PyCLI/blob/master/LICENSE) or click the badge above.
