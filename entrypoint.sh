#!/bin/sh

# Add openai certs
PEM_SOURCE_PATH="/extra-certs.pem"
CERTIFI_CACERT_PATH="$(python -m certifi)"
cat "$PEM_SOURCE_PATH" >> "$CERTIFI_CACERT_PATH"

# Run db migration and upgrade
flask db init
flask db migrate
flask db upgrade

# Start the Flask application
exec "$@"
