#!/bin/bash

if [ -f .env ]; then
    read -r -p ".env file already exists. Do you want to overwrite it? (y/n): " choice
    case "$choice" in
        y|Y ) echo "Overwriting .env file..." ;;
        * ) return ;;
    esac
fi

touch .env
echo "Created .env file."

# Set the default environment variables
./scripts/bash/config/dotenv/set_default.sh