Version 0.2.0
-------------

:Date: TBC

* Officially supporting python 3.11.
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
