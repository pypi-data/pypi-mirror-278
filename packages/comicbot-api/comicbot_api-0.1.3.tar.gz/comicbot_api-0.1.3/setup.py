# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comicbot_api', 'comicbot_api.utils', 'comicbot_api.version1']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.11.1',
 'loguru>=0.7.2,<0.8.0',
 'pyyaml>=6.0,<7.0',
 'requests==2.28.1']

setup_kwargs = {
    'name': 'comicbot-api',
    'version': '0.1.3',
    'description': 'A client to retrieve new releases of comic books, filterable by publisher and format.',
    'long_description': "# ComicBot API\n![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)\n\n\n![](./docs/source/_static/images/fortress-of-solitude.jpeg)\n<!-- TOC -->\n* [ComicBot API](#comicbot-api)\n  * [Requirements](#requirements)\n* [Project Expectations](#project-expectations)\n  * [How to get started](#how-to-get-started)\n    * [Create a virtual environment](#create-a-virtual-environment)\n    * [Enter virtual environment](#enter-virtual-environment)\n    * [Install Poetry, the package manager for this project](#install-poetry-the-package-manager-for-this-project)\n    * [Build distribution of project](#build-distribution-of-project)\n    * [Running Unit Tests](#running-unit-tests)\n      * [Pytest to run all unit tests in `test/`](#pytest-to-run-all-unit-tests-in-test)\n    * [Pytest to run all unit tests and lint code with `Pylama`](#pytest-to-run-all-unit-tests-and-lint-code-with-pylama)\n    * [Linting](#linting)\n    * [Deployment](#deployment-)\n  * [Roadmap](#roadmap)\n<!-- TOC -->\n\n## Requirements\n- Python 3.9 or above\n- Virtualenv 20.14.1 or above\n\n# Project Expectations\n- Client library to get new releases, or releases for a given date. \n- Client can filter by the format of releases e.g. 'single-issue' or by publisher e.g. 'marvel'\n- Client should be straight forward and easy to use by using the KISS model (Keep It Simple Stupid)\n- Cache results where possible as not to hit provider with too many requests for the same data\n\n## How to get started\n### Create a virtual environment\n```bash\nvirtualenv -p python3.9 venv\n```\n\n### Enter virtual environment\n```bash\nsource venv/bin/activate\n```\n\n### Install Poetry, the package manager for this project\n```bash\npip install poetry\n```\n\n### Build distribution of project\n```bash\npoetry build\n```\nBuild artifacts will be located in `dist/`\n### Running Unit Tests\n#### Pytest to run all unit tests in `test/`\n```bash\npytest\n```\n\n### Pytest to run all unit tests and lint code with `Pylama`\n```bash\npytest --pylama\n```\n\n### Linting\nThis project strives to keep the code style in line with [PEP8](https://peps.python.org/pep-0008/).\nTo test the project for compliance with PEP8, I use [Pylama](https://github.com/klen/pylama)\n```bash\npip install pylama\n```\n```bash\npylama comicbot_api\n```\n\n### Deployment \nTo deploy, one must obtain an API key from the public pypi (https://pypi.org/project/comicbot-api/)\nand add it to the local `poetry` configuration with the following command:\n```bash\npoetry config pypi-token.pypi <pypi-token>\n```\nOnce we have a valid token, we can push distributions to PyPi. \n```bash\npoetry build\npoertry publish\n```\nor do both with\n```bash\npoetry publish --build\n```\n***\n## Roadmap\n- [ ] Database to cache results from source\n- [ ] Sphinx Automatic Documentation Creation",
    'author': 'Aaron Steed',
    'author_email': 'asteed7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
