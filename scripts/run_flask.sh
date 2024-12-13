#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# Initialize the command
cmd="flask run --cert=$SSL_CERT_FILE --key=$SSL_KEY_FILE"

for var in $(compgen -e); do
    if [[ $var == FLASK_* && $var != "FLASK_APP" && $var != "FLASK_RELOAD" && $var != "FLASK_DEBUG" && $var != "FLASK_SECRET_KEY" ]]; then
        param_name=$(echo "$var" | sed 's/FLASK_//' | tr '[:upper:]' '[:lower:]' | tr '_' '-')
        cmd="$cmd --$param_name=${!var}"
    fi
done

# Add debug and reload options if they are set to true
if [ "$FLASK_DEBUG" = "true" ]; then
    cmd="$cmd --debug"
else
    cmd="$cmd --no-debugger"
fi

if [ "$FLASK_RELOAD" = "true" ]; then
    cmd="$cmd --reload"
else
    cmd="$cmd --no-reload"
fi

# Run the Flask application
export FLASK_APP=$FLASK_APP
eval "$cmd"