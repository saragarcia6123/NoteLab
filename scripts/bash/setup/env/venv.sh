#!/bin/bash

# Run using "source ./scripts/bash/setup/env/venv.sh"

# Check if venv module is installed
if ! python3 -m venv --help &> /dev/null; then
    echo "venv module is not installed. Please install it to proceed."
    exit 1
fi

skip_venv_setup=false
if [ -d "venv" ]; then
    read -r -p "The virtual environment is already set up. Do you want to overwrite it? (y/n): " choice
    case "$choice" in
        y|Y ) echo "Overwriting virtual environment...";;
        * ) skip_venv_setup=true;;
    esac
fi

if [ "$skip_venv_setup" = false ]; then
    rm -rf venv

    python_version=$(cat .python-version)
    python3 -m venv venv --python="$python_version"
    source venv/bin/activate
    pip install --upgrade pip

    echo "Virtual environment is set up."
fi