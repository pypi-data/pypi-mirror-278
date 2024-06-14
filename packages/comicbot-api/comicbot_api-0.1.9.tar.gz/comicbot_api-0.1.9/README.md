# ComicBot API
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


![](./docs/source/_static/images/fortress-of-solitude.jpeg)
<!-- TOC -->
* [ComicBot API](#comicbot-api)
  * [Requirements](#requirements)
* [Project Expectations](#project-expectations)
  * [How to get started](#how-to-get-started)
    * [Create a virtual environment](#create-a-virtual-environment)
    * [Enter virtual environment](#enter-virtual-environment)
    * [Install Poetry, the package manager for this project](#install-poetry-the-package-manager-for-this-project)
    * [Build distribution of project](#build-distribution-of-project)
    * [Running Unit Tests](#running-unit-tests)
      * [Pytest to run all unit tests in `test/`](#pytest-to-run-all-unit-tests-in-test)
    * [Pytest to run all unit tests and lint code with `Pylama`](#pytest-to-run-all-unit-tests-and-lint-code-with-pylama)
    * [Linting](#linting)
    * [Deployment](#deployment-)
  * [Roadmap](#roadmap)
<!-- TOC -->

## Requirements
- Python 3.9 or above
- Virtualenv 20.14.1 or above

# Project Expectations
- Client library to get new releases, or releases for a given date. 
- Client can filter by the format of releases e.g. 'single-issue' or by publisher e.g. 'marvel'
- Client should be straight forward and easy to use by using the KISS model (Keep It Simple Stupid)
- Cache results where possible as not to hit provider with too many requests for the same data

## How to get started
### Create a virtual environment
```bash
virtualenv -p python3.9 venv
```

### Enter virtual environment
```bash
source venv/bin/activate
```

### Install Poetry, the package manager for this project
```bash
pip install poetry
```

### Build distribution of project
```bash
poetry build
```
Build artifacts will be located in `dist/`
### Running Unit Tests
#### Pytest to run all unit tests in `test/`
```bash
pytest
```

### Pytest to run all unit tests and lint code with `Pylama`
```bash
pytest --pylama
```

### Linting
This project strives to keep the code style in line with [PEP8](https://peps.python.org/pep-0008/).
To test the project for compliance with PEP8, I use [Pylama](https://github.com/klen/pylama)
```bash
pip install pylama
```
```bash
pylama comicbot_api
```

### Deployment 
To deploy, one must obtain an API key from the public pypi (https://pypi.org/project/comicbot-api/)
and add it to the local `poetry` configuration with the following command:
```bash
poetry config pypi-token.pypi <pypi-token>
```
Once we have a valid token, we can push distributions to PyPi. 
```bash
poetry build
poertry publish
```
or do both with
```bash
poetry publish --build
```
***
## Roadmap
- [ ] Database to cache results from source
- [ ] Sphinx Automatic Documentation Creation