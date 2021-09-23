#!/bin/sh -e

# Install npm dependencies
npm install

# Execute the command
exec "$@"
