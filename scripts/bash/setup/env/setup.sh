#!/bin/bash

echo "Setting up virtual environment..."

# Ask to deactivate any active virtual environment
./scripts/bash/config/env/deactivate.sh

# Check if there is an active virtual environment
source ./scripts/bash/config/env/active.sh
active=$?

skip=0
if [ $active -eq 3 ]; then
    echo "Both venv and conda environments are active. Please deactivate one to avoid conflicts."
    exit 1
elif [ $active -ne 0 ]; then
    echo "Virtual environment was not deactivated. Skipping setup..."
    skip=1
fi

if [ $skip -eq 1 ]; then
    return 0
fi

echo "Setting up virtual environment..."

read -r -p "Would you like to use venv or conda? (v/c): " choice
case "$choice" in
    v|V ) ./scripts/bash/setup/env/venv.sh;;
    c|C ) ./scripts/bash/setup/env/conda.sh;;
    * ) echo "Invalid choice. Skipping..."; exit 0;;
esac

echo "Virtual environment setup complete."