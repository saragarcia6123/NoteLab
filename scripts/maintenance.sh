#!/bin/bash

# Clear cache
find . -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -exec rm -f {} +

./scripts/update_dependencies.sh
python scripts/generate_readme.py