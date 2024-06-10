# link-stacklog

[![PyPI](https://img.shields.io/pypi/v/link-stacklog.svg)](https://pypi.org/project/link-stacklog/)
[![Changelog](https://img.shields.io/github/v/release/theFestest/link-stacklog?include_prereleases&label=changelog)](https://github.com/theFestest/link-stacklog/releases)
[![Tests](https://github.com/theFestest/link-stacklog/actions/workflows/test.yml/badge.svg)](https://github.com/theFestest/link-stacklog/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/theFestest/link-stacklog/blob/master/LICENSE)

Link backlog management utility using a stack style interface

## Installation

Install this tool using `pip`:
```bash
pip install link-stacklog
```
## Usage

For help, run:
```bash
link-stacklog --help
```
You can also use:
```bash
python -m link_stacklog --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd link-stacklog
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
