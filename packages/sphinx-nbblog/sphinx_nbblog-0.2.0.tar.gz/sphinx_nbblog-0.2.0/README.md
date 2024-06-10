# Sphinx nbblog

A small [Sphinx](https://www.sphinx-doc.org) extension to enable tags and archive in documentation such as for a blog.

[![PyPI - Version](https://img.shields.io/pypi/v/sphinx-nbblog.svg)](https://pypi.org/project/sphinx-nbblog)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sphinx-nbblog.svg)](https://pypi.org/project/sphinx-nbblog)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)
- [Notes](#notes)

## Installation

```console
pip install sphinx-nbblog
```

## Usage

Add `sphinx-nbblog` somewhere in the `extensions` list in `conf.py`

```
extensions = [
    ...
    "sphinx_nbblog",
]
```

In an .rst file or in a .ipynb raw rst cell:

```
.. nbblog::
   :abstract: what is this about
   :date: 2023-09-23
   :tags: yes, no, maybe
```

In another file, such as archive.rst

```
Archive
=======

.. archive::
```

The abstract currently does nothing but at some point I will
probably make it visible in the archive page.


## Development

I use [Hatch](https://hatch.pypa.io/latest/), [pyenv](https://github.com/pyenv/pyenv), and [LunarVim](https://www.lunarvim.org/)

```
hatch run lvim
```


### Test

After installing the python versions with pyenv, run:

```
hatch run test:test
```


## License

`sphinx-nbblog` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Notes

This project is based on [sphinx-tags](https://github.com/melissawm/sphinx-tags)

