#!/bin/bash

pip install --upgrade pip setuptools wheel

source ./scripts/bash/config/poetry.sh
flag=$?
if [ $flag -eq 1 ]; then
    echo "Poetry setup failed. Exiting..."
    exit 1
fi

echo "Setting up poetry dependencies..."

python_version=$(cat .python-version)

poetry env use "$python_version"
poetry config virtualenvs.in-project true
poetry lock
poetry install
poetry update
poetry check


