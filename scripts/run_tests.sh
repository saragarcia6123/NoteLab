#!/bin/bash

# Source environment variables from .env file
set -o allexport
source .env
set +o allexport

# Check if TESTS_ROOT is set
if [ -z "$TESTS_DIR" ]; then
  echo "ERROR: TESTS_ROOT is not set in .env"
  exit 1
fi

PYTHONPATH=$(pwd)/src
export PYTHONPATH
pytest --cov=src/notelab --cov-report=term-missing "$TESTS_DIR"

exit $?
