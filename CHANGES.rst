Version 0.2.2
-------------

:Date: TBC

* MyPy pre-commit hook added for static type checking.
* ``cli.Command.check_installed`` updated to improve type safety.
* ``cli.Command._execute_with_arguments`` updated to improve type safety.
* Improved type safety of checking for absence of errors in tests.
* Additional pre-commit hooks added to improve maintainability.

Version 0.2.1
-------------

:Date: 20-January-2024

* Officially supporting python 3.12.
* Dependency updates.

Version 0.2.0
-------------

:Date: 3-January-2022

* Officially supporting python 3.11.
* Fixing the GitHub workflow badges in the README.
* Updated ``CHANGELOG.rst`` to ``CHANGES.rst`` for consistency with newer projects.
* Shifting project to use isort in preference to reorder-python-imports.
  This is for consistency with newer projects and ease of use.
* Adding dead code detection, static typing, and doc linting to pre-commit hooks.
* Updating pre-commit hooks to latest.
* Removing .pylintrc file as new versions of pylint don't really require this.
* Fixed a bug where the version regex could mismatch and crash.

Version 0.1.1
-------------

:Date: 5-March-2022

* Adding support for positional arguments being passed to the cli tool.

Version 0.1.0
-------------

:Date: 9-February-2022

* Initial release of CliPy Hooks.
