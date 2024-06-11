build_harness
=============

A command line CI pipeline build harness utility for Python 3 projects based on known
best practices.

There are lots of accessories that are useful for establishing a high quality Python
pipeline and copy-pasting all the bits and pieces to initialize a new project is
tedious and error prone. This utility aims to streamline the creation of a project with
all the necessary development and pipeline dependencies and a ready to run pipeline.

.. contents::

.. section-numbering::


Installation
------------

NOTE: ``build-harness`` requires git >= 2.28.0 due to the use of the
``--initial-branch`` option to manage a user specified default branch at
initialization.

Ensure that git is installed where ``build_harness`` is going to be installed. eg.

.. code-block::

   sudo apt install -y git

The ``build_harness`` package is available from PyPI. Installing into a virtual
environment is recommended.

.. code-block::

   # A first time installation creating an initial virtual environment and then
   # initializing the new project.
   python3 -m venv .venv \
     && .venv/bin/pip install build_harness \
     && .venv/bin/build-harness bootstrap my_new_project

The bootstrap command generates a new Python project with the name ``my_new_project``
from a template with a ready to run CI pipeline and an initial commit of the template
files. You will need to set up the git remote to correctly point to your git
repository and from there your initial "feature" should be tweaking any project
configuration to meet your specific needs.

Note that Ubuntu, for example, separates ``pip`` and ``venv`` installations from the
main Python installation and they are not installed by default, so if you are
working with a fresh Ubuntu install you will need something like this to acquire them
before running the above commands:

.. code-block::

   sudo apt update && sudo apt install -y python3-pip python3-venv

Note also that the ``flit`` package manager and ``gitlab-ci`` CI pipeline are presently
the only official choice for use with ``build_harness``. Over time support for other
package managers and CI tools are expected to be added.


Getting started
---------------

Installation makes a command line utility ``build-harness`` available in the virtual
environment. There are currently five groups of sub-commands available.

acceptance
   Run and manage Gherkin features and step files using the *behave* package.
bootstrap
   Create a new project with ready to run CI pipeline that runs tests, checks
   coverage and publishes a release to pypi.org on a semantic version git tag.
formatting
   Format source code to PEP-8 standard using the *isort* and *black* packages.
install
   Install and manage project dependencies in the virtual environment. The install
   command will look for a virtual environment ``.venv`` in the project root directory
   and create it if needed. Then it installs and manages all the project dependencies
   there.

   This command only installs packages when they are missing or out of date, so it
   makes efficient use of network capacity and can reduce installation time when only
   incremental changes are needed.
package
   Build wheel and sdist packages of the project.
publish
   Publish project artifacts to publication repositories such as PyPI and readthedocs.
static-analysis
   Run static analysis on source code; *pydocstyle*, *flake8* and *mypy* packages.
unit-test
   Run unit tests of the project using *pytest*.

Further options for these commands can be explored using the ``--help`` argument.

.. code-block::

   build-harness --help
   build-harness <subcommand> --help

A quick summary of using each of the sub-commands, or a specified sub-command.

.. code-block::

   # Install project dependencies into the virtual environment.
   build-harness install
   # Check if project dependencies are up to date in the virtual environment.
   build-harness install --check

.. code-block::

   # Format code to PEP-8 standards using isort, black.
   build-harness formatting
   # Fail (exit non-zero) if formatting needs to be applied.
   build-harness formatting --check

.. code-block::

   # Run formatting, pydocstyle, flake8 and mypy analysis on the project.
   build-harness static-analysis

.. code-block::

   # Run pytest on unit tests in the project.
   build-harness unit-test
   # Test that coverage passes the specified threshold.
   build-harness unit-test --check <int>

.. code-block::

   # Run Python behave on Gherkin based features.
   build-harness acceptance tests
   # Generate step file snippets for unimplemented features.
   build-harness acceptance snippets
   # Report where tags are used in feature files.
   build-harness acceptance tags


.. code-block::

   # Publish package artifacts to PyPI.org using a token
   build-harness build --release-id <pep-440 release id>
   build-harness publish --user __token__ --password <token> --publish yes


Concepts
--------

For now, the sub-commands are limited to a specific set of tools (the ones I have
found to be most useful).

Fine tuning configuration of the underlying tools is generally possible using
configuration files such as sections added to ``pyproject.toml`` or ``setup.cfg`` or
tool specific files in some cases.


Release Management
^^^^^^^^^^^^^^^^^^

In essence release management is the definition of release states before and after a
formal "production" release, how the transitions between release states occur, how
those transitions interact with repository branching strategies and how each release
state is identified in project packaging (the release id), source control and other
related artifacts for the purpose of traceability. Python has myriad ways of managing
releases for a project and almost all of them require some custom workflow from the
user to make it work for automation so it's really difficult to support all of them.
For this reason the default packaging option of ``build_harness`` using the ``package
--release-id`` option does nothing relating to the release id and assumes that the
user has done whatever is necessary for their workflow to correctly define the
release id for packaging.

Having said that, the goal of the ``build_harness`` project is to have useful
out-of-the-box functionality as much as possible, so described here are workflows
that have been integrated into the project. Because release management preferences
are so varied a separate utility called ``release-flow`` is introduced for
identifying branches and relating them to source control repository branches. See the
`Release identity`_ section below for more details.

There's a fairly useful survey of Python release management in the answers to this
`StackOverflow question <https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package>`_.
The `setuptools_scm package <https://pypi.org/project/setuptools-scm/>`_ also has some
useful notes on different ways to control release id insertion to a package.


Release identity
++++++++++++++++

Very closely related to release management is the concept of a release identity,
how that identity changes between release states and how those changes are mapped to
changes in source control repository branches and/or tags. Similar to release
management there are myriad ways of identifying formal releases and pre-releases,
constrained only by the PEP-440 definitions for Python projects.

The ``release-flow`` utility applies a relatively simple release identity and
branching strategy that in my experience is useful for most projects:

* Use `semantic versions <https://semver.org>`_ to identify formal releases
* Apply a semantic version tag to commits in the default/main branch of the source
  control repository to identify a formal release to the pipeline
* Non-releases are identified using the PEP-440 compliant release id ``<last
  semantic version>-post<commit offset from last semantic version>``

Further to the above steps relating to the ``release-flow`` utility, these steps must
be applied by the CI pipeline:

* All artifacts are identified with the release id in the filename
* Python packages have the release id applied to project metadata

Finally, the source control repository itself must have a tag semantic version
tag applied to the first commit of the repository. Recommend that the first commit
tag is "0.0.0".


VERSION file workflow
+++++++++++++++++++++

This is the workflow used by the ``build_harness`` project itself, so you can refer
to the source code for an example of how to implement this workflow.

* The package reads the content of a simple text file named ``VERSION`` in the
  top-level Python package of your project and applies it to the `__version__`
  variable in the package.
* If the file does not exist a default release ID is applied as defined within the
  project package.
* Use the snippets below to set the Python ``__version__`` variable for the project
  from the content of the VERSION file.

The default release id must be readily recognisable as having not been built by a
pipeline. eg. If a developer builds the package locally it should be clear that the
package they built is not an official release (which in turn should only have been
built by a pipeline).

A default value I have historically used is "0.0.0". Within the limitations defined
by PEP-440 another option could be "0.0.0+local". The advantage of using the "+local"
prefix is that as defined by PEP-440 the presence of this local identifier suffix
will result in the failure of an attempted upload to pypi.org, so there is much less
change of accidental publishing of a pre-release package.

For manual release definition you have to ensure that the content of the VERSION file
reflects the release id you are releasing. Doing this manually is error prone and
easily acquires a number of deficiencies with respect to how organizations often want
to organize their releases.

For automation the pipeline just needs to be able to update the content of the file
with the release id defined for a release; this is easily achieved by defining
semantic version tags on the repo (or some similar such rule that can be incorporated
into the pipeline code) as a formal release and having the pipeline update the
VERSION file with the tag text.

.. code-block::

    # top-level __init__.py
    """flit requires top-level docstring summary of project"""

    from ._version import __version__  # noqa: F401

.. code-block::

    # _version.py
    import pathlib

    from ._default_values import DEFAULT_RELEASE_ID

    def acquire_version() -> str:
        """
        Acquire PEP-440 compliant version from VERSION file.

        Returns:
            Acquired version text.
        Raises:
            RuntimeError: If version is not valid.
        """
        here = pathlib.Path(__file__).parent
        version_file_path = (here / "VERSION").absolute()

        if version_file_path.is_file():
            with version_file_path.open(mode="r") as version_file:
                version = version_file.read().strip()
        else:
            version = DEFAULT_RELEASE_ID

        if not version:
            raise RuntimeError("Unable to acquire version")

        return version

    __version__ = acquire_version()

.. code-block::

    # _default_values.py
    DEFAULT_RELEASE_ID = "0.0.0"


Publishing workflow
+++++++++++++++++++

The ``publish-flow`` utility implements a simple mapping between branches and tags and
whether or not to publish artifacts. PyPI.org has a test upload site which in this
simple workflow is used to test the upload for all non-release packages. On a
semantic version release tag the workflow enables publishing to pypi.org, or the
PEP-503 artifact repository of your choice, as defined in ``.pyirc``.

Note that for publishing, the default CI pipeline requires the secret
``PYPI_API_TOKEN`` to contain the token needed to publish packages to pypi.org. You
will need to generate an API token using your pypi.org account for the CI pipeline to
successfully complete.

Questions
---------

- **Why not just use CookieCutter?**

  ``build_harness`` complements the use of ``CookieCutter`` nicely - you can use
  ``build_harness`` to establish and maintain your Python project pipeline with minimal
  effort and then focus on using ``CookieCutter`` to implement your business specific
  customization of build, test and analysis options.

  ``build_harness`` also lends itself to being easily applied across multiple use cases,
  from the pipeline itself, to ``pre-commit`` hooks, to developers manually running
  specific components of the pipeline for test and debug.

- **Why aren't you using ``flake8-import-order``?**

  This plugin appears to conflict with ``isort``. Since isort actually
  actually formats rather than just reporting a format failure I consider this more useful
  and have prioritized use of isort. In future it may be possible to configure flake8-import-order
  to align with isort, or vice-versa.

- **Why aren't you using ``flake8-black``?**

  The ``flake8-black`` package is developed independently of ``black`` and seems to introduce it's own
  problems synchronizing with the evolving black package, and in addition suffers from the same "why
  check when you can actually format?" problem as ``flake8-import-order``.

