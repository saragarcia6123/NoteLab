#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it to proceed."
    exit 1
fi

# Check if venv module is installed
if ! python3 -m venv --help &> /dev/null; then
    echo "venv module is not installed. Please install it to proceed."
    exit 1
fi

skip_venv_setup=false
if [ -d "venv" ]; then
    read -r -p "The virtual environment is already set up. Do you want to overwrite it? (y/n): " choice
    case "$choice" in
        y|Y ) echo "Overwriting virtual environment...";;
        * ) skip_venv_setup=true;;
    esac
fi

if [ "$skip_venv_setup" = false ]; then
    rm -rf venv  # Remove existing virtual environment

    # Create a new virtual environment
    python3 -m venv venv
    source venv/bin/activate

    echo "Virtual environment is set up."
fi

# Check if .env already exists
skip_env_setup=false
if [ -f .env ]; then
    read -r -p ".env file already exists. Do you want to overwrite it? (y/n): " choice
    case "$choice" in
        y|Y ) echo "Overwriting .env file..." ;;
        * ) skip_env_setup=true ;;
    esac
fi

if [ "$skip_env_setup" = false ]; then
    touch .env
    echo "Created .env file."
fi

pip install pytest pytest-cov python-dotenv

# Generate SSL certificate if not present
./scripts/gen_ssl_certificate.sh

# Change the default package name
./scripts/update_package_name.sh

# Set default environment variables
./scripts/set_default_envs.sh

# Set up the database
./scripts/database_setup.sh

# Run Flask setup
./scripts/flask_config.sh

# Update dependencies
./scripts/update_dependencies.sh

echo "Environment is set up. Run the application using './scripts/run.sh'"