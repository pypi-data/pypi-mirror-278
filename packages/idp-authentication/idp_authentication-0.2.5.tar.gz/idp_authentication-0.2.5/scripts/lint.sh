#!/bin/bash

APP_PATH="idp_authentication"

echo "Running black checks on  ($APP_PATH)"
black $APP_PATH --check

echo "Running isort checks on ($APP_PATH)"
isort $APP_PATH --check
