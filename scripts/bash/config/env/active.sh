#!/bin/bash

# Returns:
# 0 - No active virtual environment found
# 1 - venv is active
# 2 - conda is active
# 3 - Both venv and conda are active

echo "Checking for active virtual environment..."

venv=0
conda=0

# Check for venv
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is active."
    venv=1
fi

# Check for conda
if command -v conda &> /dev/null; then
    if conda info --envs | grep -q "\*" ; then
        echo "Conda environment is active."
        conda=1
    fi
fi

# Check for both
if [ $venv -eq 1 ] && [ $conda -eq 1 ]; then
    echo "Both venv and conda environments are active. Please deactivate one to avoid conflicts."
    return 3
else
    if [ $venv -eq 1 ]; then
        return 1
    fi
    if [ $conda -eq 1 ]; then
        return 2
    fi
fi

echo "No active virtual environment found."
return 0