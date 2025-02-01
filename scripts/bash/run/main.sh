#!/bin/bash

run_main() {
    echo "Running main script..."

    find scripts/bash -type f -name "*.sh" -exec chmod +x {} \;

    export "$(grep -v '^#' .env | xargs)"
    PYTHONPATH="$(pwd)/$PROJECT_ROOT:$PYTHONPATH"
    export PYTHONPATH="$PYTHONPATH"

    ./scripts/bash/run/tests.sh
    ./scripts/bash/run/flask.sh

}

if ! run_main; then
    echo "Error detected."
fi
