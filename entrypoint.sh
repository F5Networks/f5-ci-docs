#!/usr/bin/env bash

# Add local user to container
USER_ID=${LOCAL_USER_ID:-9001}
echo "Starting with UID : $USER_ID"
useradd --create-home --shell /bin/bash --uid $USER_ID user
export HOME=/home/user

# Run the command as the user
if [ ${#@} == 0 ]; then
  exec chroot --skip-chdir --userspec=user / bash
else
  exec chroot --skip-chdir --userspec=user / "$@"
fi
