#!/bin/sh -e

HOST="${1}"
PORT="${2}"

if [ "${HOST}" = '' ] || [ "${PORT}" = '' ]; then
    echo "Usage: ${0} HOST PORT"

    exit 1
fi

scp -P "${PORT}" tmp/configuration.ldif "${HOST}:~/src/directory-tools/tmp"
scp -P "${PORT}" tmp/data.ldif "${HOST}:~/src/directory-tools/tmp"
