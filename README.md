# dila

[![Build Status](https://travis-ci.org/socialwifi/dila.svg?branch=master)](https://travis-ci.org/socialwifi/dila)
[![Latest Version](https://img.shields.io/pypi/v/dila.svg)](https://github.com/socialwifi/dila/blob/master/CHANGELOG.md)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/dila.svg)](https://pypi.python.org/pypi/dila/)
[![Wheel Status](https://img.shields.io/pypi/wheel/dila.svg)](https://pypi.python.org/pypi/dila/)
[![License](https://img.shields.io/pypi/l/dila.svg)](https://github.com/socialwifi/dila/blob/master/LICENSE)

Dila is a open source web-based translation platform for translators, content creators and developers.

## Installation
Requires python >=3.5. To install run:
`pip3 install dila`

## Usage
To run development server you have to setup postgresql database first. Then run:
```
cat >config.py <<_EOL
SECRET_KEY = 'secret'
DEBUG = True
DATABASE_URL = 'postgresql://username:password@localhost/dila_database'
_EOL
export DILA_CONFIG_MODULE=config.py
dila run_dev_server
```

## Development and testing
Tests requires docker. Development server even if can be run without it also is easier to run with docker.
You can install it from [here](https://docs.docker.com/engine/getstarted/linux_install_help/).

### Development
To run development server run
```
source activate-env
dila_install_requirements
dila_dev_server_start
```
To stop run `dila_dev_server_stop`

### Tests
To run tests you should create virtualenv and install requirements. Then run `pytest`
```
virtualenv -p python3 $HOME/dila-virtualenv
. $HOME/dila-virtualenv/bin/activate
pip install -r base_requirements.txt
pip install -r test_requirements.txt
pytest
```
Pytest is configured to setup dependencies in docker, so you still must have docker.

### Acceptance tests
To run acceptance tests you can use separate virtualenv:

```
virtualenv -p python3 $HOME/dila-acceptance-virtualenv
. $HOME/dila-acceptance-virtualenv/bin/activate
pip install -r acceptance_test/test_requirements.txt
pytest acceptance_test
```
In the future we should run pytest in docker as well.
