Contributor guidelines
======================

.. _documentation: https://snapbox.readthedocs.io/#writing-documentation
.. _pre-commit: https://pre-commit.com/#installation
.. _black: https://black.readthedocs.io/
.. _isort: https://pycqa.github.io/isort/
.. _doc8: https://doc8.readthedocs.io/
.. _ruff: https://beta.ruff.rs/docs/
.. _uv: https://uv.readthedocs.io/
.. _issues: https://github.com/barseghyanartur/snapbox/issues
.. _discussions: https://github.com/barseghyanartur/snapbox/discussions
.. _pull request: https://github.com/barseghyanartur/snapbox/pulls
.. _support: https://snapbox.readthedocs.io/#support
.. _installation: https://snapbox.readthedocs.io/#installation
.. _features: https://snapbox.readthedocs.io/#features
.. _prerequisites: https://snapbox.readthedocs.io/#prerequisites

Developer prerequisites
-----------------------
pre-commit
~~~~~~~~~~
Refer to `pre-commit`_ for installation instructions.

TL;DR:

.. code-block:: sh

    pip install pipx --user  # Install pipx
    pipx install pre-commit  # Install pre-commit
    pre-commit install  # Install pre-commit hooks

Installing `pre-commit`_ will ensure you adhere to the project code quality
standards.

Code standards
--------------
`black`_, `isort`_, `ruff`_ and `doc8`_ will be automatically triggered by
`pre-commit`_. Still, if you want to run checks manually:

.. code-block:: sh

    make black
    make doc8
    make isort
    make ruff

Requirements
------------
Requirements are compiled using `uv`_.

.. code-block:: sh

    make compile-requirements

Virtual environment
-------------------
You are advised to work in virtual environment.

TL;DR:

.. code-block:: sh

    python -m venv env
    pip install -e .[all]

Documentation
-------------
Check `documentation`_.

Testing
-------
Check `testing`_.

If you introduce changes or fixes, make sure to test them locally using
all supported environments. For that use tox.

.. code-block:: sh

    tox

In any case, GitHub Actions will catch potential errors, but using tox speeds
things up.

For a quick test of the package and all examples, use the following `Makefile`
command:

.. code-block:: sh

    make test-all

Pull requests
-------------
You can contribute to the project by making a `pull request`_.

For example:

- To fix documentation typos.
- To improve documentation (for instance, to add new recipe or fix
  an existing recipe that doesn't seem to work).
- To introduce a new feature (for instance, add support for a non-supported
  file type).

**Good to know:**

- This library consists of a single ``imgbox`` module.

**General list to go through:**

- Does your change require documentation update?
- Does your change require update to tests?
- Does your change rely on third-party package or a cloud based service?
  If so, please consider turning it into a dedicated standalone package,
  since this library is dependency free (and will always stay so).

**When fixing bugs (in addition to the general list):**

- Make sure to add regression tests.

**When adding a new feature (in addition to the general list):**

- Make sure to update the documentation (check whether the `installation`_,
  `features`_ require changes).

Questions
---------
Questions can be asked on GitHub `discussions`_.

Issues
------
For reporting a bug or filing a feature request use GitHub `issues`_.

**Do not report security issues on GitHub**. Check the `support`_ section.
