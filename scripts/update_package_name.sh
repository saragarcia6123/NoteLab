#!/bin/bash

# Ask user for new package name
# shellcheck disable=SC2162
read -p "Enter the new package name: " new_package_name

# Replace underscores with hyphens
new_package_name=$(echo "$new_package_name" | tr '_' '-')

# Validate the new package name (only letters, numbers, and hyphens)
if [[ ! "$new_package_name" =~ ^[a-z0-9-]+$ ]]; then
    echo "Invalid package name. Use only lowercase letters, numbers, and hyphens."
    exit 1
fi

# Get the old package name from pyproject.toml
old_package_name=$(grep -Po '(?<=^name = ").*(?=")' pyproject.toml)
echo "Old package name: $old_package_name"

# Warn if old and new package names are the same
if [ "$old_package_name" = "$new_package_name" ]; then
    echo "Old and new package names are the same."; exit 0
fi

# Confirm the package name change
read -p "Are you sure you want to change the package name from $old_package_name to $new_package_name? (y/n): " choice
case "$choice" in
    y|Y ) echo "Updating package name...";;
    * ) echo "Operation cancelled"; exit 0;;
esac

# Convert both old and new package names to underscored versions
old_package_name_underscore=$(echo "$old_package_name" | tr '-' '_')
new_package_name_underscore=$(echo "$new_package_name" | tr '-' '_')

# Update the package name references in pyproject.toml
escaped_new_package_name=$(printf '%s\n' "$new_package_name" | sed 's/[&/\]/\\&/g')
sed -i "s/$old_package_name/$escaped_new_package_name/g" pyproject.toml

escaped_new_package_name_underscore=$(printf '%s\n' "$new_package_name_underscore" | sed 's/[&/\]/\\&/g')
sed -i "s/$old_package_name_underscore/$escaped_new_package_name_underscore/g" pyproject.toml

poetry lock

# Update the package name in src and tests directories
if [ -d "src/$old_package_name_underscore" ]; then
    mv "src/$old_package_name_underscore" "src/$new_package_name_underscore"
fi

if [ -d "tests/$old_package_name_underscore" ]; then
    mv "tests/$old_package_name_underscore" "tests/$new_package_name_underscore"
fi

# Replace all occurrences in the project files
find . -type f -exec sed -i "s/$old_package_name/$new_package_name/g" {} +
find . -type f -exec sed -i "s/$old_package_name_underscore/$new_package_name_underscore/g" {} +

# Update the package name in .env if present
if [ -f .env ]; then
    sed -i "s/^PACKAGE_NAME=.*/PACKAGE_NAME=$new_package_name_underscore/" .env
    sed -i "s/^PROJECT_ROOT=.*/PROJECT_ROOT=src\/$new_package_name_underscore/" .env
fi

./scripts/set_env_var.sh PACKAGE_NAME "$new_package_name"
./scripts/set_env_var.sh PROJECT_ROOT "src/$new_package_name_underscore"
./scripts/set_env_var.sh TESTS_DIR "tests/$new_package_name_underscore"

echo "Package name updated successfully from '$old_package_name' to '$new_package_name'."
