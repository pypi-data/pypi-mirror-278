#!/bin/bash -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place idp_authentication --exclude=__init__.py
black idp_authentication
isort idp_authentication