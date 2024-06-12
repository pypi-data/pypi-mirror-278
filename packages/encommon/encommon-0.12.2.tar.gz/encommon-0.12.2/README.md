# Enasis Network Common Library

> :children_crossing: This project has not released its first major version.

Common classes and functions used in various public and private projects.

[![](https://img.shields.io/github/actions/workflow/status/enasisnetwork/encommon/build.yml?style=flat-square&label=GitHub%20actions)](https://github.com/enasisnetwork/encommon/actions)<br>
[![codecov](https://img.shields.io/codecov/c/github/enasisnetwork/encommon?token=7PGOXKJU0E&style=flat-square&logoColor=FFFFFF&label=Coverage)](https://codecov.io/gh/enasisnetwork/encommon)<br>
[![](https://img.shields.io/readthedocs/encommon?style=flat-square&label=Read%20the%20Docs)](https://encommon.readthedocs.io)<br>
[![](https://img.shields.io/pypi/v/encommon.svg?style=flat-square&label=PyPi%20version)](https://pypi.org/project/encommon)<br>
[![](https://img.shields.io/pypi/dm/encommon?style=flat-square&label=PyPi%20downloads)](https://pypi.org/project/encommon)

## Documentation
Documentation is on [Read the Docs](https://encommon.readthedocs.io).
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `docs/html` directory.

## Projects using library
- [Enasis Network Remote Connect](https://github.com/enasisnetwork/enconnect)
- [Enasis Network Homie Automate](https://github.com/enasisnetwork/enhomie)

## Installing the package
Installing stable from the PyPi repository
```
pip install encommon
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/encommon
```

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/encommon.git
```
Set up the Python virtual environments expected by the Makefile.
```
make -s venv-create
```

### Execute the linters and tests
The comprehensive approach is to use the `check` recipe. This will stop on
any failure that is encountered.
```
make -s check
```
However you can run the linters in a non-blocking mode.
```
make -s linters-pass
```
And finally run the various tests to validate the code and produce coverage
information found in the `htmlcov` folder in the root of the project.
```
make -s pytest
```

## Version management
:warning: Ensure that no changes are pending.

1. Rebuild the environment.
   ```
   make -s check-revenv
   ```

1. Update the [version.txt](encommon/version.txt) file.

1. Push to the `main` branch.

1. Create [repository](https://github.com/enasisnetwork/encommon) release.

1. Build the Python package.<br>
   ```
   make -s pypackage
   ```

1. Upload Python package to PyPi test.
   ```
   make -s pypi-upload-test
   ```

1. Upload Python package to PyPi prod.
   ```
   make -s pypi-upload-prod
   ```

1. Update [Read the Docs](https://encommon.readthedocs.io) documentation.
