tempyenv
=====================

Description
===========

The easy and quick way to create a temporary Python virtual environment.

`tempyenv` sets up a python environment in a temporary path and auto removes the environment when you exit.

[![Build Status](https://app.travis-ci.com/outbit/tempyenv.svg?branch=develop "ansible-docs latest build")](http://travis-ci.org/outbit/tempyenv)
[![PIP Version](https://img.shields.io/pypi/v/tempyenv.svg "tempyenv PyPI version")](https://pypi.python.org/pypi/tempyenv)


Installation
===========

Using [uv](https://docs.astral.sh/uv/) (recommended):
```shell
$ uv tool install tempyenv
```

Using pip:
```shell
$ python -m pip install tempyenv
```

Using [Homebrew](https://brew.sh):
```shell
$ brew install outbit/tap/tempyenv
```

Usage
===========

```bash
$ tempyenv
(tempyenv) is setting up your virtual environment...hold tight
Virtual environment created at /var/folders/4b/dnp21z017cg_rbgfdtzclqlm0000gn/T/tmpacwjkg5z/venv
Virtual environment loading from /var/folders/4b/dnp21z017cg_rbgfdtzclqlm0000gn/T/tmpacwjkg5z/venv
(tempyenv)$ which pip
/var/folders/j4/skpmllqx5ls_6s4kn3l25gq00000gn/T/tmpo5a2dwmh/venv/bin/pip
(tempyenv)$ exit
Cleaning up temporary virtual environment...
Temporary environment removed successfully.
```

Help
```bash
$ tempyenv -h
usage: tempyenv [-h] [-p PYTHON_EXEC] [-v]

options:
  -h, --help            show this help message and exit
  -p, --python PYTHON_EXEC
                        Specify the Python executable
  -v, --version         show program's version number and exit
```

To specify a specific version of python
```bash
$ tempyenv -p python3.14
```

License
=======

tempyenv is released under the [MIT License](LICENSE.md).

Author
======

David Whiteside (<david@davidwhiteside.com>)

