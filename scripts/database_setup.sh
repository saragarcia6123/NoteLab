#!/bin/bash

# Get the database path from .env
database_path=$(grep -Po '(?<=^DB_PATH=).*$' .env)

# Create necessary directories if they don't exist
mkdir -p "$(dirname "$database_path")"

# Check if the database file exists
create=false
if [ -f "$database_path" ]; then
    echo "Database file $database_path exists. Would you like to overwrite it? (y/n)"
    read -r choice
    case "$choice" in
        y|Y ) echo "Overwriting database file..."; create=true;;
        * ) echo "Skipping database setup...";;
    esac
else
    echo "Database file $database_path does not exist. Creating a new database"; create=true
fi

if [ "$create" = true ]; then
    # Create a new database using Python
    python3 - <<EOF
import sqlite3
conn = sqlite3.connect('$database_path')
conn.close()
EOF
    echo "Database setup complete."
fi