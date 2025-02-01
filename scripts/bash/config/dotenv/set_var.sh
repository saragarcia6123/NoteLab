#!/bin/bash

set_environment_variable() {
    local key=$1
    local value=$2
    # Update or add the key-value pair in .env
    if grep -q "^${key}=" .env; then
        # Update the existing key
        sed -i'' -e "s|^${key}=.*|${key}=${value}|" .env
    else
        # Add the new key
        echo "${key}=$value" >> .env
    fi
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 key value"
    exit 1
fi

# Call the function with the provided arguments
set_environment_variable "$1" "$2"

echo "Environment variable $1 set to $2"