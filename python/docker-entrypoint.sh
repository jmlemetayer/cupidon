#!/bin/sh -e

# Create a virtual environment
python -m venv /app/virtual_environment

# Activate the virtual environment
. /app/virtual_environment/bin/activate

# Install python dependencies
pip install --no-cache-dir -r /app/requirements.txt

# Execute the command
exec "$@"
