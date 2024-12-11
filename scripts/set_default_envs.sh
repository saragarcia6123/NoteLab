#!/bin/bash

# Get the package name from pyproject.toml
package_name=$(grep -Po '(?<=^name = ").*(?=")' pyproject.toml)
./scripts/set_env_var.sh PACKAGE_NAME "$package_name"
package_name_underscore=$(echo "$package_name" | tr '-' '_')

# Read the default environment variables from scripts/default_envs.txt
while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
    value=${value//\{PACKAGE_NAME\}/$package_name}
    value=${value//\{PACKAGE_NAME_UNDERSCORE\}/$package_name_underscore}
    ./scripts/set_env_var.sh "$key" "$value"
done < res/paths.txt

echo "Default environment variables set"