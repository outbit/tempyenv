tempyenv
=====================

Description
===========

The easiest and quickest way to create a temp/tmp/temporary python virtual environment.

tempyenv sets up a python environment in a temporary path.  Quick way to create a throw away python environment.

[![Build Status](https://app.travis-ci.com/outbit/tempyenv.svg?branch=develop "ansible-docs latest build")](http://travis-ci.org/outbit/tempyenv)
[![PIP Version](https://img.shields.io/pypi/v/tempyenv.svg "tempyenv PyPI version")](https://pypi.python.org/pypi/tempyenv)
[![Coverage Status](https://coveralls.io/repos/outbit/tempyenv/badge.svg?branch=develop&service=github)](https://coveralls.io/github/outbit/tempyenv?branch=develop)
[![Gitter IM](https://badges.gitter.im/Join%20Chat.svg)](https://matrix.to/#/#tempyenv:gitter.im)


Installation
===========

```shell
$ python -m pip install tempyenv
```

Usage
===========

```bash
$ tmpyenv
```

or

```bash
$ tempyenv
(tempyenv) is setting up your virtual environment...hold tight
Virtual environment created at /var/folders/4b/dnp21z017cg_rbgfdtzclqlm0000gn/T/tmpacwjkg5z/venv
Virtual environment loading from /var/folders/4b/dnp21z017cg_rbgfdtzclqlm0000gn/T/tmpacwjkg5z/venv
(tempyenv)(venv) $ echo "now you can pip install in your virtual environment"
```

License
=======

tempyenv is released under the [MIT License](LICENSE.md).

Author
======

David Whiteside (<david@davidwhiteside.com>)

