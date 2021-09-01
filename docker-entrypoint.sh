#!/bin/sh -e

# Add cupidon user and group
groupadd -f -o -g ${CUPIDON_GID:-911} cupidon
useradd -o -u ${CUPIDON_UID:-911} -g cupidon cupidon

# Configure file and directory permission
chown -R cupidon:cupidon ${CONFIG_DIR:-/config}

# Execute the command as cupidon
su -p cupidon -c '"$0" "$@"' -- "$@"
