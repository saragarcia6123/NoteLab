#!/bin/bash

# Ensure there is an active virtual environment before proceeding
source ./scripts/bash/config/env/active.sh
active=$?
if [ $active -eq 0 ]; then
    exit 1
fi

# Install poetry if not already installed
if [ $active -eq 1 ]; then
    if ! command -v poetry &> /dev/null; then
        echo "Poetry is not installed. Installing..."
        pip install poetry
    fi
elif [ $active -eq 2 ]; then
   # Check if poetry is installed in the conda environment
    if ! conda list | grep -q poetry; then
        echo "Poetry is not installed in the active conda environment. Installing..."
        conda install poetry
    fi
elif [ $active -eq 3 ]; then
  exit 1
fi

