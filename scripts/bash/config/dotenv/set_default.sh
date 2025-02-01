#!/bin/bash

# Sets the default environment variables in .env according to pyproject.toml

# Get the package name from pyproject.toml
package_name=$(grep -Po '(?<=^name = ").*(?=")' pyproject.toml)

# Set the package name in .env
./scripts/bash/config/dotenv/set_var.sh PACKAGE_NAME "$package_name"

# Read the default environment variables from res/paths.txt and set them in .env
while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    value=${value//\{PACKAGE_NAME\}/$package_name} # Replace {PACKAGE_NAME} with the actual package name
    ./scripts/bash/config/dotenv/set_var.sh "$key" "$value"
done < res/paths.txt

echo "Default environment variables set"