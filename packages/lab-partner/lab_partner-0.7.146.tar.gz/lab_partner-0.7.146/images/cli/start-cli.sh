#!/bin/bash

set -e

echo "Creating docker group membership"
addgroup docker --gid 998
usermod -aG docker root

exec /bin/bash