#!/bin/bash

# Clear cache files
find . -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -exec rm -f {} +

./scripts/bash/config/dependencies.sh
flag=$?
if [ $flag -eq 1 ]; then
    exit 1
fi

python scripts/python/generate_readme.py