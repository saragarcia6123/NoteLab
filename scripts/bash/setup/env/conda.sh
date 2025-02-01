#!/bin/bash

# Run using "source ./scripts/bash/setup/env/conda.sh"

echo "Setting up conda environment..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install conda and try again."
    exit 1
fi

source /usr/etc/profile.d/conda.sh

# Get the current package name from pyproject.toml
package_name=$(awk -F'=' '/name/ {print $2}' pyproject.toml | tr -d ' "')

# Prompt for environment name (default: package_name) set to package_name if empty
read -r -p "Enter the environment name (default: $package_name): " env_name
env_name=${env_name:-$package_name}

if ! command -v conda &> /dev/null; then
    conda init bash
fi

# Check if the environment already exists
create_new=false
if conda info --envs | grep -q "$env_name"; then
    read -r -p "The environment already exists. Do you want to overwrite it? (y/n): " choice
    case "$choice" in
        y|Y ) echo "Overwriting conda environment..."; conda env remove --name "$env_name";;
    esac
else
    create_new=true
fi

python_version=$(cat .python-version)

if [ "$create_new" = true ]; then
    conda create -n "$env_name" python="$python_version" -y
    echo "Conda environment created successfully"
fi

conda activate "$env_name"
echo "Conda environment activated"
