# Building VoteTrackerPlus

Follow the steps in this section to build VTP. Unless you make changes to the source you will not need to do this more than once.

## 1) Pre-requisites

For all these build setups you will need the following tools:

- **Python**. You will need Python **>= 3.8**

    If you are using an older Python and are not sure how to install a more recent one look at [RealPython's Managing Multiple Python Versions with pyenv][realpython-pyenv].

- **Pip**.  You will usually need Pip **>= 21.3**

    Check your Pip version:

    ```
        $ pip -V
    ```

    If you are on an older Pip, then _after_ installing and activating the virtual environment run:

    ```
        $ pip install --upgrade pip
    ```

## 2) Building/creating a local install

To build VTP, you need to:

0. Start at the root of the cloned source tree.
1. Create a Python virtual environment
2. Activate the virtual environment
3. Upgrade to a recent Pip.
4. Build the package using an a _local project install_ (aka as an _editable install_).

Multiple Python build systems can be used to support the last step. VTP currently supports Poetry (recommended as it will be simpler) and Setuptools (on older or legacy systems).

### 2.1) Build with Poetry

If you are able to use a recent Python setup (since mid-2020) build with [Poetry][poetry]. You will need **Poetry >= 1.1**.

To install Poetry see: <https://python-poetry.org/docs/1.1/#installation>

You can check your Poetry version with:

```
    $ poetry --version
```

Then build VTP as follows:

```
    $ ln -s _tools/build/poetry_pyproject.toml pyproject.toml
    $ ln -s _tools/build/poetry_poetry.lock poetry.lock
    $ poetry shell
    $ poetry install
```

There is a makefile rule for this step if you know what that is and can run it:

```
    $ make poetry-build
```

### 2.2) Build with Setuptools

If you are running on older systems installed since 2019 (including Ubuntu 20.04 without upgrades) or are otherwise limited to Setuptools, after activating the virtual environment use Pip to see if you have Setuptools:

```
    $ pip freeze | grep setuptools
```

If there is no Setuptools use Pip to install it:

```
    $ pip install setuptools
```

If Setuptools is present but not >= 64.0.0, use Pip to upgrade it:

```
    $ pip install --upgrade setuptools
```

Then build VTP as follows:

```
    $ ln -s _tools/build/setuptools_pyproject.toml pyproject.toml
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install --editable .
```

Note - there is a makefile rule for this step if you know what that is and can run it:

```
    $ make setuptools-build
```

_Note_: Don't leave the `.` off of the `pip install .`

If you can't upgrade Setuptools for any reason, then you should build as follows:

```
    $ ln -s _tools/build/setuptools_legacy_pyproject.toml pyproject.toml
    $ ln -s _tools/build/setuptools_legacy_setup.cfg setup.cfg
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install --editable .
```

Note - there is a makefile rule for this step if you know what that is and can run it:

```
    $ make setuptools-legacy-build
```
## 3) Concepts

- **Editable installs**

    Python editable installs ensure that all import statements, both inside the project and in external packages point to the same python files, and make it so that all paths and scripts just work.  Note that is all per python environment.  Multiple python environments work as expected but that level of sophistication is not described here.

    Editable installs are usually run with Pip:

    ```
        $ pip install --editable <project directory>
    ```

    Poetry does editable installs by default.

    ```
        $ poetry install
    ```

    The actual work is done by a build tool which supports [PEP 660][pep-660].
    This includes Setuptools >= 64.0.0 and Poetry >= 1.1.0.


- **pyproject.toml**

    Modern Python packaging introduces a single configuration file for managing the building and packaging of a Python project. This file, called `pyproject.toml` allows specifying builds using any of a number of different packaging and build backends.
    
    `pyproject.toml` specifies the build backend in a section called [`build-system`][pyproject-build-system]. See the [Poetry build system][poetry-build-system] and the [Setuptools build system][setuptools-build-system]

    [Poetry][poetry-pyproject] and [Setuptools][setuptools-pyproject] support `pyproject.toml`. A number of other build tools do as well.

    To learn more about `pyproject.toml` read [PEP 518][pep-518]and [PEP 621][pep-621].


- **setup.cfg**

    An older configuration file supported only by Setuptools. In versions of Setuptools that don't support [PEP 660][pep-660] `pyproject.toml` is mostly empty, and the work of configuration is done by [`setup.cfg`][setuptools-setupcfg].

    It's preferrable not to need `setup.cfg` as it's not compatible with any other build tools, but on older systems that may be the only available choice.


## 4) References

### 4.1) Guides

To learn about packaging in general read the[Python Packaging User Guide][packaging-user-guide]

To learn about the tools:

- [Pip][pip]
    - [Pip User Guide][pip-userguide]
- [Poetry][poetry]
- [Setuptools][setuptools]
    - [Setuptools User Guide][setuptools-user-guide]

Read about editable installs:

- [Pip and editable installs][pip-editable-installs]

### 4.2) Specifications

- [PEP 517][pep-517]: _Build-System Independent Format or Source Trees_

    Defines the API between Python build system frontends and backends.

- [PEP 518][pep-518]: _Specifying Minimum Build System Requirements for Python Projects_
    
    Defines `pyproject.toml`, and its `build-system` section.

- [PEP 621][pep-621]: _Storing Project Metadata in pyproject.toml

    Defines the metadata properties (key names and value types) that can be
    used for projects across Python build systems.

- [PEP 660][pep-660]: _Editable installs for pyproject.toml based builds_

    Defines the API providing portable editable installs between build backends.


[packaging-user-guide]: https://packaging.python.org
[pyproject-build-system]: https://peps.python.org/pep-0517#build-backend-interface
[realpython-pyenv]: https://realpython.com/intro-to-pyenv

[pip]: https://pip.pypa.io
[pip-editable-installs]: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
[poetry]: https://python-poetry.org
[poetry-build-system]: https://python-poetry.org/docs/1.1/pyproject/#poetry-and-pep-517
[poetry-install]: https://python-poetry.org/docs/1.1/#installation
[poetry-pyproject]: https://python-poetry.org/docs/1.1/pyproject/
[setuptools]: https://setuptools.pypa.io
[setuptools-build-system]: https://setuptools.pypa.io/en/latest/build_meta.html
[setuptools-pyproject]: https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
[setuptools-setupcfg]: https://setuptools.pypa.io/en/latest/userguide/declarative_config.html

[pep-517]: https://peps.python.org/pep-0517
[pep-518]: https://peps.python.org/pep-0518
[pep-621]: https://peps.python.org/pep-0621
[pep-660]: https://peps.python.org/pep-0660
