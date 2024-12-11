#!/bin/bash

# Install poetry if not already installed
if ! command -v poetry &> /dev/null; then
    echo "Installing poetry..."
    pip install poetry
fi

pip install --upgrade pip
poetry install
poetry update
poetry check