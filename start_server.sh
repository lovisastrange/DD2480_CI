#!/bin/bash

CURRENT_DIR=$(pwd)/src

# Correctly reference the path to your virtual environment's activation script
VENV_PATH="../.venv/bin/activate"

# Use the correct command to activate the virtual environment.
# Note: When using osascript, you might not be able to directly source the activation script due to how environments are handled.
# You may need to invoke a shell explicitly and then run source command within that shell context.
FLASK_CMD="cd \\\"$CURRENT_DIR\\\"; source \\\"$VENV_PATH\\\"; flask --app main run --port 8000"

NGROK_CMD="ngrok http --domain=mantis-peaceful-locust.ngrok-free.app 8000"

osascript <<EOF
tell application "Terminal"
    do script "$FLASK_CMD"
end tell
EOF

sleep 2

osascript <<EOF
tell application "Terminal"
    do script "$NGROK_CMD"
end tell
EOF