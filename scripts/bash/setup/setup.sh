#!/bin/bash

echo "Setting up project..."

# Ensure all scripts are marked as executable
find scripts/bash -type f -name "*.sh" -exec chmod +x {} \;

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it to proceed."
    exit 1
fi

# Environment setup
source ./scripts/bash/setup/env/setup.sh
flag=$?
if [ $flag -eq 1 ]; then
    echo "Environment setup failed. Exiting..."
    exit 1
fi

# Install dependencies
source ./scripts/bash/config/dependencies.sh
flag=$?
if [ $flag -eq 1 ]; then
    echo "Dependency installation failed. Exiting..."
    exit 1
fi

# Generate SSL certificate
./scripts/bash/setup/ssl_cert.sh

# Set up the database
./scripts/bash/setup/database.sh

# .env setup
./scripts/bash/config/dotenv/setup.sh

# Configure Flask
./scripts/bash/config/flask.sh

echo "Environment is set up. Run the application using './scripts/bash/run/main.sh'"