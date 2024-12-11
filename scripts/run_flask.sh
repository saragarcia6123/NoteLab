#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# Initialize the command
cmd="flask run --host=$FLASK_HOST --port=$FLASK_PORT --cert=$SSL_CERT_FILE --key=$SSL_KEY_FILE"

# Add debug and reload options if they are set to true
if [ "$FLASK_DEBUG" = "true" ]; then
    cmd="$cmd --debug"
fi

if [ "$FLASK_RELOAD" = "true" ]; then
    cmd="$cmd --reload"
fi

# Run the Flask application
export FLASK_APP=$FLASK_APP
eval "$cmd"