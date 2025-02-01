#!/bin/bash

echo "Running tests..."

if [ ! -f .env ]; then
  echo "ERROR: .env file not found!"
  exit 1
fi

set -o allexport
source .env
set +o allexport

if [ -z "$TESTS_DIR" ]; then
  echo "ERROR: TESTS_DIR is not set in .env"
  exit 1
fi

export TEST_ENV=true

PYTHONPATH=$(pwd)/src
export PYTHONPATH

pytest --cov=src/notelab --cov-report=term-missing "$TESTS_DIR"

echo "Tests completed successfully."

unset TEST_ENV

exit $?
