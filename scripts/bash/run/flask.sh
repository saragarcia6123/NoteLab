#!/bin/bash

echo "Starting Flask..."

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

if [[ -z "$SSL_CERT_FILE" || -z "$SSL_KEY_FILE" ]]; then
    echo "SSL certificate or key file is missing!"
    exit 1
fi

cmd="flask run --cert=$SSL_CERT_FILE --key=$SSL_KEY_FILE"

for var in $(compgen -e); do
    if [[ $var == FLASK_* && $var != "FLASK_APP" && $var != "FLASK_RELOAD" && $var != "FLASK_DEBUG" && $var != "FLASK_SECRET_KEY" ]]; then
        param_name=$(echo "$var" | sed 's/FLASK_//' | tr '[:upper:]' '[:lower:]' | tr '_' '-')
        cmd="$cmd --$param_name=${!var}"
    fi
done

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

export FLASK_APP=$FLASK_APP
eval "$cmd"
