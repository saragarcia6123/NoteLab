#!/bin/bash

# Function to run the main commands
run_main() {
    export "$(grep -v '^#' .env | xargs)"
    PYTHONPATH="$(pwd)/$PROJECT_ROOT:$PYTHONPATH"
    export PYTHONPATH="$PYTHONPATH"

    ./scripts/run_tests.sh
    ./scripts/run_flask.sh
}

# Run the main commands and catch errors
if ! run_main; then
    echo "Error detected."
fi