#!/bin/bash

echo "Setting up Flask..."

# Extract $PROJECT_ROOT from .env
PROJECT_ROOT=$(grep -E '^PROJECT_ROOT=' .env | cut -d '=' -f 2)

# Validate that PROJECT_ROOT is not empty
if [ -z "$PROJECT_ROOT" ]; then
    echo "Error: PROJECT_ROOT is not defined in .env"
    exit 1
fi

# Function to read default values from flask_defaults.txt
read_defaults() {
    while IFS='=' read -r key value; do
        value=${value//\{PROJECT_ROOT\}/$PROJECT_ROOT}
        eval "FLASK_${key^^}=\"$value\""
    done < res/flask_defaults.txt
}

# Read default values
read_defaults

# Prompt for user input with a default value
prompt() {
    local var_name=$1
    local prompt_text=$2
    local default_value=$3
    local current_value=${!var_name}

    if [ -z "$current_value" ]; then
        current_value=$default_value
    fi

    # shellcheck disable=SC2162
    read -p "$prompt_text [$current_value]: " input
    if [ -n "$input" ]; then
      eval "$var_name"=\""$input"\"
    else
      eval "$var_name"=\""$current_value"\"
    fi
}

# Run the user through all parameters
full_setup() {
    echo "Running full setup..."

    # Check if FLASK_SECRET_KEY is set
    skip_secret_key=false
    if grep -q "^FLASK_SECRET_KEY=" .env; then
        read -r -p "There is already a secret key set. Would you like to regenerate it? (y/n): " choice
        case "$choice" in
            y|Y ) echo "Regenerating secret key";;
              * ) echo "Secret key unchanged"; skip_secret_key=true;;
        esac
    fi

    # shellcheck disable=SC2013
    for var in $(grep -E '^[^#]' res/flask_defaults.txt | cut -d '=' -f 1); do
        default_var="FLASK_${var^^}"
        prompt "$default_var" "Enter value for ${var^^}" "${!default_var}"
    done

    # Export parameters to .env
    # shellcheck disable=SC2013
    for var in $(grep -E '^[^#]' res/flask_defaults.txt | cut -d '=' -f 1); do
        default_var="FLASK_${var^^}"
        ./scripts/bash/config/dotenv/set_var.sh "$default_var" "${!default_var}"
    done

    if [ "$skip_secret_key" = false ]; then
        FLASK_SECRET_KEY=$(openssl rand -base64 32)
        ./scripts/bash/config/dotenv/set_var.sh FLASK_SECRET_KEY "$FLASK_SECRET_KEY"
    fi

    echo "Parameters set."
}

# Run the full setup
full_setup

echo "Flask setup complete."