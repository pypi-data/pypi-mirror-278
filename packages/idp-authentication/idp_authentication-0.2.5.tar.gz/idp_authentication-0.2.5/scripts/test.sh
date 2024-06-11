#!/bin/bash
APP_PATH="idp_authentication"

export PYTHONPATH=$APP_PATH
set -e
set -x
pytest --cov-report term-missing --cov=$APP_PATH --cov-fail-under=85
