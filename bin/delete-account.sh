#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} USER_NAME"
    echo "Example: ${0} jdoe"
}

. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
USER_NAME="${1}"

if [ "${USER_NAME}" = "" ]; then
    usage

    exit 1
fi

${DELETE} "uid=${USER_NAME},ou=users,${SUFFIX}"
