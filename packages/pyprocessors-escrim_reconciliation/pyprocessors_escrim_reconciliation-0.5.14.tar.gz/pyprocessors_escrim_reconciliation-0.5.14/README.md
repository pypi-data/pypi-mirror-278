# pyprocessors_escrim_reconciliation

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_escrim_reconciliation)](https://github.com/oterrier/pyprocessors_escrim_reconciliation/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_escrim_reconciliation/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_escrim_reconciliation/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_escrim_reconciliation)](https://codecov.io/gh/oterrier/pyprocessors_escrim_reconciliation)
[![docs](https://img.shields.io/readthedocs/pyprocessors_escrim_reconciliation)](https://pyprocessors_escrim_reconciliation.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_escrim_reconciliation)](https://pypi.org/project/pyprocessors_escrim_reconciliation/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_escrim_reconciliation)](https://pypi.org/project/pyprocessors_escrim_reconciliation/)

EscrimReconciliation annotations coming from different annotators

## Installation

You can simply `pip install pyprocessors_escrim_reconciliation`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_escrim_reconciliation
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
