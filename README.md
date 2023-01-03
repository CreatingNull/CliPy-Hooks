# ![NullTek Documentation](https://raw.githubusercontent.com/CreatingNull/NullTek-Assets/main/img/logo/NullTekDocumentationLogo.png) CliPy Hooks

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clipy-hooks?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/clipy-hooks/)
[![PyPI](https://img.shields.io/pypi/v/clipy-hooks?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/clipy-hooks/)
[![Format](https://img.shields.io/github/actions/workflow/status/CreatingNull/clipy-hooks/run-pre-commit.yaml?branch=main&logo=pre-commit&style=flat-square&label=format)](https://github.com/CreatingNull/clipy-hooks/actions/workflows/run-pre-commit.yaml)
[![Tests](https://img.shields.io/github/actions/workflow/status/CreatingNull/clipy-hooks/run-tests.yaml?branch=main&logo=GitHub&style=flat-square&label=tests)](https://github.com/CreatingNull/clipy-hooks/actions/workflows/run-tests.yaml)
[![License](https://img.shields.io/github/license/CreatingNull/clipy-hooks?style=flat-square)](https://github.com/CreatingNull/clipy-hooks/blob/main/LICENSE)

This project is a library handling generic execution of command line interfaces using python, it is a cross-platform shim between pre-installed system executables and pre-commit.
The intended use-case is for creating new [pre-commit](https://pre-commit.com) hooks without fussing over the boilerplate of handling the CLI.

Credit to pocc's awesome [pre-commit hooks](https://github.com/pocc/pre-commit-hooks) as he wrote the underlying class as part of his C linters.

---

## Getting Started

### Installing

The easiest way to use the project is to install the latest pypi release via pip.

```shell
pip install clipy-hooks
```

## License

The source of this repo maintains the Apache 2.0 open-source license of the original code, for details on the current licensing see [LICENSE](https://github.com/CreatingNull/clipy-hooks/blob/main/LICENSE) or click the badge above.
