#!/bin/sh -e

DOMAIN=$(cat tmp/domain.txt)
HOST_NAME=$(cat tmp/hostname.txt)
HOST="${HOST_NAME}.${DOMAIN}"
echo "Username: admin"
echo "Password: admin"
SYSTEM=$(uname)

if [ "${SYSTEM}" = Darwin ]; then
    open "http://${HOST}:5000"
else
    xdg-open "http://${HOST}:5000"
fi
